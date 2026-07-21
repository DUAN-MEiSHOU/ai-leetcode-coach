import unittest

from app.services.python_code_analysis_service import PythonCodeAnalysisService


class PythonCodeAnalysisServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = PythonCodeAnalysisService()

    def test_extracts_imports_calls_and_surrounding_lines(self) -> None:
        context = self.service.analyze(
            "from collections import Counter\n"
            "\n"
            "def count_items(items):\n"
            "    return Counter(items).most_common(1)\n",
            selected_line_number=4,
        )

        self.assertTrue(context.syntax_valid)
        self.assertEqual(context.imports, ["collections.Counter"])
        self.assertEqual(
            context.function_calls,
            ["collections.Counter", "collections.Counter.most_common"],
        )
        self.assertEqual(context.standard_library_calls, context.function_calls)
        self.assertEqual(context.selected_line, "    return Counter(items).most_common(1)")
        self.assertEqual([line.number for line in context.surrounding_lines], [2, 3, 4])

    def test_reports_syntax_errors_without_execution(self) -> None:
        context = self.service.analyze("def broken(:\n    pass\n")

        self.assertFalse(context.syntax_valid)
        self.assertIn("invalid syntax", context.syntax_error)
        self.assertEqual(context.function_calls, [])
