"""
This directory corresponds to the standard electronic interfaces that should be shared across multiple solvers.

The aim is to provide a standard translation interface between SPICE solvers and our own solvers.
Note: the API definitions in this section correspond to electronic frequencies (ie sub terahertz and that
can be represented by standard electronic circuit elements (including RF lumped elements).

In order to have the option to eventually break off the packages into more maintainable subpackages, all the relevant
types will be contained within this sublevel __init__.py. However, this is not possible due to how coupled our software structure currently is.
"""
