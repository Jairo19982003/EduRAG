"""
Students Router - CRUD operations for students
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import logging

from app.core.database import get_supabase_client

logger = logging.getLogger(__name__)
router = APIRouter()


class StudentCreate(BaseModel):
    """Student creation model"""
    name: str
    email: EmailStr
    cohort: str


class StudentUpdate(BaseModel):
    """Student update model"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cohort: Optional[str] = None


class StudentResponse(BaseModel):
    """Student response model"""
    id: int
    name: str
    email: str
    cohort: str
    created_at: str


@router.post("/", response_model=dict)
async def create_student(student: StudentCreate):
    """Create a new student"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("students").insert({
            "name": student.name,
            "email": student.email,
            "cohort": student.cohort
        }).execute()
        
        if result.data:
            logger.info(f"Student created: {student.email}")
            return {"message": "Student created successfully", "data": result.data[0]}
        else:
            raise HTTPException(status_code=400, detail="Failed to create student")
    except Exception as e:
        logger.error(f"Error creating student: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[dict])
async def get_students():
    """Get all students"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("students").select("*").execute()
        return result.data if result.data else []
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{student_id}", response_model=dict)
async def get_student(student_id: str):
    """Get a specific student"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("students").select("*").eq("id", student_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching student: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{student_id}", response_model=dict)
async def update_student(student_id: str, student: StudentUpdate):
    """Update a student"""
    try:
        supabase = get_supabase_client()
        update_data = {k: v for k, v in student.dict(exclude_unset=True).items()}
        
        result = supabase.table("students").update(update_data).eq("id", student_id).execute()
        
        if result.data:
            logger.info(f"Student updated: {student_id}")
            return {"message": "Student updated successfully", "data": result.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{student_id}", response_model=dict)
async def delete_student(student_id: str):
    """Delete a student and all associated enrollments"""
    try:
        supabase = get_supabase_client()
        
        # First, delete all enrollments for this student
        try:
            enrollments_result = supabase.table("enrollments").delete().eq("student_id", student_id).execute()
            deleted_enrollments = len(enrollments_result.data) if enrollments_result.data else 0
            logger.info(f"Deleted {deleted_enrollments} enrollments for student {student_id}")
        except Exception as e:
            logger.warning(f"Error deleting enrollments: {e}")
        
        # Then delete the student
        result = supabase.table("students").delete().eq("id", student_id).execute()
        
        if result.data:
            logger.info(f"Student deleted: {student_id}")
            return {
                "message": "Student deleted successfully",
                "enrollments_deleted": deleted_enrollments if deleted_enrollments else 0
            }
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student: {e}")
        raise HTTPException(status_code=500, detail=str(e))
