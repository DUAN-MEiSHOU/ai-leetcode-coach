import ast
import sys

from app.schemas.coach import PythonCodeContext, SourceLine


class PythonCodeAnalysisService:
    """Extracts Python structure with ast; it never executes submitted code."""

    def analyze(
        self,
        content: str,
        selected_line_number: int | None = None,
    ) -> PythonCodeContext:
        lines = content.splitlines()
        selected_line = self._selected_line(lines, selected_line_number)
        surrounding_lines = self._surrounding_lines(lines, selected_line_number)

        try:
            tree = ast.parse(content)
        except SyntaxError as error:
            return PythonCodeContext(
                syntax_valid=False,
                syntax_error=self._format_syntax_error(error),
                selected_line_number=selected_line_number,
                selected_line=selected_line,
                surrounding_lines=surrounding_lines,
            )

        aliases, imports = self._collect_imports(tree)
        calls = self._collect_calls(tree, aliases)
        standard_library_calls = [
            call for call in calls if self._is_standard_library_call(call, aliases)
        ]

        return PythonCodeContext(
            syntax_valid=True,
            imports=imports,
            function_calls=calls,
            standard_library_calls=standard_library_calls,
            selected_line_number=selected_line_number,
            selected_line=selected_line,
            surrounding_lines=surrounding_lines,
        )

    def _collect_imports(self, tree: ast.AST) -> tuple[dict[str, str], list[str]]:
        aliases: dict[str, str] = {}
        imports: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for imported in node.names:
                    module = imported.name
                    local_name = imported.asname or module.split(".")[0]
                    aliases[local_name] = module
                    imports.append(self._format_import(module, imported.asname))
            elif isinstance(node, ast.ImportFrom) and node.module:
                for imported in node.names:
                    resolved_name = f"{node.module}.{imported.name}"
                    local_name = imported.asname or imported.name
                    aliases[local_name] = resolved_name
                    imports.append(self._format_from_import(node.module, imported.name, imported.asname))

        return aliases, sorted(set(imports))

    def _collect_calls(self, tree: ast.AST, aliases: dict[str, str]) -> list[str]:
        calls = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = self._call_name(node.func)
            if name:
                calls.append(self._resolve_alias(name, aliases))

        return sorted(set(calls))

    def _call_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Call):
            return self._call_name(node.func)
        if isinstance(node, ast.Attribute):
            parent = self._call_name(node.value)
            return f"{parent}.{node.attr}" if parent else node.attr
        return None

    def _resolve_alias(self, call: str, aliases: dict[str, str]) -> str:
        root, separator, suffix = call.partition(".")
        resolved_root = aliases.get(root, root)
        return f"{resolved_root}{separator}{suffix}" if separator else resolved_root

    def _is_standard_library_call(self, call: str, aliases: dict[str, str]) -> bool:
        root = call.split(".")[0]
        imported_roots = {module.split(".")[0] for module in aliases.values()}
        return root in sys.stdlib_module_names or root in imported_roots & sys.stdlib_module_names

    def _selected_line(self, lines: list[str], line_number: int | None) -> str | None:
        if line_number is None or line_number > len(lines):
            return None
        return lines[line_number - 1]

    def _surrounding_lines(
        self,
        lines: list[str],
        line_number: int | None,
    ) -> list[SourceLine]:
        if line_number is None or line_number > len(lines):
            return []

        start = max(0, line_number - 3)
        end = min(len(lines), line_number + 2)
        return [
            SourceLine(number=index + 1, content=line)
            for index, line in enumerate(lines[start:end], start=start)
        ]

    def _format_import(self, module: str, alias: str | None) -> str:
        return f"{module} as {alias}" if alias else module

    def _format_from_import(self, module: str, name: str, alias: str | None) -> str:
        target = f"{module}.{name}"
        return f"{target} as {alias}" if alias else target

    def _format_syntax_error(self, error: SyntaxError) -> str:
        location = f"line {error.lineno}" if error.lineno else "unknown line"
        return f"{error.msg} ({location})"
