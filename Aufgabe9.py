from Aufgabe5 import solver
from Aufgabe6 import solver2
from Aufgabe7 import plotter

"""
aufgabe9.py
===========

Aufgabe 9: Anwendung an realem Problem - Kettenlinie / Stromleitung.

Gegeben:
    * Abstand der Masten:  w = 100 m
    * Maximaler Durchhang in der Mitte: 10 m
    * Gleichung der Kettenlinie:  y(x) = a*cosh((x - x0)/a) - a + y0
      mit x0 = 0 (Scheitelpunkt liegt auf y-Achse)
    * Randbedingung:  y(50 m) = y0 + 10 m

Einsetzen ergibt:
    a*cosh(50/a) - a + y0 = y0 + 10
    a*(cosh(50/a) - 1) = 10
=>  f(a) = a*(cosh(50/a) - 1) - 10  =  0

Diese Gleichung kann nicht analytisch nach a aufgeloest werden, also
verwenden wir den SOLVER aus Aufgabe 5 / 6.

Anschliessend wird die Seillaenge berechnet:
    l = 2a * sinh(w/(2a))   =   2a * sinh(50/a)

Aufruf:
    python aufgabe9.py
"""

from __future__ import annotations

import math

from solver import BisectionSolver, NewtonRaphsonSolver


# Bekannte Groessen
W: float = 100.0           # Abstand zwischen den Masten in m
SAG: float = 10.0          # Durchhang in der Mitte in m
HALF_W: float = W / 2.0    # 50 m


def constraint(a: float) -> float:
    """
    Funktion deren Nullstelle den Kruemmungsradius a liefert:
        f(a) = a*(cosh(w/(2a)) - 1) - sag
    """
    if a == 0:
        raise ZeroDivisionError("a darf nicht 0 sein.")
    return a * (math.cosh(HALF_W / a) - 1.0) - SAG


def cable_length(a: float) -> float:
    """l = 2a * sinh(w/(2a))."""
    return 2.0 * a * math.sinh(HALF_W / a)


def main() -> None:
    print("=" * 60)
    print("Aufgabe 9 - Kettenlinie zwischen Strommasten")
    print("=" * 60)
    print(f"  Mastabstand    w   = {W} m")
    print(f"  Durchhang     sag  = {SAG} m\n")

    # Sinnvolles Intervall waehlen:
    # Fuer kleines a -> cosh(50/a) sehr gross -> f(a) >> 0
    # Fuer grosses a -> cosh(50/a) ~ 1 + (50/a)^2 / 2  ->  f(a) ~ 1250/a - 10
    #                                                         (negativ fuer a > 125)
    # Daher liegt a irgendwo zwischen ~50 und ~200.
    a_low, a_high = 50.0, 500.0
    print(f"  Intervall fuer a: [{a_low}, {a_high}]")
    print(f"    f({a_low})  = {constraint(a_low):>12.6f}")
    print(f"    f({a_high}) = {constraint(a_high):>12.6f}\n")

    # ---------- Loesung mit Bisektion ----------
    bs = BisectionSolver(func=constraint, epsilon=1e-10)
    a_bs, it_bs = bs.solve(a_low, a_high)
    l_bs = cable_length(a_bs)
    print("[Bisektion]")
    print(f"   Kruemmungsradius a = {a_bs:.10f} m   ({it_bs} Iterationen)")
    print(f"   Leitungslaenge   l = {l_bs:.6f} m\n")

    # ---------- Loesung mit Newton-Raphson ----------
    # Ableitung von f(a) = a*cosh(50/a) - a - 10:
    #   f'(a) = cosh(50/a) - (50/a)*sinh(50/a) - 1
    def dconstraint(a: float) -> float:
        return math.cosh(HALF_W / a) - (HALF_W / a) * math.sinh(HALF_W / a) - 1.0

    nr = NewtonRaphsonSolver(func=constraint, dfunc=dconstraint, epsilon=1e-10)
    a_nr, it_nr = nr.solve(125.0)  # gute Anfangsschaetzung aus Taylor-Reihe
    l_nr = cable_length(a_nr)
    print("[Newton-Raphson]")
    print(f"   Kruemmungsradius a = {a_nr:.10f} m   ({it_nr} Iterationen)")
    print(f"   Leitungslaenge   l = {l_nr:.6f} m\n")

    # Plausibilitaetscheck: bei a -> oo wuerde l -> 100 m gehen (gerade Linie).
    # Mit Durchhang von 10m muss l etwas groesser als 100m sein -> erwartet ~ 102.7 m.
    print("Ergebnis:")
    print(f"   Die elektrische Leitung hat eine Laenge von ca. {l_bs:.2f} m.")



if __name__ == "__main__":
    solver()
    solver2()
    plotter()
    main()