import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateCreditUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api

class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(
            create_credit_user_request
        )

        credit_request_request = CreditRequestRequest(
            accountId = account_response.id,
            amount = 5000,
            termMonths = 12
        )
        credit_response = api_manager.credit_user_steps.credit_request(
            create_credit_user_request,
            credit_request_request
        )

        credit_repay_request = CreditRepayRequest(
            creditId = credit_response.creditId,
            accountId = account_response.id,
            amount = credit_request_request.amount,
        )

        repay_response = api_manager.credit_user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request
        )
        assert repay_response.creditId == credit_repay_request.creditId
        assert repay_response.amountDeposited == credit_repay_request.amount

        user_from_db = User.get_user_by_user_name(db_session, create_credit_user_request.username)
        assert user_from_db.username == create_credit_user_request.username, "Created user is not added to db"

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.account_id == credit_request_request.accountId, "Deposit account doesn't match credit request"
        assert credit_from_db.amount == credit_request_request.amount, "Credit amount doesn't match"
        assert credit_from_db.term_months == credit_request_request.termMonths, "Credit term doesn't match"

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.id == account_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == 0, "Balance is not updated"

    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, db_session: Session):
        #The amount exceeds the outstanding debt balance

        account_response = api_manager.user_steps.create_account(
            create_credit_user_request
        )

        credit_request_request = CreditRequestRequest(
            accountId = account_response.id,
            amount = 5000,
            termMonths=12
        )
        credit_response = api_manager.credit_user_steps.credit_request(
            create_credit_user_request,
            credit_request_request
        )

        credit_repay_request = CreditRepayRequest(
            creditId = credit_response.creditId,
            accountId = account_response.id,
            amount = credit_request_request.amount + 1000
        )

        repay_response = api_manager.credit_user_steps.credit_repay_invalid(
            create_credit_user_request,
            credit_repay_request
        )

        user_from_db = User.get_user_by_user_name(db_session, create_credit_user_request.username)
        assert user_from_db.username == create_credit_user_request.username, "Created user is not added to db"

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.account_id == credit_request_request.accountId, "Deposit account doesn't match credit request"
        assert credit_from_db.amount == credit_request_request.amount, "Credit amount doesn't match"
        assert credit_from_db.term_months == credit_request_request.termMonths, "Credit term doesn't match"

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.id == account_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == credit_request_request.amount, "Balance should not be updated"