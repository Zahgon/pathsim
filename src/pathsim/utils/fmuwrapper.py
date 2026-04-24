#########################################################################################
##
##                   FMU WRAPPER - VERSION AGNOSTIC FMI INTERFACE
##                            (pathsim/utils/fmuwrapper.py)
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np
import ctypes
from dataclasses import dataclass
from typing import Optional, Tuple

from .register import Register


# HELPER CLASSES ========================================================================

@dataclass
class EventInfo:
    """Unified event information structure for both FMI 2.0 and 3.0.

    Attributes
    ----------
    discrete_states_need_update : bool
        whether discrete state iteration is needed
    terminate_simulation : bool
        whether FMU requests simulation termination
    nominals_changed : bool
        whether nominal values of continuous states changed
    values_changed : bool
        whether continuous state values changed
    next_event_time_defined : bool
        whether FMU has scheduled a next time event
    next_event_time : float
        time of next scheduled event (if defined)
    """
    discrete_states_need_update: bool = False
    terminate_simulation: bool = False
    nominals_changed: bool = False
    values_changed: bool = False
    next_event_time_defined: bool = False
    next_event_time: float = 0.0


@dataclass
class StepResult:
    """Result information from a co-simulation step.

    Attributes
    ----------
    event_encountered : bool
        whether an event was encountered during step (FMI 3.0 only)
    terminate_simulation : bool
        whether FMU requests simulation termination (FMI 3.0 only)
    early_return : bool
        whether step returned early (FMI 3.0 only)
    last_successful_time : float
        last time successfully reached (FMI 3.0 only)
    """
    event_encountered: bool = False
    terminate_simulation: bool = False
    early_return: bool = False
    last_successful_time: float = 0.0


# FMI VERSION-SPECIFIC OPERATIONS =======================================================

class _FMI2Ops:
    """FMI 2.0 specific operations."""

    @staticmethod
    def set_real(fmu, refs, values):
        pass

    @staticmethod
    def get_real(fmu, refs):
        pass

    @staticmethod
    def set_integer(fmu, refs, values):
        pass

    @staticmethod
    def get_integer(fmu, refs):
        pass

    @staticmethod
    def do_step(fmu, current_time, step_size):
        pass

    @staticmethod
    def get_derivatives(fmu, n_states):
        pass

    @staticmethod
    def update_discrete_states(fmu):
        pass

    @staticmethod
    def setup_experiment(fmu, tolerance, start_time, stop_time):
        pass

    @staticmethod
    def enter_initialization_mode(fmu, tolerance, start_time, stop_time):
        pass

    @staticmethod
    def exit_initialization_mode(fmu, mode):
        pass


class _FMI3Ops:
    """FMI 3.0 specific operations."""

    @staticmethod
    def set_real(fmu, refs, values):
        pass

    @staticmethod
    def get_real(fmu, refs):
        pass

    @staticmethod
    def set_integer(fmu, refs, values):
        pass

    @staticmethod
    def get_integer(fmu, refs):
        pass

    @staticmethod
    def do_step(fmu, current_time, step_size):
        pass

    @staticmethod
    def get_derivatives(fmu, n_states):
        pass

    @staticmethod
    def update_discrete_states(fmu):
        pass

    @staticmethod
    def setup_experiment(fmu, tolerance, start_time, stop_time):
        # FMI 3.0 passes these to enterInitializationMode instead
        pass

    @staticmethod
    def enter_initialization_mode(fmu, tolerance, start_time, stop_time):
        pass

    @staticmethod
    def exit_initialization_mode(fmu, mode):
        pass


# MAIN WRAPPER CLASS ====================================================================

