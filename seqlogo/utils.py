"""
Copyright (c) 2018, Marcus D. Sherman

This code is part of the seqlogo distribution and governed by its
license.  Please see the LICENSE file that should have been included
as part of this package.

@author: "Marcus D. Sherman"
@copyright: "Copyright 2018, University of Michigan, Mills Lab
@email: "mdsherman<at>betteridiot<dot>tech"

"""
from collections import OrderedDict
from copy import deepcopy
import numpy as np
import pandas as pd
import seqlogo as sl


_AA_LETTERS = "ACDEFGHIKLMNPQRSTVWY"
_REDUCED_AA_LETTERS = "ACDEFGHIKLMNPQRSTVWYX*-"
_AMBIG_AA_LETTERS = "ACDEFGHIKLMNOPQRSTUVWYBJZX*-"

_DNA_LETTERS = "ACGT"
_REDUCED_DNA_LETTERS = "ACGTN-"
_AMBIG_DNA_LETTERS = "ACGTRYSWKMBDHVN-"

_RNA_LETTERS = "ACGU"
_REDUCED_RNA_LETTERS = "ACGUN-"
_AMBIG_RNA_LETTERS = "ACGURYSWKMBDHVN-"

_IDX_LETTERS = {
    "DNA": _DNA_LETTERS, "reduced DNA": _REDUCED_DNA_LETTERS, "ambig DNA": _AMBIG_DNA_LETTERS,
    "RNA": _RNA_LETTERS, "reduced RNA": _REDUCED_RNA_LETTERS, "ambig RNA": _AMBIG_RNA_LETTERS,
    "AA":_AA_LETTERS, "reduced AA": _REDUCED_AA_LETTERS, "ambig AA": _AMBIG_AA_LETTERS
}

_NA_ALPHABETS = set((
    "DNA", "reduced DNA", "ambig DNA"
    "RNA", "reduced RNA", "ambig RNA"
))


_AA_ALPHABETS = set((
    "AA", "reduced AA", "ambig AA"
))

# Using Robinson-Robinson Frequencies --> Order matters
_AA_background = OrderedDict((
    ('A', 0.087135727479), ('C', 0.033468612677), ('D', 0.046870296325), ('E', 0.049525516559),
    ('F', 0.039767240243), ('G', 0.088606655336), ('H', 0.033621241997), ('I', 0.036899088289), 
    ('K', 0.080483022246), ('L', 0.085361634465), ('M', 0.014743987313), ('N', 0.040418278548), 
    ('P', 0.050677889818), ('Q', 0.038269289735), ('R', 0.040894944605), ('S', 0.069597088795),
    ('T', 0.058530491824), ('V', 0.064717068767), ('W', 0.010489421950), ('Y', 0.029922503029)
    ))


_NA_background = {nt: 0.25 for nt in 'ACGT'}


_conv_alph_len = {
    'reduced AA': (len(_REDUCED_AA_LETTERS) - 3, len(_REDUCED_AA_LETTERS) - 3),
    'ambig AA': (len(_AMBIG_AA_LETTERS) - 6, len(_AMBIG_AA_LETTERS) - 3),
    'reduced DNA': (len(_REDUCED_DNA_LETTERS) - 2, len(_REDUCED_DNA_LETTERS) - 2),
    'ambig DNA': (len(_AMBIG_DNA_LETTERS) - 12,len(_AMBIG_DNA_LETTERS) - 2),
    'reduced RNA': (len(_REDUCED_RNA_LETTERS) - 2, len(_REDUCED_RNA_LETTERS) - 2),
    'ambig RNA': (len(_AMBIG_RNA_LETTERS) - 12, len(_AMBIG_RNA_LETTERS) - 2)
}


