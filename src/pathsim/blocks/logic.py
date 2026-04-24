#########################################################################################
##
##                            COMPARISON AND LOGIC BLOCKS
##                                 (blocks/logic.py)
##
##              definitions of comparison and boolean logic blocks
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from ._block import Block

from ..optim.operator import Operator


# BASE LOGIC BLOCK ======================================================================

class Logic(Block):
    """Base logic block.

    Note
    ----
    This block doesnt implement any functionality itself.
    Its intended to be used as a base for the comparison and logic blocks.
    Its **not** intended to be used directly!

    """

    def __len__(self):
        """Purely algebraic block"""
        return 1


    def update(self, t):
        """update algebraic component of system equation

        Parameters
        ----------
        t : float
            evaluation time
        """
        pass


# COMPARISON BLOCKS =====================================================================

class GreaterThan(Logic):
    """Greater-than comparison block.

    Compares two inputs and outputs 1.0 if a > b, else 0.0.

    .. math::

        y =
        \\begin{cases}
        1 & , a > b \\\\
        0 & , a \\leq b
        \\end{cases}

    Attributes
    ----------
    op_alg : Operator
        internal algebraic operator
    """

    input_port_labels = {"a":0, "b":1}
    output_port_labels = {"y":0}

    def __init__(self):
        raise NotImplementedError


class LessThan(Logic):
    """Less-than comparison block.

    Compares two inputs and outputs 1.0 if a < b, else 0.0.

    .. math::

        y =
        \\begin{cases}
        1 & , a < b \\\\
        0 & , a \\geq b
        \\end{cases}

    Attributes
    ----------
    op_alg : Operator
        internal algebraic operator
    """

    input_port_labels = {"a":0, "b":1}
    output_port_labels = {"y":0}

    def __init__(self):
        raise NotImplementedError


class Equal(Logic):
    """Equality comparison block.

    Compares two inputs and outputs 1.0 if |a - b| <= tolerance, else 0.0.

    .. math::

        y =
        \\begin{cases}
        1 & , |a - b| \\leq \\epsilon \\\\
        0 & , |a - b| > \\epsilon
        \\end{cases}

    Parameters
    ----------
    tolerance : float
        comparison tolerance for floating point equality

    Attributes
    ----------
    op_alg : Operator
        internal algebraic operator
    """

    input_port_labels = {"a":0, "b":1}
    output_port_labels = {"y":0}

    def __init__(self, tolerance=1e-12):
        raise NotImplementedError


# BOOLEAN LOGIC BLOCKS ==================================================================

class LogicAnd(Logic):
    """Logical AND block.

    Outputs 1.0 if both inputs are nonzero, else 0.0.

    .. math::

        y = a \\land b

    Attributes
    ----------
    op_alg : Operator
        internal algebraic operator
    """

    input_port_labels = {"a":0, "b":1}
    output_port_labels = {"y":0}

    def __init__(self):
        raise NotImplementedError


class LogicOr(Logic):
    """Logical OR block.

    Outputs 1.0 if either input is nonzero, else 0.0.

    .. math::

        y = a \\lor b

    Attributes
    ----------
    op_alg : Operator
        internal algebraic operator
    """

    input_port_labels = {"a":0, "b":1}
    output_port_labels = {"y":0}

    def __init__(self):
        raise NotImplementedError


class LogicNot(Logic):
    """Logical NOT block.

    Outputs 1.0 if input is zero, else 0.0.

    .. math::

        y = \\lnot x

    Attributes
    ----------
    op_alg : Operator
        internal algebraic operator
    """

    def __init__(self):
        raise NotImplementedError
