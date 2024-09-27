# Sintetizador
mediante el uso de langchain y el algoritmo tdf-idf se obtienen resúmenes a partir de videos alojados en YouTube  y de archivos  ppt,docx,pdf 

# TextRank: Funcionamiento y Matemáticas Subyacentes

## Introducción

TextRank es un algoritmo de procesamiento de lenguaje natural basado en grafos, inspirado en el algoritmo PageRank de Google. Se utiliza principalmente para extraer palabras clave y generar resúmenes automáticos de textos.

## Funcionamiento Básico

1. **Construcción del grafo**: El texto se convierte en un grafo donde las palabras o frases son nodos, y las conexiones entre ellas son aristas.

2. **Iteración**: Se aplica un algoritmo iterativo para calcular la importancia de cada nodo.

3. **Extracción**: Se seleccionan los nodos (palabras o frases) más importantes según sus puntuaciones.

## Matemáticas Detrás de TextRank

### 1. Fórmula Principal

La puntuación de cada nodo se calcula utilizando la siguiente fórmula:

```
WS(Vi) = (1-d) + d * Σ (WS(Vj) / Out(Vj))
```

Donde:
- `WS(Vi)` es la puntuación del nodo i
- `d` es un factor de amortiguación (generalmente 0.85)
- `Vj` son los nodos conectados a Vi
- `Out(Vj)` es el número de conexiones salientes de Vj

### 2. Proceso Iterativo

El algoritmo se repite hasta que las puntuaciones convergen o se alcanza un número máximo de iteraciones.

### 3. Matriz de Adyacencia

La estructura del grafo se representa mediante una matriz de adyacencia A, donde:

```
A[i][j] = 1 si hay una conexión entre i y j
A[i][j] = 0 si no hay conexión
```

### 4. Normalización

Las puntuaciones se normalizan para que sumen 1:

```
WS_norm(Vi) = WS(Vi) / Σ WS(Vk)
```

## Aplicaciones

1. **Extracción de palabras clave**: Se seleccionan las palabras con las puntuaciones más altas.

2. **Generación de resúmenes**: Se eligen las frases más importantes basándose en sus puntuaciones.

## Ventajas y Limitaciones

### Ventajas
- No requiere entrenamiento previo
- Independiente del idioma
- Eficiente computacionalmente

### Limitaciones
- No considera el significado semántico profundo
- Puede ser sensible a la estructura del texto

## Conclusión

TextRank es un algoritmo poderoso y versátil para el procesamiento de texto, que combina la teoría de grafos con el procesamiento del lenguaje natural para extraer información importante de manera eficiente.

# Guia de instalación del proyecto

REQUISISTOS:
```
python 3.8 o superior
git 
```

Clonar el repositorio mediante el siguiente comando:

```bash
$ git clone https://github.com/simsimi2143/Sintetizador.git
```

Instalar las librerias necesarias para ejecutar el proyecto mediante el siguiente comando:

```bash
pip install -r requirements.txt
```

Para ejecutar el proyecto simplemente debe ejecuter lo siguiente:

```bash
cd .\Sintetizador\
```

ya dentro de la carpeta de sintetiazador se ejecuta el siguiente comando:
```bash
\Sintetizador> streamlit run app.py
```