"""

`seqLogo` is Python port of the Bioconductor package `seqLogo`_.

The purpose of `seqLogo` is to process both Position Frequency Matrices (PFM)
and Position Weight Matrices (PWM) and produce `WebLogo`_-like motif plots


Note:
    Additional support for extended alphabets have been added.

The main class of `seqLogo` is:

#. ``seqLogo.Pwm``: the main PWM handler

However, additional helpful methods are exposed:

#. ``seqLogo.pfm2pwm``: automatically converts a PFM to a PWM
#. ``seqLogo.seqLogo``: the main method for plotting WebLogo-like motif plots

.. _seqLogo:
    http://bioconductor.org/packages/release/bioc/html/seqLogo.html
.. _WebLogo:
    http://weblogo.threeplusone.com/

This code is part of the seqLogo distribution and governed by its
license.  Please see the LICENSE file that should have been included
as part of this package.

"""
from seqlogo.core import *
from seqlogo.seqlogo import *
