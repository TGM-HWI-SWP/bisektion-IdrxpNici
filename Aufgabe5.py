def solver():

    """
    aufgabe5.py
    ===========
    
    Aufgabe 5: SOLVER mit Methode der Intervallhalbierung (Bisektion).
    
    Die Wurzelfunktion sqrt(n) = x wird umgeformt zu:
            f(x) = x**2 - n  =  0
    Die Nullstelle dieser Funktion ist sqrt(n).
    
    Es wird fuer n = 25, 81, 144 getestet und mit der analytischen Loesung
    math.sqrt(n) verglichen.
    
    Aufruf:
        python aufgabe5.py
    """
    
    from __future__ import annotations
    
    import math
    
    from solver import BisectionSolver, make_function_from_string
    
    
    def test_sqrt_with_bisection(n: float, a: float, b: float,
                                epsilon: float = 1e-10) -> None:
        """Loest sqrt(n) = x mit Bisektion und vergleicht mit math.sqrt(n)."""
        # Funktion dynamisch ueber String + eval erzeugen
        f = make_function_from_string(f"x**2 - {n}")
        solver = BisectionSolver(func=f, epsilon=epsilon)
    
        try:
            root, iters = solver.solve(a, b)
        except (ValueError, RuntimeError) as exc:
            print(f"  FEHLER fuer n={n}: {exc}")
            return
    
        analytical = math.sqrt(n)
        error = abs(root - analytical)
        print(f"  n = {n:>4}  |  Intervall [{a},{b}]  |  Iterationen: {iters:>3}")
        print(f"            numerisch  : {root:.12f}")
        print(f"            analytisch : {analytical:.12f}")
        print(f"            |Fehler|   : {error:.2e}")
        print()
    
    
    def main() -> None:
        print("=" * 60)
        print("Aufgabe 5 - Bisektions-Solver, Test mit sqrt(n)")
        print("=" * 60)
    
        # Drei vorgegebene Testfaelle
        test_sqrt_with_bisection(n=25,  a=0, b=10)
        test_sqrt_with_bisection(n=81,  a=0, b=20)
        test_sqrt_with_bisection(n=144, a=0, b=20)
 
 
    if __name__ == "__main__":
     main()

if __name__ == "__main__":
    solver()

