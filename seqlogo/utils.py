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


NA_COLORSCHEMES = set((
    'monochrome', 'base pairing', 'classic'
))

AA_ALPHABETS = set((
    "AA", "reduced AA", "ambig AA"
))

AA_COLORSCHEMES = set((
    'monochrome', 'hydrophobicity', 'chemistry','charge'
))
