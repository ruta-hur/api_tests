import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.user_crud import UserCrudDb as User

@pytest.mark.api

class TestDeposit:
    def test_deposit_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId = account_response.id,
            amount = 1005
        )

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request,
            deposit_request
        )
        assert deposit_response.balance == 1005
        assert account_response.id == deposit_request.accountId

        user_from_db = User.get_user_by_user_name(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Created user is not added to db"

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.id == account_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == deposit_request.amount, "Balance is not updated"


    @pytest.mark.parametrize(
        'test_amount',
        [999.99,
        9000.99]
        )

    def test_deposit_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, test_amount: float, db_session: Session):
        #incorrect amount

        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId = account_response.id,
            amount = test_amount
        )

        deposit_response = api_manager.user_steps.deposit_account_invalid(
            create_user_request,
            deposit_request
        )

        user_from_db = User.get_user_by_user_name(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Created user is not added to db"

        account_id_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_id_from_db.id == account_response.id, "Created account is not added to db"
        assert account_id_from_db.balance == 0, "Balance should not be updated"