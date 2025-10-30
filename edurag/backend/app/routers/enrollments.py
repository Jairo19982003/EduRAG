"""
Enrollments Router - Manage course enrollments
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging

from app.core.database import get_supabase_client

logger = logging.getLogger(__name__)
router = APIRouter()


class EnrollmentCreate(BaseModel):
    """Enrollment creation model"""
    student_id: str  # UUID as string
    course_id: str   # UUID as string
    status: str = "active"


@router.post("/", response_model=dict)
async def create_enrollment(enrollment: EnrollmentCreate):
    """Create a new enrollment"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("enrollments").insert(enrollment.dict()).execute()
        
        if result.data:
            logger.info(f"Enrollment created: student {enrollment.student_id} in course {enrollment.course_id}")
            return {"message": "Enrollment created successfully", "data": result.data[0]}
        else:
            raise HTTPException(status_code=400, detail="Failed to create enrollment")
    except Exception as e:
        logger.error(f"Error creating enrollment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[dict])
async def get_enrollments():
    """Get all enrollments"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("enrollments").select("*, students(*), courses(*)").execute()
        return result.data if result.data else []
    except Exception as e:
        logger.error(f"Error fetching enrollments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{enrollment_id}", response_model=dict)
async def delete_enrollment(enrollment_id: int):
    """Delete an enrollment"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("enrollments").delete().eq("id", enrollment_id).execute()
        
        if result.data:
            logger.info(f"Enrollment deleted: {enrollment_id}")
            return {"message": "Enrollment deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Enrollment not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting enrollment: {e}")
        raise HTTPException(status_code=500, detail=str(e))
