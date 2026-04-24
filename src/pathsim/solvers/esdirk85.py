########################################################################################
##
##                   EMBEDDED DIAGONALLY IMPLICIT RUNGE KUTTA METHOD
##                                (solvers/esdirk85.py)
##
##                                  Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import DiagonallyImplicitRungeKutta


# SOLVERS ==============================================================================

class ESDIRK85(DiagonallyImplicitRungeKutta):
    """Sixteen-stage, 8th order ESDIRK method with embedded 5th order error
    estimate. L-stable and stiffly accurate (ESDIRK(16,8)[2]SAL-[(16,5)]).

    Characteristics
    ---------------
    * Order: 8 (propagating) / 5 (embedded)
    * Stages: 16 (1 explicit, 15 implicit)
    * Adaptive timestep
    * L-stable, stiffly accurate
    * Stage order 2

    Note
    ----
    Fifteen implicit solves per step make this very expensive. It is only
    justified when the right-hand side evaluation is itself costly (large
    state dimension, expensive ``ODE`` blocks) and very tight tolerances are
    required so that the 8th order convergence compensates through much
    larger steps. For generating stiff reference solutions to validate other
    solvers. In almost all practical block-diagram simulations, ``ESDIRK54``
    is the better choice.

    References
    ----------
    .. [1] Alamri, Y., & Ketcheson, D. I. (2024). "Very high-order A-stable
           stiffly accurate diagonally implicit Runge-Kutta methods with
           error estimators". Journal of Scientific Computing, 100,
           Article 84. :doi:`10.1007/s10915-024-02627-w`
    .. [2] Kennedy, C. A., & Carpenter, M. H. (2019). "Diagonally implicit
           Runge-Kutta methods for stiff ODEs". Applied Numerical
           Mathematics, 146, 221-244.
           :doi:`10.1016/j.apnum.2019.07.008`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
