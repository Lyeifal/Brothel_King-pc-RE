#### Test Runner — Lightweight test framework for Brothel King ####
# Phase 6.4: In-game test harness for component-level testing.
#
# Usage in a test file:
#   label test_girl_stats:
#       $ runner = TestRunner.instance()
#       $ runner.assert_eq(girl.get_stat("charm"), 50, "Initial charm")
#       $ runner.report()
#
# Run from dev console: test.run("test_girl_stats")

init -1 python:

    class TestRunner(object):
        """Lightweight test framework for game components."""

        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(TestRunner, cls).__new__(cls)
            return cls._instance

        @classmethod
        def instance(cls):
            return cls.__new__(cls)

        def __init__(self):
            if hasattr(self, '_initialized'):
                return
            self._initialized = True
            self.reset()

        def reset(self):
            self.passed = 0
            self.failed = 0
            self.skipped = 0
            self.results = []

        # ── Assertions ──

        def assert_eq(self, actual, expected, label=""):
            if actual == expected:
                self.passed += 1
                self.results.append(("PASS", label, "%s == %s" % (repr(actual), repr(expected))))
            else:
                self.failed += 1
                self.results.append(("FAIL", label, "Expected %s, got %s" % (repr(expected), repr(actual))))

        def assert_true(self, condition, label=""):
            self.assert_eq(bool(condition), True, label)

        def assert_contains(self, container, item, label=""):
            self.assert_eq(item in container, True, label or "%s in container" % repr(item))

        def assert_not_none(self, value, label=""):
            self.assert_eq(value is not None, True, label or "value is not None")

        # ── Reporting ──

        def report(self):
            lines = [
                "{b}Test Results:{/b}",
                "  {color=[c_emerald]}Passed: %s{/color}" % self.passed,
                "  {color=[c_red]}Failed: %s{/color}" % self.failed,
            ]
            for status, label, detail in self.results:
                color = c_emerald if status == "PASS" else c_red
                lines.append("  {color=[%s]}[%s]{/color} %s: %s" % (color, status, label, detail))
            return "\n".join(lines)

        def summary(self):
            return "%s passed, %s failed" % (self.passed, self.failed)

    test_runner = TestRunner()
