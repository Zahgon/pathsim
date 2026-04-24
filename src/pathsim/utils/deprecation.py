#########################################################################################
##
##                              DEPRECATION UTILITIES
##                              (utils/deprecation.py)
##
##           Decorator and utilities for marking deprecated functions and classes
##
#########################################################################################

# IMPORTS ===============================================================================

import warnings
import functools


# DEPRECATION DECORATOR =================================================================

def deprecated(version=None, replacement=None, reason=None):
    """Decorator to mark functions, methods, or classes as deprecated.

    Emits a DeprecationWarning when the decorated item is called/instantiated
    and adds RST-formatted deprecation notice to the docstring.

    Parameters
    ----------
    version : str | None
        Version when the item will be removed (e.g., "1.0.0")
    replacement : str | None
        Name of the replacement to use instead (e.g., "new_function")
    reason : str | None
        Additional explanation for the deprecation

    Returns
    -------
    decorator : callable
        Decorator function

    Example
    -------
    .. code-block:: python

        @deprecated(version="1.0.0", replacement="new_function")
        def old_function():
            pass

        @deprecated(version="2.0.0", reason="No longer needed")
        class OldClass:
            pass
    """

    def decorator(obj):
        # Build warning message
        pass

    return decorator


def _prepend_deprecation_notice(docstring, notice):
    """Prepend deprecation notice to docstring.

    Parameters
    ----------
    docstring : str | None
        Original docstring
    notice : str
        RST-formatted deprecation notice

    Returns
    -------
    new_docstring : str
        Docstring with deprecation notice prepended
    """
    if docstring is None:
        return notice + "\n"

    # Find indentation from existing docstring
    lines = docstring.split('\n')
    indent = ""
    for line in lines[1:]:  # Skip first line
        stripped = line.lstrip()
        if stripped:
            indent = line[:len(line) - len(stripped)]
            break

    # Indent the notice to match docstring
    indented_notice = "\n".join(
        indent + line if line.strip() else line
        for line in notice.split('\n')
    )

    # Insert after first line (summary) with blank line
    if len(lines) > 1:
        return lines[0] + "\n\n" + indented_notice + "\n" + "\n".join(lines[1:])
    else:
        return docstring + "\n\n" + indented_notice
