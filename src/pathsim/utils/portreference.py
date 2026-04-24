#########################################################################################
##
##                                PORT REFERENCE CLASS 
##                              (utils/portreference.py)
##                              
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np


# CLASS =================================================================================

class PortReference:
    """Container class that holds a reference to a block and a list of ports.
    Optimized with cached integer indices for ultra-fast transfers.

    Note
    ----
    The default port, when no ports are defined in the arguments is `0`.

    Parameters
    ----------
    block : Block
        internal block reference
    ports : list[int, str]
        list of port indices or names
    """

    __slots__ = ["block", "ports", "_input_indices", "_output_indices"]

    def __init__(self, block=None, ports=None):

        # Default port is '0'
        raise NotImplementedError


    def __len__(self):
        """The number of ports managed by 'PortReference'"""
        raise NotImplementedError


    def _get_input_indices(self):
        """Get cached input indices, resolving string aliases to integers.
        Also expands the input array if needed.
        """
        pass


    def _get_output_indices(self):
        """Get cached output indices, resolving string aliases to integers.
        Also expands the output array if needed.
        """
        pass


    def _validate_input_ports(self):
        """Check the existence of the input ports, specifically string port 
        aliases for the block inputs. Raises a ValueError if not existent.
        """
        pass


    def _validate_output_ports(self):
        """Check the existence of the output ports, specifically string port 
        aliases for the block outputs. Raises a ValueError if not existent.
        """
        pass


    def to(self, other):
        """Transfer the data between two `PortReference` instances, 
        in this direction `self` -> `other`. From outputs to inputs.
        
        Uses numpy fancy indexing with cached integer indices.

        Parameters
        ----------
        other : PortReference
            the `PortReference` instance to transfer data to from `self`
        """
        pass


    def get_inputs(self):
        """Return the input values of the block at specified ports

        Returns
        -------
        out : numpy.ndarray
            input values of block
        """
        pass


    def set_inputs(self, vals):
        """Set the block inputs with values at specified ports

        Parameters
        ----------
        vals : array-like
            values to set at block input ports
        """
        pass


    def get_outputs(self):
        """Return the output values of the block at specified ports

        Returns
        -------
        out : numpy.ndarray
            output values of block
        """
        pass


    def set_outputs(self, vals):
        """Set the block outputs with values at specified ports

        Parameters
        ----------
        vals : array-like
            values to set at block output ports
        """
        pass

        
    def to_dict(self):
        """Serialization into dict"""
        pass
