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

class RKDP87(ExplicitRungeKutta):
    """Dormand-Prince 8(7) pair (DOP853). Thirteen stages, 8th order with
    embedded 7th order error estimate.

    The highest-order general-purpose explicit pair in this library. Has the
    FSAL property (not exploited in this implementation).

    Characteristics
    ---------------
    * Order: 8 (propagating) / 7 (embedded)
    * Stages: 13
    * Explicit, adaptive timestep

    Note
    ----
    Only worthwhile when the dynamics are very smooth and tolerances are
    extremely tight (roughly :math:`10^{-10}` or below). The 13 function
    evaluations per step are expensive, but the 8th order convergence means
    the step size can be much larger than with lower-order methods at the
    same error. Suitable for generating reference solutions to validate other
    solvers in a block diagram. For typical engineering tolerances
    (:math:`10^{-4}`--:math:`10^{-8}`), ``RKDP54`` or ``RKV65`` are more
    efficient.

    References
    ----------
    .. [1] Prince, P. J., & Dormand, J. R. (1981). "High order embedded
           Runge-Kutta formulae". Journal of Computational and Applied
           Mathematics, 7(1), 67-75.
           :doi:`10.1016/0771-050X(81)90010-3`
    .. [2] Hairer, E., Nørsett, S. P., & Wanner, G. (1993). "Solving
           Ordinary Differential Equations I: Nonstiff Problems". Springer
           Series in Computational Mathematics, Vol. 8.
           :doi:`10.1007/978-3-540-78862-1`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
