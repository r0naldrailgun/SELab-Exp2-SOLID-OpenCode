from typing import Optional
from store.ports import OrderRepository, OrderLike


class MySqlDatabase:
    def __init__(self, connection_string: str = "mysql://localhost/store"):
        self._connection_string = connection_string
        self._orders = {}

    def save_order(self, order: OrderLike) -> None:
        self._orders[order.id] = order

    def load_order(self, order_id: int) -> Optional[OrderLike]:
        return self._orders.get(order_id)

    # OrderRepository protocol methods
    def save(self, order: OrderLike) -> None:
        self.save_order(order)

    def load(self, order_id: int) -> Optional[OrderLike]:
        return self.load_order(order_id)