"""Direct-run designated task test for the missing parse_and_clamp wiring."""

import sys
import unittest


def _build_suite():
    class ParseAndClampTaskTests(unittest.TestCase):
        def test_fixed_mixed_boundary_input(self):
            try:
                from clamp import parse_and_clamp
            except ImportError as error:
                self.fail(f"GAP-HEAVY-PARSE-AND-CLAMP: parse_and_clamp is not implemented: {error}")
            self.assertEqual(
                parse_and_clamp("-2, 0, 5, 9", 0, 5),
                [0, 0, 5, 5],
                "GAP-HEAVY-PARSE-AND-CLAMP: fixed mixed boundary input must clamp to [0, 0, 5, 5]",
            )

        def test_invalid_bounds_raise_value_error(self):
            try:
                from clamp import parse_and_clamp
            except ImportError as error:
                self.fail(f"GAP-HEAVY-PARSE-AND-CLAMP: parse_and_clamp is not implemented: {error}")
            with self.assertRaises(
                ValueError,
                msg="GAP-HEAVY-PARSE-AND-CLAMP: invalid bounds must raise ValueError",
            ):
                parse_and_clamp("1", 5, 0)

        def test_invalid_tokens_raise_value_error(self):
            try:
                from clamp import parse_and_clamp
            except ImportError as error:
                self.fail(f"GAP-HEAVY-PARSE-AND-CLAMP: parse_and_clamp is not implemented: {error}")
            with self.assertRaises(
                ValueError,
                msg="GAP-HEAVY-PARSE-AND-CLAMP: invalid tokens must raise ValueError",
            ):
                parse_and_clamp("1,x", 0, 5)

    return unittest.defaultTestLoader.loadTestsFromTestCase(ParseAndClampTaskTests)


def _run_suite() -> int:
    result = unittest.TextTestRunner(verbosity=2).run(_build_suite())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(_run_suite())
