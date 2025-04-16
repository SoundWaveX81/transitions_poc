from django_json_widget.widgets import JSONEditorWidget

from django.contrib import admin
from django.db.models import JSONField

from .models import Order, OrderLine


class OrderLineInline(admin.StackedInline):
    model = OrderLine
    fields = ("product",)
    show_change_link = True
    readonly_fields = ("product",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderLineInline,
    ]
    list_select_related = True
    readonly_fields = ("total_price",)
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget(options={"mode": "view", "modes": ["view"]})},
    }


admin.site.register(OrderLine)
