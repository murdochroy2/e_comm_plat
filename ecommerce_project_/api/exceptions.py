from rest_framework.exceptions import APIException
from rest_framework import status


class InsufficientStockError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Insufficient stock for one or more products"
    default_code = "insufficient_stock"
