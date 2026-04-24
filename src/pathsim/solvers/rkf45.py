########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                 (solvers/rkf45.py)
##
##                                 Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import ExplicitRungeKutta


# SOLVERS ==============================================================================

class RKF45(ExplicitRungeKutta):
    """Runge-Kutta-Fehlberg 4(5) pair. Six stages, 4th order propagation with
    5th order error estimate.

    The historically first widely-used embedded pair for automatic step-size
    control. The 4th order solution is propagated; the difference to the 5th
    order solution provides a local error estimate.

    Characteristics
    ---------------
    * Order: 4 (propagating) / 5 (error estimate)
    * Stages: 6
    * Explicit, adaptive timestep

    Note
    ----
    Largely superseded by the Dormand-Prince (``RKDP54``) and Cash-Karp
    (``RKCK54``) pairs, which achieve better accuracy per function evaluation
    on most problems. Still useful for reproducing legacy results or when
    comparing against published benchmarks that used RKF45.

    References
    ----------
    .. [1] Fehlberg, E. (1969). "Low-order classical Runge-Kutta formulas
           with stepsize control and their application to some heat transfer
           problems". NASA Technical Report TR R-315.
    .. [2] Fehlberg, E. (1970). "Klassische Runge-Kutta-Formeln vierter und
           niedrigerer Ordnung mit Schrittweiten-Kontrolle und ihre Anwendung
           auf Wärmeleitungsprobleme". Computing, 6(1-2), 61-71.
           :doi:`10.1007/BF02241732`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
