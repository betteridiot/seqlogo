"""
Copyright (c) 2018, Marcus D. Sherman

This code is part of the seqLogo distribution and governed by its
license.  Please see the LICENSE file that should have been included
as part of this package.

@author: "Marcus D. Sherman"
@copyright: "Copyright 2018, University of Michigan, Mills Lab
@email: "mdsherman<at>betteridiot<dot>tech"

"""

_AA_LETTERS = "GPAVLIMCFYWHKRQNEDST"
_REDUCED_AA_LETTERS = "ACDEFGHIKLMNPQRSTVWYX*-"
_EXT_AA_LETTERS = "ACDEFGHIKLMNPQRSTVWYBXZJUO"

_DNA_LETTERS = "ACGT"
_REDUCED_DNA_LETTERS = "ACGTN-"
_EXT_DNA_LETTERS = "GATCBDSW"
_AMBIG_DNA_LETTERS = "ACGTRYSWKMBDHVN-"

_RNA_LETTERS = "ACGU"
_REDUCED_RNA_LETTERS = "ACGUN-"
_EXT_RNA_LETTERS = "GAUCBDSW"
_AMBIG_RNA_LETTERS = "ACGURYSWKMBDHVN-"

_IDX_LETTERS = {
    "DNA": _DNA_LETTERS, "DNA with N": _REDUCED_DNA_LETTERS, "extended DNA": _EXT_DNA_LETTERS, "ambiguous DNA": _AMBIG_DNA_LETTERS,
    "RNA": _RNA_LETTERS, "RNA with N": _REDUCED_RNA_LETTERS,"extended RNA": _EXT_RNA_LETTERS, "ambiguous RNA": _AMBIG_RNA_LETTERS,
    "AA":_AA_LETTERS, "reduced AA": _REDUCED_AA_LETTERS, "extended AA": _EXT_AA_LETTERS
}


NA_ALPHABETS = set((
    "DNA", "DNA with N", "extended DNA", "ambiguous DNA"
    "RNA", "RNA with N", "extended RNA", "ambiguous RNA"
))

NA_COLORSCHEMES = set((
    'monochrome', 'base pairing', 'classic'
))

AA_ALPHABETS = set((
    "AA", "reduced AA", "extended AA"
))

AA_COLORSCHEMES = set((
    'monochrome', 'hydrophobicity', 'chemistry','charge'
))

def gen_hydrophobicity_map():
    """Generates a hydrophobicity dictionary of all amino acids"""
    hydro_map = {}
    for letter in _AA_LETTERS:
        if letter in "RKDENQ":
            hydro_map[letter] = 'hydrophilic'
        elif letter in "SGHTAP":
            hydro_map[letter] = 'neutral'
        elif letter in "YVMCLFIW":
            hydro_map[letter] = 'hydrophobic'
        else:
            raise ValueError('{} is not a canonical amino acid'.format(letter))
    return hydro_map


_HYDROPHOBICITY_CANON_AA = gen_hydrophobicity_map()


def gen_chemistry_map():
    """Generates a chemistry dictionary of all amino acids"""
    chem_map = {}
    for letter in _AA_LETTERS:
        if letter in "GSTYC":
            chem_map[letter] = 'polar'
        elif letter in "QN":
            chem_map[letter] = 'neutral'
        elif letter in "KRH":
            chem_map[letter] = 'basic'
        elif letter in "DE":
            chem_map[letter] = 'acidic'
        elif letter in "AVLIPWFM":
            chem_map[letter] = 'hydrophobic'
        else:
            raise ValueError('{} is not a canonical amino acid'.format(letter))
    return chem_map


_CHEMISTRY_CANON_AA = gen_chemistry_map()

# All colors are matched as closely as possible to [weblogo](http://weblogo.threeplusone.com/manual.html) color palettes. 

_COLOR_MAP ={
    "black": "#000000",
    "orange": "#ffb400",
    "red": "#ff0063",
    "blue": "#0000ff",
    "green": "#008000",
    "purple": "#ab0080"
}

_CANON_NT_COLORMAP = {
    "G": _COLOR_MAP['orange'],
    "T": _COLOR_MAP['red'],
    "U": _COLOR_MAP['red'],
    "C": _COLOR_MAP['blue'],
    "A": _COLOR_MAP['green']
}

_CANON_HYDRO_AA_COLORMAP = {
    'hydrophilic': _COLOR_MAP['blue'],
    'neutral': _COLOR_MAP['green'],
    'hydrophobic': _COLOR_MAP['black']
}

_CANON_CHEM_AA_COLORMAP = {
    'polar': _COLOR_MAP['green'],
    'neutral': _COLOR_MAP['purple'],
    'basic': _COLOR_MAP['blue'],
    'acidic': _COLOR_MAP['red'],
    'hydrophobic': _COLOR_MAP['black'],
}
