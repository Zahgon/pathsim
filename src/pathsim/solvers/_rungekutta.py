########################################################################################
##
##                       BASE CLASS FOR RUNGE-KUTTA INTEGRATORS
##                              (solvers/_rungekutta.py)
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from .._constants import (
    TOLERANCE, 
    SOL_BETA, 
    SOL_SCALE_MIN,
    SOL_SCALE_MAX
    )

from ._solver import ExplicitSolver, ImplicitSolver


# SOLVERS ==============================================================================

class ExplicitRungeKutta(ExplicitSolver):
    """Base class for explicit Runge-Kutta integrators which implements 
    the timestepping at intermediate stages and the error control if 
    the coefficients for the local truncation error estimate are defined.        
    
    Note
    ----
    This class is not intended to be used directly!!!

    Attributes
    ----------
    n : int 
        order of stepping integration scheme
    m : int
        order of embedded integration scheme for error control
    s : int
        numer of RK stages
    history : deque[numeric]
        internal history of past results
    beta : float
        safety factor for error control
    Ks : dict
        slopes at RK stages
    BT : dict[int: None, list[float]], None
        butcher table
    TR : list[float]
        coefficients for truncation error estimate
    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError


    def error_controller(self, dt):
        """Compute scaling factor for adaptive timestep based on 
        absolute and relative local truncation error estimate, 
        also checks if the error tolerance is achieved and returns 
        a success metric.

        Parameters
        ----------
        dt : float 
            integration timestep

        Returns
        -------
        success : bool
            timestep was successful
        err : float
            truncation error estimate
        scale : float
            timestep rescale from error controller
        """
        pass


    def step(self, f, dt):
        """Performs the (explicit) timestep at the intermediate RK stages 
        for (t+dt) based on the state and input at (t)

        Parameters
        ----------
        f : numeric, array[numeric]
            evaluation of function
        dt : float 
            integration timestep

        Returns
        -------
        success : bool
            timestep was successful
        err : float
            truncation error estimate
        scale : float
            timestep rescale from error controller        
        """
        pass


class DiagonallyImplicitRungeKutta(ImplicitSolver):
    """Base class for diagonally implicit Runge-Kutta (DIRK) integrators 
    which implements the timestepping at intermediate stages, involving
    the numerical solution of the implicit update equation and the 
    error control if the coefficients for the local truncation error 
    estimate are defined.

    Extensions and checks to also handle explicit first stages (ESDIRK) 
    and additional final evaluation coefficients (not stiffly accurate)
    
    Note
    ----
    This class is not intended to be used directly!!!

    Attributes
    ----------
    n : int 
        order of stepping integration scheme
    m : int
        order of embedded integration scheme for error control
    s : int
        numer of RK stages
    beta : float
        safety factor for error control
    Ks : dict
        slopes at RK stages
    BT : dict[int: None, list[float]], None
        butcher table
    A : list[float], None
        coefficients for final solution evaluation
    TR : list[float]
        coefficients for truncation error estimate

    """

    def __init__(self, *solver_args, **solver_kwargs):
        raise NotImplementedError


    def error_controller(self, dt):
        """Compute scaling factor for adaptive timestep based on 
        absolute and relative local truncation error estimate, 
        also checks if the error tolerance is achieved and returns 
        a success metric.

        Parameters
        ----------
        dt : float 
            integration timestep

        Returns
        -------
        success : bool
            timestep was successful
        err : float
            truncation error estimate
        scale : float
            timestep rescale from error controller
        """
        pass


    def solve(self, f, J, dt):
        """Solves the implicit update equation using the optimizer of the engine.

        Parameters
        ----------
        f : array_like
            evaluation of function
        J : array_like
            evaluation of jacobian of function
        dt : float 
            integration timestep

        Returns
        -------
        err : float
            residual error of the fixed point update equation
        """
        pass


    def step(self, f, dt):
        """performs the (explicit) timestep at the intermediate RK stages 
        for (t+dt) based on the state and input at (t)

        Parameters
        ----------
        f : array_like
            evaluation of function
        dt : float 
            integration timestep

        Returns
        -------
        success : bool
            timestep was successful
        err : float
            truncation error estimate
        scale : float
            timestep rescale from error controller
        """
        pass
