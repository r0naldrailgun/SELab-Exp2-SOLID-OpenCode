from store.ports import EmailSender, SmsSender, PushSender, Customer


class NotificationService:
    def send_email(self, customer: Customer, message: str) -> None:
        print(f"[email] to {customer.email}: {message}")

    def send_sms(self, customer: Customer, message: str) -> None:
        print(f"[sms] to {customer.phone}: {message}")

    def send_push(self, customer: Customer, message: str) -> None:
        print(f"[push] to {customer.name}: {message}")


class SmsOnlyNotifier:
    def send_sms(self, customer: Customer, message: str) -> None:
        print(f"[sms] to {customer.phone}: {message}")