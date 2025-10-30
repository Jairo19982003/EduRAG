"""
PDF Processing Service
Handles PDF text extraction, chunking, and embedding generation
"""

import os
import uuid
from typing import List, Dict, Optional, Tuple
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AsyncOpenAI
import tiktoken

from app.core.config import settings
from app.core.database import get_supabase_client

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# Initialize tokenizer
encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken"""
    return len(encoding.encode(text))


async def extract_text_from_pdf(file_path: str) -> Tuple[str, Dict]:
    """
    Extract text from PDF file
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Tuple of (extracted_text, metadata)
    """
    try:
        text_content = []
        metadata = {
            "total_pages": 0,
            "extraction_method": "pdfplumber",
            "page_breaks": []
        }
        
        with pdfplumber.open(file_path) as pdf:
            metadata["total_pages"] = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                
                if page_text:
                    # Track where page breaks occur in the text
                    current_length = sum(len(t) for t in text_content)
                    metadata["page_breaks"].append({
                        "page": page_num,
                        "char_position": current_length
                    })
                    
                    text_content.append(f"\n\n--- Page {page_num} ---\n\n")
                    text_content.append(page_text)
        
        full_text = "".join(text_content)
        metadata["total_chars"] = len(full_text)
        metadata["total_tokens"] = count_tokens(full_text)
        
        return full_text, metadata
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    metadata: Optional[Dict] = None
) -> List[Dict]:
    """
    Split text into chunks using LangChain's RecursiveCharacterTextSplitter
    
    Args:
        text: Text to chunk
        chunk_size: Target chunk size in tokens
        chunk_overlap: Overlap between chunks in tokens
        metadata: Optional metadata to include with each chunk
        
    Returns:
        List of chunk dictionaries with text, index, and metadata
    """
    try:
        # Convert token-based sizes to approximate character sizes
        # Average: 1 token ≈ 4 characters for English text
        char_chunk_size = chunk_size * 4
        char_overlap = chunk_overlap * 4
        
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=char_chunk_size,
            chunk_overlap=char_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Split text into chunks
        text_chunks = text_splitter.split_text(text)
        
        # Create chunk objects with metadata
        chunks = []
        page_breaks = metadata.get("page_breaks", []) if metadata else []
        
        for idx, chunk_text in enumerate(text_chunks):
            # Calculate which page this chunk starts on
            chunk_start_pos = text.find(chunk_text)
            chunk_page = 1
            
            for page_break in page_breaks:
                if chunk_start_pos >= page_break["char_position"]:
                    chunk_page = page_break["page"]
            
            chunk_obj = {
                "chunk_text": chunk_text,
                "chunk_index": idx,
                "token_count": count_tokens(chunk_text),
                "metadata": {
                    "page": chunk_page,
                    "char_length": len(chunk_text),
                    **(metadata or {})
                }
            }
            chunks.append(chunk_obj)
        
        return chunks
        
    except Exception as e:
        raise Exception(f"Error chunking text: {str(e)}")


async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using OpenAI
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embedding vectors
    """
    try:
        # OpenAI API allows batch embedding (max 2048 texts per request)
        batch_size = 2048
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            response = await openai_client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=batch
            )
            
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
        
    except Exception as e:
        raise Exception(f"Error generating embeddings: {str(e)}")


async def store_chunks_in_database(
    chunks: List[Dict],
    embeddings: List[List[float]],
    material_id: str
) -> int:
    """
    Store chunks and their embeddings in the database
    
    Args:
        chunks: List of chunk dictionaries
        embeddings: List of embedding vectors
        material_id: UUID of the material
        
    Returns:
        Number of chunks stored
    """
    try:
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match")
        
        # Prepare chunk records for insertion
        chunk_records = []
        for chunk, embedding in zip(chunks, embeddings):
            chunk_records.append({
                "id": str(uuid.uuid4()),
                "material_id": material_id,
                "chunk_text": chunk["chunk_text"],
                "chunk_index": chunk["chunk_index"],
                "token_count": chunk["token_count"],
                "embedding": embedding,
                "metadata": chunk["metadata"]
            })
        
        # Insert chunks in batches (Supabase has a limit)
        batch_size = 100
        supabase = get_supabase_client()
        
        for i in range(0, len(chunk_records), batch_size):
            batch = chunk_records[i:i + batch_size]
            supabase.table("material_chunks").insert(batch).execute()
        
        return len(chunk_records)
        
    except Exception as e:
        raise Exception(f"Error storing chunks in database: {str(e)}")


async def process_pdf_file(
    file_path: str,
    material_id: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> Dict:
    """
    Complete PDF processing pipeline:
    1. Extract text from PDF
    2. Chunk the text
    3. Generate embeddings
    4. Store in database
    
    Args:
        file_path: Path to PDF file
        material_id: UUID of the material
        chunk_size: Target chunk size in tokens
        chunk_overlap: Overlap between chunks in tokens
        
    Returns:
        Processing summary with statistics
    """
    try:
        # Update status to processing
        supabase = get_supabase_client()
        supabase.table("materials").update({
            "processing_status": "processing"
        }).eq("id", material_id).execute()
        
        # Step 1: Extract text
        text, pdf_metadata = await extract_text_from_pdf(file_path)
        
        if not text or len(text.strip()) < 100:
            raise Exception("PDF appears to be empty or contains too little text")
        
        # Step 2: Chunk text
        chunks = chunk_text(text, chunk_size, chunk_overlap, pdf_metadata)
        
        if not chunks:
            raise Exception("No chunks created from PDF")
        
        # Step 3: Generate embeddings
        chunk_texts = [chunk["chunk_text"] for chunk in chunks]
        embeddings = await generate_embeddings(chunk_texts)
        
        # Step 4: Store in database
        chunks_stored = await store_chunks_in_database(chunks, embeddings, material_id)
        
        # Update material status
        supabase.table("materials").update({
            "processing_status": "completed",
            "chunks_count": chunks_stored,
            "processed_at": "now()"
        }).eq("id", material_id).execute()
        
        # Return summary
        return {
            "success": True,
            "material_id": material_id,
            "total_pages": pdf_metadata["total_pages"],
            "total_chars": pdf_metadata["total_chars"],
            "total_tokens": pdf_metadata["total_tokens"],
            "chunks_created": chunks_stored,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap
        }
        
    except Exception as e:
        # Update status to failed
        supabase.table("materials").update({
            "processing_status": "failed"
        }).eq("id", material_id).execute()
        
        raise Exception(f"PDF processing failed: {str(e)}")


async def delete_material_chunks(material_id: str) -> int:
    """
    Delete all chunks for a material (cleanup)
    
    Args:
        material_id: UUID of the material
        
    Returns:
        Number of chunks deleted
    """
    try:
        supabase = get_supabase_client()
        result = supabase.table("material_chunks").delete().eq(
            "material_id", material_id
        ).execute()
        
        # Reset material processing status
        supabase.table("materials").update({
            "processing_status": "pending",
            "chunks_count": 0,
            "processed_at": None
        }).eq("id", material_id).execute()
        
        return len(result.data) if result.data else 0
        
    except Exception as e:
        raise Exception(f"Error deleting chunks: {str(e)}")
