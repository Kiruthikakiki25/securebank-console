from src.json_repository import JsonAccountRepository
from src.repository import AccountRepository

def get_repository() -> AccountRepository:
    return JsonAccountRepository()