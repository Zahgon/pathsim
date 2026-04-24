########################################################################################
##
##                   EMBEDDED DIAGONALLY IMPLICIT RUNGE KUTTA METHOD
##                                (solvers/esdirk32.py)
##
##                                  Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from ._rungekutta import DiagonallyImplicitRungeKutta


# SOLVERS ==============================================================================

class ESDIRK43(DiagonallyImplicitRungeKutta):
    """Six-stage, 4th order ESDIRK method with embedded 3rd order error
    estimate. L-stable and stiffly accurate.

    Characteristics
    ---------------
    * Order: 4 (propagating) / 3 (embedded)
    * Stages: 6 (1 explicit, 5 implicit)
    * Adaptive timestep
    * L-stable, stiffly accurate
    * Stage order 2

    Note
    ----
    Recommended default for stiff block diagrams. L-stability damps
    high-frequency parasitic modes that arise from stiff subsystems (e.g.
    PID controllers with large derivative gain, fast electrical or chemical
    dynamics). The adaptive step-size control concentrates computational
    effort where the solution changes rapidly. For non-stiff systems,
    ``RKDP54`` avoids the implicit solve cost and is more efficient. For
    tighter tolerances on stiff problems, ``ESDIRK54`` provides 5th order
    accuracy.

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
