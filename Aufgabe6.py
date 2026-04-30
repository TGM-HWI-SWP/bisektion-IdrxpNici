def solver2():

    """
    aufgabe6.py
    ===========

    Aufgabe 6: Alternative Loesungsmoeglichkeit - Newton-Raphson-Verfahren.

    Es wird derselbe Funktionstyp wie in Aufgabe 5 getestet:
            f(x)  = x**2 - n
            f'(x) = 2*x

    Newton-Iterationsformel:
            x_{n+1} = x_n - f(x_n) / f'(x_n)

    Getestet mit n = 25, 81, 144 sowie ergaenzend mit dem Beispiel aus
    Aufgabe 2 (sqrt-Funktion mit beliebiger Katalognummer).

    Aufruf:
        python aufgabe6.py
    """

    from __future__ import annotations

    import math

    from solver import NewtonRaphsonSolver


    def test_sqrt_with_newton(n: float, x0: float,
                            epsilon: float = 1e-10) -> None:
        """Loest sqrt(n) = x mit Newton-Raphson und vergleicht mit math.sqrt(n)."""
        # Funktion und analytische Ableitung
        def f(x: float) -> float:
            return x ** 2 - n

        def df(x: float) -> float:
            return 2.0 * x

        solver = NewtonRaphsonSolver(func=f, dfunc=df, epsilon=epsilon)

        try:
            root, iters = solver.solve(x0)
        except (ValueError, ZeroDivisionError, RuntimeError) as exc:
            print(f"  FEHLER fuer n={n}: {exc}")
            return

        analytical = math.sqrt(n)
        error = abs(root - analytical)
        print(f"  n = {n:>4}  |  Startwert x0 = {x0}  |  Iterationen: {iters:>3}")
        print(f"            numerisch  : {root:.12f}")
        print(f"            analytisch : {analytical:.12f}")
        print(f"            |Fehler|   : {error:.2e}")
        print()


    def main() -> None:
        print("=" * 60)
        print("Aufgabe 6 - Newton-Raphson-Solver, Test mit sqrt(n)")
        print("=" * 60)

        # Selbe Testfaelle wie Aufgabe 5
        test_sqrt_with_newton(n=25,  x0=10)
        test_sqrt_with_newton(n=81,  x0=20)
        test_sqrt_with_newton(n=144, x0=20)

        # Hinweis: Newton-Raphson konvergiert bei f(x) = x**2 - n
        # quadratisch und benoetigt damit deutlich weniger Iterationen
        # als die Bisektion (lineare Konvergenz).


    if __name__ == "__main__":
        main()
if __name__ == "__main__":
    solver2()