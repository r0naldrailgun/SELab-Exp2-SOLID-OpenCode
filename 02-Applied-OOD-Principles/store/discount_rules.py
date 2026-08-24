from store.ports import DiscountRule, DiscountContext


class VipDiscountRule:
    def apply(self, context: DiscountContext) -> float:
        if context.is_vip:
            return round(context.subtotal * 0.20, 2)
        return 0.0


class VolumeDiscountRule:
    def apply(self, context: DiscountContext) -> float:
        if context.item_count >= 10:
            return round(context.subtotal * 0.10, 2)
        return 0.0


class CouponDiscountRule:
    def apply(self, context: DiscountContext) -> float:
        if "WELCOME10" in context.coupons:
            return round(context.subtotal * 0.10, 2)
        return 0.0


def build_discount_rules():
    return [
        VipDiscountRule(),
        VolumeDiscountRule(),
        CouponDiscountRule(),
    ]