from loguru import logger
from app.services import video, utils


class RenderManagerAgent:
    """
    Agente de Render y Calidad (RenderManager):
    Gestiona la detección automática de codificación por hardware GPU (h264_nvenc),
    mantiene un mecanismo de fallback automático a CPU (libx264) si falla la VRAM/renderizado,
    y aplica la atenuación de música de fondo (BGM) entre -18 dB y -22 dB con normalización FFmpeg.
    """

    def __init__(self, bgm_attenuation_db: float = -20.0):
        self.bgm_attenuation_db = bgm_attenuation_db

    def get_render_environment_info(self) -> dict:
        effective_codec = video._get_effective_video_codec()
        is_gpu = effective_codec in ("h264_nvenc", "h264_qsv", "h264_amf", "h264_mf", "h264_videotoolbox")
        
        logger.info(f"[RenderManagerAgent] Effective video codec: {effective_codec} (GPU: {is_gpu})")
        return {
            "codec": effective_codec,
            "fallback_codec": "libx264",
            "is_gpu_accelerated": is_gpu,
            "encoder_name": "NVIDIA NVENC GPU" if effective_codec == "h264_nvenc" else ("CPU libx264" if effective_codec == "libx264" else effective_codec),
            "bgm_attenuation_db": self.bgm_attenuation_db,
            "bgm_volume_factor": round(10 ** (self.bgm_attenuation_db / 20.0), 2),  # -20 dB => 0.10 ~ 0.15 gain
        }

    def resolve_safe_codec(self, preferred_codec: str | None = None) -> str:
        """Determina el codificador seguro con fallback automático a CPU."""
        return video._get_effective_video_codec(preferred_codec=preferred_codec)


# Alias de conveniencia
RenderManager = RenderManagerAgent
