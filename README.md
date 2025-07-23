# MAGIC POST - Generador de Contenido con IA

MAGIC POST es una aplicación que utiliza Inteligencia Artificial para generar contenido optimizado para diferentes plataformas de redes sociales. Con este generador, puedes crear posts atractivos y relevantes, adaptados al tono y audiencia específicos que necesites.

![MAGIC POST Logo](frontend/public/logo192.png)

## Características

- ✍️ Generación de contenido para diferentes redes sociales (Twitter, Instagram, LinkedIn, Blog)
- 🎨 Generación de imágenes complementarias
- 🌈 Personalización de tono y estilo
- 🌍 Soporte multilingüe
- 🚀 Modelos de IA avanzados (LLaMA 3, Mistral)

## Requisitos previos

- Node.js (v14 o superior)
- Python (v3.9 o superior)
- Git

## Estructura del proyecto

```
project-ai-llms-group-4/
├── backend/             # Servidor FastAPI
│   ├── __init__.py
│   ├── generate_with_rag.py
│   ├── generator.py
│   ├── image_generator.py
│   ├── ingest.py
│   ├── main.py
│   ├── requirements.txt
│   └── retriever.py
├── data/                # Datos para entrenamiento/RAG
└── frontend/            # Cliente React
    ├── package.json
    ├── public/
    └── src/
```

## Configuración del entorno

### Variables de entorno

1. Crea un archivo `.env` en la raíz del proyecto:

```
# API Keys
OPENROUTER_API_KEY=your_openrouter_api_key_here
STABILITY_API_KEY=your_stability_api_key_here

# Configuración
MODEL_ID=meta-llama/llama-3-8b-instruct  # o el modelo que prefieras
```

## Instalación

### Backend (Python/FastAPI)

1. Navega al directorio del backend:

```bash
cd backend
```

2. Crea y activa un entorno virtual:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Frontend (React)

1. Navega al directorio del frontend:

```bash
cd frontend
```

2. Instala las dependencias:

```bash
npm install
```

## Ejecución

### Iniciar el backend

1. Desde la raíz del proyecto, activa el entorno virtual si aún no está activado:

```bash
# Windows
backend\venv\Scripts\activate

# macOS/Linux
source backend/venv/bin/activate
```

2. Inicia el servidor FastAPI:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

El backend estará disponible en: http://localhost:8000

### Iniciar el frontend

1. En una nueva terminal, navega al directorio del frontend:

```bash
cd frontend
```

2. Inicia la aplicación React:

```bash
npm start
```

La aplicación estará disponible en: http://localhost:3001

## API Endpoints

- `GET /`: Estado de la API
- `POST /generate`: Genera contenido y opcionalmente una imagen

## Tecnologías utilizadas

### Backend
- FastAPI - Framework web de Python
- OpenRouter - API para acceso a modelos de lenguaje
- Stability AI - Generación de imágenes con IA

### Frontend
- React - Biblioteca de JavaScript para interfaces de usuario
- Axios - Cliente HTTP para realizar peticiones
- Styled Components - CSS-in-JS
- Framer Motion - Animaciones

## Solución de problemas

### Error en la generación de imágenes

Si encuentras errores relacionados con `image_generator.py`, asegúrate de:

1. Tener una clave API válida para Stability AI
2. Verificar la sintaxis correcta del parámetro 'prompt' en la solicitud

### Problemas de CORS

Si experimentas problemas de CORS, verifica:

1. Que la configuración CORS en `main.py` incluya el origen de tu frontend
2. Que estés utilizando la URL correcta en `API_URL` en el frontend

## Contribuidores

- Equipo 4 - IA Bootcamp

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.