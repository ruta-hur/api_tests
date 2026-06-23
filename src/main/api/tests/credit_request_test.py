import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.account_table import Account
from src.main.api.models.create_user_request import CreateCreditUserRequest, CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api

class TestCreditRequest:
    def test_credit_request_valid(self, api_manager: ApiManager, create_credit_user_request:CreateCreditUserRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_request_request = CreditRequestRequest(
            accountId = account_response.id,
            amount = 5000,
            termMonths = 12
        )
        credit_response = api_manager.credit_user_steps.credit_request(
            create_credit_user_request,
            credit_request_request
        )
        assert credit_response.amount == credit_request_request.amount
        assert credit_response.termMonths == credit_request_request.termMonths

        user_from_db = User.get_user_by_user_name(db_session, create_credit_user_request.username)
        assert user_from_db.username == create_credit_user_request.username, "Created user is not added to db"

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.account_id == credit_request_request.accountId, "Deposit account doesn't match credit request"
        assert credit_from_db.amount == credit_request_request.amount, "Credit amount doesn't match"
        assert credit_from_db.term_months == credit_request_request.termMonths, "Credit term doesn't match"


    def test_credit_request_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        #incorrect role (ROLE_USER instead of ROLE_CREDIT_SECRET)

        account_response = api_manager.user_steps.create_account(create_user_request)

        credit_request_request = CreditRequestRequest(
            accountId = account_response.id,
            amount = 5000,
            termMonths = 12
        )
        credit_response = api_manager.credit_user_steps.credit_request_invalid(
            create_user_request,
            credit_request_request
        )

        user_from_db = User.get_user_by_user_name(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Created user is not added to db"
        assert user_from_db.role == create_user_request.role, "Created user role is not according to requested role"

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.balance == 0, "Balance should be zero"