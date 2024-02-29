from enum import Enum

from starlette import status


class AppStatus(Enum):
    SUCCESS = status.HTTP_200_OK, 200, 'SUCCESS.'
    DELETED_SUCCESSFULLY = status.HTTP_200_OK, 200, 'DELETED_SUCCESSFULLY'
    UPDATE_SUCCESSFULLY = status.HTTP_200_OK, 200, 'UPDATE_SUCCESSFULLY'

    ERROR_MISSING_TOKEN_ERROR = status.HTTP_401_UNAUTHORIZED, 401, 'ERROR_MISSING_TOKEN_ERROR'
    ERROR_PASSWORD_INVALID = status.HTTP_401_UNAUTHORIZED, 401, 'ACCOUNT_OR_PASSWORD_INVALID'
    ERROR_INACTIVE_USER = status.HTTP_401_UNAUTHORIZED, 401, 'INACTIVE_USER'
    ERROR_INVALID_TOKEN = status.HTTP_401_UNAUTHORIZED, 401, 'INVALID_TOKEN'

    ERROR_404_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'NOT_FOUND'
    ERROR_EMAIL_NOT_EXIST = status.HTTP_404_NOT_FOUND, 404, 'EMAIL_NOT_EXIST'
    ERROR_USER_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'USER_NOT_FOUND'
    ERROR_CUSTOMER_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'CUSTOMER_NOT_FOUND'
    ERROR_PROMOTION_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'PROMOTION_NOT_FOUND'
    ERROR_BRANCH_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'BRANCH_NOT_FOUND'
    ERROR_EMPLOYEE_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'EMPLOYEE_NOT_FOUND'

    ERROR_ACCOUNT_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'ACCOUNT_ALREADY_EXIST'
    ERROR_EMAIL_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'EMAIL_ALREADY_EXIST'
    ERROR_PHONE_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'PHONE_ALREADY_EXIST'
    ERROR_PROMOTION_CODE_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'PHONE_ALREADY_EXIST'
    ERROR_BRANCH_ADDRESS_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'BRANCH_ADDRESS_EXIST'
    ERROR_BRANCH_PHONE_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'BRANCH_PHONE_EXIST'
    ERROR_BRANCH_EMAIL_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'BRANCH_EMAIL_EXIST'
    ERROR_BRANCH_NAME_DETIL_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'BRANCH_NAME_DETAIL_EXIST'

    ERROR_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR, 500, 'SERVER_ERROR'
    ERROR_AWS_EXCEPTION = status.HTTP_500_INTERNAL_SERVER_ERROR, 500, 'ERROR_AWS_EXCEPTION'
    ERROR_UPLOAD_FILE_FAILED = status.HTTP_500_INTERNAL_SERVER_ERROR, 500, 'ERROR_UPLOAD_FILE_FAILED'

    # need to refactor soon
    ERROR_VALIDATION = status.HTTP_400_BAD_REQUEST, 1000, 'ERROR_VALIDATION'
    LOGIN_SUCCESS = status.HTTP_200_OK, 200, 'LOGIN_SUCCESS'

    @property
    def status_code(self):
        return self.value[0]

    @property
    def app_status_code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]

    @property
    def meta(self):
        return dict(status_code=self.value[0], message=self.value[2])
