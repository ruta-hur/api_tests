import random
import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.account_table import Account
from src.main.api.models.create_user_request import CreateCreditUserRequest, CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api

class TestCreditRequest:
    def test_credit_request_valid(self, api_manager: ApiManager, create_credit_user_request:CreateCreditUserRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_request_request = CreditRequestRequest(
            accountId = account_response.id,
            amount = random.randint(5000, 15000),
            termMonths = 12
        )
        credit_response = api_manager.credit_user_steps.credit_request(
            create_credit_user_request,
            credit_request_request
        )
        assert credit_response.amount == credit_request_request.amount, "Credit amount doesn't match"
        assert credit_response.termMonths == credit_request_request.termMonths, "Credit term doesn't match"


        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.account_id == credit_request_request.accountId, "Deposit account doesn't match credit request"
        assert credit_from_db.amount == credit_request_request.amount, "Credit amount doesn't match"


    def test_credit_request_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        #incorrect role (ROLE_USER instead of ROLE_CREDIT_SECRET)

        account_response = api_manager.user_steps.create_account(create_user_request)

        credit_request_request = CreditRequestRequest(
            accountId = account_response.id,
            amount = random.randint(5000, 15000),
            termMonths = 12
        )
        credit_response = api_manager.credit_user_steps.credit_request_invalid(
            create_user_request,
            credit_request_request
        )

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.balance == 0, "Balance should be zero"