import unittest

from plane.number import get_field, FiniteField, Polynomial, ExtensionFiniteField
from plane.util import factorize, is_prime


class CreateFieldTest(unittest.TestCase):
    def test_factor(self):
        for i in range(2, 1002):
            with self.subTest(f"Factor : {i}", i=i):
                factor = factorize(i)

                num = 1
                for p, e in factor.items():
                    num *= pow(p, e)

                self.assertEqual(i, num)

    def test_polynomial_mod(self):
        ff = FiniteField(5)
        one = ff.one
        two = one + one
        three = one + two
        four = two + two

        a = Polynomial(ff, {4: one, 3: two, 2: three, 1: two, 0: one})
        b = Polynomial(ff, {1: one, 0: three})
        c = Polynomial(ff, {1: three, 0: two})
        d = a * b + c
        self.assertEqual(d % a, c, ((d % a).get_min(), c.get_min()))

    def test_polynomial_gcd(self):
        ff = FiniteField(5)
        one = ff.one
        two = one + one
        three = one + two
        four = two + two

        a = Polynomial(ff, {2: one, 1: three, 0: four})
        b = Polynomial(ff, {1: one, 0: four})
        c = Polynomial(ff, {1: one, 0: two})
        ab = a * b
        ac = a * c
        self.assertEqual(ab.gcd(ac), a, (ab.gcd(ac).get_min(), a.get_min()))

    def test_construct_field(self):
        for i in range(2, 10):
            if is_prime(i):
                for p in range(1, 11):
                    n = pow(i, p)
                    if n > 2000:
                        break

                    with self.subTest(f"{n} = {i}**{p}"):
                        field = get_field(n)
                        if p == 1:
                            self.assertIsInstance(field, FiniteField)
                        else:
                            self.assertIsInstance(field, ExtensionFiniteField)

                        check = field.zero
                        for _ in range(1, i):
                            check += field.one
                            self.assertFalse(check.is_zero())
                        check += field.one
                        self.assertTrue(check.is_zero())


if __name__ == '__main__':
    unittest.main()
