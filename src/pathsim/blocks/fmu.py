#########################################################################################
##
##                           FUNCTIONAL MOCK-UP UNIT (FMU) BLOCKS
##                                   (pathsim/blocks/fmu.py)
##
#########################################################################################

# IMPORTS ===============================================================================

import bisect

from ._block import Block
from .dynsys import DynamicalSystem

from ..events.schedule import Schedule, ScheduleList
from ..events.zerocrossing import ZeroCrossing
from ..utils.fmuwrapper import FMUWrapper


# BLOCKS ================================================================================

class CoSimulationFMU(Block):
    """Co-Simulation FMU block using FMPy with support for FMI 2.0 and FMI 3.0.

    This block wraps an FMU (Functional Mock-up Unit) for co-simulation.
    The FMU encapsulates a simulation model that can be executed independently
    and synchronized with the main simulation at discrete communication points.

    Parameters
    ----------
    fmu_path : str
        path to the FMU file (.fmu)
    instance_name : str, optional
        name for the FMU instance (default: 'fmu_instance')
    start_values : dict, optional
        dictionary of variable names and their initial values
    dt : float, optional
        communication step size for co-simulation. If None, uses the FMU's
        default experiment step size if available.

    Attributes
    ----------
    fmu_wrapper : FMUWrapper
        version-agnostic FMU wrapper instance providing access to model_description,
        fmu, and other FMPy objects for advanced usage
    dt : float
        communication step size
    """

    def __init__(self, fmu_path, instance_name="fmu_instance", start_values=None, dt=None):
        raise NotImplementedError


    def _step_fmu(self, t):
        """Perform one FMU co-simulation step."""
        pass


    def reset(self):
        """Reset the FMU instance."""
        pass


    def __len__(self):
        """FMU is a discrete time source-like block without direct passthrough."""
        return 0


class ModelExchangeFMU(DynamicalSystem):
    """Model Exchange FMU block using FMPy with support for FMI 2.0 and FMI 3.0.

    This block wraps an FMU (Functional Mock-up Unit) for model exchange.
    The FMU provides the right-hand side of an ODE system that is integrated
    by PathSim's numerical solvers. Internal FMU events (state events, time
    events, and step completion events) are translated to PathSim events.

    Parameters
    ----------
    fmu_path : str
        path to the FMU file (.fmu)
    instance_name : str, optional
        name for the FMU instance (default: 'fmu_instance')
    start_values : dict, optional
        dictionary of variable names and their initial values
    tolerance : float, optional
        tolerance for event detection (default: 1e-10)
    verbose : bool, optional
        enable verbose output (default: False)

    Attributes
    ----------
    fmu_wrapper : FMUWrapper
        version-agnostic FMU wrapper instance providing access to model_description,
        fmu, and other FMPy objects for advanced usage
    time_event : ScheduleList or None
        dynamic time event for FMU-scheduled events
    """

    def __init__(self, fmu_path, instance_name="fmu_instance", start_values=None,
                 tolerance=1e-10, verbose=False):

        raise NotImplementedError


    def _get_derivatives(self, x, u, t):
        """Evaluate FMU derivatives (RHS of ODE)."""
        pass


    def _get_jacobian(self, x, u, t):
        """Evaluate Jacobian of FMU derivatives w.r.t. states (∂ẋ/∂x)."""
        pass


    def _get_outputs(self, x, u, t):
        """Evaluate FMU outputs (algebraic part)."""
        pass


    def _get_event_indicator(self, idx):
        """Get value of a specific event indicator."""
        pass


    def _handle_event(self, t):
        """Handle FMU event with fixed-point iteration for discrete states."""
        pass


    def _update_time_events(self, next_time):
        """Update or create time event schedule."""
        pass


    def sample(self, t, dt):
        """Sample block after successful timestep and handle FMU step completion events."""
        pass


    def reset(self):
        """Reset the FMU instance."""
        pass