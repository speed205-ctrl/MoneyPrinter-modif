# MoneyPrinterModif

## Creditos y Reconocimiento
Este proyecto es un fork y una version mejorada basada en el trabajo original de [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo). Agradecemos a los creadores y colaboradores del repositorio original por haber sentado las bases de esta herramienta automatizada de generacion de videos.

---

## Mejoras e Innovaciones Implementadas en MoneyPrinterModif

### 1. Arquitectura de Multi-Agentes de Inteligencia Artificial
Se creo el modulo `app/agents/` con cuatro agentes autonomos especializados:
- IdeaGeneratorAgent (`app/agents/idea_generator.py`): Agente encargado de generar titulos virales e ideas/hooks de alta retencion para cualquier nicho (Terror, Suspenso, Leyendas Urbanas, Historia, Finanzas) con aplicacion automatica en 1-clic al tema del video.
- ScriptDirectorAgent (`app/agents/script_director.py`): Encargado de la direccion narrativa del guion, la inyeccion de pausas ortograficas para lectura fluida, el calculo preciso de palabras por minuto (WPM) ajustado a la velocidad de la voz y la recomendacion del tono ideal.
- MaterialCuratorAgent (`app/agents/material_curator.py`): Encargado de la busqueda y descarga concurrente de metraje de stock (Pexels, Pixabay, Local) con filtrado por relacion de aspecto (9:16 vertical / 16:9 horizontal) y sistema de reintentos mediante tenacity.
- RenderManagerAgent (`app/agents/render_manager.py`): Encargado de gestionar la aceleracion por hardware GPU (NVIDIA NVENC), el fallback automatico a CPU (libx264) y la atenuacion de musica de fondo (-20 dB) con normalizacion de audio.

### 2. Rediseño Visual de la Interfaz (UI/UX - MoneyPrinterModif)
- Tema Glassmorphic Studio: Interfaz estilizada en tono oscuro slate, contenedores traslucidos, bordes con acentos neones y tipografia moderna de Google Fonts (Outfit e Inter).
- Script Studio Viewer: Consola de visualizacion de guion que calcula en tiempo real:
  - Tiempo estimado de duracion del audio.
  - Conteo exacto de palabras y caracteres.
  - Categoria del contenido identificada por IA (Terror, Historia, Noticias, Motivacion).
  - Voz recomendada por IA y velocidad sugerida (ejemplo: es-MX-JorgeNeural a 0.88x).

### 3. Generador de Ideas Virales con IA Integrado
- Acordeon interactivo en la interfaz para ingresar un nicho y generar 5 propuestas de titulos virales con gancho narrativo, con boton para aplicar la idea seleccionada directamente al tema del video.

### 4. Sistema de Recomendacion Inteligente de Voces
- Integracion de motor de recomendacion automatica en `app/services/voice.py` que selecciona la voz mas adecuada segun la tematica del guion (ejemplo: voces graves y pausadas para terror o voces formales para documentales).

### 5. Soporte y Fallback Automatico para Kimi / Moonshot AI
- Auto-deteccion y conmutacion automatica entre los endpoints de Kimi China (`api.moonshot.cn`) e Internacional (`api.moonshot.ai`). Si una API Key devuelve un error 401 en la plataforma china, el sistema conmuta automaticamente al servidor internacional sin interrumpir la experiencia del usuario.

### 6. Auto-Deteccion de Aceleracion por Hardware GPU
- El motor de video ahora detecta automaticamente si la tarjeta grafica del sistema soporta NVIDIA NVENC (`h264_nvenc`), Intel QSV (`h264_qsv`) o AMD AMF (`h264_amf`), activando la GPU de forma predeterminada sin requerir configuracion manual.

### 7. Persistencia de Configuracion y Prompts Personalizados
- Los prompts de sistema y configuraciones personalizadas del usuario se persisten en el archivo `config.toml` para garantizar que no se borren ni se pierdan al recargar la pagina en el navegador.

---

## Instalacion y Uso

### Requisitos Previos
- Python 3.10, 3.11 o 3.12
- FFmpeg instalado en el sistema

### Pasos de Instalacion
1. Clonar el repositorio:
   git clone https://github.com/speed205-ctrl/MoneyPrinter-modif.git
   cd MoneyPrinter-modif

2. Crear y activar entorno virtual:
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/macOS:
   source .venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Iniciar la interfaz WebUI:
   streamlit run webui/Main.py

---

## Licencia y Creditos Originales
Proyecto original: [https://github.com/harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)
Licencia: MIT License (respetando los terminos del repositorio original).
