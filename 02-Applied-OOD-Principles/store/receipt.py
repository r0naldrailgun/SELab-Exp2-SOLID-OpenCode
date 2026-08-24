from store.ports import ReceiptFormatter, OrderLike, PricingResult


class ReceiptFormatter:
    def format(self, order: OrderLike, pricing: PricingResult, receipt: str) -> str:
        lines = [f"--- Receipt for order {order.id} ---"]
        for item in order.get_items():
            lines.append(f"  {item.name:20s} x{item.quantity}  ${item.line_total:.2f}")
        lines.append(f"  Subtotal    ${pricing.subtotal:.2f}")
        lines.append(f"  Discount   -${pricing.discount:.2f}")
        lines.append(f"  Shipping    ${pricing.shipping:.2f}")
        lines.append(f"  TOTAL       ${pricing.total:.2f}")
        lines.append(f"  Payment     {receipt}")
        return "\n".join(lines)

    def print(self, order: OrderLike, pricing: PricingResult, receipt: str) -> None:
        print(self.format(order, pricing, receipt))