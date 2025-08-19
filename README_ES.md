# 👽 g-calculator-cli 
[![Python Tests](https://github.com/maldos23/g-calculator-cli/actions/workflows/python-tests.yml/badge.svg)](https://github.com/maldos23/g-calculator-cli/actions/workflows/python-tests.yml)

Una calculadora de línea de comandos potente y flexible que soporta expresiones matemáticas, variables y funciones. Disponible en inglés y español.

## Características

- Operaciones aritméticas básicas (+, -, *, /, //, %, **)
- Funciones matemáticas (sin, cos, tan, sqrt, log, ln, exp, etc.)
- Constantes matemáticas (pi, e, tau)
- Asignación de variables
- Historial de comandos
- Interfaz bilingüe (Inglés/Español)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/maldos32/g-calculator-cli.git
cd g-calculator-cli 
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Modo Interactivo

Ejecuta la calculadora en modo interactivo:

```bash
# Interfaz en inglés (predeterminado)
python src/main.py

# Interfaz en español
python src/main.py --lang es
```

### Modo Línea de Comandos

Evalúa expresiones directamente desde la línea de comandos:

```bash
# Inglés
python src/main.py "2 + 2 * 3"
python src/main.py "sin(pi/2)"

# Español
python src/main.py --lang es "2 + 2 * 3"
```

### Comandos Disponibles

En modo interactivo:

- Inglés:
  - `help` o `?` - Mostrar ayuda
  - `hist` - Mostrar historial
  - `exit` o `quit` - Salir del programa

- Español:
  - `ayuda` o `?` - Mostrar ayuda
  - `hist` - Mostrar historial
  - `salir` - Salir del programa

### Ejemplos

```python
# Aritmética básica
2 + 2 * 3         # = 8
(5 - 2)**3 / 7    # ≈ 1.857

# Funciones
sqrt(16) + sin(pi/2)  # = 5
log(100, 10)          # = 2
ln(e)                 # = 1
fact(5)               # = 120

# Variables
x = 2.5
y = x**2 + 3         # = 9.25
```

## Funciones Soportadas

- Trigonométricas: `sin`, `cos`, `tan`
- Logarítmicas: `log` (base 10), `ln` (natural)
- Otras: `sqrt`, `exp`, `abs`, `round`, `floor`, `ceil`, `fact`/`factorial`
- Conversión de ángulos: `deg`, `rad`

## Constantes Matemáticas

- `pi` (π) = 3.141592...
- `e` = 2.718281...
- `tau` (τ) = 6.283185...

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
