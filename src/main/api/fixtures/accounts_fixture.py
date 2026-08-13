import pytest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.random.random_data import RandomData


@pytest.fixture
def deposit_account(api_manager, create_user_request):
    account_response = api_manager.user_steps.create_account(create_user_request)

    deposit_request = DepositRequest(
        accountId = account_response.id,
        amount = RandomData.random_deposit_amount()
    )

    deposit_response = api_manager.user_steps.deposit_account(
        create_user_request,
        deposit_request
    )

    return account_response, deposit_request, deposit_response

