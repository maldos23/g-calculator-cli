#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import ast
import math
import operator as op
from src.main import Evaluator, repl

UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed math functions
FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': lambda x, base=10: math.log(x, base),
    'ln': math.log,
    'exp': math.exp,
    'abs': abs,
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
    'fact': math.factorial,
    'factorial': math.factorial,
    'deg': math.degrees,
    'rad': math.radians,
}

# Allowed constants
CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau,
}

HELP_TEXT = """\
Terminal Calculator
-------------------
Type mathematical expressions and press Enter.
Examples:
  2 + 2 * 3
  (5 - 2)**3 / 7
  sqrt(16) + sin(pi/2)
  log(100, 10)   # base 10 logarithm
  ln(e)          # natural logarithm
  fact(5)        # factorial
  x = 2.5
  y = x**2 + 3

Commands:
  help   -> show this help
  hist   -> show recent results
  exit   -> quit the program
"""

class Evaluator(ast.NodeVisitor):
    def __init__(self, variables=None):
        self.vars = dict(CONSTANTS)
        if variables:
            self.vars.update(variables)

    def eval_expr(self, expr: str):
        """Evaluate an expression (eval mode)."""
        try:
            node = ast.parse(expr, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"Syntax error: {e.msg}")
        return self.visit(node.body)

    def eval_line(self, line: str):
        """Evaluate a line that may be an assignment or expression."""
        if '=' in line:
            # 'exec' mode to allow simple assignments
            try:
                module = ast.parse(line, mode='exec')
            except SyntaxError as e:
                raise ValueError(f"Syntax error: {e.msg}")
            # Only allow simple assignments
            if (len(module.body) == 1 and isinstance(module.body[0], ast.Assign)
                and len(module.body[0].targets) == 1 and isinstance(module.body[0].targets[0], ast.Name)):
                name = module.body[0].targets[0].id
                value = self.visit(module.body[0].value)
                self.vars[name] = value
                return value, name
            else:
                raise ValueError("Only simple assignments are allowed (e.g. x = 2).")
        else:
            value = self.eval_expr(line)
            return value, None

    # AST Visitors
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            try:
                return OPERATORS[op_type](left, right)
            except ZeroDivisionError:
                raise ZeroDivisionError("Division by zero.")
        raise ValueError(f"Operator not allowed: {op_type.__name__}")

    def visit_UnaryOp(self, node):
        value = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](value)
        raise ValueError(f"Unary operator not allowed: {op_type.__name__}")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only function calls by name are allowed.")
        name = node.func.id
        if name not in FUNCTIONS:
            raise ValueError(f"Function not allowed: {name}")
        func = FUNCTIONS[name]
        args = [self.visit(arg) for arg in node.args]
        kwargs = {kw.arg: self.visit(kw.value) for kw in node.keywords}
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Error calling {name}: {e}")

    def visit_Name(self, node):
        if node.id in self.vars:
            return self.vars[node.id]
        raise ValueError(f"Unknown name: {node.id}")

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Constant not allowed: {node.value!r}")

    # Compatibility with Python <3.8 (Num, Str, etc.)
    def visit_Num(self, node):  # pragma: no cover
        return node.n

    def generic_visit(self, node):
        raise ValueError(f"Structure not allowed: {type(node).__name__}")


def main():
    """Main entry point for the calculator CLI."""
    parser = argparse.ArgumentParser(description='Terminal Calculator')
    parser.add_argument('--lang', 
                       choices=['en', 'es'], 
                       default='en',
                       help='Language for the calculator (en/es)')
    parser.add_argument('expression', 
                       nargs='*', 
                       help='Expression to evaluate')
    
    args = parser.parse_args()
    
    # If expression is provided, evaluate it directly
    if args.expression:
        expr = ' '.join(args.expression)
        try:
            ev = Evaluator(lang=args.lang)
            res, _ = ev.eval_line(expr)
            print(res)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Otherwise, start interactive mode
        repl(lang=args.lang)

if __name__ == "__main__":
    main()
