import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api

class TestTransfer:
    def test_transfer_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        account1_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId = account1_response.id,
            amount = 5000
        )

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request,
            deposit_request
        )
        account2_response = api_manager.user_steps.create_account(create_user_request)

        transfer_request = TransferRequest(
            fromAccountId = account1_response.id,
            toAccountId = account2_response.id,
            amount = 1000
        )

        transfer_response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert transfer_response.fromAccountIdBalance == deposit_response.balance - transfer_request.amount
        assert transfer_response.fromAccountId == account1_response.id
        assert transfer_response.toAccountId == account2_response.id

        user_from_db = User.get_user_by_user_name(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Created user is not added to db"

        account_id_from_db = Account.get_account_by_id(db_session, account1_response.id)
        assert account_id_from_db.id == account1_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == deposit_request.amount - transfer_request.amount, "Balance is not updated"

        account_id_from_db = Account.get_account_by_id(db_session, account2_response.id)
        assert account_id_from_db.id == account2_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == transfer_request.amount, "Balance is not updated"


    def test_transfer_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        #transfer is less than balance

        account1_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId = account1_response.id,
            amount = 1001
        )

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request,
            deposit_request
        )
        account2_response = api_manager.user_steps.create_account(create_user_request)

        transfer_request = TransferRequest(
            fromAccountId = account1_response.id,
            toAccountId = account2_response.id,
            amount = 5000
        )

        transfer_response = api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        user_from_db = User.get_user_by_user_name(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Created user is not added to db"

        account_id_from_db = Account.get_account_by_id(db_session, account1_response.id)
        assert account_id_from_db.id == account1_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == deposit_request.amount, "Balance is not updated"

        account_id_from_db = Account.get_account_by_id(db_session, account2_response.id)
        assert account_id_from_db.id == account2_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == 0, "Balance is not updated"