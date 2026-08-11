import json
import re
from loguru import logger
from app.services import llm


class IdeaGeneratorAgent:
    """
    Agente Generador de Ideas y Títulos Virales (IdeaGenerator):
    Genera propuestas de títulos de alto impacto y premisas/hooks virales
    para cualquier nicho (ej. Terror, Suspenso, Leyendas, Ciencia, Historia).
    """

    def __init__(self, default_language: str = "es"):
        self.default_language = default_language

    def generate_ideas(
        self,
        niche: str,
        count: int = 5,
        language: str = "",
        app_config: dict | None = None,
    ) -> list[dict]:
        target_lang = language or self.default_language
        logger.info(f"[IdeaGeneratorAgent] Generating {count} viral ideas for niche: '{niche}'")

        prompt = f"""
# Role: Viral Short-Form Video Idea Generator

## Task:
Generate {count} compelling, viral, high-retention video titles and hooks for short videos (TikTok/Reels/Shorts) in the niche: "{niche}".

## Output Format:
Return ONLY a valid JSON list of objects with "title" and "hook" keys. Example:
[
  {{"title": "El secreto guardado en la habitación 404", "hook": "Un hotel antiguo escondía una habitación que no aparecía en los planos."}},
  {{"title": "La llamada de medianoche que nadie debió contestar", "hook": "Un teléfono público suena todas las noches a las 3:33 AM con el mismo susurro."}}
]

## Rules:
1. Return ONLY raw JSON list, no markdown wrapper, no extra text.
2. The language MUST be: {target_lang}.
""".strip()

        response = llm._generate_response(prompt=prompt, app_config=app_config)

        if not response or response.startswith("Error:"):
            logger.warning(f"[IdeaGeneratorAgent] LLM failed to generate ideas: {response}")
            return self._fallback_ideas(niche, count)

        try:
            # Clean JSON formatting wrappers if present
            clean_json = response.strip()
            clean_json = re.sub(r"^```json\s*", "", clean_json, flags=re.MULTILINE)
            clean_json = re.sub(r"^```\s*", "", clean_json, flags=re.MULTILINE)
            clean_json = clean_json.strip()

            ideas = json.loads(clean_json)
            if isinstance(ideas, list):
                return ideas[:count]
        except Exception as exc:
            logger.warning(f"[IdeaGeneratorAgent] JSON parse error: {exc}. Raw response: {response}")

        return self._fallback_ideas(niche, count)

    @staticmethod
    def _fallback_ideas(niche: str, count: int = 5) -> list[dict]:
        return [
            {
                "title": f"El misterio oculto de {niche}",
                "hook": f"Un suceso inexplicable revelado sobre {niche} que pocos conocen.",
            },
            {
                "title": f"La leyenda urbana mas oscura de {niche}",
                "hook": f"Una historia escalofriante transmitida por generaciones sobre {niche}.",
            },
            {
                "title": f"Lo que nadie te conto sobre {niche}",
                "hook": f"Un secreto perturbador que cambio la forma de ver {niche}.",
            },
        ][:count]


# Alias de conveniencia
IdeaGenerator = IdeaGeneratorAgent