def convert_pm(non_std_pm, pm_type = 'pfm', alphabet_type = 'reduced DNA', background = None, pseudocount = None):
    ambig_start, len_alph = _conv_alph_len[alphabet_type]

    # Convert all to pfm for easy weight calculations
    if pm_type == 'pwm':
        pm = sl.pwm2pfm(non_std_pm, background, pseudocount, alphabet_type)
    elif pm_type == 'ppm':
        pm = sl.ppm2pfm(non_std_pm, alphabet_type)
    else:
        pm = non_std_pm
    new_pm = pd.DataFrame(non_std_pm[:,:ambig_start].copy(), columns = list(_IDX_LETTERS[alphabet_type][:ambig_start]))
    if isinstance(pm, pd.DataFrame):
        weights = pm.iloc[:,:len_alph].sum(axis = 1) / pm.sum(axis = 1)
    elif isinstance(pm, np.ndarray):
        weights = pm[:,:len_alph].sum(axis = 1) / pm.sum(axis = 1)

    if 'ambig' in alphabet_type:
        pd_pm = pd.DataFrame(pm, columns = list(_IDX_LETTERS[alphabet_type]))
        # dealing with ambiguous sequences
        for letter in _IDX_LETTERS[alphabet_type][ambig_start:-1]: # Don't care about '-'
            ambig_pairs = _AMBIGUITIES[alphabet_type][letter]
            new_pm.loc[:,list(ambig_pairs)] += (pd_pm[letter]/len(ambig_pairs))[:, np.newaxis]
        if pm_type == 'ppm':
            new_pm = sl.pfm2ppm(new_pm, alphabet_type.split()[1])
        elif pm_type == 'pwm':
            new_pm = sl.pfm2pwm(new_pm, background, pseudocount, alphabet_type.split()[1])
        return new_pm.values, weights

    # Dealing with reduced sequences
    else:
        # equally distribute the 'N/X/*/-' counts
        new_pm += pm[:,len_alph:-1].sum(axis = 1)[:, np.newaxis] / new_pm.shape[1]

        # Return in same form as given
        if pm_type == 'pwm':
            new_pm = sl.pfm2pwm(new_pm, background, pseudocount, alphabet_type.split()[1])
        elif pm_type == 'ppm':
            new_pm = sl.pfm2ppm(new_pm, alphabet_type.split()[1])
        return new_pm, weights


NA_COLORSCHEMES = set((
    'monochrome', 'base pairing', 'classic'
))

AA_ALPHABETS = set((
    "AA", "reduced AA", "ambig AA"
))

AA_COLORSCHEMES = set((
    'monochrome', 'hydrophobicity', 'chemistry','charge'
))

dna_ambiguity = {
    "A": "A",
    "C": "C",
    "G": "G",
    "T": "T",
    "M": "AC",
    "R": "AG",
    "W": "AT",
    "S": "CG",
    "Y": "CT",
    "K": "GT",
    "V": "ACG",
    "H": "ACT",
    "D": "AGT",
    "B": "CGT",
    "N": 'ACGT'
}

rna_ambiguity = {
    "A": "A",
    "C": "C",
    "G": "G",
    "U": "U",
    "M": "AC",
    "R": "AG",
    "W": "AU",
    "S": "CG",
    "Y": "CU",
    "K": "GU",
    "V": "ACG",
    "H": "ACU",
    "D": "AGU",
    "B": "CGU",
    "N": 'ACGU'
}

amino_acid_ambiguity = {
    "A": "A",
    "B": "ND",
    "C": "C",
    "D": "D",
    "E": "E",
    "F": "F",
    "G": "G",
    "H": "H",
    "I": "I",
    "K": "K",
    "L": "L",
    "M": "M",
    "N": "N",
    "P": "P",
    "Q": "Q",
    "R": "R",
    "S": "S",
    "T": "T",
    "V": "V",
    "W": "W",
    "Y": "Y",
    "Z": "QE",
    "J": "IL",
    'U': 'U',
    'O': 'O',
    'X': "ACDEFGHIKLMNPQRSTVWY",
    '*': "ACDEFGHIKLMNPQRSTVWY"
}

_AMBIGUITIES = {
    "ambig DNA": dna_ambiguity,
    "ambig RNA": rna_ambiguity,
    "ambig AA": amino_acid_ambiguity
}
