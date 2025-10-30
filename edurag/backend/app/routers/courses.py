"""
Courses Router - CRUD operations for courses
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

from app.core.database import get_supabase_client

logger = logging.getLogger(__name__)
router = APIRouter()


class CourseCreate(BaseModel):
    """Course creation model"""
    code: str
    name: str
    syllabus: Optional[str] = None
    credits: Optional[int] = 3


class CourseUpdate(BaseModel):
    """Course update model"""
    code: Optional[str] = None
    name: Optional[str] = None
    syllabus: Optional[str] = None
    credits: Optional[int] = None


@router.post("/", response_model=dict)
async def create_course(course: CourseCreate):
    """Create a new course"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("courses").insert(course.dict()).execute()
        
        if result.data:
            logger.info(f"Course created: {course.code}")
            return {"message": "Course created successfully", "data": result.data[0]}
        else:
            raise HTTPException(status_code=400, detail="Failed to create course")
    except Exception as e:
        logger.error(f"Error creating course: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[dict])
async def get_courses():
    """Get all courses"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("courses").select("*").execute()
        return result.data if result.data else []
    except Exception as e:
        logger.error(f"Error fetching courses: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{course_id}", response_model=dict)
async def get_course(course_id: str):
    """Get a specific course"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("courses").select("*").eq("id", course_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Course not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{course_id}/materials", response_model=List[dict])
async def get_course_materials(course_id: str):
    """Get all materials for a course"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("materials").select("*").eq("course_id", course_id).execute()
        return result.data if result.data else []
    except Exception as e:
        logger.error(f"Error fetching course materials: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{course_id}", response_model=dict)
async def update_course(course_id: str, course: CourseUpdate):
    """Update a course"""
    try:
        supabase = get_supabase_client()
        update_data = {k: v for k, v in course.dict(exclude_unset=True).items()}
        
        result = supabase.table("courses").update(update_data).eq("id", course_id).execute()
        
        if result.data:
            logger.info(f"Course updated: {course_id}")
            return {"message": "Course updated successfully", "data": result.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Course not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating course: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{course_id}", response_model=dict)
async def delete_course(course_id: str):
    """Delete a course"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("courses").delete().eq("id", course_id).execute()
        
        if result.data:
            logger.info(f"Course deleted: {course_id}")
            return {"message": "Course deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Course not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting course: {e}")
        raise HTTPException(status_code=500, detail=str(e))
