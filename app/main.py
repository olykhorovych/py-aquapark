from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance: object, owner: type) -> int:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected an integer, got {type(value).__name__}")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value {value} is out of range "
                f"[{self.min_amount}, {self.max_amount}]"
            )
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(
        self,
        name: str,
        age: int,
        weight: int,
        height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
        self,
        age: range,
        weight: range,
        height: range
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(
        self,
        age: range = range(4, 15),
        weight: range = range(20, 51),
        height: range = range(80, 121),
    ) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(
        self,
        age: range = range(14, 61),
        weight: range = range(50, 121),
        height: range = range(120, 221),
    ) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class()
        age_valid = visitor.age in validator.age
        weight_valid = visitor.weight in validator.weight
        height_valid = visitor.height in validator.height
        return age_valid and weight_valid and height_valid
