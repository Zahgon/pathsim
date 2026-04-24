########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                 (solvers/rkf21.py)
##
##                                 Milan Rother 2025
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import ExplicitRungeKutta


# SOLVERS ==============================================================================

class RKF21(ExplicitRungeKutta):
    """Three-stage, 2nd order Runge-Kutta-Fehlberg method with embedded 1st order error estimate.

    Characteristics
    ---------------
    * Order: 2 (propagating) / 1 (embedded)
    * Stages: 3
    * Explicit, adaptive timestep

    Note
    ----
    The cheapest adaptive explicit method available. The low order means the
    error estimate itself is coarse, so step-size control is less reliable
    than with higher-order pairs. Useful for rough exploratory runs of a new
    block diagram or when step size is dominated by discrete events (zero
    crossings, scheduled triggers) rather than truncation error. For
    production simulations, ``RKBS32`` or ``RKDP54`` are almost always
    preferable.

    References
    ----------
    .. [1] Fehlberg, E. (1969). "Low-order classical Runge-Kutta formulas
           with stepsize control and their application to some heat transfer
           problems". NASA Technical Report TR R-315.
    .. [2] Hairer, E., Nørsett, S. P., & Wanner, G. (1993). "Solving
           Ordinary Differential Equations I: Nonstiff Problems". Springer
           Series in Computational Mathematics, Vol. 8.
           :doi:`10.1007/978-3-540-78862-1`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
