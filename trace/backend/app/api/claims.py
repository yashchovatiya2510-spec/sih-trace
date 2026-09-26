from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.claim import Claim
from app.models.user import User

router = APIRouter()

@router.get("/")
async def list_claims(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # simple mock list for now to unblock
    result = await db.execute(select(Claim).limit(100))
    return result.scalars().all()
