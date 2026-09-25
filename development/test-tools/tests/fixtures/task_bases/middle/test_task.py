"""Direct-run designated task test for the missing parse_numbers implementation."""

import sys
import unittest


def _build_suite():
    class ParseNumbersTaskTests(unittest.TestCase):
        def test_parse_numbers_accepts_signed_integers_with_whitespace(self):
            try:
                from clamp import parse_numbers
            except ImportError as error:
                self.fail(f"GAP-MIDDLE-PARSE-NUMBERS: parse_numbers is not implemented: {error}")
            self.assertEqual(
                parse_numbers(" 12 , -3 , 4 "),
                [12, -3, 4],
                "GAP-MIDDLE-PARSE-NUMBERS: signed integer tokens with whitespace must parse",
            )

        def test_parse_numbers_rejects_empty_input(self):
            try:
                from clamp import parse_numbers
            except ImportError as error:
                self.fail(f"GAP-MIDDLE-PARSE-NUMBERS: parse_numbers is not implemented: {error}")
            with self.assertRaises(
                ValueError,
                msg="GAP-MIDDLE-PARSE-NUMBERS: empty input must raise ValueError",
            ):
                parse_numbers("")

        def test_parse_numbers_rejects_noninteger_token(self):
            try:
                from clamp import parse_numbers
            except ImportError as error:
                self.fail(f"GAP-MIDDLE-PARSE-NUMBERS: parse_numbers is not implemented: {error}")
            with self.assertRaises(
                ValueError,
                msg="GAP-MIDDLE-PARSE-NUMBERS: noninteger token must raise ValueError",
            ):
                parse_numbers("12,x")

    return unittest.defaultTestLoader.loadTestsFromTestCase(ParseNumbersTaskTests)


def _run_suite() -> int:
    result = unittest.TextTestRunner(verbosity=2).run(_build_suite())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(_run_suite())
