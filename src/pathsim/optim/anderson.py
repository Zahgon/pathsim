########################################################################################
##
##                               ANDERSON ACCELERATION 
##                                (optim/anderson.py)
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from collections import deque

from .._constants import (
    TOLERANCE,
    OPT_RESTART,
    OPT_HISTORY
    )


# CLASS ================================================================================

class Anderson:
    """Anderson acceleration for fixed-point iteration.

    Solves nonlinear equations in fixed-point form :math:`x = g(x)` by
    computing the next iterate as a linear combination of previous iterates
    whose coefficients minimise the least-squares residual.

    .. math::

        x_{k+1} = \\sum_{i=0}^{m_k} \\alpha_i^{(k)}\\, g(x_{k-m_k+i})
        \\quad\\text{with}\\quad
        \\alpha^{(k)} = \\arg\\min \\bigl\\|\\sum_i \\alpha_i\\, r_{k-m_k+i}\\bigr\\|

    where :math:`r_k = g(x_k) - x_k` and :math:`m_k \\le m` is the current
    buffer depth.

    In PathSim this class is the inner fixed-point solver used by the
    simulation engine to resolve algebraic loops (cycles in the block
    diagram). Each loop-closing ``ConnectionBooster`` owns an ``Anderson``
    instance that accelerates convergence of the fixed-point iteration
    over the loop. The buffer depth ``m`` controls how many previous
    iterates are retained; larger values improve convergence on difficult
    loops at the cost of a small least-squares solve per iteration.

    Parameters
    ----------
    m : int
        buffer depth (number of stored iterates)
    restart : bool
        if True, clear the buffer once it reaches depth ``m``

    References
    ----------
    .. [1] Anderson, D. G. (1965). "Iterative Procedures for Nonlinear
           Integral Equations". Journal of the ACM, 12(4), 547--560.
           :doi:`10.1145/321296.321305`
    .. [2] Walker, H. F., & Ni, P. (2011). "Anderson Acceleration for
           Fixed-Point Iterations". SIAM Journal on Numerical Analysis,
           49(4), 1715--1735. :doi:`10.1137/10078356X`
    """

    def __init__(self, m=OPT_HISTORY, restart=OPT_RESTART):

        #length of buffer for next estimate
        raise NotImplementedError


    def __bool__(self):
        return True


    def __len__(self):
        raise NotImplementedError


    def solve(self, func, x0, iterations_max=100, tolerance=1e-6):
        """Solve the function 'func' with initial 
        value 'x0' up to a certain tolerance.

        Note
        ----
        This method is for testing purposes only and 
        not used in the simulation loop.
        
        Parameters
        ----------
        func : callable
            function to solve
        x0 : numeric
            starting value for solution
        iterations_max : int
            maximum number of solver iterations
        tolerance : float
            convergence condition

        Returns
        -------
        x : numeric
            solution
        res : float
            residual
        i : int
            iteration count
        """
        pass


    def reset(self):
        """reset the anderson accelerator"""
        pass


    def step(self, x, g):
        """Perform one iteration on the fixed-point solution.
    
        Parameters
        ----------
        x : float, array
            current solution
        g : float, array
            current evaluation of g(x)
        
        Returns
        -------
        x : float, array
            new solution
        res : float
            residual norm, fixed point error
        """
        pass



class NewtonAnderson(Anderson):
    """Hybrid Newton--Anderson fixed-point solver.

    Extends :class:`Anderson` by prepending a Newton step when a Jacobian
    of :math:`g` is available.  The Newton step

    .. math::

        \\tilde{x} = x - (J_g - I)^{-1}\\,(g(x) - x)

    provides a quadratically convergent initial correction; the subsequent
    Anderson mixing step then stabilises the iteration and damps
    oscillations.

    In PathSim this solver is used inside every implicit ODE integration
    engine (BDF, DIRK, ESDIRK).  When a block provides a local Jacobian
    (e.g. ``ODE`` or ``LTI`` blocks), the Newton pre-step yields much
    faster convergence of the implicit update equation, reducing the
    number of fixed-point iterations per timestep.  Without a Jacobian the
    solver falls back to pure Anderson acceleration.

    References
    ----------
    .. [1] Anderson, D. G. (1965). "Iterative Procedures for Nonlinear
           Integral Equations". Journal of the ACM, 12(4), 547--560.
           :doi:`10.1145/321296.321305`
    .. [2] Walker, H. F., & Ni, P. (2011). "Anderson Acceleration for
           Fixed-Point Iterations". SIAM Journal on Numerical Analysis,
           49(4), 1715--1735. :doi:`10.1137/10078356X`
    """


    def solve(self, func, x0, jac=None, iterations_max=100, tolerance=1e-6):
        """Solve the function 'func' with initial value 
        'x0' up to a certain tolerance.

        Parameters
        ----------
        func : callable
            function to solve
        x0 : numeric
            starting value for solution
        jac : callable
            jacobian of 'func'
        iterations_max : int
            maximum number of solver iterations
        tolerance : float
            convergence condition

        Note
        ----
        This method is for testing purposes only and 
        not used in the simulation loop.

        Returns
        -------
        x : numeric
            solution
        res : float
            residual
        i : int
            iteration count
        """
        pass


    def _newton(self, x, g, jac):
        """Newton step on solution, where 'f=g-x' is the 
        residual and 'jac' is the jacobian of 'g'.

        Parameters
        ----------
        x : float, array
            current solution
        g : float, array
            current evaluation of g(x)
        jac : array
            evaluation of jacobian of 'g'

        Returns
        -------
        x : float, array
            new solution
        res : float
            residual norm
        """
        pass


    def step(self, x, g, jac=None):
        """Perform one iteration on the fixed-point solution. 
        
        If the jacobian of g 'jac' is provided, a newton step 
        is performed previous to anderson acceleration.
            
        Parameters
        ----------
        x : float, array
            current solution
        g : float, array
            current evaluation of g(x)
        jac : array
            evaluation of jacobian of 'g'

        Returns
        -------
        x : float, array
            new solution
        res : float
            residual norm
        """
        pass
