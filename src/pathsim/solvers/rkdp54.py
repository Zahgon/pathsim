########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                (solvers/rkdp54.py)
##
##                                 Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import ExplicitRungeKutta


# SOLVERS ==============================================================================

class RKDP54(ExplicitRungeKutta):
    """Dormand-Prince 5(4) pair (DOPRI5). Seven stages, 5th order with
    embedded 4th order error estimate.

    The industry-standard adaptive explicit solver and the basis of MATLAB's
    ``ode45``. Has the FSAL property (not exploited in this implementation,
    so all seven stages are evaluated each step).

    Characteristics
    ---------------
    * Order: 5 (propagating) / 4 (embedded)
    * Stages: 7
    * Explicit, adaptive timestep

    Note
    ----
    Recommended default for non-stiff block diagrams. Handles smooth
    nonlinear dynamics, coupled oscillators, and signal-processing chains
    efficiently. If the simulation warns about excessive step rejections or
    very small timesteps, the system is likely stiff and an implicit solver
    (``ESDIRK43``, ``GEAR52A``) should be used instead. For very tight
    tolerances on smooth problems, ``RKV65`` or ``RKDP87`` can be more
    efficient per unit accuracy.

    References
    ----------
    .. [1] Dormand, J. R., & Prince, P. J. (1980). "A family of embedded
           Runge-Kutta formulae". Journal of Computational and Applied
           Mathematics, 6(1), 19-26.
           :doi:`10.1016/0771-050X(80)90013-3`
    .. [2] Shampine, L. F., & Reichelt, M. W. (1997). "The MATLAB ODE
           Suite". SIAM Journal on Scientific Computing, 18(1), 1-22.
           :doi:`10.1137/S1064827594276424`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
