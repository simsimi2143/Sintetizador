# Explicación del Código: Generador de Resúmenes y Cuestionarios

Este proyecto es una aplicación que permite generar resúmenes y cuestionarios a partir de archivos (PDF, DOCX, PPTX) o videos de YouTube. A continuación, se explica cómo funciona el código, paso a paso, tanto para personas con conocimientos técnicos como para aquellos sin experiencia en programación o matemáticas.

---

## 1. **Introducción**

El código utiliza varias bibliotecas de Python para procesar texto, generar resúmenes y crear cuestionarios. La aplicación está diseñada para ser fácil de usar, con una interfaz gráfica que permite a los usuarios subir archivos o introducir enlaces de YouTube.

<img src='https://media.discordapp.net/attachments/1090822505238892556/1313935312615116860/oTH6aNQAAAABJRU5ErkJggg.png?ex=67b3801e&is=67b22e9e&hm=8baed0853bf00f6995e8d1b76651685be8eb2fa03f83abe31747e66ff8374954&=&format=webp&quality=lossless&width=816&height=540'>
---

## 2. **Librerías Utilizadas**

- **Streamlit**: Para crear la interfaz gráfica de la aplicación.
- **PyPDF2**: Para extraer texto de archivos PDF.
- **python-docx**: Para extraer texto de archivos DOCX.
- **python-pptx**: Para extraer texto de archivos PPTX.
- **youtube_transcript_api**: Para obtener la transcripción de videos de YouTube.
- **spaCy**: Para procesar el texto y generar resúmenes.
- **NetworkX**: Para crear grafos y analizar la similitud entre oraciones.
- **OpenAI**: Para generar cuestionarios utilizando un modelo de lenguaje avanzado.



## 3. **Funcionamiento del Código**

<img src='https://media.discordapp.net/attachments/1090822505238892556/1313934481341677699/IICv1UQAAAABJRU5ErkJggg.png?ex=67b37f58&is=67b22dd8&hm=af36151ca7676a44c87e0c6272502da24e8782e68833e08f62127d95b94efae5&=&format=webp&quality=lossless&width=677&height=540'>

### 3.1. **Carga del Modelo de spaCy**

El código carga un modelo de lenguaje en español (`es_core_news_md`) y añade un componente llamado `textrank`, que se utiliza para extraer las oraciones más importantes del texto.

```python
nlp = spacy.load("es_core_news_md")
nlp.add_pipe("textrank")
```

---

### 3.2. **Configuración del Cliente de OpenAI**

Se configura el cliente de OpenAI para utilizar la API de NVIDIA, que permite generar cuestionarios a partir del texto.

```python
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key = "tu_clave_api_secreta"
)
```

---

### 3.3. **Extracción de Texto de Archivos**

El código incluye funciones para extraer texto de diferentes tipos de archivos:

- **PDF**: Usa `PyPDF2` para leer el archivo y extraer el texto de cada página.
- **DOCX**: Usa `python-docx` para leer el archivo y extraer el texto de cada párrafo.
- **PPTX**: Usa `python-pptx` para leer el archivo y extraer el texto de cada diapositiva.

```python
def extract_text_from_pdf(pdf_file):
    # Código para extraer texto de PDF

def extract_text_from_word(docx_file):
    # Código para extraer texto de DOCX

def extract_text_from_ppt(ppt_file):
    # Código para extraer texto de PPTX
```

---

### 3.4. **Procesamiento del Texto y Generación de Resúmenes**

El texto extraído se divide en "chunks" (fragmentos) de aproximadamente 200 palabras. Luego, se utiliza spaCy para procesar el texto y generar un resumen.

```python
def chunk_text(text, words_per_chunk=200):
    # Divide el texto en chunks de 200 palabras

def generate_summary(text, num_sentences=5):
    # Limpia el texto y lo divide en chunks
    # Procesa el texto con spaCy
    # Crea un grafo de similitud entre oraciones
    # Genera el resumen basado en las oraciones más importantes
```

#### 3.4.1. **Detalles Matemáticos**

- **Grafo de Similitud**: Se crea un grafo donde cada nodo representa una oración. Las aristas entre nodos se crean si la similitud entre dos oraciones es mayor que un umbral (0.90 en este caso).
- **Similitud**: La similitud entre oraciones se calcula utilizando el modelo de spaCy, que utiliza embeddings (vectores numéricos) para representar el significado de las oraciones.

---

### 3.5. **Generación de Cuestionarios**

El código utiliza la API de OpenAI para generar un cuestionario a partir del texto. Se envía el texto al modelo de lenguaje, que genera preguntas y respuestas.

```python
def generate_quiz(text):
    # Envía el texto a la API de OpenAI
    # Recibe y muestra el cuestionario generado
```

---

### 3.6. **Interfaz Gráfica con Streamlit**

La interfaz gráfica permite a los usuarios subir archivos o introducir enlaces de YouTube. Dependiendo de la opción seleccionada, la aplicación genera un resumen o un cuestionario.

```python
st.title('Generador de Resúmenes y Cuestionarios a partir de Archivos o Videos de YouTube')

# Barra lateral para seleccionar la opción
with st.sidebar:
    st.header("Opciones")
    option = st.radio("Selecciona una opción:", ("Archivo", "YouTube"))
```

<img src='https://cdn.discordapp.com/attachments/1036462454550577192/1340785480039665734/56d8b1ea-22af-447e-983e-bb50536fbf9a.png?ex=67b39f49&is=67b24dc9&hm=851631fe1b72449f6ce2db2bdd2c0d05ce6e56dc5ec2be50e209951f7cc2e93f&'>
---

## 4. **Explicación Paso a Paso para Personas sin Conocimientos Técnicos**

1. **Subir un Archivo o Introducir un Enlace de YouTube**:
   - Si eliges "Archivo", puedes subir un archivo PDF, DOCX o PPTX.
   - Si eliges "YouTube", introduces la URL de un video.

2. **Procesamiento del Texto**:
   - La aplicación extrae el texto del archivo o del video de YouTube.
   - Divide el texto en partes más pequeñas para facilitar su análisis.

3. **Generación del Resumen**:
   - La aplicación analiza el texto y selecciona las oraciones más importantes.
   - Muestra un resumen corto del contenido.

4. **Generación del Cuestionario**:
   - Si eliges generar un cuestionario, la aplicación crea preguntas basadas en el texto.
   - Puedes responder las preguntas y la aplicación te dirá si son correctas.

5. **Visualización de Resultados**:
   - El resumen o el cuestionario se muestran en la pantalla.
   - También puedes ver el texto completo si lo deseas.

---

## 5. **Conclusión**

Este proyecto es una herramienta útil para resumir contenido y generar cuestionarios de manera automática. Es ideal para estudiantes, profesores o cualquier persona que necesite procesar grandes cantidades de texto de manera eficiente.


