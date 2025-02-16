import streamlit as st
import PyPDF2
import docx
from pptx import Presentation
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
import pytextrank
import re
import networkx as nx
import pandas as pd
from openai import OpenAI

# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_md")
nlp.add_pipe("textrank")

# Configurar el cliente de OpenAI (NVIDIA API)
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key = "tu_clave_api_secreta"
)

# --- FUNCIONES PARA CARGAR TEXTOS DE ARCHIVOS ---
def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error al procesar el archivo PDF: {str(e)}")
        return None

def extract_text_from_word(docx_file):
    try:
        doc = docx.Document(docx_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error al procesar el archivo DOCX: {str(e)}")
        return None

def extract_text_from_ppt(ppt_file):
    try:
        prs = Presentation(ppt_file)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error al procesar el archivo PPTX: {str(e)}")
        return None

# --- FUNCIONES PARA PROCESAR Y GENERAR RESUMEN ---
def chunk_text(text, words_per_chunk=200):
    """
    Divide el texto en chunks de aproximadamente n palabras,
    intentando no cortar en medio de una palabra.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_count = 0

    for word in words:
        current_chunk.append(word)
        current_count += 1

        # Si llegamos al límite de palabras o encontramos un punto
        if current_count >= words_per_chunk or word.endswith('.'):
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_count = 0

    # Añadir el último chunk si quedaron palabras
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def generate_summary(text, num_sentences=5):
    # Limpiar el texto
    text = text.replace("\n", "").replace("\r", "")
    text = re.sub(' +', ' ', text)

    # Dividir el texto en chunks más grandes
    chunks = chunk_text(text, words_per_chunk=200)

    # Crear un nuevo texto con los chunks separados por puntos
    processed_text = ". ".join(chunks)

    # Procesar el texto con spaCy
    doc = nlp(processed_text)

    # Crear un grafo de similitud
    sentences = list(doc.sents)
    G = nx.Graph()

    # Añadir nodos (chunks)
    for i, sent in enumerate(sentences):
        G.add_node(i, text=sent.text)

    # Añadir aristas basadas en similitud
    threshold = 0.90  # Ajusta el umbral aquí
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            similarity = sentences[i].similarity(sentences[j])
            if similarity > threshold:
                G.add_edge(i, j, weight=similarity)

    # Generar el resumen basado en los nodos conectados
    important_sentences = set()
    for i in G.nodes:
        if G.degree[i] > 0:  # Si el nodo tiene conexiones, es relevante
            important_sentences.add(i)

    # Ordenar las oraciones importantes por aparición en el texto original
    summary = [sentences[i].text for i in sorted(important_sentences)]

    return ' '.join(summary[:num_sentences])

# --- FUNCIÓN PARA CONTAR PALABRAS ---
def count_words(text):
    return len(text.split())

# --- FUNCIÓN PARA GENERAR CUESTIONARIO ---
def generate_quiz(text):
    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": f"Genera un cuestionario de 5 preguntas a partir del siguiente texto: {text}"}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error al generar el cuestionario: {str(e)}")
        return None

# --- INTERFAZ CON STREAMLIT ---
st.title('Generador de Resúmenes y Cuestionarios a partir de Archivos o Videos de YouTube')

# Barra lateral (sidebar) para seleccionar la opción
with st.sidebar:
    st.header("Opciones")
    option = st.radio("Selecciona una opción:", ("Archivo", "YouTube"))
    if option == "YouTube":
        youtube_option = st.radio("¿Qué deseas hacer con el video de YouTube?", ("Generar resumen", "Generar cuestionario"))

# Procesar un archivo
if option == "Archivo":
    file = st.file_uploader('Sube un archivo', type=['pdf', 'docx', 'pptx'])
    if file is not None:
        # Extraer el texto del archivo
        if file.name.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif file.name.endswith('.docx'):
            text = extract_text_from_word(file)
        elif file.name.endswith('.pptx'):
            text = extract_text_from_ppt(file)
        
        if text:
            # Generar el resumen
            summary = generate_summary(text, num_sentences=5)
            
            # Contar palabras en la transcripción completa y en el resumen
            total_words_transcription = count_words(text)
            total_words_summary = count_words(summary)
            
            # Checkbox para mostrar/ocultar la transcripción completa
            mostrar_transcripcion = st.checkbox("Mostrar transcripción completa")
            
            # Crear columnas para distribuir la transcripción y el resumen
            col1, col2 = st.columns(2)
            
            # Mostrar el resumen en la primera columna
            with col1:
                st.subheader("Resumen generado")
                st.write(summary)
                st.metric(label="Palabras Resumen", value=total_words_summary)
            
            # Mostrar la transcripción completa si el checkbox está activado
            if mostrar_transcripcion:
                with col2:
                    st.subheader("Transcripción completa")
                    st.write(text)
                    st.metric(label="Palabras Transcripción", value=total_words_transcription)

# Procesar un video de YouTube
elif option == "YouTube":
    youtube_link = st.text_input('Introduce la URL del video de YouTube')
    if youtube_link:
        try:
            # Extraer el ID del video de YouTube
            video_id = youtube_link.split("v=")[1]
            
            # Descargar la transcripción
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
            
            # Unir las transcripciones en un solo texto
            text = " ".join([entry['text'] for entry in transcript])
            
            if youtube_option == "Generar resumen":
                # Generar el resumen
                summary = generate_summary(text, num_sentences=5)
                
                # Contar palabras en la transcripción completa y en el resumen
                total_words_transcription = count_words(text)
                total_words_summary = count_words(summary)
                
                # Checkbox para mostrar/ocultar la transcripción completa
                mostrar_transcripcion = st.checkbox("Mostrar transcripción completa")
                
                # Crear columnas para distribuir la transcripción y el resumen
                col1, col2 = st.columns(2)
                
                # Mostrar el resumen en la primera columna
                with col1:
                    st.subheader("Resumen generado")
                    st.write(summary)
                    st.metric(label="Palabras Resumen", value=total_words_summary)
                
                # Mostrar la transcripción completa si el checkbox está activado
                if mostrar_transcripcion:
                    with col2:
                        st.subheader("Transcripción completa")
                        st.write(text)
                        st.metric(label="Palabras Transcripción", value=total_words_transcription)
            
            elif youtube_option == "Generar cuestionario":
                # Generar el cuestionario
                quiz = generate_quiz(text)
                
                if quiz:
                    st.subheader("Cuestionario generado")
                    st.write(quiz)
                    
                    # Botón para evaluar respuestas
                    if st.button("Evaluar respuestas"):
                        st.subheader("Respuestas correctas")
                        st.write("Aquí se mostrarían las respuestas correctas.")  # Puedes expandir esta parte
        
        except Exception as e:
            st.error(f"Error al obtener la información del video. Vuelve a intentar con otro enlace. Detalles: {str(e)}")