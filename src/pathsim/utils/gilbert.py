########################################################################################
##
##                       METHODS FOR STATESPACE REALIZATIONS
##                                (utils/gilbert.py)
##
##                                Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np


# STATESPACE REALIZATION ===============================================================

def gilbert_realization(Poles=[], Residues=[], Const=0.0, tolerance=1e-9): 
    """Build real valued statespace model from transfer function 
    in pole residue form by Gilbert's method and an additional
    similarity transformation to get fully real valued matrices.

    pole residue form:

    .. math::

        \\mathbf{H}(s) = \\mathbf{D} + \\sum_{n=1}^N \\frac{\\mathbf{R}_n}{s - p_n}
    
    statespace form:
        
    .. math::

        \\mathbf{H}(s) = \\mathbf{C} (s \\mathbf{I} - \\mathbf{A})^{-1} \\mathbf{B} + \\mathbf{D} 
    
    Notes
    -----  
    The resulting system is identical to the so-called 
    'Modal Form' and is a minimal realization.

    Parameters
    ---------- 
    Poles : array
        real and complex poles
    Residues : array
        array of real and complex residue matrices
    Const : array
        matrix for constant term
    tolerance : float
        relative tolerance for checking real poles
    
    Returns 
    -------
    A : array
        state matrix
    B : array 
        input mapping matrix
    C : array
        state to output projection matrix
    D : array, float
        direct passthrough

    Note
    ----
    If some poles are complex-valued, their conjugate-values are automatically
    added if missing, to enforce the model realness and stability.

    """
    pass
