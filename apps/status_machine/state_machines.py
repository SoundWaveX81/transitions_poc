from .constants import MachineTypes, OrderStatuses

STATUS_MACHINES = {
    MachineTypes.ORDER.value: {
        "field": "status",  # status field in order model
        "states": OrderStatuses.values_as_list(),
        "transitions": {
            OrderStatuses.CREATED.value: [
                OrderStatuses.DRAFT.value,
                OrderStatuses.ARCHIVED.value,
            ],
            OrderStatuses.DRAFT.value: [
                OrderStatuses.DRAFT.value,
                OrderStatuses.ON_CUSTOMER.value,
                OrderStatuses.ON_COMPANY.value,
                OrderStatuses.ARCHIVED.value,
            ],
            OrderStatuses.ON_CUSTOMER.value: [
                OrderStatuses.ON_COMPANY.value,
                OrderStatuses.REJECTED.value,
                OrderStatuses.LOST.value,
                OrderStatuses.ARCHIVED.value,
            ],
            OrderStatuses.ON_COMPANY.value: [
                OrderStatuses.SUPPORT.value,
                OrderStatuses.REJECTED.value,
                OrderStatuses.LOST.value,
                OrderStatuses.ARCHIVED.value,
            ],
            OrderStatuses.SUPPORT.value: [],
            OrderStatuses.REJECTED.value: [],
            OrderStatuses.LOST.value: [],
            OrderStatuses.ARCHIVED.value: [],
        },
    }
}
