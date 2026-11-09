"""Run verification tests with: python -m unittest test_calculator.py -v"""
import math
import unittest
from calculator import amortization_schedule, monthly_payment


class TestLoanCalculator(unittest.TestCase):
    def test_known_payment(self):
        # Benchmark: $200,000 at 6% over 30 years.
        self.assertAlmostEqual(monthly_payment(200_000, 6, 30), 1199.1010503055138, places=7)

    def test_zero_interest(self):
        result = amortization_schedule(12_000, 0, 3)
        self.assertAlmostEqual(result["required_monthly_payment"], 12000 / 36)
        self.assertEqual(result["months_to_payoff"], 36)
        self.assertAlmostEqual(result["total_interest"], 0)
        self.assertAlmostEqual(result["total_paid"], 12000)

    def test_extra_payments_save_interest_and_time(self):
        baseline = amortization_schedule(25_000, 6.5, 5)
        faster = amortization_schedule(25_000, 6.5, 5, 100)
        self.assertLess(faster["total_interest"], baseline["total_interest"])
        self.assertLess(faster["months_to_payoff"], baseline["months_to_payoff"])

    def test_no_extra_means_same_schedule(self):
        self.assertEqual(
            amortization_schedule(15_000, 5, 4),
            amortization_schedule(15_000, 5, 4, 0)
        )

    def test_one_payment_for_large_extra(self):
        result = amortization_schedule(5_000, 5, 5, 100_000)
        self.assertEqual(result["months_to_payoff"], 1)
        self.assertAlmostEqual(result["total_paid"], 5000 * (1 + .05 / 12))

    def test_last_balance_zero_and_payment_not_overpaid(self):
        for extra in (0, 20, 300, 100_000):
            with self.subTest(extra=extra):
                result = amortization_schedule(10_000, 7, 3, extra)
                self.assertEqual(result["schedule"][-1]["Remaining Balance"], 0)
                self.assertLessEqual(result["months_to_payoff"], 36)
                self.assertTrue(all(row["Remaining Balance"] >= 0 for row in result["schedule"]))
                self.assertAlmostEqual(
                    sum(row["Principal"] for row in result["schedule"]), 10_000, places=6
                )

    def test_invalid_inputs(self):
        invalid = [
            (0, 5, 3, 0), (-100, 5, 3, 0), (10_000, -1, 3, 0),
            (10_000, 41, 3, 0), (10_000, 5, 0, 0), (10_000, 5, 41, 0),
            (10_000, 5, 3, -10), (float("nan"), 5, 3, 0),
            (10_000, float("inf"), 3, 0), (10_000, 5, 2.5, 0),
            ("hello", 5, 3, 0),
        ]
        for args in invalid:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    amortization_schedule(*args)

    def test_large_valid_loan(self):
        result = amortization_schedule(1_000_000, 40, 40)
        self.assertTrue(math.isfinite(result["total_interest"]))
        self.assertEqual(result["months_to_payoff"], 480)
        self.assertEqual(result["schedule"][-1]["Remaining Balance"], 0)


if __name__ == "__main__":
    unittest.main()
