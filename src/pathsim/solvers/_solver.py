########################################################################################
##
##                            BASE NUMERICAL INTEGRATOR CLASSES
##                                  (solvers/_solver.py)
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from collections import deque

from .._constants import (
    TOLERANCE,
    SIM_TIMESTEP,
    SIM_TIMESTEP_MIN,
    SIM_TIMESTEP_MAX,
    SOL_TOLERANCE_LTE_ABS, 
    SOL_TOLERANCE_LTE_REL,
    SOL_TOLERANCE_FPI,
    SOL_ITERATIONS_MAX
    )

from ..optim.anderson import (
    Anderson, 
    NewtonAnderson
    )


# BASE SOLVER CLASS ====================================================================

class Solver:
    """Base skeleton class for solver definition. Defines the basic solver methods and 
    the metadata.

    Specific solvers need to implement (some of) the base class methods defined here. 
    This depends on the type of solver (implicit/explicit, multistage, adaptive).

    Parameters
    ----------
    initial_value : float, np.ndarray
        initial condition / integration constant
    tolerance_lte_abs : float
        absolute tolerance for local truncation error (for solvers with error estimate)
    tolerance_lte_rel : float
        relative tolerance for local truncation error (for solvers with error estimate)
    parent : None | Solver
        parent solver instance that manages the intermediate stages, stage counter, etc.

    Attributes
    ----------
    x : float, np.ndarray
        internal 'working' state
    history : deque[float, np.ndarray]
        internal history of past results
    n : int
        order of integration scheme
    s : int
        number of internal intermediate stages
    _stage : int
        counter for current intermediate stage
    eval_stages : list[float]
        rations for evaluation times of intermediate stages
    """

    def __init__(
        self, 
        initial_value=0,
        parent=None, 
        tolerance_lte_abs=SOL_TOLERANCE_LTE_ABS, 
        tolerance_lte_rel=SOL_TOLERANCE_LTE_REL
        ):

        #set state and initial condition (ensure array format for consistency)
        self.initial_value = initial_value
        self.x = np.atleast_1d(initial_value).copy()

        #track if initial value was scalar for output formatting
        self._scalar_initial = np.isscalar(initial_value)

        #tolerances for local truncation error (for adaptive solvers)
        self.tolerance_lte_abs = tolerance_lte_abs
        self.tolerance_lte_rel = tolerance_lte_rel  

        #parent solver instance
        self.parent = parent

        #flag to identify adaptive/fixed timestep solvers
        self.is_adaptive = False

        #history of past solutions, default only one
        self.history = deque([], maxlen=1)

        #order of the integration scheme
        self.n = 1

        #number of stages
        self.s = 1

        #current evaluation stage for multistage solvers
        self._stage = 0

        #intermediate evaluation times as ratios between [t, t+dt]
        self.eval_stages = [0.0]


    def __str__(self):
        return self.__class__.__name__


    def __len__(self):
        """size of the internal state, i.e. the order
        
        Returns
        -------
        size : int
            size of the current internal state
        """
        return len(np.atleast_1d(self.x))


    def __bool__(self):
        return True


    @property
    def stage(self):
        """stage property management to interface with parent solver

        Returns
        -------
        stage : int
            current intermediate evaluation stage of solver
        """
        pass


    @stage.setter
    def stage(self, val):
        """stage property management to interface with parent solver,
        setter method for property

        Parameters
        ----------
        val : int
            set intermediate evaluation stage of solver
        """
        pass


    def is_first_stage(self):
        return self.stage == 0


    def is_last_stage(self):
        return self.stage == self.s - 1


    def stages(self, t, dt):
        """Generator that yields the intermediate evaluation 
        time during the timestep 't + ratio * dt' and also updates 
        the current stage number for internal use.

        Parameters
        ----------
        t : float 
            evaluation time
        dt : float
            integration timestep
        """
        for self.stage, ratio in enumerate(self.eval_stages):
            yield t + ratio * dt


    def get(self):
        """Returns current internal state of the solver.

        Returns
        -------
        x : float, np.ndarray
            current internal state of the solver
        """
        return self.x


    def set(self, x):
        """Sets the internal state of the integration engine.

        This method is required for event based simulations,
        and to handle discontinuities in state variables.

        Parameters
        ----------
        x : float, np.ndarray
            new internal state of the solver

        """
        pass


    @property
    def state(self):
        """Property for cleaner access to internal state.

        Returns
        -------
        x : float, np.ndarray
            current internal state of the solver
        """
        pass


    @state.setter
    def state(self, value):
        """Property setter for internal state.

        Parameters
        ----------
        value : float, np.ndarray
            new internal state of the solver
        """
        pass


    def reset(self, initial_value=None):
        """"Resets integration engine to initial value, 
        optionally provides new initial value
    
        Parameters
        ----------
        initial_value : None | float | np.ndarray
            new initial value of the engine, optional
        """

        #update initial value if provided
        if initial_value is not None:
            self.initial_value = initial_value

        #overwrite state with initial value (ensure array format)
        self.x = np.atleast_1d(self.initial_value).copy()
        self.history.clear()


    def buffer(self, dt):
        """Saves the current state to an internal state buffer which 
        is especially relevant for multistage and implicit solvers.

        Multistep solver implement rolling buffers for the states 
        and timesteps.

        Resets the stage counter.
        
        Parameters
        ----------
        dt : float
            integration timestep
    
        """

        #buffer internal state to history
        self.history.appendleft(self.x)


    @classmethod
    def cast(cls, other, parent, **solver_kwargs):
        """Cast the integration engine to the new type and initialize 
        with previous solver arguments so it can continue from where 
        the 'old' solver stopped.
            
        Parameters
        ----------
        other : Solver
            solver instance to cast to new solver type
        parent : None | Solver
            solver instance to use as parent
        solver_kwargs : dict
            additional args for the new solver

        Returns
        -------
        engine : Solver
            new solver instance cast from `other`      
        """

        if not isinstance(other, Solver):
            raise ValueError("'other' must be instance of 'Solver' or child")

        #assemble additional solver kwargs (default)
        _solver_kwargs = {
            "tolerance_lte_rel": other.tolerance_lte_rel,
            "tolerance_lte_abs": other.tolerance_lte_abs
        }

        #update from casting
        _solver_kwargs.update(solver_kwargs)

        #create new solver instance
        engine = cls(
            initial_value=other.initial_value, 
            parent=parent,
            **_solver_kwargs
            )
        
        #set internal state of new engine from other
        engine.set(other.get())

        return engine


    @classmethod
    def create(cls, initial_value, parent=None, from_engine=None, **solver_kwargs):
        """Create a new solver instance, optionally inheriting state from existing engine.

        This provides a unified interface for solver creation that handles both
        new instantiation and solver switching (previously done via cast).

        Parameters
        ----------
        initial_value : float, array
            initial condition / integration constant
        parent : None | Solver
            parent solver instance for stage synchronization
        from_engine : None | Solver
            existing solver to inherit state and settings from
        solver_kwargs : dict
            additional args for the solver (tolerances, etc.)

        Returns
        -------
        engine : Solver
            new solver instance
        """
        if from_engine is not None:
            #inherit tolerances from existing engine if not specified
            if "tolerance_lte_rel" not in solver_kwargs:
                solver_kwargs["tolerance_lte_rel"] = from_engine.tolerance_lte_rel
            if "tolerance_lte_abs" not in solver_kwargs:
                solver_kwargs["tolerance_lte_abs"] = from_engine.tolerance_lte_abs

            #create new solver
            engine = cls(initial_value, parent, **solver_kwargs)

            #preserve state from old engine
            engine.state = from_engine.state

            return engine

        #simple creation without existing engine
        return cls(initial_value, parent, **solver_kwargs)


    # checkpoint methods ---------------------------------------------------------------

    def to_checkpoint(self, prefix):
        """Serialize solver state for checkpointing.

        Parameters
        ----------
        prefix : str
            NPZ key prefix for this solver's arrays

        Returns
        -------
        json_data : dict
            JSON-serializable metadata
        npz_data : dict
            numpy arrays keyed by path
        """
        pass


    def load_checkpoint(self, json_data, npz, prefix):
        """Restore solver state from checkpoint.

        Parameters
        ----------
        json_data : dict
            solver metadata from checkpoint JSON
        npz : dict-like
            numpy arrays from checkpoint NPZ
        prefix : str
            NPZ key prefix for this solver's arrays
        """
        pass


    # methods for adaptive timestep solvers --------------------------------------------

    def error_controller(self):
        """Returns the estimated local truncation error (abs and rel) and scaling factor
        for the timestep, only relevant for adaptive timestepping methods.

        Returns
        -------
        success : bool
            True if the timestep was successful
        error : float
            estimated error of the internal error controller
        scale : float | None
            estimated timestep rescale factor for error control, None if no rescale needed
        """
        return True, 0.0, None


    def revert(self):
        """Revert integration engine to previous timestep. 

        This is only relevant for adaptive methods where the simulation 
        timestep 'dt' is rescaled and the engine step is recomputed with 
        the smaller timestep.
        """
        
        #reset internal state to previous state from history
        self.x = self.history.popleft() 


    # methods for timestepping ---------------------------------------------------------

    def step(self, f, dt):
        """Performs the explicit timestep for (t+dt) based
        on the state and input at (t).

        Returns the local truncation error estimate and the
        rescale factor for the timestep if the solver is adaptive.

        Parameters
        ----------
        f : numeric, array[numeric]
            evaluation of rhs function
        dt : float
            integration timestep

        Returns
        -------
        success : bool
            True if the timestep was successful
        error : float
            estimated error of the internal error controller
        scale : float | None
            estimated timestep rescale factor for error control, None if no rescale needed
        """
        return True, 0.0, None


    # methods for interpolation --------------------------------------------------------

    def interpolate(self, r, dt):
        """Interpolate solution after successful timestep as a ratio 
        in the interval [t, t+dt].

        This is especially relevant for Runge-Kutta solvers that 
        have a higher order interpolant. Otherwise this is just 
        linear interpolation using the buffered state.
        
        Parameters
        ----------
        r : float
            ration for interpolation within timestep
        dt : float
            integration timestep

        Returns
        -------
        x : numeric, array[numeric]
            interpolated state
        """
        pass