class FMUWrapper:
    """Version-agnostic wrapper for FMI 2.0 and 3.0 FMUs.

    This class provides a unified interface for working with FMUs regardless of
    FMI version (2.0 or 3.0) or interface type (Co-Simulation or Model Exchange).
    It handles all version-specific API differences internally.

    Parameters
    ----------
    fmu_path : str
        path to the FMU file (.fmu)
    instance_name : str, optional
        name for the FMU instance (default: 'fmu_instance')
    mode : str, optional
        FMU interface mode: 'cosimulation' or 'model_exchange' (default: 'cosimulation')

    Attributes
    ----------
    fmu_path : str
        path to the FMU file
    instance_name : str
        name of the FMU instance
    mode : str
        interface mode ('cosimulation' or 'model_exchange')
    model_description : ModelDescription
        FMI model description from FMPy (use this for metadata access)
    fmu : FMU2Slave | FMU3Slave | FMU2Model | FMU3Model
        underlying FMPy FMU instance
    fmi_version : str
        detected FMI version ('2.0' or '3.0')
    n_states : int
        number of continuous states (Model Exchange only)
    n_event_indicators : int
        number of event indicators (Model Exchange only)
    input_refs : dict
        mapping from input variable names to value references
    output_refs : dict
        mapping from output variable names to value references
    """

    def __init__(self, fmu_path, instance_name="fmu_instance", mode="cosimulation"):

        # Import FMPy (lazy import to avoid dependency if not used)
        raise NotImplementedError

    def _create_fmu_instance(self, FMU2Slave, FMU2Model, FMU3Slave, FMU3Model):
        """Create the appropriate FMU instance based on version and mode."""
        pass

    def _build_variable_maps(self):
        """Build internal variable name to reference mappings."""
        pass

    def _build_state_derivative_maps(self):
        """Build state and derivative value reference lists (Model Exchange only).

        In FMI, state variables have a 'derivative' attribute pointing to their
        derivative variable. This method extracts the ordered lists of value
        references needed for Jacobian computation via directional derivatives.
        """
        pass

    # ===================================================================================
    # CONVENIENCE METHODS FOR BLOCK INITIALIZATION
    # ===================================================================================

    def create_port_registers(self) -> Tuple[Register, Register]:
        """Create input and output registers for block I/O.

        Returns
        -------
        inputs : Register
            input register with FMU input variable names as labels
        outputs : Register
            output register with FMU output variable names as labels
        """
        pass

    def initialize(self, start_values=None, start_time=0.0, stop_time=None,
                   tolerance=None) -> Optional[EventInfo]:
        """Complete FMU initialization sequence.

        Performs: instantiate -> setup_experiment -> enter_initialization_mode
        -> set start values -> exit_initialization_mode

        Parameters
        ----------
        start_values : dict, optional
            dictionary of variable names and their initial values
        start_time : float, optional
            simulation start time (default: 0.0)
        stop_time : float, optional
            simulation stop time
        tolerance : float, optional
            tolerance for integration/event detection

        Returns
        -------
        event_info : EventInfo or None
            event information for FMI 3.0 Model Exchange, None otherwise
        """
        pass

    @property
    def default_step_size(self) -> Optional[float]:
        """Get default step size from FMU's default experiment, if defined."""
        pass

    @property
    def default_tolerance(self) -> Optional[float]:
        """Get default tolerance from FMU's default experiment, if defined."""
        pass

    @property
    def needs_completed_integrator_step(self) -> bool:
        """Check if FMU requires completedIntegratorStep notifications (Model Exchange only)."""
        pass

    @property
    def provides_jacobian(self) -> bool:
        """Check if FMU provides directional derivatives for Jacobian computation."""
        pass

    def get_state_jacobian(self):
        """Compute Jacobian of state derivatives w.r.t. states (Model Exchange only).

        Uses FMU's directional derivative capability to compute ∂ẋ/∂x.
        Requires the FMU to have providesDirectionalDerivative=true.

        Returns
        -------
        jacobian : np.ndarray
            n_states x n_states Jacobian matrix, or None if not supported
        """
        pass

    # ===================================================================================
    # FMU LIFECYCLE METHODS
    # ===================================================================================

    def instantiate(self, visible=False, logging_on=False):
        """Instantiate the FMU."""
        pass

    def setup_experiment(self, tolerance=None, start_time=0.0, stop_time=None):
        """Setup experiment parameters."""
        pass

    def enter_initialization_mode(self):
        """Enter initialization mode."""
        pass

    def exit_initialization_mode(self) -> Optional[EventInfo]:
        """Exit initialization mode and return event information."""
        pass

    def reset(self):
        """Reset FMU to initial state."""
        pass

    def terminate(self):
        """Terminate FMU."""
        pass

    def free_instance(self):
        """Free FMU instance and resources."""
        pass

    # ===================================================================================
    # VARIABLE ACCESS METHODS
    # ===================================================================================

    def set_real(self, refs, values):
        """Set real-valued variables by reference."""
        pass

    def get_real(self, refs):
        """Get real-valued variables by reference."""
        pass

    def set_variable(self, name, value):
        """Set a single variable by name (automatically detects type)."""
        pass

    def set_inputs_from_array(self, values):
        """Set all FMU inputs from an array."""
        pass

    def get_outputs_as_array(self):
        """Get all FMU outputs as an array."""
        pass

    # ===================================================================================
    # CO-SIMULATION METHODS
    # ===================================================================================

    def do_step(self, current_time, step_size) -> StepResult:
        """Perform a co-simulation step."""
        pass

    # ===================================================================================
    # MODEL EXCHANGE METHODS
    # ===================================================================================

    def set_time(self, time):
        """Set current time (Model Exchange only)."""
        pass

    def set_continuous_states(self, states):
        """Set continuous states (Model Exchange only)."""
        pass

    def get_continuous_states(self):
        """Get continuous states (Model Exchange only)."""
        pass

    def get_derivatives(self):
        """Get state derivatives (Model Exchange only)."""
        pass

    def get_event_indicators(self):
        """Get event indicators (Model Exchange only)."""
        pass

    def enter_event_mode(self):
        """Enter event mode (Model Exchange only)."""
        pass

    def enter_continuous_time_mode(self):
        """Enter continuous time mode (Model Exchange only)."""
        pass

    def update_discrete_states(self) -> EventInfo:
        """Update discrete states during event iteration (Model Exchange only)."""
        pass

    def completed_integrator_step(self) -> Tuple[bool, bool]:
        """Notify FMU that integrator step completed (Model Exchange only).

        Returns
        -------
        enter_event_mode : bool
            whether FMU requests event mode
        terminate_simulation : bool
            whether FMU requests simulation termination
        """
        pass

    def __del__(self):
        """Cleanup FMU resources on deletion."""
        raise NotImplementedError
