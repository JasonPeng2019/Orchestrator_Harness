"""Direct-run prerequisites for the fully correct heavy clamp and parser."""

import sys
import unittest


def _build_suite():
    from clamp import clamp
    from parse_numbers import parse_numbers

    class ClampPrerequisiteTests(unittest.TestCase):
        def test_rejects_low_greater_than_high(self):
            with self.assertRaises(ValueError):
                clamp(10, 20, 10)

        def test_below_low_returns_low(self):
            self.assertEqual(clamp(1, 5, 10), 5)

        def test_interior_value_is_unchanged(self):
            self.assertEqual(clamp(7, 5, 10), 7)

        def test_low_endpoint_is_unchanged(self):
            self.assertEqual(clamp(5, 5, 10), 5)

        def test_high_endpoint_is_unchanged(self):
            self.assertEqual(clamp(10, 5, 10), 10)

        def test_above_high_returns_high(self):
            self.assertEqual(clamp(12, 5, 10), 10)

    class ParseNumbersPrerequisiteTests(unittest.TestCase):
        def test_accepts_signed_integers_with_whitespace(self):
            self.assertEqual(parse_numbers(" 12 , -3 , 4 "), [12, -3, 4])

        def test_rejects_empty_input(self):
            with self.assertRaises(ValueError):
                parse_numbers("")

        def test_rejects_noninteger_token(self):
            with self.assertRaises(ValueError):
                parse_numbers("12,x")

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        [
            loader.loadTestsFromTestCase(ClampPrerequisiteTests),
            loader.loadTestsFromTestCase(ParseNumbersPrerequisiteTests),
        ]
    )
    return suite


def _run_suite() -> int:
    result = unittest.TextTestRunner(verbosity=2).run(_build_suite())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(_run_suite())
