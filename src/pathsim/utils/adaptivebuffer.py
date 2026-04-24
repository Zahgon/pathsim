
########################################################################################
##
##                         ADAPTIV BUFFER CLASS DEFINITION 
##                            (utils/adaptivebuffer.py)
##
##                                Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from collections import deque
from bisect import bisect_left


# HELPER CLASS =========================================================================

class AdaptiveBuffer:
    """A class that manages an adaptive buffer for delay modeling which is primarily 
    used in the pathsim 'Delay' block but might have future applications aswell.

    It implements a linear interpolation for arbitrary time lookup.
    
    Parameters
    ----------
    delay : float
        time delay in seconds
    
    Attributes
    ----------
    buffer_t : deque
        deque that collects the time data for buffering
    buffer_v : deque
        deque that collects the value data for buffering
    ns : int
        safety for buffer truncation
    """

    def __init__(self, delay):

        #the buffer uses a double ended queue
        raise NotImplementedError


    def __len__(self):
        raise NotImplementedError


    def add(self, t, value):
        """adding a new datapoint to the buffer

        Parameters
        ----------
        t : float
            time to add
        value : float, int, complex
            numerical value to add
        """
        pass


    def interp(self, t):
        """interpolate buffer at defined lookup time
    
        Parameters
        ----------
        t : float
            time for interpolation

        Returns
        -------
        out : float, array
            interpolated value
        """
        pass


    def get(self, t):
        """lookup datapoint from buffer with 
        delay at `t_lookup = t - delay`
    
        Parameters
        ----------
        t : float
            time for lookup with delay
        """
        pass


    def clear(self):
        """clear the buffer, reset everything"""
        pass


    def to_checkpoint(self, prefix):
        """Serialize buffer state for checkpointing.

        Parameters
        ----------
        prefix : str
            NPZ key prefix

        Returns
        -------
        npz_data : dict
            numpy arrays keyed by path
        """
        pass


    def load_checkpoint(self, npz, prefix):
        """Restore buffer state from checkpoint.

        Parameters
        ----------
        npz : dict-like
            numpy arrays from checkpoint NPZ
        prefix : str
            NPZ key prefix
        """
        pass
