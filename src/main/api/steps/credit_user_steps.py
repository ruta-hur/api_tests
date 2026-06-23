from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateCreditUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class CreditUserSteps(BaseSteps):
    def credit_request(self, create_user_request: CreateCreditUserRequest, credit_request_request: CreditRequestRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,password=create_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_created()
        ).post(credit_request_request)
        return response

    def credit_request_invalid(self, create_user_request: CreateCreditUserRequest, credit_request_request: CreditRequestRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,password=create_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.forbidden()
        ).post(credit_request_request)
        return response

    def credit_repay(self, create_user_request: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,password=create_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid(self, create_user_request: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,password=create_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.unprocessable()
        ).post(credit_repay_request)
        return response