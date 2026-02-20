"""Tests for Chapter 32: Numeric Computing."""

import cmath
import math
import random
import statistics
from decimal import Decimal, InvalidOperation
from fractions import Fraction


class TestMathModule:
    """Test math module functions."""

    def test_constants(self) -> None:
        """math provides fundamental constants."""
        assert abs(math.pi - 3.14159265) < 1e-6
        assert abs(math.e - 2.71828182) < 1e-6
        assert math.inf > 1e308
        assert math.isnan(math.nan)

    def test_basic_functions(self) -> None:
        """math provides common mathematical functions."""
        assert math.sqrt(16) == 4.0
        assert math.ceil(3.2) == 4
        assert math.floor(3.8) == 3
        assert math.factorial(5) == 120

    def test_logarithms(self) -> None:
        """math provides logarithmic functions."""
        assert math.log(math.e) == 1.0
        assert math.log10(100) == 2.0
        assert math.log2(8) == 3.0

    def test_trigonometry(self) -> None:
        """math provides trigonometric functions."""
        assert abs(math.sin(math.pi / 2) - 1.0) < 1e-10
        assert abs(math.cos(0) - 1.0) < 1e-10

    def test_number_theory(self) -> None:
        """math provides number theory functions."""
        assert math.gcd(12, 8) == 4
        assert math.lcm(4, 6) == 12
        assert math.isclose(0.1 + 0.2, 0.3)

    def test_cmath_complex(self) -> None:
        """cmath handles complex number operations."""
        z = complex(3, 4)
        assert abs(cmath.phase(z) - 0.9272952) < 1e-5
        assert abs(abs(z) - 5.0) < 1e-10


class TestDecimal:
    """Test Decimal for precise arithmetic."""

    def test_decimal_precision(self) -> None:
        """Decimal avoids floating-point rounding errors."""
        assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
        assert 0.1 + 0.2 != 0.3  # float fails

    def test_decimal_from_string(self) -> None:
        """Decimal should be created from strings for precision."""
        d = Decimal("3.14159")
        assert str(d) == "3.14159"

    def test_decimal_quantize(self) -> None:
        """quantize rounds to a specific number of places."""
        d = Decimal("3.14159")
        assert d.quantize(Decimal("0.01")) == Decimal("3.14")

    def test_decimal_invalid(self) -> None:
        """Invalid operations raise InvalidOperation."""
        try:
            Decimal("not_a_number")
            assert False, "Should have raised"
        except InvalidOperation:
            pass


class TestFractions:
    """Test Fraction for exact rationals."""

    def test_fraction_creation(self) -> None:
        """Fractions represent exact rational numbers."""
        f = Fraction(1, 3)
        assert f.numerator == 1
        assert f.denominator == 3

    def test_fraction_auto_reduce(self) -> None:
        """Fractions auto-reduce to lowest terms."""
        assert Fraction(4, 8) == Fraction(1, 2)

    def test_fraction_arithmetic(self) -> None:
        """Fractions support exact arithmetic."""
        assert Fraction(1, 3) + Fraction(1, 6) == Fraction(1, 2)
        assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)

    def test_fraction_from_float(self) -> None:
        """Fractions can approximate floats."""
        f = Fraction(0.5)
        assert f == Fraction(1, 2)


class TestRandomAndStatistics:
    """Test random and statistics modules."""

    def test_random_seed_reproducible(self) -> None:
        """Setting seed makes random reproducible."""
        random.seed(42)
        a = random.random()
        random.seed(42)
        b = random.random()
        assert a == b

    def test_random_choice(self) -> None:
        """choice picks from a sequence."""
        random.seed(42)
        items = ["a", "b", "c", "d"]
        result = random.choice(items)
        assert result in items

    def test_random_shuffle(self) -> None:
        """shuffle randomizes a list in place."""
        random.seed(42)
        items = [1, 2, 3, 4, 5]
        random.shuffle(items)
        assert sorted(items) == [1, 2, 3, 4, 5]

    def test_random_sample(self) -> None:
        """sample returns unique elements."""
        random.seed(42)
        result = random.sample(range(100), k=5)
        assert len(result) == 5
        assert len(set(result)) == 5

    def test_statistics_mean(self) -> None:
        """statistics.mean computes arithmetic mean."""
        assert statistics.mean([1, 2, 3, 4, 5]) == 3

    def test_statistics_median(self) -> None:
        """statistics.median returns the middle value."""
        assert statistics.median([1, 3, 5]) == 3
        assert statistics.median([1, 3, 5, 7]) == 4

    def test_statistics_stdev(self) -> None:
        """statistics.stdev computes standard deviation."""
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        assert abs(statistics.stdev(data) - 2.0) < 0.2
