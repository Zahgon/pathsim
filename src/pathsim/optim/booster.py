########################################################################################
##
##                               ConnectionBooster CLASS 
##                                  (optim/booster.py)
##
##       class to boost connections, injecting a fixed point acelerator for loop 
##             closing connections to simplify the algebraic loop solver
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from .anderson import Anderson


# CLASS =================================================================================

class ConnectionBooster:
    """Wraps a `Connection` instance and injects a fixed point accelerator. 

    This class is part of the solver structure and intended to improve the 
    algebraic loop solver of the simulation.

    Parameters
    ----------
    connection : Connection
        connection instance to be boosted with an algebraic loop accelerator

    Attributes
    ----------
    accelerator : Anderson
        internal fixed point accelerator instance
    history : float | int | array_like
        history, previous evaliation of the connection value
    """

    def __init__(self, connection):
        raise NotImplementedError


    def __bool__(self):
        raise NotImplementedError


    def get(self):
        """Return the output values of the source block that is referenced in 
        the connection.

        Return 
        ------
        out : float | int | array_like
            output values of source, referenced in connection
        """
        pass


    def set(self, val): 
        """Set targets input values.

        Parameters
        ----------
        val : float | int | array_like
            input values to set at inputs of the targets, referenced by the 
            connection

        """
        pass


    def reset(self):
        """Reset the internal fixed point accelerator and update the history 
        to the most recent value
        """
        pass


    def update(self):
        """Wraps the `Connection.update` method for data transfer from source 
        to targets and injects a solver step of the fixed point accelerator, 
        updates the history required for the next solver step, returns the 
        fixed point residual.

        Returns
        -------
        res : float
            fixed point residual of internal lixed point accelerator
        """
        pass