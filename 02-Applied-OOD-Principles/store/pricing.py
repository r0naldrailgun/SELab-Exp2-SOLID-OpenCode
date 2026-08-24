from typing import List
from store.ports import DiscountCalculator, DiscountRule, DiscountContext, OrderLike
from store.discount_rules import build_discount_rules


class DiscountCalculator:
    def __init__(self, rules: List[DiscountRule] = None):
        self.rules = rules or build_discount_rules()

    def calculate(self, order: OrderLike) -> float:
        context = DiscountContext(
            subtotal=order.get_subtotal(),
            item_count=order.get_item_count(),
            is_vip=order.customer.is_vip,
            coupons=order.coupons,
        )
        for rule in self.rules:
            discount = rule.apply(context)
            if discount > 0:
                return discount
        return 0.0