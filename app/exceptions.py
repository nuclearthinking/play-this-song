class AppException(Exception):
    ...


class NotAuthorizedException(AppException):
    ...


class NotEnoughPermissions(AppException):
    ...
