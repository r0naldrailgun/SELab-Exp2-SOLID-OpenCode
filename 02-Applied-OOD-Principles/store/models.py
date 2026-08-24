from dataclasses import dataclass, field
from typing import List
from store.ports import OrderLike, Customer, OrderItem


@dataclass
class Order:
    id: int
    customer: Customer
    items: List[OrderItem] = field(default_factory=list)
    status: str = "pending"
    payment_method: str = ""
    coupons: List[str] = field(default_factory=list)

    @property
    def subtotal(self) -> float:
        return sum(item.line_total for item in self.items)

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

    # OrderLike protocol methods
    def get_items(self) -> List[OrderItem]:
        return self.items

    def get_subtotal(self) -> float:
        return self.subtotal

    def get_item_count(self) -> int:
        return self.item_count


class BundleOrder:
    def __init__(self, id: int, customer: Customer, orders: List[Order]):
        self.id = id
        self.customer = customer
        self.orders = orders
        self.status = "pending"
        self.payment_method = ""
        self.coupons = []

    # OrderLike protocol methods
    def get_items(self) -> List[OrderItem]:
        return [item for order in self.orders for item in order.items]

    def get_subtotal(self) -> float:
        return sum(order.get_subtotal() for order in self.orders)

    def get_item_count(self) -> int:
        return sum(order.get_item_count() for order in self.orders)