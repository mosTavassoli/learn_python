from abc import ABCMeta, ABC, abstractmethod
from pydantic import BaseModel, Field, field_validator, ValidationError


class IPerson(metaclass=ABCMeta):

    @abstractmethod
    def person_method(self):
        """ This is AN Interface """
        pass


class Teacher(IPerson):

    def person_method(self):
        return "I am a teacher"


class Student(IPerson):

    def person_method(self):
        return "I am a student"


class PersonFactory:

    @staticmethod
    def person_builder(person_type: str):
        match person_type:
            case "student":
                return Student()
            case "teacher":
                return Teacher()
            case _:
                return -1


# if __name__ == "__main__":
#     choice = input("What is your choice: \n")
#     person = PersonFactory().person_builder(choice)
#     print(person.person_method())


# ------------------------------------------
# 1️⃣ Data Validation Layer (Pydantic)
# ------------------------------------------
class PaymentRequest(BaseModel):
    method: str
    amount: float = Field(gt=0, description="Amount must be greater than zero.")

    @field_validator("method")
    def validate_method(cls, v):
        allowed = {"paypal", "stripe", "satispay"}
        if v.lower() not in allowed:
            raise ValueError(f"Unsupported payment method '{v}'. Must be one of {allowed}.")
        return v.lower()


# ------------------------------------------
# 2️⃣ Business Logic Layer (Abstract + Concrete)
# ------------------------------------------
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class PayPalProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        return f"Paid {amount}€ using PayPal."


class StripeProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        return f"Paid {amount}€ using Stripe."


class SatispayProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        return f"Paid {amount}€ using Satispay."


# ------------------------------------------
# 3️⃣ Factory Layer (Object Creation)
# ------------------------------------------
class PaymentFactory:
    @staticmethod
    def get_processor(method: str) -> PaymentProcessor:
        match method.lower():
            case "paypal":
                return PayPalProcessor()
            case "stripe":
                return StripeProcessor()
            case "satispay":
                return SatispayProcessor()
            case _:
                raise ValueError(f"Unknown payment method: {method}")


# ------------------------------------------
# 4️⃣ Client Code (Entry Point)
# ------------------------------------------
if __name__ == "__main__":
    try:
        method = input("Enter payment method (paypal / stripe / satispay): ").strip()
        amount = float(input("Enter amount (€): "))

        # 🧠 Validate user input
        req = PaymentRequest(method=method, amount=amount)

        # 🏭 Get correct processor via Factory
        processor = PaymentFactory.get_processor(req.method)

        # 💸 Process payment
        print(processor.pay(req.amount))

    except ValidationError as ve:
        print(f"⚠️ Input validation error:\n{ve}")
    except ValueError as e:
        print(f"⚠️ Payment error: {e}")
