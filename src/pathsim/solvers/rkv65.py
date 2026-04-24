########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                 (solvers/rkv65.py)
##
##                                 Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

from ._rungekutta import ExplicitRungeKutta


# SOLVERS ==============================================================================

class RKV65(ExplicitRungeKutta):
    """Verner 6(5) "most robust" pair. Nine stages, 6th order with
    embedded 5th order error estimate.

    Characteristics
    ---------------
    * Order: 6 (propagating) / 5 (embedded)
    * Stages: 9
    * Explicit, adaptive timestep

    Note
    ----
    Fills the gap between 5th order pairs (``RKDP54``) and the expensive 8th
    order ``RKDP87``. The extra stages pay off when the dynamics are smooth
    and tolerances are tight (roughly :math:`10^{-8}` or below), because the
    higher order allows much larger steps. For tolerances in the
    :math:`10^{-4}`--:math:`10^{-6}` range, ``RKDP54`` is usually cheaper
    overall due to fewer stages.

    References
    ----------
    .. [1] Verner, J. H. (2010). "Numerically optimal Runge-Kutta pairs
           with interpolants". Numerical Algorithms, 53(2-3), 383-396.
           :doi:`10.1007/s11075-009-9290-3`
    .. [2] Hairer, E., Nørsett, S. P., & Wanner, G. (1993). "Solving
           Ordinary Differential Equations I: Nonstiff Problems". Springer
           Series in Computational Mathematics, Vol. 8.
           :doi:`10.1007/978-3-540-78862-1`

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError
