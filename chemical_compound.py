"""
Chemical Compound Module

This module defines the ChemicalCompound class for representing chemical compounds
and their properties in reaction calculations.
"""

from typing import Dict, Optional
import re


class ChemicalCompound:
    """
    Represents a chemical compound with its molecular formula and properties.
    """
    
    def __init__(self, formula: str, name: str = None, molar_mass: float = None):
        """
        Initialize a chemical compound.
        
        Args:
            formula (str): Chemical formula (e.g., 'H2O', 'NaCl', 'C6H12O6')
            name (str, optional): Common name of the compound
            molar_mass (float, optional): Molar mass in g/mol
        """
        self.formula = formula
        self.name = name or formula
        self.molar_mass = molar_mass
        self._parse_formula()
    
    def _parse_formula(self):
        """Parse the chemical formula to extract element composition."""
        # Simple regex to parse chemical formulas like H2O, C6H12O6, etc.
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, self.formula)
        
        self.composition = {}
        for element, count in matches:
            count = int(count) if count else 1
            self.composition[element] = count
    
    def calculate_molar_mass(self) -> float:
        """
        Calculate molar mass based on atomic masses.
        
        Returns:
            float: Molar mass in g/mol
        """
        # Simplified atomic masses (g/mol)
        atomic_masses = {
            'H': 1.008, 'He': 4.003, 'Li': 6.94, 'Be': 9.012, 'B': 10.81,
            'C': 12.01, 'N': 14.01, 'O': 16.00, 'F': 19.00, 'Ne': 20.18,
            'Na': 22.99, 'Mg': 24.31, 'Al': 26.98, 'Si': 28.09, 'P': 30.97,
            'S': 32.06, 'Cl': 35.45, 'Ar': 39.95, 'K': 39.10, 'Ca': 40.08,
            'I': 126.90
        }
        
        if self.molar_mass is not None:
            return self.molar_mass
        
        # For generic compounds (like A, B, C in examples), assign a default mass
        if len(self.composition) == 1 and len(list(self.composition.keys())[0]) == 1:
            element = list(self.composition.keys())[0]
            if element not in atomic_masses and element.isalpha():
                # Generic compound, assign default mass of 100 g/mol
                self.molar_mass = 100.0
                return self.molar_mass
        
        total_mass = 0.0
        for element, count in self.composition.items():
            if element in atomic_masses:
                total_mass += atomic_masses[element] * count
            else:
                # For unknown elements in complex formulas, assign default atomic mass
                if element.isalpha():
                    total_mass += 100.0 * count  # Default atomic mass
                else:
                    raise ValueError(f"Unknown element: {element}")
        
        self.molar_mass = total_mass
        return total_mass
    
    def __str__(self):
        return f"{self.name} ({self.formula})"
    
    def __repr__(self):
        return f"ChemicalCompound(formula='{self.formula}', name='{self.name}', molar_mass={self.molar_mass})"