#########################################################################################
##
##                                     BASE BLOCK 
##                                 (blocks/_block.py)
##
##            This module defines the base 'Block' class that is the parent 
##         to all other blocks and can serve as a base for new or custom blocks
##
#########################################################################################

# IMPORTS ===============================================================================

import inspect
from functools import lru_cache

from ..utils.deprecation import deprecated
from ..utils.register import Register
from ..utils.portreference import PortReference


# BASE BLOCK CLASS ======================================================================

class Block:
    """Base 'Block' object that defines the inputs, outputs and the block interface.

    Block interconnections are handled via the io interface of the blocks. 
    It is realized by dicts for the 'inputs' and for the 'outputs', where the 
    key of the dict is the input/output channel and the corresponding value is 
    the input/output value. 

    The block can spawn discrete events that are handled by the main simulation 
    for triggers, discrete time blocks, etc.

    Mathematically the block behavior is defined by two operators in most cases

    .. math::
    
        \\begin{align}
        \\dot{x} &= f_\\mathrm{dyn}(x, u, t)\\\\
               y &= f_\\mathrm{alg}(x, u, t)
        \\end{align}


    they are algebraic operators for the algebraic path of the block and for the 
    dynamic path that feeds into the internal numerical integration engine.

    There are special cases where one or both of them are not defined, also for 
    purely algebraic blocks such as multipliers and functions, there exists a 
    simplified operator definition:
    
    .. math::

        y = f_\\mathrm{alg}(u)
    

    Note
    ----
    This block is not intended to be used directly and serves as a base 
    class definition for other blocks to be inherited.
    

    Attributes
    ----------
    inputs : Register
        input value register of block
    outputs : Register
        output value register of block
    state : None | float | np.ndarray
        state of `engine` exposed as a property, only exists for dynamic blocks
    engine : None | Solver
        numerical integrator instance, only exists for dynamic blocks
    events : list[Event]
        list of internal events, for mixed signal blocks
    _active : bool
        flag that sets the block active or inactive
    op_alg : Operator | DynamicOperator | None
        internal callable operator for algebraic components of block
    op_dyn : DynamicOperator | None
        internal callable operator for dynamic (ODE) components of block
    """

    input_port_labels = None
    output_port_labels = None

    def __init__(self):

        #registers to hold input and output values
        raise NotImplementedError


    def __len__(self):
        """The '__len__' method of the block is used to compute the length of the 
        algebraic path of the block. 

        For instant time blocks or blocks with purely algebraic components 
        (adders, amplifiers, etc.) it returns 1, otherwise (integrator, delay, etc.) 
        it returns 0.

        If the block is disabled '_active == False', it returns 0 as well, since
        this breaks the signal path.

        Returns
        -------
        len : int
            length of the algebraic path of the block
        """
        raise NotImplementedError


    def __getitem__(self, key):
        """The '__getitem__' method is intended to make connection creation more 
        convenient and therefore just returns the block itself and the key directly 
        after doing some basic checks.

        Parameters
        ----------
        key : int, str, slice, tuple[int, str], list[int, str]
            port indices or port names, or list / tuple of them

        Returns
        -------
        PortReference
            container object that hold block reference and list of ports
        """
        raise NotImplementedError


    def __call__(self):
        """The '__call__' is an alias for the 'get_all' method."""
        raise NotImplementedError


    def __bool__(self):
        raise NotImplementedError


    # methods for access to metadata ----------------------------------------------------

    @property
    def size(self):
        """Get size information from block, such as 
        number of internal states, etc.

        Returns
        -------
        sizes : tuple[int]
            size of block (default 1) and number 
            of internal states (from internal engine)
        """
        pass


    @property
    def shape(self):
        """Get the number of input and output ports of the block

        Returns
        -------
        shape : tuple[int]
            number of input and output ports
        """ 
        pass


    @classmethod
    @lru_cache()
    def info(cls):
        """Get block metadata for introspection and UI integration.

        Returns a dictionary containing block type information, port mappings,
        and parameter definitions. Results are cached per class.

        Returns
        -------
        info : dict
            Block metadata with the following keys:
            - type : str
                Class name of the block
            - description : str
                Block docstring
            - shape : tuple
                Input/output shape (n_inputs, n_outputs)
            - size : int
                State vector size
            - in_labels : dict
                Input port name to index mapping
            - out_labels : dict
                Output port name to index mapping
            - parameters : dict
                Parameter names mapped to their default values
        """
        pass


    # methods for visualization ---------------------------------------------------------

    def plot(self, *args, **kwargs):
        """Block specific visualization, enables plotting 
        access from the simulation level.

        This gets primarily used by the visualization blocks 
        such as the 'Scope' and 'Spectrum'.

        Parameters
        ----------
        args : tuple
            args for the plot methods
        kwargs : dict
            kwargs for the plot method
        """
        pass


    # methods for simulation management -------------------------------------------------

    def on(self):
        """Activate the block and all internal events, sets the boolean
        evaluation flag to 'True'.
        """
        pass


    def off(self):
        """Deactivate the block and all internal events, sets the boolean 
        evaluation flag to 'False'. Also resets the block.
        """
        pass


    def reset(self):
        """Reset the blocks inputs and outputs and also its internal solver, 
        if the block has a solver instance.
        """
        pass


    def linearize(self, t):
        """Linearize the algebraic and dynamic components of the block.

        This is done by linearizing the internal 'Operator' and 'DynamicOperator' 
        instances in the current system operating point. The operators create 
        1st order taylor approximations internally and use them on subsequent 
        calls after linearization.

        Parameters
        ----------
        t : float 
            evaluation time
        """
        pass


    def delinearize(self):
        """Revert the linearization of the blocks algebraic and dynamic components.
        
        This is resets the internal 'Operator' and 'DynamicOperator' instances, 
        deleting the linear surrogate model and using the original function for 
        subsequent calls.
        """
        pass


    # methods for blocks with integration engines ---------------------------------------

    def set_solver(self, Solver, parent, **solver_args):
        """Initialize the numerical integration engine with local truncation error
        tolerance if required.

        If the block already has an integration engine, it is changed.
        If the block does not have an 'initial_value' attribute, this method
        does nothing (block is not dynamic).

        Parameters
        ----------
        Solver : Solver
            numerical integrator class
        parent : None | Solver
            numerical integrator instance for stage synchronization
        solver_args : dict
            additional args for the solver
        """
        pass


    def revert(self):
        """Revert the block to the state of the previous timestep, if the 
        block has a solver instance indicated by the 'has_engine' flag.

        This is required for adaptive solvers to revert the state to the 
        previous timestep.
        """
        pass


    def buffer(self, dt):
        """
        Buffer current internal state of the block and the current timestep
        if the block has a solver instance (is stateful).

        This is required for multistage, multistep and adaptive integrators.

        Parameters
        ----------
        dt : float
            integration timestep
        """
        pass


    # methods for sampling data ---------------------------------------------------------
    
    def sample(self, t, dt):
        """Samples the data of the blocks inputs or internal state when called. 

        This can record block parameters after a successful timestep such as 
        for the 'Scope' and 'Delay' blocks but also for sampling from a random 
        distribution in the 'RNG' and the noise blocks.
        
        Parameters
        ----------
        t : float
            evaluation time for sampling
        dt : float
            integration timestep
        """
        pass


    # methods for extracting data -------------------------------------------------------
        
    def read(self):
        """Read data from recording blocks.
        
        Note
        ----
        Not implemented by default, special recording blocks 
        implement this method.
        """
        pass


    @deprecated(version="1.0.0", reason="its against pathsims philosophy")
    def collect(self):
        """Yield (category, id, data) tuples for recording blocks to simplify 
        global data collection from all recording blocks.

        Note
        ----
        Yields an empty generator by default, needs to be implemented by 
        special recording blocks.
        """
        pass


    # methods for inter-block data transfer ---------------------------------------------

    def get_all(self):
        """Retrieves and returns internal states of engine (if available) 
        and the block inputs and outputs as arrays for use outside. 

        Either for monitoring, postprocessing or event detection. 
        In any case this enables easy access to the current block state.

        Returns
        -------
        inputs : array
            block input register
        outputs : array
            block output register
        states : array
            internal states of the block
        """
        pass


    @property
    def state(self):
        """Expose the state of the internal integration engine / 
        `Solver` instance as an attribute of `Block`. 
    
        Note
        ----
        Only applies to blocks that are dynamic.

        Returns
        -------
        state : None, float, np.ndarray
            returns the current state of the block if the block is dynamic 
            (has an internal `Solver` instance), otherwise returns `None`
        """
        pass


    @state.setter
    def state(self, val):
        """Setter method for the exposed internal `Solver` instance. 
        
        Note
        ----
        Only applies to blocks that are dynamic.

        Parameters
        ----------
        val : float, np.ndarray
            value to set internal solver state to
        """
        pass


    # checkpoint methods ----------------------------------------------------------------

    def to_checkpoint(self, prefix, recordings=False):
        """Serialize block state for checkpointing.

        Parameters
        ----------
        prefix : str
            key prefix for NPZ arrays (assigned by simulation)
        recordings : bool
            include recording data (for Scope blocks)

        Returns
        -------
        json_data : dict
            JSON-serializable metadata
        npz_data : dict
            numpy arrays keyed by path
        """
        pass


    def load_checkpoint(self, prefix, json_data, npz):
        """Restore block state from checkpoint.

        Parameters
        ----------
        prefix : str
            key prefix for NPZ arrays (assigned by simulation)
        json_data : dict
            block metadata from checkpoint JSON
        npz : dict-like
            numpy arrays from checkpoint NPZ
        """
        pass


    # methods for block output and state updates ----------------------------------------

    def update(self, t):
        """The 'update' method is called iteratively for all blocks to evaluate the 
        algebraic components of the global system ode from the DAG.

        It is meant for instant time blocks (blocks that dont have a delay due to the 
        timestep, such as Amplifier, etc.) and updates the 'outputs' of the block 
        directly based on the 'inputs' and possibly internal states. 

        Note
        ----
        The implementation of the 'update' method in the base 'Block' class is intended 
        as a fallback and is not performance optimized. Special blocks might reimplement 
        this method differently for higher performance, for example SISO or MISO blocks.

        Parameters
        ----------
        t : float
            evaluation time
        """
        pass


    def solve(self, t, dt):
        """The 'solve' method performs one iterative solution step that is required
        to solve the implicit update equation of the solver if an implicit solver 
        (numerical integrator) is used.

        It returns the relative difference between the new updated solution 
        and the previous iteration of the solution to track convergence within 
        an outer loop.

        This only has to be implemented by blocks that have an internal 
        integration engine with an implicit solver.

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
        """The 'step' method is used in transient simulations and performs an action 
        (numeric integration timestep, recording data, etc.) based on the current 
        inputs and the current internal state. 

        It performs one timestep for the internal states. For instant time blocks,
        the 'step' method does not has to be implemented specifically. 
        
        The method handles timestepping for dynamic blocks with internal states
        such as 'Integrator', 'StateSpace', etc.

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
        scale : float | None
            timestep rescale from adaptive integrators, None if no rescale needed
        """
        pass