# EXTENDED BASE SOLVER CLASSES =========================================================

class ExplicitSolver(Solver):
    """Base class for explicit solver definition.

    Attributes
    ----------
    x_0 : numeric, array[numeric]
        internal 'working' initial value
    x : numeric, array[numeric]
        internal 'working' state
    n : int
        order of integration scheme
    s : int
        number of internal intermediate stages
    stage : int
        counter for current intermediate stage
    eval_stages : list[float]
        rations for evaluation times of intermediate stages

    """

    def __init__(self, *solver_args, **solver_kwargs):
        super().__init__(*solver_args, **solver_kwargs)

        #flag to identify implicit/explicit solvers
        self.is_explicit = True
        self.is_implicit = False

        #intermediate evaluation times for multistage solvers as ratios between [t, t+dt]
        self.eval_stages = [0.0]


    # method for direct integration ----------------------------------------------------

    def integrate_singlestep(self, func, time=0.0, dt=SIM_TIMESTEP):
        """Directly integrate the function for a single timestep 'dt' with 
        explicit solvers. This method is primarily intended for testing purposes.
        
        Parameters
        ----------  
        func : callable
            function to integrate f(x, t)
        time : float
            starting time for timestep
        dt : float
            integration timestep

        Returns 
        -------
        success : bool
            True if the timestep was successful
        error_norm : float
            estimated error of the internal error controller
        scale : float
            estimated timestep rescale factor for error control
        """
        pass


    def integrate(
        self, 
        func,
        time_start=0.0, 
        time_end=1.0, 
        dt=SIM_TIMESTEP, 
        dt_min=SIM_TIMESTEP_MIN, 
        dt_max=SIM_TIMESTEP_MAX, 
        adaptive=True
        ):
        """Directly integrate the function 'func' from 'time_start' 
        to 'time_end' with timestep 'dt' for explicit solvers. 

        This method is primarily intended for testing purposes or 
        for use as a standalone numerical integrator.

        Example
        -------

        This is how to directly use the solver to integrate an ODE:

        .. code-block:: python
            
            #1st order linear ODE
            def f(x, u, t):
                return -x

            #initial condition
            x0 = 1
    
            #initialize ODE solver
            sol = Solver(x0)

            #integrate from 0 to 5 with timestep 0.1
            t, x = sol.integrate(f, time_end=5, dt=0.1)

    
        Parameters
        ----------
        func : callable
            function to integrate f(x, t)
        time_start : float
            starting time for integration
        time_end : float
            end time for integration
        dt : float
            timestep or initial timestep for adaptive solvers
        dt_min : float
            lower bound for timestep, default '0.0'
        dt_max : float
            upper bound for timestep, default 'None'
        adaptive : bool
            use adaptive timestepping if available

        Returns
        -------
        outout_times : array[float]
            time points of the solution
        output_states : array[numeric], array[array[numeric]]
            state values at solution time points
        """
        pass


