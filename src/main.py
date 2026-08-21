from fastapi import FastAPI, Depends, HTTPException
from src.repository import AccountRepository
from src.dependencies import get_repository
from src.dto import AccountDTO

app = FastAPI(title="SecureBank API")

@app.get("/accounts", response_model=list[AccountDTO])
def list_accounts(repo: AccountRepository = Depends(get_repository)):
    accounts = repo.list_all()
    return [AccountDTO.from_account(a) for a in accounts]

@app.get("/accounts/{account_id}", response_model=AccountDTO)
def get_account(account_id: str, repo: AccountRepository = Depends(get_repository)):
    acc = repo.get(account_id)
    if acc is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountDTO.from_account(acc)