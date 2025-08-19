#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.main import Evaluator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.eval_en = Evaluator(lang='en')
        self.eval_es = Evaluator(lang='es')

    def test_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        test_cases = [
            ("2 + 2", 4),
            ("3 - 1", 2),
            ("2 * 3", 6),
            ("8 / 4", 2),
            ("7 // 2", 3),
            ("7 % 3", 1),
            ("2 ** 3", 8),
            ("-5", -5),
            ("+5", 5),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result, _ = self.eval_en.eval_line(expr)
                self.assertEqual(result, expected)

    def test_complex_expressions(self):
        """Test more complex mathematical expressions."""
        test_cases = [
            ("2 + 3 * 4", 14),
            ("(2 + 3) * 4", 20),
            ("2 ** 3 + 1", 9),
            ("8 / (2 * 2)", 2),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result, _ = self.eval_en.eval_line(expr)
                self.assertEqual(result, expected)

    def test_mathematical_functions(self):
        """Test mathematical functions."""
        import math
        
        test_cases = [
            ("abs(-5)", 5),
            ("round(3.7)", 4),
            ("floor(3.7)", 3),
            ("ceil(3.2)", 4),
            ("fact(5)", 120),
            ("sqrt(16)", 4),
            ("sin(0)", 0),
            ("cos(0)", 1),
            ("tan(0)", 0),
            ("log(100, 10)", 2),
            ("ln(1)", 0),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result, _ = self.eval_en.eval_line(expr)
                self.assertAlmostEqual(result, expected, places=10)

    def test_constants(self):
        """Test mathematical constants."""
        import math
        
        test_cases = [
            ("pi", math.pi),
            ("e", math.e),
            ("tau", math.tau),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result, _ = self.eval_en.eval_line(expr)
                self.assertEqual(result, expected)

    def test_variables(self):
        """Test variable assignment and usage."""
        # Assign variable
        result, name = self.eval_en.eval_line("x = 5")
        self.assertEqual(result, 5)
        self.assertEqual(name, "x")
        
        # Use variable in expression
        result, _ = self.eval_en.eval_line("x * 2")
        self.assertEqual(result, 10)
        
        # Complex assignment
        result, name = self.eval_en.eval_line("y = x + 3")
        self.assertEqual(result, 8)
        self.assertEqual(name, "y")

    def test_error_handling(self):
        """Test error handling."""
        error_cases = [
            # División por cero
            ("1/0", ZeroDivisionError),
            # Variable indefinida
            ("z + 1", ValueError),
            # Sintaxis inválida
            ("2 +* 3", ValueError),
            # Función no permitida
            ("foo(2)", ValueError),
            # Asignación múltiple
            ("x, y = 1, 2", ValueError),
        ]
        
        for expr, error_type in error_cases:
            with self.subTest(expr=expr):
                with self.assertRaises(error_type):
                    self.eval_en.eval_line(expr)

    def test_language_errors(self):
        """Test error messages in different languages."""
        # Test division by zero in English
        with self.assertRaises(ZeroDivisionError) as cm_en:
            self.eval_en.eval_line("1/0")
        self.assertEqual(str(cm_en.exception), "Division by zero.")
        
        # Test division by zero in Spanish
        with self.assertRaises(ZeroDivisionError) as cm_es:
            self.eval_es.eval_line("1/0")
        self.assertEqual(str(cm_es.exception), "División entre cero.")

if __name__ == '__main__':
    unittest.main()
