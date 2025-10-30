"""
Database connection management for Supabase
"""

from supabase import create_client, Client
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global Supabase client instance
_supabase_client: Optional[Client] = None


async def init_db():
    """Initialize Supabase client"""
    global _supabase_client
    try:
        _supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        logger.info("Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        raise


def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    if _supabase_client is None:
        raise RuntimeError("Supabase client not initialized. Call init_db() first.")
    return _supabase_client


async def close_db():
    """Close Supabase connection"""
    global _supabase_client
    if _supabase_client:
        logger.info("Closing Supabase connection")
        _supabase_client = None
