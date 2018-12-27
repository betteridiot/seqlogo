"""
Copyright (c) 2018, Marcus D. Sherman

This code is part of the seqlogo distribution and governed by its
license.  Please see the LICENSE file that should have been included
as part of this package.

@author: "Marcus D. Sherman"
@copyright: "Copyright 2018, University of Michigan, Mills Lab
@email: "mdsherman<at>betteridiot<dot>tech"

"""
import os
import numpy as np
import pandas as pd
from functools import partial
from seqlogo import utils


def _init_pm(pm_matrix, pm_type = 'pwm', alphabet = 'DNA'):
    """Checks for the file (if filename is supplied) and reads it in if present.
    Otherwise it just ensures that the position matrix (PM) dimensions match the
    expected alphabet.

    Args:
        pm_matrix (str or `numpy.ndarray` or `pandas.DataFrame`): The user supplied
                        PM. If it is a filename, the file will be opened
                        and parsed. If it is an `numpy.ndarray` or `pandas.DataFrame`,
                        it will just be assigned. (default: None))
        pm_type (str): whether the PM is a PWM or PFM (default: 'pwm')
        alphabet (str): Desired alphabet to use. Order matters (default: 'DNA')
                "DNA" := "ACGT"
                "reduced DNA" := "ACGTN-"
                "ambig DNA" := "ACGTRYSWKMBDHVN-"
                "RNA" := "ACGU"
                "reduced RNA" := "ACGUN-"
                "ambig RNA" := "ACGURYSWKMBDHVN-"
                "AA" : = "ACDEFGHIKLMNPQRSTVWY"
                "reduced AA" := "ACDEFGHIKLMNPQRSTVWYX*-"
                "ambig AA" := "ACDEFGHIKLMNOPQRSTUVWYBJZX*-"
                (default: "DNA")

    Returns:
        pm (`seqlogo.Pwm`): a properly formatted PWM instance object

    Raises:
        FileNotFoundError if `pfm_filename_or_array` is a string, but not a file
        ValueError if desired alphabet is not supported
        ValueError if the PM is not well formed
        ValueError if the probabilities do not add up to 1
        TypeError if `pfm_filename_or_array` is not a file or array-like structure
    """
    if type(pm_matrix) == str:
        if not os.path.isfile(pm_matrix):
            raise FileNotFoundError('{} was not found'.format(pm_matrix))
        if alphabet not in utils._IDX_LETTERS:
            raise ValueError('alphabet must be a version of DNA, RNA, or AA')

        pm = pd.read_table(pm_matrix, delim_whitespace = True, header = None, comment = '#')

    elif isinstance(pm_matrix, np.ndarray):
        pm = pd.DataFrame(data = pm_matrix)
    elif isinstance(pm_matrix, pd.DataFrame):
        pm = pm_matrix
    elif isinstance(pm_matrix, Pwm):
        return pm_matrix
    else:
        raise TypeError('pfm_filename_or_array` must be a filename, `np.ndarray`, `pd.DataFrame`, or `Pwm`')

    ex_alph_len = len(utils._IDX_LETTERS[alphabet])

    if not pm.shape[1] == ex_alph_len and alphabet in utils.NA_ALPHABETS:
        if pm.shape[0] == ex_alph_len:
            pwm = pwm.transpose()
        else:
            raise ValueError('{} alphabet selected, but PM is not {} rows'.format(alphabet, ex_alph_len))
    if not pm.shape[1] == ex_alph_len and alphabet in utils.AA_ALPHABETS:
        if pm.shape[0] == ex_alph_len:
            pm = pwm.transpose()
        else:
            raise ValueError('{} alphabet selected, but PM is not {} rows'.format(alphabet, ex_alph_len))

    pm.columns = list(utils._IDX_LETTERS[alphabet])

    if pm_type == 'pwm':
        if not pm.sum(axis = 1).between(1, 1 + 1e-7).all():
            raise ValueError('All or some PWM columns do not add to 1')

    return pm


def pfm2pwm(pfm_filename_or_array, alphabet = "DNA"):
    """Convert a Position Frequency Matrix (PFM) to a PWM

    Args:
        pfm_filename_or_array (str or `numpy.ndarray` or `pandas.DataFrame`): The user supplied
                        PFM. If it is a filename, the file will be opened
                        and parsed. If it is an `numpy.ndarray` or `pandas.DataFrame`,
                        it will just be assigned. (default: None))
        alphabet (str): Desired unambiguous alphabet to use (DNA, RNA, or AA) (default: "DNA")

    Returns:
        (`Pwm`): instance of the Pwm object based on PFM supplied by user.
    """
    pfm = _init_pm(pfm_filename_or_array, pm_type = 'pfm', alphabet = alphabet)
    pwm = Pwm(pfm.divide(pfm.sum(axis='columns'), axis='index'), counts = pfm.values, alphabet = alphabet)
    return pwm


@partial(np.vectorize, otypes = [np.float64])
def __proportion(prob):
    """Vectorized proportion formula that feeds into _row_wise_ic

    Args:
        prob (`np.float64`): probability for a given letter at given position

    returns (`np.float64`): normalized probability
    """
    if prob > 0:
        return prob * np.log2(prob)
    else:
        return 0


def _row_wise_ic(row):
    """Get the information content for each row across all letters

    Args:
        row (`pandas.Series`): row from the PWM

    Returns:
        The information content for the row
    """
    return 2 + np.sum(__proportion(row), axis = 1)


