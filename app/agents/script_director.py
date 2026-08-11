import math
from loguru import logger
from app.services import llm, voice


class ScriptDirectorAgent:
    """
    Agente Director y Guionista (ScriptDirector):
    Estructura guiones narrativos de alta retención para Reels/TikTok/Shorts,
    optimiza las pausas ortográficas (...) para voces neuronales en cualquier LLM
    (incluyendo Gemma 4 / Ollama, OpenAI, Kimi) y calcula el tiempo de audio
    ajustado a la velocidad de la voz (WPM).
    """

    def __init__(self, default_language: str = "es"):
        self.default_language = default_language

    def generate_and_direct(
        self,
        subject: str,
        language: str = "",
        paragraph_number: int = 1,
        script_prompt: str = "",
        custom_system_prompt: str = "",
        app_config: dict | None = None,
    ) -> dict:
        target_language = language or self.default_language
        logger.info(f"[ScriptDirectorAgent] Directing script for subject: {subject}")

        # Inyectar instrucción de pausas ortográficas para TTS
        enhanced_prompt = (
            f"{custom_system_prompt}\n"
            "Asegúrate de incluir pausas dramáticas con puntos suspensivos (...) y comas (,) "
            "para que la locución de voz se escuche con pausas naturales."
        ).strip()

        script_text = llm.generate_script(
            video_subject=subject,
            language=target_language,
            paragraph_number=paragraph_number,
            video_script_prompt=script_prompt,
            custom_system_prompt=enhanced_prompt,
            app_config=app_config,
        )

        voice_rec = voice.get_voice_recommendation(
            video_subject=subject,
            script=script_text,
            language=target_language,
        )

        voice_rate = voice_rec.get("recommended_rate", 1.0)
        metrics = self.analyze_script(script_text, voice_rate=voice_rate)

        return {
            "script": script_text,
            "voice_recommendation": voice_rec,
            "metrics": metrics,
        }

    @staticmethod
    def analyze_script(script_text: str, voice_rate: float = 1.0) -> dict:
        words = script_text.split()
        word_count = len(words)
        char_count = len(script_text)
        
        # Tasa estándar de habla: ~140 Palabras Por Minuto (WPM) ajustada a la velocidad de la voz
        wpm = max(40.0, 140.0 * voice_rate)
        est_seconds = math.ceil((word_count / wpm) * 60) if word_count > 0 else 0
        minutes = est_seconds // 60
        seconds = est_seconds % 60
        time_formatted = f"{minutes}:{seconds:02d}"

        return {
            "word_count": word_count,
            "char_count": char_count,
            "wpm": round(wpm, 1),
            "voice_rate": voice_rate,
            "estimated_seconds": est_seconds,
            "estimated_time_formatted": time_formatted,
        }


# Alias de conveniencia
ScriptDirector = ScriptDirectorAgent
