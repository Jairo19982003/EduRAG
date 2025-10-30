"""
Script to configure Supabase Storage bucket for PDF uploads
"""

from app.services.storage import ensure_bucket_exists

if __name__ == "__main__":
    print("=" * 60)
    print("  Configuring Supabase Storage Bucket")
    print("=" * 60)
    print()
    
    success = ensure_bucket_exists()
    
    if success:
        print("\n✅ Storage bucket configured successfully!")
        print("\nYou can now upload PDFs through the AdminView interface.")
        print("The system will automatically:")
        print("  1. Upload PDF to Supabase Storage")
        print("  2. Extract text using pdfplumber")
        print("  3. Chunk text into 500-token segments")
        print("  4. Generate embeddings with OpenAI")
        print("  5. Store chunks in material_chunks table")
    else:
        print("\n❌ Failed to configure storage bucket")
        print("\nPlease check:")
        print("  - SUPABASE_URL is set correctly in .env")
        print("  - SUPABASE_SERVICE_ROLE_KEY is set correctly in .env")
        print("  - You have permissions to create buckets")
