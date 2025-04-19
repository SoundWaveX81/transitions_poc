import importlib
import typing

from django.core.exceptions import ValidationError

from apps.status_machine.constants import MachineTypes, OrderStatuses
from apps.status_machine.models import OrderStatus
from apps.status_machine.state_machines import STATUS_MACHINES

if typing.TYPE_CHECKING:
    from apps.order.models import Order


class OrderStatusMachine:
    def __init__(self, instance: "Order"):
        self.machine_name = MachineTypes.ORDER.value
        self.instance = instance

        try:
            config = STATUS_MACHINES[self.machine_name]
        except KeyError:
            raise ValueError(f"Status Machine {self.machine_name} is not defined")

        self.field = config["field"]
        self.states = config["states"]
        self.transitions = config["transitions"]
        self.current_status = getattr(instance, self.field)

    def can_transition(self, to_state: str) -> bool | list[str]:
        if self.current_status.code not in self.states or to_state not in self.states:
            return False
        return to_state in self.transitions.get(self.current_status.code, [])

    def transition(self, to_state: str, save: bool = True):
        if to_state not in self.states:
            raise ValidationError(f"Destination status {to_state} is not valid")

        if not self.can_transition(to_state):
            raise ValidationError(f"Transition from {self.current_status.code} to {to_state} is not allowed")

        try:
            validators_module = importlib.import_module(
                "apps.status_machine.validations.order_status_machine_transition_validations"
            )
            validator_func = getattr(
                validators_module,
                f"validate_{OrderStatuses(self.current_status.code).name}_to_{OrderStatuses(to_state).name}",
                None,
            )
            if validator_func:
                validator_func(self.instance)
        except ModuleNotFoundError:
            raise ValidationError("validations Method for this transitions are not implemented yet")

        to_state_instance = OrderStatus.objects.get(code=to_state)

        setattr(self.instance, self.field, to_state_instance)
        if save:
            self.instance.save(update_fields=[self.field])

        self.current_status = to_state_instance
