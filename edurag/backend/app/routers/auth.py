"""Authentication Router"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login():
    """Login endpoint"""
    return {"message": "Login endpoint - to be implemented"}


@router.post("/register")
async def register():
    """Register endpoint"""
    return {"message": "Register endpoint - to be implemented"}
