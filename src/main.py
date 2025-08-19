#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import math
import operator as op
import sys
import argparse
from collections import deque
from src.translations import TRANSLATIONS

# Allowed operators
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

UNARY = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed mathematical functions
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

class Evaluator(ast.NodeVisitor):
    def __init__(self, variables=None, lang='en'):
        self.vars = dict(CONSTANTS)
        self.lang = lang
        self.msgs = TRANSLATIONS[lang]
        if variables:
            self.vars.update(variables)

    def eval_expr(self, expr: str):
        """Evaluates an expression (eval mode)."""
        try:
            node = ast.parse(expr, mode='eval')
        except SyntaxError as e:
            raise ValueError(self.msgs['syntax_error'].format(e.msg))
        return self.visit(node.body)

    def eval_line(self, line: str):
        """Evaluates a line that can be an assignment or expression."""
        if '=' in line:
            try:
                module = ast.parse(line, mode='exec')
            except SyntaxError as e:
                raise ValueError(self.msgs['syntax_error'].format(e.msg))
            if (len(module.body) == 1 and isinstance(module.body[0], ast.Assign)
                and len(module.body[0].targets) == 1 and isinstance(module.body[0].targets[0], ast.Name)):
                name = module.body[0].targets[0].id
                value = self.visit(module.body[0].value)
                self.vars[name] = value
                return value, name
            else:
                raise ValueError(self.msgs['simple_assign_only'])
        else:
            value = self.eval_expr(line)
            return value, None

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            try:
                return OPERATORS[op_type](left, right)
            except ZeroDivisionError:
                raise ZeroDivisionError(self.msgs['zero_division'])
        raise ValueError(self.msgs['invalid_operator'].format(op_type.__name__))

    def visit_UnaryOp(self, node):
        value = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in UNARY:
            return UNARY[op_type](value)
        raise ValueError(self.msgs['invalid_unary'].format(op_type.__name__))

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError(self.msgs['function_only'])
        name = node.func.id
        if name not in FUNCTIONS:
            raise ValueError(self.msgs['invalid_function'].format(name))
        func = FUNCTIONS[name]
        args = [self.visit(arg) for arg in node.args]
        kwargs = {kw.arg: self.visit(kw.value) for kw in node.keywords}
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ValueError(self.msgs['function_error'].format(name, e))

    def visit_Name(self, node):
        if node.id in self.vars:
            return self.vars[node.id]
        raise ValueError(self.msgs['unknown_name'].format(node.id))

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(self.msgs['invalid_constant'].format(repr(node.value)))

    def visit_Num(self, node):  # pragma: no cover
        return node.n

    def generic_visit(self, node):
        raise ValueError(self.msgs['invalid_structure'].format(type(node).__name__))

def repl(lang='en'):
    msgs = TRANSLATIONS[lang]
    print(msgs['welcome'])
    ev = Evaluator(lang=lang)
    history = deque(maxlen=50)

    help_commands = {'help', '?'} if lang == 'en' else {'ayuda', '?'}
    exit_commands = {'exit', 'quit'} if lang == 'en' else {'salir', 'exit'}
    hist_commands = {'hist', 'history'} if lang == 'en' else {'hist'}

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{msgs['goodbye']}")
            break

        if not line:
            continue

        if line.lower() in exit_commands:
            print(msgs['goodbye'])
            break
        if line.lower() in help_commands:
            print(msgs['help'])
            continue
        if line.lower() in hist_commands:
            if not history:
                print(msgs['empty_history'])
            else:
                for i, item in enumerate(history, 1):
                    expr, res = item
                    print(f"{i:02d}. {expr} = {res}")
            continue

        try:
            result, name = ev.eval_line(line)
            history.append((line, result))
            if name is not None:
                print(f"{name} = {result}")
            else:
                print(result)
        except ZeroDivisionError as zde:
            print(f"Error: {str(zde)}")
        except ValueError as ve:
            print(f"Error: {str(ve)}")
        except Exception as e:
            print(f"{msgs['unexpected_error'].format(e)}")

def main():
    parser = argparse.ArgumentParser(description='Terminal Calculator')
    parser.add_argument('--lang', choices=['en', 'es'], default='en',
                       help='Language for the calculator (en/es)')
    parser.add_argument('expression', nargs='*', help='Expression to evaluate')
    
    args = parser.parse_args()
    
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
        repl(lang=args.lang)

if __name__ == "__main__":
    main()
