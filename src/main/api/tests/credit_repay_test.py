import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateCreditUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api

class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, create_credit: CreditRequestRequest, db_session: Session  ):
        account_response, credit_response = create_credit

        credit_repay_request = CreditRepayRequest(
            creditId = credit_response.creditId,
            accountId = account_response.id,
            amount = credit_response.amount
        )

        repay_response = api_manager.credit_user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request
        )

        assert repay_response.amountDeposited == credit_repay_request.amount, "Credit amount doesn't match"

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.balance == 0, "Balance is not updated"

    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, create_credit: CreditRequestRequest, db_session: Session  ):
        #The amount exceeds the outstanding debt balance
        account_response, credit_response = create_credit

        credit_repay_request = CreditRepayRequest(
            creditId = credit_response.creditId,
            accountId = account_response.id,
            amount = credit_response.amount + 1000

        )

        repay_response = api_manager.credit_user_steps.credit_repay_invalid(
            create_credit_user_request,
            credit_repay_request
        )

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.balance == credit_response.amount, "Balance should not be updated"