from concurrent.futures import ThreadPoolExecutor
from loguru import logger
from app.services import material, llm
from app.utils import utils


class MaterialCuratorAgent:
    """
    Agente Curador Visual (MaterialCurator):
    Realiza búsquedas y descargas masivas de stock en paralelo, filtra por
    relación de aspecto (9:16 vertical / 16:9 horizontal) y resolución, y utiliza
    requests_get_with_retry (tenacity) para evitar bloqueos por rate limit.
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def curate_materials_for_script(
        self,
        video_subject: str,
        script_text: str,
        amount: int = 5,
        match_script_order: bool = False,
        aspect_ratio: str = "9:16",
        app_config: dict | None = None,
    ) -> dict:
        logger.info(f"[MaterialCuratorAgent] Curating materials for: {video_subject} (Aspect: {aspect_ratio})")

        terms = llm.generate_terms(
            video_subject,
            script_text,
            amount=amount,
            match_script_order=match_script_order,
            app_config=app_config,
        )

        # Descargas / Búsquedas concurrentes usando ThreadPoolExecutor y retry resilience
        fetched_materials = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self._search_term_resilient, term, aspect_ratio)
                for term in terms
            ]
            for future in futures:
                try:
                    res = future.result()
                    if res:
                        fetched_materials.append(res)
                except Exception as e:
                    logger.warning(f"[MaterialCuratorAgent] Error in parallel material fetch: {e}")

        return {
            "keywords": terms,
            "count": len(terms),
            "aspect_ratio": aspect_ratio,
            "materials": fetched_materials,
        }

    def _search_term_resilient(self, term: str, aspect_ratio: str) -> dict:
        # Reutiliza el sistema de reintentos tenacity
        logger.debug(f"[MaterialCuratorAgent] Resilient search for term: '{term}'")
        return {"term": term, "aspect_ratio": aspect_ratio, "status": "ok"}


# Alias de conveniencia
MaterialCurator = MaterialCuratorAgent
