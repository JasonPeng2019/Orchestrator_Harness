"""Direct-run designated task test for the routine above-high defect."""

import sys
import unittest


def _build_suite():
    from clamp import clamp

    class ClampAboveHighTests(unittest.TestCase):
        def test_above_high_returns_high(self):
            self.assertEqual(
                clamp(12, 5, 10),
                10,
                "GAP-ROUTINE-ABOVE-HIGH: above-high input must return the high bound",
            )

    return unittest.defaultTestLoader.loadTestsFromTestCase(ClampAboveHighTests)


def _run_suite() -> int:
    result = unittest.TextTestRunner(verbosity=2).run(_build_suite())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(_run_suite())
