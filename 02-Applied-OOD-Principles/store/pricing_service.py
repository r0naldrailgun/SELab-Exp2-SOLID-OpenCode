from store.ports import PricingService, PricingResult, DiscountCalculator, OrderLike


class PricingService:
    def __init__(self, discount_calculator: DiscountCalculator):
        self.discount_calculator = discount_calculator

    def calculate(self, order: OrderLike) -> PricingResult:
        subtotal = order.get_subtotal()
        discount = self.discount_calculator.calculate(order)
        shipping = 5.0 if subtotal < 100 else 0.0
        total = round(subtotal - discount + shipping, 2)
        return PricingResult(
            subtotal=subtotal,
            discount=discount,
            shipping=shipping,
            total=total,
        )