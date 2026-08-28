from fastapi import APIRouter, Depends, HTTPException
from src.services.account_service import AccountService
from src.dependencies import get_service
from src.dto import AccountDTO
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/accounts", tags=["accounts"])

class CreateAccountRequest(BaseModel):
    name: str
    initial_deposit: float = 0.0

class DepositWithdrawRequest(BaseModel):
    amount: float

class TransferRequest(BaseModel):
    to_id: str
    amount: float

@router.get("", response_model=list[AccountDTO])
def list_accounts(svc: AccountService = Depends(get_service)):
    return [AccountDTO.from_account(a) for a in svc.list_accounts()]

@router.get("/{account_id}", response_model=AccountDTO)
def get_account(account_id: str, svc: AccountService = Depends(get_service)):
    try:
        return AccountDTO.from_account(svc._get(account_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Account not found")

@router.post("", response_model=AccountDTO, status_code=201)
def create_account(req: CreateAccountRequest, svc: AccountService = Depends(get_service)):
    acc = svc.create_account(req.name, req.initial_deposit)
    return AccountDTO.from_account(acc)

@router.post("/{account_id}/deposit", response_model=AccountDTO)
def deposit(account_id: str, req: DepositWithdrawRequest, svc: AccountService = Depends(get_service)):
    try:
        return AccountDTO.from_account(svc.deposit(account_id, req.amount))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{account_id}/withdraw", response_model=AccountDTO)
def withdraw(account_id: str, req: DepositWithdrawRequest, svc: AccountService = Depends(get_service)):
    try:
        return AccountDTO.from_account(svc.withdraw(account_id, req.amount))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{account_id}/transfer", response_model=AccountDTO)
def transfer(account_id: str, req: TransferRequest, svc: AccountService = Depends(get_service)):
    try:
        return AccountDTO.from_account(svc.transfer(account_id, req.to_id, req.amount))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{account_id}", response_model=AccountDTO)
def close_account(account_id: str, svc: AccountService = Depends(get_service)):
    try:
        return AccountDTO.from_account(svc.close_account(account_id))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))