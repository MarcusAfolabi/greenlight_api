from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/balance")
async def get_balance(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's payout balance."""
    # TODO: Implement get balance
    pass

@router.post("/request")
async def request_payout(amount: float, current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Request a payout."""
    # TODO: Implement request payout
    pass

@router.get("/history")
async def get_payout_history(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's payout history."""
    # TODO: Implement get payout history
    pass
