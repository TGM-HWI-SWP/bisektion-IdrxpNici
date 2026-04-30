"""
aufgabe8.py
===========

Aufgabe 8: Test des SOLVERS am Polynom

        P4(x) = 2x + x**2 + 3x**3 - x**4

Bekannte Nullstellen: x1 = 0   und   x2 ~ 3,4567.

Wir suchen die Nullstelle bei x ~ 3,4567 und untersuchen, wie viele
Iterationen die Bisektion fuer verschiedene Genauigkeiten benoetigt:
    * epsilon = 1e-2
    * epsilon = 1e-8

Aufruf:
    python aufgabe8.py
"""

from __future__ import annotations

import math

from solver import BisectionSolver


def polynom_p4(x: float) -> float:
    """P4(x) = 2x + x**2 + 3x**3 - x**4."""
    return 2 * x + x ** 2 + 3 * x ** 3 - x ** 4


def main() -> None:
    print("=" * 60)
    print("Aufgabe 8 - Genauigkeitsanalyse Polynom P4(x)")
    print("=" * 60)

    # Wahl des Intervalls:
    # Aus dem Graphen (s. PDF) erkennt man, dass P4 zwischen x = 1 und x = 4
    # die x-Achse zwischen positivem und negativem Bereich kreuzt.
    # P4(1) = 2 + 1 + 3 - 1 = 5     (positiv)
    # P4(4) = 8 + 16 + 192 - 256 = -40 (negativ)
    # Damit ist der Zwischenwertsatz erfuellt.
    a, b = 1.0, 4.0
    print(f"Intervall: [a, b] = [{a}, {b}]")
    print(f"  P4(a) = {polynom_p4(a):>12.6f}")
    print(f"  P4(b) = {polynom_p4(b):>12.6f}\n")

    # Test mit verschiedenen Genauigkeiten
    for eps in (1e-2, 1e-8):
        solver = BisectionSolver(func=polynom_p4, epsilon=eps, max_iter=10000)
        root, iters = solver.solve(a, b)
        print(f"  epsilon = {eps:.0e}")
        print(f"    Nullstelle ~ {root:.10f}")
        print(f"    Iterationen: {iters}")
        print(f"    P4(root)   = {polynom_p4(root):.2e}\n")

    # Theoretischer Vergleich: pro Iteration halbiert sich das Intervall.
    # Anfangsweite = b - a = 3. Nach n Iterationen ist die Weite 3/2^n.
    # Bedingung: 3/2^n < eps  =>  n > log2(3/eps)
    print("Theoretische untere Schranke (Intervallhalbierung):")
    for eps in (1e-2, 1e-8):
        n_min = math.ceil(math.log2((b - a) / eps))
        print(f"    epsilon = {eps:.0e}  ->  n_min = {n_min}")

    print("\nInterpretation:")
    print("  Die Bisektion konvergiert linear: pro Iteration halbiert sich")
    print("  die Intervalllaenge. Fuer epsilon = 1e-8 werden ~6x so viele")
    print("  Iterationen benoetigt wie fuer epsilon = 1e-2.")


if __name__ == "__main__":
    main()
