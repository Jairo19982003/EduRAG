"""
Script to create material_chunks table and indexes in Supabase
Run this once to set up the vector database structure
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_vector_database():
    """Create material_chunks table and indexes in Supabase"""
    
    # Initialize Supabase client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
        return False
    
    supabase: Client = create_client(url, key)
    
    # Read SQL file
    sql_file = "sql/create_material_chunks.sql"
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("📝 Reading SQL script...")
        print(f"   File: {sql_file}")
        print(f"   Size: {len(sql_content)} characters\n")
        
        # Split SQL into individual statements
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        print(f"🚀 Executing {len(statements)} SQL statements...\n")
        
        # Execute each statement
        for i, statement in enumerate(statements, 1):
            # Skip comments and empty statements
            if not statement or statement.startswith('--'):
                continue
            
            # Get first line for display
            first_line = statement.split('\n')[0][:60]
            print(f"   [{i}/{len(statements)}] {first_line}...")
            
            try:
                # Note: Supabase client doesn't support raw SQL execution directly
                # You need to execute this SQL through Supabase SQL Editor or psycopg2
                pass
            except Exception as e:
                print(f"      ⚠️  Error: {str(e)}")
        
        print("\n" + "="*60)
        print("⚠️  IMPORTANT: Execute the SQL script manually")
        print("="*60)
        print("\nThe Supabase Python client doesn't support raw SQL execution.")
        print("Please follow these steps:\n")
        print("1. Open Supabase Dashboard: https://supabase.com/dashboard")
        print("2. Select your project: zoeemafduhhnmdyfqbwo")
        print("3. Go to 'SQL Editor' in the left sidebar")
        print("4. Create a new query")
        print("5. Copy and paste the content from: sql/create_material_chunks.sql")
        print("6. Click 'Run' to execute\n")
        print("Alternative: Use psql client:")
        print("psql postgresql://postgres:[password]@db.zoeemafduhhnmdyfqbwo.supabase.co:5432/postgres")
        print("\n")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: SQL file not found: {sql_file}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("  EduRAG - Vector Database Setup")
    print("="*60)
    print()
    
    success = setup_vector_database()
    
    if success:
        print("✅ Instructions displayed successfully!")
        print("\nAfter running the SQL script, you can proceed with:")
        print("  - Implementing PDF upload endpoint")
        print("  - Testing vector search functionality")
    else:
        print("❌ Setup failed. Please check the errors above.")