class ImplicitSolver(Solver):
    """
    Base class for implicit solver definition.

    Attributes
    ----------
    x_0 : numeric, array[numeric]
        internal 'working' initial value
    x : numeric, array[numeric]
        internal 'working' state
    n : int
        order of integration scheme
    s : int
        number of internal intermediate stages
    stage : int
        counter for current intermediate stage
    eval_stages : list[float]
        rations for evaluation times of intermediate stages
    opt : NewtonAnderson, Anderson, etc.
        optimizer instance to solve the implicit update equation

    """

    def __init__(self, *solver_args, **solver_kwargs):
        super().__init__(*solver_args, **solver_kwargs)

        #flag to identify implicit/explicit solvers
        self.is_explicit = False
        self.is_implicit = True

        #intermediate evaluation times for multistage solvers as ratios between [t, t+dt]
        self.eval_stages = [1.0]

        #initialize optimizer for solving implicit update equation (default args)
        self.opt = NewtonAnderson()


    def buffer(self, dt):
        """Saves the current state to an internal state buffer which 
        is especially relevant for multistage and implicit solvers.

        Resets the stage counter and the optimizer of implicit methods.
        
        Parameters
        ----------
        dt : float
            integration timestep
        """

        #buffer internal state to history
        self.history.appendleft(self.x)

        #reset stage counter
        self.stage = 0

        #reset optimizer
        self.opt.reset()


    # methods for timestepping ---------------------------------------------------------

    def solve(self, j, J, dt):
        """Advances the solution of the implicit update equation of the solver 
        with the optimizer of the engine and tracks the evolution of the 
        solution by providing the residual norm of the fixed-point solution.

        Parameters
        ----------
        f : numeric, array[numeric]
            evaluation of rhs function
        J : array[numeric]
            evaluation of jacobian of rhs function 
        dt : float 
            integration timestep

        Returns
        -------
        err : float
            residual error of the fixed point update equation
        """
        return 0.0


    # method for direct integration ----------------------------------------------------

    def integrate_singlestep(
        self, 
        func,
        jac,
        time=0.0, 
        dt=SIM_TIMESTEP, 
        tolerance_fpi=SOL_TOLERANCE_FPI, 
        max_iterations=SOL_ITERATIONS_MAX
        ):
        """
        Directly integrate the function 'func' for a single timestep 'dt' with 
        implicit solvers. This method is primarily intended for testing purposes.

        Parameters
        ----------  
        func : callable
            function to integrate f(x, t)
        jac : callable
            jacobian of f w.r.t. x
        time_start : float
            starting time for timestep
        dt : float
            integration timestep
        tolerance_fpi : float
            convergence criterion for implicit update equation
        max_iterations : int
            maximum numer of iterations for optimizer to solve 
            implicit update equation

        Returns 
        -------
        success : bool
            True if the timestep was successful
        error_norm : float
            estimated error of the internal error controller 
            or solver when not converged
        scale : float
            estimated timestep rescale factor for error control
        """
        pass


    def integrate(
        self, 
        func, 
        jac,
        time_start=0.0, 
        time_end=1.0, 
        dt=SIM_TIMESTEP, 
        dt_min=SIM_TIMESTEP_MIN, 
        dt_max=SIM_TIMESTEP_MAX, 
        adaptive=True,
        tolerance_fpi=SOL_TOLERANCE_FPI, 
        max_iterations=SOL_ITERATIONS_MAX
        ):
        """Directly integrate the function 'func' from 'time_start' 
        to 'time_end' with timestep 'dt' for implicit solvers. 

        This method is primarily intended for testing purposes or 
        for use as a standalone numerical integrator.

        Example
        -------

        This is how to directly use the solver to integrate an ODE:

        .. code-block:: python
            
            #1st order linear ODE
            def f(x, t):
                return -x

            #initial condition
            x0 = 1
    
            #initialize ODE solver
            sol = Solver(x0)

            #integrate from 0 to 5 with timestep 0.1
            t, x = sol.integrate(f, time_end=5, dt=0.1)
    
        Parameters
        ----------
        func : callable
            function to integrate f(x, t)
        jac : callable
            jacobian of f w.r.t. x
        time_start : float
            starting time for integration
        time_end : float
            end time for integration
        dt : float
            timestep or initial timestep for adaptive solvers
        dt_min : float
            lower bound for timestep, default '0.0'
        dt_max : float
            upper bound for timestep, default 'None'
        adaptive : bool
            use adaptive timestepping if available
        tolerance_fpi : float
            convergence criterion for implicit update equation
        max_iterations : int
            maximum numer of iterations for optimizer to solve 
            implicit update equation

        Returns
        -------
        outout_times : array[float]
            time points of the solution
        output_states : array[numeric], array[array[numeric]]
            state values at solution time points    
        """
        pass
