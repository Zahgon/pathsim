#########################################################################################
##
##                                   Register Class
##                            (pathsim/utils/register.py)
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np


# CLASSES ===============================================================================

class Register:
    """This class is a intended to be used for the inputs and outputs of blocks. 

    Its basic functionality is similar to a `dict` but with some additional methods 
    and implemented as a numpy array for fast data transfer. 
    
    The core functionality is that values can be added dynamically and the size of the 
    register doesnt have to be specified. It also implements some methods to interact 
    with numpy arrays and to streamline convergence checks.
    
    Parameters
    ----------
    size : int, optional
        initial size of the register 
    mapping : dict[str: int]
        string aliases for integer ports

    Attributes
    ----------
    _data : np.ndarray
        internal numpy array that holds the values
    _mapping : dict[str: int]
        internal mapping for port aliases from string to int (index)
    """
    
    __slots__ = ["_data", "_mapping"]
    
    def __init__(self, size=None, mapping=None, dtype=np.float64):
        raise NotImplementedError
    
    
    def _map(self, key):
        """Map string keys to integers defined in '_mapping'

        Parameters
        ----------
        key : int, str
            port key, to map to index

        Returns
        -------
        _key : int
            port index 
        """
        pass
    

    def _get_max_index(self, key):
        """Identify max index from different key types."""
        pass
    

    def __len__(self):
        raise NotImplementedError
    

    def __iter__(self):
        """Iteration and unpacking into tuples or lists"""
        raise NotImplementedError
    

    def __getitem__(self, key):
        """Get the value for direct access to the 
        register values.
        
        Parameters
        ----------
        key : int, str
            port key, where to get value from

        Returns
        -------
        out : float, obj
            value from port at `key` position
        """
        raise NotImplementedError
    

    def __setitem__(self, key, value):
        """Set the value at key index for direct access
        to the register values.

        Parameters
        ----------
        key : int, str
            port key, where to set value
        val : float, obj
            value to set at port
        """
        raise NotImplementedError


    def resize(self, size):
        """Resize the internal data array to accommodate more entries.

        Creates a new zero-filled array instead of in-place resize to avoid
        numpy ValueError when other references to the array exist (e.g., from
        fancy indexing in PortReference).

        Parameters
        ----------
        size : int
            new size for the internal data array
        """
        pass


    def reset(self):
        """Set all stored values to zero."""
        pass
    

    def to_array(self):
        """Returns a copy of the internal array.

        Returns
        -------
        arr : np.ndarray
            converted register as array
        """
        pass
    

    def update_from_array(self, arr):
        """Update the register values from an array in place.

        Parameters
        ----------
        arr : np.ndarray, list, tuple, float
            array or scalar that is used to update internal register values
        """
        pass

    
    def __contains__(self, key):
        """Check if a key is in mapping or is valid integer index."""
        raise NotImplementedError
