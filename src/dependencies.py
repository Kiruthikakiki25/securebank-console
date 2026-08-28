from src.json_repository import JsonAccountRepository
from src.services.account_service import AccountService

def get_service() -> AccountService:
    repo = JsonAccountRepository()
    return AccountService(repo)