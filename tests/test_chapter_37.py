"""Tests for Chapter 37: Abstract Syntax Trees."""

import ast
import types


class TestASTBasics:
    """Test AST parsing and inspection."""

    def test_parse_expression(self) -> None:
        """ast.parse creates an AST from source code."""
        tree = ast.parse("x = 1 + 2")
        assert isinstance(tree, ast.Module)
        assert len(tree.body) == 1
        assert isinstance(tree.body[0], ast.Assign)

    def test_parse_function(self) -> None:
        """ast.parse handles function definitions."""
        tree = ast.parse("def greet(name): return f'Hello, {name}'")
        func = tree.body[0]
        assert isinstance(func, ast.FunctionDef)
        assert func.name == "greet"

    def test_ast_dump(self) -> None:
        """ast.dump shows AST structure as a string."""
        tree = ast.parse("42")
        dumped = ast.dump(tree)
        assert "Constant" in dumped
        assert "42" in dumped

    def test_literal_eval_safe(self) -> None:
        """ast.literal_eval safely evaluates literal expressions."""
        assert ast.literal_eval("42") == 42
        assert ast.literal_eval("[1, 2, 3]") == [1, 2, 3]
        assert ast.literal_eval("{'a': 1}") == {"a": 1}

    def test_literal_eval_rejects_code(self) -> None:
        """ast.literal_eval rejects non-literal expressions."""
        try:
            ast.literal_eval("__import__('os')")
            assert False, "Should have raised"
        except (ValueError, SyntaxError):
            pass

    def test_ast_node_fields(self) -> None:
        """AST nodes have typed fields."""
        tree = ast.parse("x + y")
        expr = tree.body[0]
        assert isinstance(expr, ast.Expr)
        binop = expr.value
        assert isinstance(binop, ast.BinOp)
        assert isinstance(binop.op, ast.Add)


class TestNodeVisitor:
    """Test AST node visiting and transformation."""

    def test_node_visitor(self) -> None:
        """NodeVisitor walks the AST tree."""

        class NameCollector(ast.NodeVisitor):
            def __init__(self) -> None:
                self.names: list[str] = []

            def visit_Name(self, node: ast.Name) -> None:
                self.names.append(node.id)
                self.generic_visit(node)

        tree = ast.parse("x = y + z")
        collector = NameCollector()
        collector.visit(tree)
        assert "y" in collector.names
        assert "z" in collector.names

    def test_function_counter(self) -> None:
        """NodeVisitor can count specific node types."""

        class FuncCounter(ast.NodeVisitor):
            def __init__(self) -> None:
                self.count = 0

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                self.count += 1
                self.generic_visit(node)

        source = """
def foo(): pass
def bar(): pass
def baz(): pass
"""
        tree = ast.parse(source)
        counter = FuncCounter()
        counter.visit(tree)
        assert counter.count == 3

    def test_node_transformer(self) -> None:
        """NodeTransformer modifies the AST."""

        class DoubleConstants(ast.NodeTransformer):
            def visit_Constant(self, node: ast.Constant) -> ast.Constant:
                if isinstance(node.value, int):
                    return ast.Constant(value=node.value * 2)
                return node

        tree = ast.parse("x = 5")
        new_tree = DoubleConstants().visit(tree)
        ast.fix_missing_locations(new_tree)
        code = compile(new_tree, "<test>", "exec")
        ns: dict = {}
        exec(code, ns)  # noqa: S102
        assert ns["x"] == 10

    def test_ast_walk(self) -> None:
        """ast.walk iterates all nodes without recursion control."""
        tree = ast.parse("a = b + c * d")
        node_types = {type(node).__name__ for node in ast.walk(tree)}
        assert "BinOp" in node_types
        assert "Name" in node_types
        assert "Add" in node_types


class TestCompileEvalExec:
    """Test compile, eval, and exec."""

    def test_eval_expression(self) -> None:
        """eval evaluates a single expression."""
        result = eval("2 + 3")  # noqa: S307
        assert result == 5

    def test_eval_with_namespace(self) -> None:
        """eval can use a custom namespace."""
        ns = {"x": 10, "y": 20}
        result = eval("x + y", ns)  # noqa: S307
        assert result == 30

    def test_exec_statements(self) -> None:
        """exec runs arbitrary statements."""
        ns: dict = {}
        exec("result = [i**2 for i in range(5)]", ns)  # noqa: S102
        assert ns["result"] == [0, 1, 4, 9, 16]

    def test_compile_to_code(self) -> None:
        """compile creates a code object from source."""
        code = compile("x = 42", "<test>", "exec")
        assert isinstance(code, types.CodeType)
        ns: dict = {}
        exec(code, ns)  # noqa: S102
        assert ns["x"] == 42

    def test_code_object_attributes(self) -> None:
        """Code objects have inspection attributes."""

        def example(a: int, b: int) -> int:
            return a + b

        code = example.__code__
        assert code.co_name == "example"
        assert code.co_argcount == 2
        assert "a" in code.co_varnames
        assert "b" in code.co_varnames
