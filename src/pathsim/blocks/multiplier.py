#########################################################################################
##
##                        REDUCTION BLOCKS (blocks/multiplier.py)
##
##                     This module defines static 'Multiplier' block
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from math import prod

from ._block import Block
from ..utils.register import Register
from ..optim.operator import Operator


# MISO BLOCKS ===========================================================================

class Multiplier(Block):
    """Multiplies all signals from all input ports (MISO).
      
    .. math::
        
        y(t) = \\prod_i u_i(t)

            
    Note
    ----
    This block is purely algebraic and its operation (`op_alg`) will be called 
    multiple times per timestep, each time when `Simulation._update(t)` is 
    called in the global simulation loop.


    Attributes
    ----------
    op_alg : Operator
        internal algebraic operator that wraps 'prod'
    """
    input_port_labels = None
    output_port_labels = {"out":0}

    def __init__(self):
        raise NotImplementedError


    def update(self, t):
        """update system equation

        Parameters
        ----------
        t : float
            evaluation time
        """
        pass