class Pwm:
    """Main class for handling Position Weight Matrices (PWM).

    A PWM differs from a Position Frequency Matrix in that instead of counts for
    a given letter, the normalized weight is already calculated.

    This class automatically generates the consensus sequence for a given `alphabet` and PWM. It also calculates the Information Content (IC) for each position.

    Attributes:
        pwm (`pandas.DataFrame`): PWM DataFrame generated by user-submitted PWM
        consensus (str): The consensus sequence determined by the PWM
        ic (`numpy.ndarray`): The information content for each position
        entropy ('`numpy.ndarray'): an alias for `ic`
        width (int): Length of the sequence/motif
        length (int): an alias for `width`
        alphabet (str): Desired alphabet to use. Order matters (default: 'DNA')
        weight (`numpy.array`): 1-D array of ones. Used for WebLogo comparability
        counts (`pandas.DataFrame`): Counts of letters at the given position. If
                `counts` is not supplied (because PWM was the entry-point), a
                *pseudo-count* is produced by casting the PWM * 100 as an integer array.
    """

    __slots__ = ['_pwm', '_consensus', '_ic', '_width', '_alphabet',
                '_counts', '_weight']
    __all__ = ['pwm', 'consensus', 'ic', 'width', 'alphabet', 'counts', 
            'entropy', 'length', 'weight']

    def __init__(self, pwm_filename_or_array = None, counts = None, alphabet = "DNA"):
        """Initializes the Pwm

        Creates the Pwm instance. If the user does not define `pwm_filename_or_array`,
        it will be initialized to empty. Will generate all other attributes as soon
        as a `pwm_filename_or_array` is supplied.

        Args:
            pwm_filename_or_array (str or `numpy.ndarray` or `pandas.DataFrame`): The user supplied
                PWM. If it is a filename, the file will be opened
                and parsed. If it is an `numpy.ndarray` or `pandas.DataFrame`,
                it will just be assigned. (default: None)
            counts (`numpy.ndarray` or `pandas.DataFrame` or `Pwm`): count data for each letter
                at a given position. (default: None)
            alphabet (str): Desired alphabet to use. Order matters (default: 'DNA')
                "DNA" := "ACGT"
                "reduced DNA" := "ACGTN-"
                "ambig DNA" := "ACGTRYSWKMBDHVN-"
                "RNA" := "ACGU"
                "reduced RNA" := "ACGUN-"
                "ambig RNA" := "ACGURYSWKMBDHVN-"
                "AA" : = "ACDEFGHIKLMNPQRSTVWY"
                "reduced AA" := "ACDEFGHIKLMNPQRSTVWYX*-"
                "ambig AA" := "ACDEFGHIKLMNOPQRSTUVWYBJZX*-"
                (default: "DNA")

        """
        self._pwm = self._consensus = self._ic = self._weight = None
        self._width = self._counts = self._alphabet = None
        if counts is not None:
            self.counts = counts

        if pwm_filename_or_array is not None:
            self._update_pwm(pwm_filename_or_array, alphabet)

    def _update_pwm(self, pwm, alphabet):
        """Ensures correct consensus, IC, width, and alphabet accompany the supplied
        PWM.

        This function is called any time the user initializes or updates the PWM.
        All other attributes are 'read-only'.

        Args:
            pwm (str or `numpy.ndarray` or `pandas.DataFrame`): The user supplied
                PWM. If it is a filename, the file will be opened
                and parsed. If it is an `numpy.ndarray` or `pandas.DataFrame`,
                it will just be assigned. (default: None))
            alphabet (str): Desired unambiguous alphabet to use (DNA, RNA, or AA)
        """
        if alphabet is None:
            alphabet = self.alphabet
        self._pwm = _init_pm(pwm, alphabet)
        self._consensus = self._generate_consensus(self.pwm)
        self._ic = self._generate_ic(self.pwm)
        self._width = pwm.shape[0]
        self._alphabet = alphabet
        self._weight = np.ones((self.width,), dtype=np.int8)

    @property
    def weight(self):
        return self._weight

    @property
    def entropy_interval(self):
        return None

    @property
    def length(self):
        return self.width

    @property
    def entropy(self):
        return self.ic

    @property
    def counts(self):
        if self._counts is None:
            self.counts = (self.pwm * 100).astype(np.int64).values
        return self._counts

    @counts.setter
    def counts(self, counts):
        self._counts = counts

    def __len__(self):
        return self.pwm.shape[0]

    def __str__(self):
        return self.pwm.__str__()

    def __repr__(self):
        return self.pwm.__str__()

    @classmethod
    def __dir__(cls):
        """Just used to clean up the attributes and methods shown when `dir()` is called"""
        return sorted(cls.__all__)

    @staticmethod
    def _generate_consensus(pwm):
        return ''.join(pwm.idxmax(axis=1))

    @staticmethod
    def _generate_ic(pwm):
        return _row_wise_ic(pwm)

    @staticmethod
    def _get_width(pwm):
        return pwm.shape[0]

    @staticmethod
    def _get_alphabet(alphabet):
        return utils._IDX_LETTERS[alphabet]

    @property
    def consensus(self):
        return self._consensus

    @property
    def ic(self):
        return self._ic

    @property
    def width(self):
        return self._width

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def entropy(self):
        return self.ic

    @property
    def length(self):
        return self.width

    @property
    def pwm(self):
        return self._pwm

    @pwm.setter
    def pwm(self, pwm_filename_or_array, alphabet = "DNA"):
        self._update_pwm(pwm_filename_or_array, alphabet = alphabet)