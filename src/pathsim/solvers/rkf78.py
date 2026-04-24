########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                 (solvers/rkf78.py)
##
##                                 Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import ExplicitRungeKutta


# SOLVERS ==============================================================================

class RKF78(ExplicitRungeKutta):
    """Runge-Kutta-Fehlberg 7(8) pair. Thirteen stages, 7th order propagation
    with 8th order error estimate.

    Characteristics
    ---------------
    * Order: 7 (propagating) / 8 (error estimate)
    * Stages: 13
    * Explicit, adaptive timestep

    Note
    ----
    One of the earliest very-high-order embedded pairs. At the same stage
    count, the Dormand-Prince pair (``RKDP87``) generally provides better
    error constants. Consider ``RKDP87`` for new work unless Fehlberg-pair
    compatibility is required.

    References
    ----------
    .. [1] Fehlberg, E. (1968). "Classical fifth-, sixth-, seventh-, and
           eighth-order Runge-Kutta formulas with stepsize control". NASA
           Technical Report TR R-287.
    .. [2] Hairer, E., Nørsett, S. P., & Wanner, G. (1993). "Solving
           Ordinary Differential Equations I: Nonstiff Problems". Springer
           Series in Computational Mathematics, Vol. 8.
           :doi:`10.1007/978-3-540-78862-1`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
