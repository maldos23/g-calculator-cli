# 👽 g-calculator-cli 

A powerful and flexible command-line calculator that supports mathematical expressions, variables, and functions. Available in English and Spanish.

## Features

- Basic arithmetic operations (+, -, *, /, //, %, **)
- Mathematical functions (sin, cos, tan, sqrt, log, ln, exp, etc.)
- Mathematical constants (pi, e, tau)
- Variable assignments
- Command history
- Bilingual interface (English/Spanish)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/maldos23/g-calculator-cli.git
cd terminal-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the calculator in interactive mode:

```bash
# English interface (default)
python src/main.py

# Spanish interface
python src/main.py --lang es
```

### Command Line Mode

Evaluate expressions directly from the command line:

```bash
# English
python src/main.py "2 + 2 * 3"
python src/main.py "sin(pi/2)"

# Spanish
python src/main.py --lang es "2 + 2 * 3"
```

### Available Commands

In interactive mode:

- English:
  - `help` or `?` - Show help
  - `hist` - Show command history
  - `exit` or `quit` - Exit the program

- Spanish:
  - `ayuda` or `?` - Mostrar ayuda
  - `hist` - Mostrar historial
  - `salir` - Salir del programa

### Examples

```python
# Basic arithmetic
2 + 2 * 3         # = 8
(5 - 2)**3 / 7    # ≈ 1.857

# Functions
sqrt(16) + sin(pi/2)  # = 5
log(100, 10)          # = 2
ln(e)                 # = 1
fact(5)               # = 120

# Variables
x = 2.5
y = x**2 + 3         # = 9.25
```

## Supported Functions

- Trigonometric: `sin`, `cos`, `tan`
- Logarithmic: `log` (base 10), `ln` (natural)
- Other: `sqrt`, `exp`, `abs`, `round`, `floor`, `ceil`, `fact`/`factorial`
- Angle conversion: `deg`, `rad`

## Mathematical Constants

- `pi` (π) = 3.141592...
- `e` = 2.718281...
- `tau` (τ) = 6.283185...

## License

This project is licensed under the MIT License - see the LICENSE file for details.
