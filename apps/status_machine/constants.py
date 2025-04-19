from enum import Enum


class OrderStatuses(Enum):
    CREATED = 1000
    DRAFT = 2000
    ON_CUSTOMER = 3000
    ON_COMPANY = 4000
    SUPPORT = 5000
    REJECTED = 8000
    LOST = 9000
    ARCHIVED = 10000

    @staticmethod
    def values_as_list():
        return [item.value for item in OrderStatuses]

    @staticmethod
    def labels_as_list():
        return [item.name for item in OrderStatuses]


class MachineTypes(Enum):
    ORDER = "order"
