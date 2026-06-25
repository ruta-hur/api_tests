import random, pytest
from src.main.api.models.credit_request_request import CreditRequestRequest


@pytest.fixture
def create_credit(api_manager, create_credit_user_request):
    account_response = api_manager.user_steps.create_account(create_credit_user_request)
    credit_request = CreditRequestRequest(
        accountId = account_response.id,
        amount = random.randint(5000, 15000),
        termMonths = 12
    )
    credit_response = api_manager.credit_user_steps.credit_request(
        create_credit_user_request,
        credit_request
    )
    return account_response, credit_response