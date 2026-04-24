#########################################################################################
##
##                               FILTERS (filters.py)
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from scipy.signal import butter, tf2ss

from math import factorial

from .lti import StateSpace
from ..utils.register import Register
from ..utils.mutable import mutable


# FILTER BLOCKS =========================================================================

@mutable
class ButterworthLowpassFilter(StateSpace):
    """Direct implementation of a low pass butterworth filter block.

    Follows the same structure as the 'StateSpace' block in the 
    'pathsim.blocks' module. The numerator and denominator of the 
    filter transfer function are generated and then the transfer 
    function is realized as a state space model. 
    
    Parameters
    ----------
    Fc : float
        corner frequency of the filter in [Hz]
    n : int
        filter order
    """

    input_port_labels = {"in":0}
    output_port_labels = {"out":0}

    def __init__(self, Fc=100, n=2):

        #filter parameters
        raise NotImplementedError


@mutable
class ButterworthHighpassFilter(StateSpace):
    """Direct implementation of a high pass butterworth filter block.

    Follows the same structure as the 'StateSpace' block in the 
    'pathsim.blocks' module. The numerator and denominator of the 
    filter transfer function are generated and then the transfer 
    function is realized as a state space model. 
    
    Parameters
    ----------
    Fc : float
        corner frequency of the filter in [Hz]
    n : int
        filter order
    """
    input_port_labels = {"in":0}
    output_port_labels = {"out":0}

    def __init__(self, Fc=100, n=2):

        #filter parameters
        raise NotImplementedError


@mutable
class ButterworthBandpassFilter(StateSpace):
    """Direct implementation of a bandpass butterworth filter block.

    Follows the same structure as the 'StateSpace' block in the 
    'pathsim.blocks' module. The numerator and denominator of the 
    filter transfer function are generated and then the transfer 
    function is realized as a state space model. 
    
    Parameters
    ----------
    Fc : list[float]
        corner frequencies (left, right) of the filter in [Hz]
    n : int
        filter order
    """
    input_port_labels = {"in":0}
    output_port_labels = {"out":0}

    def __init__(self, Fc=[50, 100], n=2):

        #filter parameters
        raise NotImplementedError


@mutable
class ButterworthBandstopFilter(StateSpace):
    """Direct implementation of a bandstop butterworth filter block.

    Follows the same structure as the 'StateSpace' block in the 
    'pathsim.blocks' module. The numerator and denominator of the 
    filter transfer function are generated and then the transfer 
    function is realized as a state space model. 
    
    Parameters
    ----------
    Fc : tuple[float], list[float]
        corner frequencies (left, right) of the filter in [Hz]
    n : int
        filter order
    """
    input_port_labels = {"in":0}
    output_port_labels = {"out":0}

    def __init__(self, Fc=[50, 100], n=2):

        #filter parameters
        raise NotImplementedError


@mutable
class AllpassFilter(StateSpace):
    """Direct implementation of a first order allpass filter, or a cascade 
    of n 1st order allpass filters
    
    .. math:: 

        H(s) = \\frac{s - 2\\pi f_s}{s + 2\\pi f_s}

    where f_s is the frequency, where the 1st order allpass has a 90 deg phase shift.
    
    Parameters
    ----------
    fs : float
        frequency for 90 deg phase shift of 1st order allpass
    n : int
        number of cascades
    """
    input_port_labels = {"in":0}
    output_port_labels = {"out":0}

    def __init__(self, fs=100, n=1):

        #filter parameters
        raise NotImplementedError
