"""
Configuration settings for EduRAG Backend
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    APP_NAME: str = "EduRAG"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # CORS settings - will be parsed from comma-separated string
    # 🔧 CONFIGURACIÓN CORS PARA PRODUCCIÓN
    # En desarrollo: http://localhost:5173,http://localhost:3000
    # En producción: URL de Vercel configurada
    # También puedes configurarlo vía variable de entorno CORS_ORIGINS en Render
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://edu-rag-pc2d.vercel.app"
    # ✅ CORS configurado para permitir:
    # - Desarrollo local: localhost:5173, localhost:3000
    # - Producción Vercel: edu-rag-pc2d.vercel.app
    # ⚠️ NOTA: NO uses barra diagonal (/) al final de las URLs
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Supabase settings
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # RAG Configuration
    RAG_CHUNK_SIZE: int = 500
    RAG_CHUNK_OVERLAP: int = 50
    RAG_TOP_K: int = 5
    RAG_SIMILARITY_THRESHOLD: float = 0.7
    
    # Server Configuration
    API_PREFIX: str = "/api"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
