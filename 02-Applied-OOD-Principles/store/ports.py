from dataclasses import dataclass
from typing import List, Protocol, Optional


class OrderLike(Protocol):
    @property
    def id(self) -> int: ...
    @property
    def customer(self) -> 'Customer': ...
    @property
    def payment_method(self) -> str: ...
    @property
    def coupons(self) -> List[str]: ...
    @property
    def status(self) -> str: ...
    @status.setter
    def status(self, value: str) -> None: ...
    def get_items(self) -> List['OrderItem']: ...
    def get_subtotal(self) -> float: ...
    def get_item_count(self) -> int: ...


class OrderValidator(Protocol):
    def validate(self, order: OrderLike) -> None: ...


@dataclass
class DiscountContext:
    subtotal: float
    item_count: int
    is_vip: bool
    coupons: List[str]


class DiscountRule(Protocol):
    def apply(self, context: DiscountContext) -> float: ...


class DiscountCalculator(Protocol):
    def calculate(self, order: OrderLike) -> float: ...


@dataclass
class PricingResult:
    subtotal: float
    discount: float
    shipping: float
    total: float


class PricingService(Protocol):
    def calculate(self, order: OrderLike) -> PricingResult: ...


class PaymentStrategy(Protocol):
    def process(self, customer_data: dict, amount: float) -> str: ...


class PaymentProcessor(Protocol):
    def process(self, order: OrderLike, amount: float) -> str: ...


class OrderRepository(Protocol):
    def save(self, order: OrderLike) -> None: ...
    def load(self, order_id: int) -> Optional[OrderLike]: ...


class EmailSender(Protocol):
    def send_email(self, customer: 'Customer', message: str) -> None: ...


class SmsSender(Protocol):
    def send_sms(self, customer: 'Customer', message: str) -> None: ...


class PushSender(Protocol):
    def send_push(self, customer: 'Customer', message: str) -> None: ...


class ReceiptFormatter(Protocol):
    def format(self, order: OrderLike, pricing: PricingResult, receipt: str) -> str: ...


@dataclass
class Customer:
    id: int
    name: str
    email: str
    phone: str = ""
    is_vip: bool = False
    address: str = ""
    credit_card: str = ""
    bitcoin_address: str = ""


@dataclass
class OrderItem:
    product_id: int
    name: str
    price: float
    quantity: int

    @property
    def line_total(self) -> float:
        return self.price * self.quantity