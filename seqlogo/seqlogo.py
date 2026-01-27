import numpy as np
import pandas as pd
import tempfile
import re
import warnings
import sys


def _get_weblogo_version():
    if sys.version_info >= (3,8):
        try:
            from importlib.metadata import version
            return version('weblogo')
        except ImportError:
            pass

    try:
        import pkg_resources
        return pkg_resources.get_distribution('weblogo').version
    except Exception:
        pass

    try:
        import weblogo
        if hasattr(weblogo, '__version__'):
            return weblogo.__version__
    except Exception:
        pass
    return "3.7.0"

weblogo_version = _get_weblogo_version()

try:
    if weblogo_version < "3.7":
        import weblogolib as wl
    else:
        import weblogo as wl
except (ModuleNotFoundError, ImportError):
    try:
        import weblogolib as wl
    except ImportError:
        raise ImportError("Neither 'weblogo' or 'weblogolib' could be imported.\nPlease install 'weblogo'")
    

from seqlogo import utils


_sizes = {
    'small': 3.54,
    'medium': 5,
    'large': 7.25,
    'xlarge': 10.25
}


def _check_pdf2svg_available():
    return shutil.which('pdf2svg') is not None


def seqlogo(pm, ic_scale = True, color_scheme = None, size = 'medium',
            format = 'png', filename = None, **kwargs):
    """The plotting method of the `seqlogo` distribution. Depends on using
    any of the 3 classes exposed by `seqlogo`:
        * `seqlogo.Ppm`
        * `seqlogo.Pwm`
        * `seqlogo.CompletePm`

    Given an `M x N` PM matrix, where `M` is the number of positions and `N`
    is the number of letters, calculate and render a WebLogo-like motif plot.

    When `ic_scale` is `True`, the height of each column is proportional to 
    its information content. The y-axis label and scale will reflect information
    content. Otherwise, all columns have the same height and y-axis label will
    reflect "bits"

    Args:
        pm (`seqlogo.Pm` subclass): a pre-formatted Pm instance
        ic_scale (bool): whether or not to scale the column heights (default: True)
        size (str): small (3.54 in), medium (5 in), large (7.25 in), xlarge (10.25) (default: 'medium')
        format (str): desired matplotlib supported output format Options are 'eps', 'pdf', 'png', 'jpeg', and 'svg' (default: "png")
        
        **Important**L
            - 'png' is the default and works in Jupyter Notebooks, RMarkdown (via reticulate), and all environments.
            - 'svg' requires pdf2svg to be install separately. If you want to use 'svg', you just install pdf2svg, and even then, it might not work on some operating systems.
                - Ubuntu/Debian : apt-get install pdf2svg
                - macOS: brew install pdf2svg
                - Windows: Download and install https://github.com/jalios/pdf2svg-windows

        filename (None | str): Name of the file to save the figure. If `None`:
            the figure will not be saved. (default: None)
        color_scheme (str): the color scheme to use for weblogo:
            'auto': None
            'monochrome': all black
            'base pairing': (NA Only) TAU are orange, GC are blue
            'classic': (NA Only) classic WebLogo color scheme for nucleic acids
            'hydrophobicity': (AA only) Color based on hydrophobicity
            'chemistry': (AA only) Color based on chemical properties
            'charge': (AA Only) Color based on charge
        **kwargs: all additional keyword arguments found at http://weblogo.threeplusone.com/manual.html 
    """
    if format == 'svg' and not _check_pdf2svg_available():
        raise RuntimeError("pdf2svg has not been found. Please install it as per the help() documentation for this function.")

    # Ensure color scheme matches the alphabet
    if pm._alphabet_type in utils._NA_ALPHABETS:
        if color_scheme is None:
            color_scheme = 'classic'
        if color_scheme not in utils.NA_COLORSCHEMES:
            raise ValueError('{} color_scheme selected is not an allowed nucleic acid color scheme'.format(color_scheme))
    elif pm._alphabet_type in utils._AA_ALPHABETS:
        if color_scheme is None:
            color_scheme = 'hydrophobicity'
        if color_scheme not in utils.AA_COLORSCHEMES:
            raise ValueError('{} color_scheme selected is not an allowed amino acid color scheme'.format(color_scheme))

    color_scheme = wl.std_color_schemes[color_scheme]

    # Setup the format writer
    out_format = wl.formatters[format]

    # Prepare the logo size
    stack_width = (_sizes[size]/pm.length) * 72

    # Initialize the options
    if ic_scale:
        unit_name = 'bits'
    else:
        unit_name = 'probability'
    options = wl.LogoOptions(unit_name = unit_name, color_scheme = color_scheme,
                            show_fineprint = False, stack_width = stack_width, **kwargs)

    #Initialize the output format
    logo_format = wl.LogoFormat(pm, options)

    out = out_format(pm, logo_format)

    # Create the file if the user supplied an filename
    if filename:
        with open('{}'.format(filename), 'wb') as out_file:
            out_file.write(out)
    
    if format == 'svg':
        svg_hash = hash(out)
        out = re.sub(rb'("#?glyph.*?)(")', rb'\1 %s\2' % str(svg_hash).encode(), out)

    try:
        if get_ipython():
            import IPython.display as ipd
            if format == 'svg':
                return ipd.SVG(out)
            elif format in ('png', 'jpeg', 'svg'):
                return ipd.Image(out)
            else:
                raise ValueError('{} format not supported for plotting in console'.format(format))
    except NameError:
        if filename is None:
            raise ValueError('If not in an IPython/Jupyter console and no filename is given, nothing will be rendered')
    
