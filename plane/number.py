from dataclasses import dataclass, field as data_field
from typing import Union, Dict

from plane.util import factorize


@dataclass
class FiniteField:
    order: int  # prime number

    @property
    def one(self):
        return FiniteFieldElement(1, self)

    @property
    def zero(self):
        return FiniteFieldElement(0, self)

    def element_list(self):
        for i in range(self.order):
            yield FiniteFieldElement(i, self)


@dataclass
class FiniteFieldElement:
    # Element of Finite Field
    number: int
    finite_field: FiniteField

    def __post_init__(self):
        self.number %= self.finite_field.order

    def __sub__(self, other: 'FiniteFieldElement'):
        return FiniteFieldElement(
            self.number - other.number,
            self.finite_field
        )

    def __mul__(self, other: 'FiniteFieldElement'):
        return FiniteFieldElement(
            self.number * other.number,
            self.finite_field
        )

    def __add__(self, other: 'FiniteFieldElement'):
        return FiniteFieldElement(
            self.number + other.number,
            self.finite_field
        )

    def __neg__(self):
        return FiniteFieldElement(-self.number, self.finite_field)

    def __truediv__(self, other):
        return FiniteFieldElement(
            self.number * pow(other.number, -1, self.finite_field.order),
            self.finite_field
        )

    def is_zero(self):
        return self.number == 0


class AddContainer:
    def __init__(self):
        self.body = {}

    def update(self, k, v):
        if k in self.body:
            self.body[k] += v
        else:
            self.body[k] = v


@dataclass
class Polynomial:
    over: FiniteField
    values: Dict[int, FiniteFieldElement] = data_field(default_factory=dict)
    degree: int = data_field(init=False)

    def __post_init__(self):
        self.values = {
            p: v for p, v in self.values.items()
            if not v.is_zero()
        }
        if self.values:
            self.degree = max(self.values)
        else:
            # deg(f*g) = deg(f) + deg(g) 를 맞추기 위해 0의 경우,
            # degree를 negative infinite로 두지만 지금은 그럴 필욘 없다.
            self.degree = -1

    @property
    def lead_coefficient(self) -> FiniteFieldElement:
        return self.values[self.degree]

    def is_zero(self):
        return self.degree == -1

    def __add__(self, other: 'Polynomial'):
        d = dict(self.values)
        for k, v in other.values.items():
            if k in d:
                d[k] += v
            else:
                d[k] = v
        return Polynomial(over=self.over, values=d)

    def __sub__(self, other: 'Polynomial'):
        d = dict(self.values)
        for k, v in other.values.items():
            if k in d:
                d[k] -= v
            else:
                d[k] = -v
        return Polynomial(over=self.over, values=d)

    def __mul__(self, other: Union[FiniteFieldElement, 'Polynomial']):
        if isinstance(other, FiniteFieldElement):
            return Polynomial(
                over=self.over,
                values={
                    p: v*other
                    for p, v in self.values.items()
                }
            )

        elif isinstance(other, Polynomial):
            result = AddContainer()
            for k1, v1 in self.values.items():
                for k2, v2 in other.values.items():
                    result.update(k1+k2, v1*v2)
            return Polynomial(over=self.over, values=result.body)

    def __truediv__(self, other: FiniteFieldElement):
        return Polynomial(
            over=self.over,
            values={
                p: v / other
                for p, v in self.values.items()
            }
        )

    def __mod__(self, other: 'Polynomial'):
        divisor = self
        q = Polynomial(over=self.over, values={})

        while divisor.degree >= other.degree:
            degree_diff = divisor.degree - other.degree
            div_coefficient = divisor.lead_coefficient / other.lead_coefficient
            div = Polynomial(
                over=self.over,
                values={
                    degree_diff: div_coefficient
                }
            )
            q += div
            divisor -= other * div

        return divisor

    def to_monic(self):
        lead_coefficient = self.lead_coefficient
        return self / lead_coefficient

    def gcd(self, other: 'Polynomial'):
        first, second = self, other
        if first.degree < second.degree:
            first, second = second, first

        while not second.is_zero():
            first, second = second, first % second

        return first.to_monic()

    def is_constant(self):
        return self.degree == 0

    def is_irreducible(self) -> bool:
        # https://en.wikipedia.org/wiki/Factorization_of_polynomials_over_finite_fields#Rabin's_test_of_irreducibility
        if self.degree < 1 == 0:
            return False

        for p in factorize(self.degree):
            test_polynomial = Polynomial(
                over=self.over,
                values={
                    self.over.order ** (self.degree // p): self.over.one,
                    1: -self.over.one
                }
            )
            if not test_polynomial.gcd(self).is_constant():
                return False

        splitting = Polynomial(
            over=self.over,
            values={
                self.over.order ** self.degree: self.over.one,
                1: -self.over.one
            }
        )
        return (splitting % self).is_zero()

    def get_min(self):
        return {k: v.number for k, v in self.values.items()}


@dataclass
class ExtensionFiniteField:
    finite_field: FiniteField
    degree: int  # >= 2
    mod: Polynomial

    @property
    def zero(self):
        return ExtensionFiniteFieldElement(
            extension_finite_field=self,
            numbers=Polynomial(
                over=self.finite_field,
                values={}
            )
        )

    @property
    def one(self):
        return ExtensionFiniteFieldElement(
            extension_finite_field=self,
            numbers=Polynomial(
                over=self.finite_field,
                values={0: self.finite_field.one}
            )
        )


@dataclass
class ExtensionFiniteFieldElement:
    # Element of Extension Finite Field
    extension_finite_field: ExtensionFiniteField
    numbers: Polynomial

    def __add__(self, other: 'ExtensionFiniteFieldElement'):
        return ExtensionFiniteFieldElement(
            extension_finite_field=self.extension_finite_field,
            numbers=self.numbers+other.numbers
        )

    def is_zero(self):
        return self.numbers.is_zero()


Field = Union[FiniteField, ExtensionFiniteField]  # 사칙연산이 가능한 수 쳬계


def find_irreducible(field: FiniteField, degree: int) -> Polynomial:
    if degree < 2:
        raise ValueError("Degree should be greater than 1")

    for first in field.element_list():
        for second in field.element_list():
            polynomial = Polynomial(
                over=field,
                values={
                    degree: field.one,
                    1: first, 0: second
                }
            )
            if polynomial.is_irreducible():
                return polynomial

    if field.order > 2:
        raise ValueError("May be strategy wrong")

    for rep in range(5, min(100, 2**degree), 2):
        lower = {degree: field.one}
        for d in range(degree):
            if rep & (1 << d):
                lower[d] = field.one
        polynomial = Polynomial(over=field, values=lower)
        if polynomial.is_irreducible():
            return polynomial

    raise ValueError("I cannot find irreducible polynomial for given degree")


def get_field(n: int) -> Field:
    factor = factorize(n)
    if len(factor) != 1:
        raise ValueError("Field element should be the power of prime number")

    for number, p in factor.items():
        base_field = FiniteField(number)
        if p == 1:
            return base_field
        else:
            return ExtensionFiniteField(base_field, p, find_irreducible(base_field, p))
    return FiniteField(n)
