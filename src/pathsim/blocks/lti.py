#########################################################################################
##
##               LINEAR TIME INVARIANT DYNAMICAL BLOCKS (blocks/lti.py)
##
##             This module defines linear time invariant dynamical blocks
##
##                                 Milan Rother 2024
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from scipy.signal import ZerosPolesGain
from scipy.signal import TransferFunction as _TransferFunction

from ._block import Block

from ..utils.register import Register
from ..utils.gilbert import gilbert_realization
from ..utils.deprecation import deprecated

from ..optim.operator import DynamicOperator
from ..utils.mutable import mutable


# LTI BLOCKS ============================================================================

class StateSpace(Block):
    """Linear time invariant (LTI) multi input multi output (MIMO) state space model.

    .. math::

        \\begin{align}
            \\dot{x} &= \\mathbf{A} x + \\mathbf{B} u \\\\
                   y &= \\mathbf{C} x + \\mathbf{D} u
        \\end{align}

    where `A`, `B`, `C` and `D` are the state space matrices, `x` is the state, 
    `u` the input and `y` the output vector.
    
    Example
    -------
    A SISO state space block with two internal states can be initialized 
    like this:

    .. code-block:: python

        S = StateSpace(
            A=-np.eye(2), 
            B=np.ones((2, 1)), 
            C=np.ones((1, 2)), 
            D=1.0
            )

    and a MIMO (2 in, 2 out) state space block with three internal states 
    can be initialized like this:

    .. code-block:: python

        S = StateSpace(
            A=-np.eye(3), 
            B=np.ones((3, 2)), 
            C=np.ones((2, 3)), 
            D=np.ones((2, 2))
            )

    Parameters
    ----------
    A, B, C, D : array_like
        real valued state space matrices
    initial_value : array_like, None
        initial state / initial condition

    Attributes
    ----------
    op_dyn : DynamicOperator
        internal dynamic operator for state equation
    op_alg : DynamicOperator
        internal algebraic operator for mapping to outputs
    """

    def __init__(self, 
                 A=-1.0, B=1.0, C=-1.0, D=1.0, 
                 initial_value=None):
        raise NotImplementedError


    def __len__(self):
        #check if direct passthrough exists
        raise NotImplementedError

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


@mutable
class TransferFunctionPRC(StateSpace):
    """This block defines a LTI (MIMO for pole residue) transfer function.

    The transfer function is defined in pole-residue-constant (PRC) form

    .. math::
        
        \\mathbf{H}(s) = \\mathbf{C} + \\sum_n^N \\frac{\\mathbf{R}_n}{s - p_n}

    where 'Poles' are the scalar (possibly complex conjugate) poles of the 
    transfer function and 'Residues' are the possibly matrix valued (in MIMO case) 
    and complex conjugate residues of the transfer function. 'Const' has same 
    shape as 'Residues'.

    Upon initialization, the state space realization of the transfer 
    function is computed using a minimal gilbert realization.

    The resulting state space model of the form

    .. math::
        
        \\begin{align}
            \\dot{x} &= \\mathbf{A} x + \\mathbf{B} u \\\\
                   y &= \\mathbf{C} x + \\mathbf{D} u
        \\end{align}

    is handled the same as the 'StateSpace' block, where `A`, `B`, `C` and `D` 
    are the state space matrices, `x` is the internal state, `u` the input and 
    `y` the output vector.
        
    Parameters
    ----------
    Poles : array
        transfer function poles
    Residues : array
        transfer function residues
    Const : array, float
        constant term of transfer function
    """

    def __init__(self, Poles=[], Residues=[], Const=0.0):

        #parameters of transfer function in pole-residue-const form
        raise NotImplementedError


@deprecated(version="1.0.0", replacement="TransferFunctionPRC")
class TransferFunction(TransferFunctionPRC):
    """Alias for TransferFunctionPRC."""
    pass


@mutable
class TransferFunctionZPG(StateSpace):
    """This block defines a LTI (SISO) transfer function.

    The transfer function is defined in zeros-poles-gain (ZPG) form

    .. math::
        
        \\mathbf{H}(s) = k \\frac{(s - z_1)(s - z_2)\\cdots(s - z_m)}{(s - p_1)(s - p_2)\\cdots(s - p_n)}

    where `Zeros` are the scalar (possibly complex conjugate) zeros of the 
    transfer function, and `Poles` are the poles (denominator zeros) of the 
    transfer function. `Gain` is the scalar factor `k`.
    
    Upon initialization, the state space realization of the transfer function is 
    computed using `scipy.signal.ZerosPolesGain(Zeros, Poles, Gain).to_ss()`.

    The resulting state space model of the form

    .. math::
        
        \\begin{align}
            \\dot{x} &= \\mathbf{A} x + \\mathbf{B} u \\\\
                   y &= \\mathbf{C} x + \\mathbf{D} u
        \\end{align}

    is handled the same as the 'StateSpace' block, where `A`, `B`, `C` and `D` 
    are the state space matrices, `x` is the internal state, `u` the input and 
    `y` the output vector.
        
    Parameters
    ----------
    Poles : array_like
        transfer function poles
    Zeros : array_like
        transfer function zeros
    Gain : float
        gain term of transfer function 
    """

    input_port_labels = {"in": 0}
    output_port_labels = {"out":0}

    def __init__(self, Zeros=[], Poles=[-1], Gain=1.0):

        #parameters of transfer function in zeros-poles-gain form
        raise NotImplementedError


@mutable
class TransferFunctionNumDen(StateSpace):
    """This block defines a LTI (SISO) transfer function.

    The transfer function is defined in polynomial (numerator-denominator) form

    .. math::
        
        \\mathbf{H}(s) = \\frac{b_n + b_{n-1} s + \\dots + b_{0} s^n}{a_m + a_{m-1} s + \\dots + a_{0} s^m}

    where `Num` is the list of numerator polynomial coefficients and `Den` the 
    list of denominator coefficients.
    
    Upon initialization, the state space realization of the transfer function is 
    computed using `scipy.signal.TransferFunction(Num, Den).to_ss()`.

    The resulting state space model of the form

    .. math::
        
        \\begin{align}
            \\dot{x} &= \\mathbf{A} x + \\mathbf{B} u \\\\
                   y &= \\mathbf{C} x + \\mathbf{D} u
        \\end{align}

    is handled the same as the 'StateSpace' block, where `A`, `B`, `C` and `D` 
    are the state space matrices, `x` is the internal state, `u` the input and 
    `y` the output vector.
        
    Parameters
    ----------
    Num : array_like
        numerator polynomial coefficients
    Den : array_like
        denominator polynomial coefficients
    """

    input_port_labels = {"in": 0}
    output_port_labels = {"out":0}

    def __init__(self, Num=[1], Den=[1, 1]):

        #parameters of transfer function in numerator-denominator
        raise NotImplementedError

