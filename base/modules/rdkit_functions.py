# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem

class RDKit:

    @classmethod
    def mol_from_smiles(self, smiles):
        m = Chem.MolFromSmiles(smiles)
        m = self.apply_aromaticity(m)
        return m

    @classmethod
    def apply_aromaticity(self, mol_rdkit):
        Chem.Kekulize(mol_rdkit, True)
        Chem.SetAromaticity(mol_rdkit,Chem.rdmolops.AromaticityModel.AROMATICITY_MDL)
        return mol_rdkit

    @classmethod
    def mol_to_smiles(self, mol_rdkit, kekulize = False):
        self.apply_aromaticity(mol_rdkit)
        if kekulize:
            Chem.Kekulize(mol_rdkit, True)
        return Chem.MolToSmiles(mol_rdkit, isomericSmiles = True)#, kekuleSmiles = kekulize)

    @classmethod
    def mol_to_molfile(self, mol_rdkit):
        return Chem.MolToMolBlock(mol_rdkit)

    @classmethod
    def mol_to_inchi(self, mol_rdkit):
        return Chem.MolToInchi(mol_rdkit)

    @classmethod
    def mol_to_inchi_key(self, mol_rdkit):
        return Chem.InchiToInchiKey(self.mol_to_inchi(mol_rdkit))

    @classmethod
    def formula(self, mol_rdkit):
        return Chem.rdMolDescriptors.CalcMolFormula(mol_rdkit)

    @classmethod
    def mass_average(self, mol_rdkit):
        from rdkit.Chem import Descriptors
        return Descriptors.MolWt(mol_rdkit)

    @classmethod
    def mass_exact(self, mol_rdkit):
        from rdkit.Chem import Descriptors
        return Descriptors.ExactMolWt(mol_rdkit)

    @classmethod
    def is_valid_mol(self, mol_rdkit):
        return \
            Chem.rdmolops.SanitizeMol(mol_rdkit, catchErrors=True) \
            == Chem.rdmolops.SanitizeFlags.SANITIZE_NONE

    @classmethod
    def reaction_from_smarts(self, smarts):
        return Chem.rdChemReactions.ReactionFromSmarts(smarts)

    @classmethod
    def reaction_to_smarts(self, reaction):
        return Chem.rdChemReactions.ReactionToSmarts(reaction)
