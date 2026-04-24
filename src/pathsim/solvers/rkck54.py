########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                (solvers/rkck54.py)
##
##                                 Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import ExplicitRungeKutta


# SOLVERS ==============================================================================

class RKCK54(ExplicitRungeKutta):
    """Cash-Karp 5(4) pair. Six stages, 5th order with embedded 4th order
    error estimate.

    Designed to improve on the stability properties of the Fehlberg pair
    (``RKF45``) while keeping the same stage count.

    Characteristics
    ---------------
    * Order: 5 (propagating) / 4 (embedded)
    * Stages: 6
    * Explicit, adaptive timestep

    Note
    ----
    Comparable to ``RKDP54`` in cost and accuracy for most non-stiff block
    diagrams. Can exhibit slightly better stability on problems with
    eigenvalues near the imaginary axis. Both pairs are solid 5th order
    choices; ``RKDP54`` is the more commonly used default.

    References
    ----------
    .. [1] Cash, J. R., & Karp, A. H. (1990). "A variable order Runge-Kutta
           method for initial value problems with rapidly varying right-hand
           sides". ACM Transactions on Mathematical Software, 16(3), 201-222.
           :doi:`10.1145/79505.79507`
    .. [2] Hairer, E., Nørsett, S. P., & Wanner, G. (1993). "Solving
           Ordinary Differential Equations I: Nonstiff Problems". Springer
           Series in Computational Mathematics, Vol. 8.
           :doi:`10.1007/978-3-540-78862-1`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
