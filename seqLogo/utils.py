"""
Copyright (c) 2018, Marcus D. Sherman

This code is part of the seqlogo distribution and governed by its
license.  Please see the LICENSE file that should have been included
as part of this package.

@author: "Marcus D. Sherman"
@copyright: "Copyright 2018, University of Michigan, Mills Lab
@email: "mdsherman<at>betteridiot<dot>tech"

"""

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

NA_ALPHABETS = set((
    "DNA", "reduced DNA", "ambig DNA"
    "RNA", "reduced RNA", "ambig RNA"
))

NA_COLORSCHEMES = set((
    'monochrome', 'base pairing', 'classic'
))

AA_ALPHABETS = set((
    "AA", "reduced AA", "ambig AA"
))

AA_COLORSCHEMES = set((
    'monochrome', 'hydrophobicity', 'chemistry','charge'
))
