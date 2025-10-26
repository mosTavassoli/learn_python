from abc import ABC, abstractmethod
from typing import List


class Coffee(ABC):
    @abstractmethod
    def get_desc(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass


class SimpleCoffee(Coffee):
    def get_desc(self):
        return "Simple Coffee"

    def get_cost(self):
        return 2.00


class CoffeeDecorator(Coffee):
    _coffee: Coffee = None

    def __init__(self, coffee):
        self._coffee = coffee

    def get_desc(self):
        return self._coffee.get_desc()

    def get_cost(self):
        return self._coffee.get_cost()


class MilkCoffee(CoffeeDecorator):
    def __init__(self, coffee):
        super().__init__(coffee)

    def get_desc(self):
        return self._coffee.get_desc() + ", Milk"

    def get_cost(self):
        return self._coffee.get_cost() + 0.5


class SugarCoffee(CoffeeDecorator):
    def __init__(self, coffee):
        super().__init__(coffee)

    def get_desc(self):
        return self._coffee.get_desc() + ", Sugar"

    def get_cost(self):
        return self._coffee.get_cost() + 0.3


def make_coffee(base: Coffee, decorators: List[type[CoffeeDecorator]]) -> Coffee:
    coffee = base
    for decorator_cls in decorators:
        coffee = decorator_cls(coffee)
    return coffee


if __name__ == "__main__":
    base = SimpleCoffee()
    toppings = [MilkCoffee, SugarCoffee]
    coffee = make_coffee(base, toppings)

    print(f"Cost: {coffee.get_cost():.2f}")
    print(f"Description: {coffee.get_desc()}")

    # coffee = SimpleCoffee()
    # print(f"{coffee.get_cost()}, {coffee.get_desc()}")
    #
    # coffee = MilkCoffee(coffee)
    # print(f"{coffee.get_cost()}, {coffee.get_desc()}")
    #
    # coffee = SugarCoffee(coffee)
    # print(f"{coffee.get_cost()}, {coffee.get_desc()}")
