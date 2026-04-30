"""
aufgabe7.py
===========

Aufgabe 7: Grafische Aufbereitung der Nullstellenfindung mit matplotlib.

Es werden in einer Figure drei Subplots dargestellt, die nach jedem
Iterationsschritt aktualisiert werden (Animation):

    1) Funktionsgraph mit aktuellem Intervall [a, b] bzw. Naeherung x_n
    2) Aktuelle Genauigkeit |f(c)| pro Iteration (Konvergenz Richtung 0)
    3) Aktuelle Loesung x_n pro Iteration

Standardmaessig wird die Bisektion fuer f(x) = x**2 - 25 visualisiert.

Aufruf:
    python aufgabe7.py                   # Bisektion (Default)
    python aufgabe7.py newton            # Newton-Raphson
"""

from __future__ import annotations

import sys
from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from solver import BisectionSolver, NewtonRaphsonSolver


# ---------------------------------------------------------------------------
def animate_bisection(func: Callable[[float], float],
                      a: float, b: float,
                      epsilon: float = 1e-8,
                      pause: float = 0.4) -> None:
    """Visualisiert die Bisektion Schritt fuer Schritt."""
    solver = BisectionSolver(func=func, epsilon=epsilon)
    root, iters = solver.solve(a, b)
    history = solver.history

    # Werte fuer Plot vorbereiten
    accuracy = [abs(fc) for (_, _, _, fc) in history]
    solutions = [c for (_, _, c, _) in history]

    # Funktionsgraph
    x_plot = np.linspace(a, b, 500)
    y_plot = [func(xi) for xi in x_plot]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Aufgabe 7 - Animation der Bisektion", fontsize=14)

    ax_func, ax_acc, ax_sol = axes
    ax_func.set_title("Funktion mit Intervall [a, b]")
    ax_func.set_xlabel("x")
    ax_func.set_ylabel("f(x)")
    ax_acc.set_title("Genauigkeit |f(c)| je Iteration")
    ax_acc.set_xlabel("Iteration")
    ax_acc.set_ylabel("|f(c)|")
    ax_acc.set_yscale("log")
    ax_sol.set_title("Naeherung c je Iteration")
    ax_sol.set_xlabel("Iteration")
    ax_sol.set_ylabel("c")

    plt.ion()  # interaktiver Modus
    for i, (ai, bi, ci, fci) in enumerate(history, start=1):
        # Subplot 1: Funktion und Intervall
        ax_func.cla()
        ax_func.set_title(f"Iteration {i}/{iters}: c = {ci:.6f}")
        ax_func.set_xlabel("x")
        ax_func.set_ylabel("f(x)")
        ax_func.plot(x_plot, y_plot, "b-", label="f(x)")
        ax_func.axhline(0, color="k", linewidth=0.5)
        ax_func.axvline(ai, color="green", linestyle="--", label=f"a = {ai:.4f}")
        ax_func.axvline(bi, color="red", linestyle="--", label=f"b = {bi:.4f}")
        ax_func.plot(ci, fci, "ro", markersize=8, label=f"c = {ci:.4f}")
        ax_func.legend(loc="best", fontsize=8)
        ax_func.grid(True, alpha=0.3)

        # Subplot 2: Genauigkeit (log-Skala)
        ax_acc.cla()
        ax_acc.set_title("Genauigkeit |f(c)|")
        ax_acc.set_xlabel("Iteration")
        ax_acc.set_ylabel("|f(c)|")
        ax_acc.set_yscale("log")
        # +1e-300 verhindert log(0)
        ax_acc.plot(range(1, i + 1), [v + 1e-300 for v in accuracy[:i]],
                    "o-", color="darkorange")
        ax_acc.grid(True, which="both", alpha=0.3)

        # Subplot 3: Naeherung c
        ax_sol.cla()
        ax_sol.set_title("Naeherung c")
        ax_sol.set_xlabel("Iteration")
        ax_sol.set_ylabel("c")
        ax_sol.plot(range(1, i + 1), solutions[:i], "s-", color="purple")
        ax_sol.axhline(root, color="gray", linestyle=":",
                       label=f"Loesung ~ {root:.6f}")
        ax_sol.legend(loc="best", fontsize=8)
        ax_sol.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.pause(pause)

    plt.ioff()
    print(f"\nBisektion: Loesung ~ {root:.10f} nach {iters} Iterationen.")
    plt.show()


# ---------------------------------------------------------------------------
def animate_newton(func: Callable[[float], float],
                   dfunc: Callable[[float], float],
                   x0: float,
                   plot_range: Tuple[float, float],
                   epsilon: float = 1e-8,
                   pause: float = 0.5) -> None:
    """Visualisiert das Newton-Raphson-Verfahren Schritt fuer Schritt."""
    solver = NewtonRaphsonSolver(func=func, dfunc=dfunc, epsilon=epsilon)
    root, iters = solver.solve(x0)
    history = solver.history

    accuracy = [abs(fx) for (_, fx) in history]
    solutions = [x for (x, _) in history]

    a, b = plot_range
    x_plot = np.linspace(a, b, 500)
    y_plot = [func(xi) for xi in x_plot]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Aufgabe 7 - Animation Newton-Raphson", fontsize=14)
    ax_func, ax_acc, ax_sol = axes

    plt.ion()
    for i, (xi, fxi) in enumerate(history, start=1):
        ax_func.cla()
        ax_func.set_title(f"Iteration {i}/{iters}: x = {xi:.6f}")
        ax_func.set_xlabel("x"); ax_func.set_ylabel("f(x)")
        ax_func.plot(x_plot, y_plot, "b-", label="f(x)")
        ax_func.axhline(0, color="k", linewidth=0.5)
        ax_func.plot(xi, fxi, "ro", markersize=8, label=f"x = {xi:.4f}")
        ax_func.legend(loc="best", fontsize=8); ax_func.grid(True, alpha=0.3)

        ax_acc.cla()
        ax_acc.set_title("Genauigkeit |f(x)|")
        ax_acc.set_xlabel("Iteration"); ax_acc.set_ylabel("|f(x)|")
        ax_acc.set_yscale("log")
        ax_acc.plot(range(1, i + 1), [v + 1e-300 for v in accuracy[:i]],
                    "o-", color="darkorange")
        ax_acc.grid(True, which="both", alpha=0.3)

        ax_sol.cla()
        ax_sol.set_title("Naeherung x")
        ax_sol.set_xlabel("Iteration"); ax_sol.set_ylabel("x")
        ax_sol.plot(range(1, i + 1), solutions[:i], "s-", color="purple")
        ax_sol.axhline(root, color="gray", linestyle=":",
                       label=f"Loesung ~ {root:.6f}")
        ax_sol.legend(loc="best", fontsize=8); ax_sol.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.pause(pause)

    plt.ioff()
    print(f"\nNewton-Raphson: Loesung ~ {root:.10f} nach {iters} Iterationen.")
    plt.show()


# ---------------------------------------------------------------------------
def main() -> None:
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "bisection"

    # Beispiel f(x) = x**2 - 25 -> Nullstelle bei x = 5
    def f(x: float) -> float:
        return x ** 2 - 25

    def df(x: float) -> float:
        return 2.0 * x

    if mode == "newton":
        animate_newton(f, df, x0=10, plot_range=(0, 10))
    else:
        animate_bisection(f, a=0, b=10)


if __name__ == "__main__":
    main()
