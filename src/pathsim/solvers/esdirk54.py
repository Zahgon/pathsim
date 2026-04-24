########################################################################################
##
##                   EMBEDDED DIAGONALLY IMPLICIT RUNGE KUTTA METHOD
##                                (solvers/esdirk54.py)
##
##                                  Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import DiagonallyImplicitRungeKutta


# SOLVERS ==============================================================================

class ESDIRK54(DiagonallyImplicitRungeKutta):
    """Seven-stage, 5th order ESDIRK method with embedded 4th order error
    estimate. L-stable and stiffly accurate (ESDIRK5(4)7L[2]SA2).

    Characteristics
    ---------------
    * Order: 5 (propagating) / 4 (embedded)
    * Stages: 7 (1 explicit, 6 implicit)
    * Adaptive timestep
    * L-stable, stiffly accurate
    * Stage order 2

    Note
    ----
    The highest-accuracy L-stable single-step solver in this library before
    the much more expensive ``ESDIRK85``. Use when tight tolerances are
    needed on a stiff block diagram (e.g. multi-rate systems combining fast
    electrical and slow thermal dynamics). At moderate tolerances,
    ``ESDIRK43`` achieves similar results with fewer implicit solves per
    step.

    References
    ----------
    .. [1] Kennedy, C. A., & Carpenter, M. H. (2019). "Diagonally implicit
           Runge-Kutta methods for stiff ODEs". Applied Numerical
           Mathematics, 146, 221-244.
           :doi:`10.1016/j.apnum.2019.07.008`
    .. [2] Hairer, E., & Wanner, G. (1996). "Solving Ordinary Differential
           Equations II: Stiff and Differential-Algebraic Problems". Springer
           Series in Computational Mathematics, Vol. 14.
           :doi:`10.1007/978-3-642-05221-7`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
