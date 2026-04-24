#########################################################################################
##
##                          NONLINEAR DYNAMICAL SYSTEM BLOCK 
##                                 (blocks/dynsys.py)
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from ._block import Block

from ..optim.operator import DynamicOperator


# BLOCKS ================================================================================

class DynamicalSystem(Block):
    """This block implements a nonlinear dynamical system / nonlinear state space model.

    Its basically the same as the `ODE` block with the addition of an output equation
    that takes the state, input and time as arguments:

    .. math::

        \\begin{align}
            \\dot{x}(t) &= \\mathrm{func}_\\mathrm{dyn}(x(t), u(t), t) \\\\
                   y(t) &= \\mathrm{func}_\\mathrm{alg}(x(t), u(t), t)
        \\end{align}

        
    Parameters
    ----------
    func_dyn : callable
        right hand side function of ode-part of the system
    func_alg : callable
        output function of the system
    initial_value : array[float]
        initial state / initial condition
    jac_dyn : callable | None
        optional jacobian of `func_dyn` to improve convergence 
        for implicit ode solvers


    Attributes
    ----------
    op_dyn : DynamicOperator
        internal dynamic operator for `func_dyn`
    op_alg : DynamicOperator
        internal dynamic operator for `func_alg`
    """

    def __init__(
        self,
        func_dyn=lambda x, u, t: -x,
        func_alg=lambda x, u, t: x,
        initial_value=0.0,
        jac_dyn=None
        ):

        raise NotImplementedError
        

    def __len__(self):
        """Potential passthrough due to `func_alg` being dependent on `u`.

        This is checked by evaluating the jacobian of the algebraic output 
        equation with respect to `u`. If there are any non-zero entries, an 
        algebraic passthrouh exists.
        
        Returns
        -------
        alg_length : int
            length of algebraic path
        """
        raise NotImplementedError


    def update(self, t):
        """update system equation for fixed point loop, by evaluating the
        output function of the system
    
        Parameters
        ----------
        t : float
            evaluation time
        """
        pass


    def solve(self, t, dt):
        """advance solution of implicit update equation of the solver

        Parameters
        ----------
        t : float
            evaluation time
        dt : float
            integration timestep

        Returns
        ------- 
        error : float
            solver residual norm
        """
        pass


    def step(self, t, dt):
        """compute timestep update with integration engine
        
        Parameters
        ----------
        t : float
            evaluation time
        dt : float
            integration timestep
    
        Returns
        ------- 
        success : bool
            step was successful
        error : float
            local truncation error from adaptive integrators
        scale : float
            timestep rescale from adaptive integrators
        """
        pass