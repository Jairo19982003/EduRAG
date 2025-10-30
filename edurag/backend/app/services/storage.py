"""
Supabase Storage Service
Handles file upload/download from Supabase Storage
"""

import os
from typing import Optional
from app.core.database import get_supabase_client

STORAGE_BUCKET = "course-materials"


def ensure_bucket_exists() -> bool:
    """
    Ensure the storage bucket exists, create if not
    
    Returns:
        True if bucket exists or was created
    """
    try:
        supabase = get_supabase_client()
        
        # Try to get bucket info
        buckets = supabase.storage.list_buckets()
        bucket_names = [b.name for b in buckets]
        
        if STORAGE_BUCKET not in bucket_names:
            # Create bucket if it doesn't exist
            supabase.storage.create_bucket(
                STORAGE_BUCKET,
                options={"public": False}
            )
            print(f"✅ Created storage bucket: {STORAGE_BUCKET}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error ensuring bucket exists: {str(e)}")
        return False


async def upload_pdf_to_storage(
    file_content: bytes,
    file_name: str,
    material_id: str
) -> str:
    """
    Upload PDF file to Supabase Storage
    
    Args:
        file_content: Binary content of the file
        file_name: Original file name
        material_id: UUID of the material (used in path)
        
    Returns:
        Storage path of the uploaded file
    """
    try:
        # Ensure bucket exists
        ensure_bucket_exists()
        
        supabase = get_supabase_client()
        
        # Create unique file path: materials/{material_id}/{filename}
        file_extension = os.path.splitext(file_name)[1]
        storage_path = f"materials/{material_id}{file_extension}"
        
        # Upload file
        supabase.storage.from_(STORAGE_BUCKET).upload(
            path=storage_path,
            file=file_content,
            file_options={"content-type": "application/pdf"}
        )
        
        return storage_path
        
    except Exception as e:
        raise Exception(f"Error uploading file to storage: {str(e)}")


async def download_pdf_from_storage(storage_path: str) -> bytes:
    """
    Download PDF file from Supabase Storage
    
    Args:
        storage_path: Path to file in storage
        
    Returns:
        Binary content of the file
    """
    try:
        supabase = get_supabase_client()
        file_content = supabase.storage.from_(STORAGE_BUCKET).download(storage_path)
        return file_content
        
    except Exception as e:
        raise Exception(f"Error downloading file from storage: {str(e)}")


async def delete_pdf_from_storage(storage_path: str) -> bool:
    """
    Delete PDF file from Supabase Storage
    
    Args:
        storage_path: Path to file in storage
        
    Returns:
        True if deleted successfully
    """
    try:
        supabase = get_supabase_client()
        supabase.storage.from_(STORAGE_BUCKET).remove([storage_path])
        return True
        
    except Exception as e:
        print(f"Error deleting file from storage: {str(e)}")
        return False


def get_public_url(storage_path: str) -> Optional[str]:
    """
    Get public URL for a file (if bucket is public)
    
    Args:
        storage_path: Path to file in storage
        
    Returns:
        Public URL or None
    """
    try:
        supabase = get_supabase_client()
        url = supabase.storage.from_(STORAGE_BUCKET).get_public_url(storage_path)
        return url
        
    except Exception as e:
        print(f"Error getting public URL: {str(e)}")
        return None
