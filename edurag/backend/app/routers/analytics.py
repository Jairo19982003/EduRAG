"""
Analytics Router - System analytics and statistics
"""

from fastapi import APIRouter, HTTPException
from ..core.database import get_supabase_client
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/stats", response_model=dict)
async def get_stats():
    """Get system statistics"""
    try:
        supabase = get_supabase_client()
        
        # Get counts from each table
        courses = supabase.table("courses").select("*", count="exact").execute()
        students = supabase.table("students").select("*", count="exact").execute()
        materials = supabase.table("materials").select("*", count="exact").execute()
        enrollments = supabase.table("enrollments").select("*", count="exact").execute()
        
        return {
            "courses": courses.count or 0,
            "students": students.count or 0,
            "materials": materials.count or 0,
            "queries": enrollments.count or 0  # Using enrollments as proxy for activity
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {
            "courses": 0,
            "students": 0,
            "materials": 0,
            "queries": 0
        }


@router.get("/detailed", response_model=dict)
async def get_detailed_analytics():
    """Get detailed analytics for dashboard"""
    try:
        supabase = get_supabase_client()
        
        # Get all data
        courses_result = supabase.table("courses").select("*").execute()
        students_result = supabase.table("students").select("*").execute()
        materials_result = supabase.table("materials").select("*, courses(code, name)").execute()
        enrollments_result = supabase.table("enrollments").select("*, students(name, email), courses(code, name)").execute()
        
        courses = courses_result.data or []
        students = students_result.data or []
        materials = materials_result.data or []
        enrollments = enrollments_result.data or []
        
        # Calculate materials per course
        materials_by_course = {}
        for material in materials:
            course_id = material.get('course_id')
            if course_id:
                materials_by_course[course_id] = materials_by_course.get(course_id, 0) + 1
        
        # Calculate enrollments per course
        enrollments_by_course = {}
        for enrollment in enrollments:
            course_id = enrollment.get('course_id')
            if course_id:
                enrollments_by_course[course_id] = enrollments_by_course.get(course_id, 0) + 1
        
        # Build course statistics
        course_stats = []
        for course in courses:
            course_id = course.get('id')
            course_stats.append({
                'id': course_id,
                'code': course.get('code'),
                'name': course.get('name'),
                'materials_count': materials_by_course.get(course_id, 0),
                'enrollments_count': enrollments_by_course.get(course_id, 0)
            })
        
        # Sort by popularity (enrollments)
        course_stats.sort(key=lambda x: x['enrollments_count'], reverse=True)
        
        # Calculate enrollments by cohort
        enrollments_by_cohort = {}
        for enrollment in enrollments:
            student = enrollment.get('students')
            if student:
                cohort = student.get('cohort', 'Sin cohorte')
                enrollments_by_cohort[cohort] = enrollments_by_cohort.get(cohort, 0) + 1
        
        # Calculate enrollments by status
        # Note: Database uses English values (active, inactive, completed)
        enrollments_by_status = {
            'activo': 0,
            'inactivo': 0,
            'completado': 0
        }
        
        # Map English database values to Spanish keys for frontend
        status_map = {
            'active': 'activo',
            'inactive': 'inactivo',
            'completed': 'completado'
        }
        
        for enrollment in enrollments:
            db_status = enrollment.get('status', 'active')
            # Convert English to Spanish
            spanish_status = status_map.get(db_status, 'activo')
            enrollments_by_status[spanish_status] = enrollments_by_status.get(spanish_status, 0) + 1
        
        # Recent activity (last 10 enrollments)
        recent_enrollments = sorted(
            enrollments,
            key=lambda x: x.get('enrollment_date', ''),
            reverse=True
        )[:10]
        
        recent_activity = []
        for enrollment in recent_enrollments:
            student = enrollment.get('students', {})
            course = enrollment.get('courses', {})
            recent_activity.append({
                'type': 'enrollment',
                'student_name': student.get('name', 'N/A'),
                'course_name': f"{course.get('code', '')} - {course.get('name', 'N/A')}",
                'date': enrollment.get('enrollment_date'),
                'status': enrollment.get('status', 'activo')
            })
        
        return {
            'overview': {
                'total_courses': len(courses),
                'total_students': len(students),
                'total_materials': len(materials),
                'total_enrollments': len(enrollments),
                'active_enrollments': enrollments_by_status.get('activo', 0),  # Now correctly mapped from 'active'
                'avg_materials_per_course': round(len(materials) / len(courses), 1) if len(courses) > 0 else 0,
                'avg_enrollments_per_course': round(len(enrollments) / len(courses), 1) if len(courses) > 0 else 0
            },
            'course_stats': course_stats[:10],  # Top 10 courses
            'enrollments_by_cohort': enrollments_by_cohort,
            'enrollments_by_status': enrollments_by_status,
            'recent_activity': recent_activity
        }
        
    except Exception as e:
        logger.error(f"Error getting detailed analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
