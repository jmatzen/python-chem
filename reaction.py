"""
Chemical Reaction Module

This module defines classes for representing chemical reactions and calculating
reaction kinetics over time.
"""

from typing import Dict, List, Tuple
import math
from chemical_compound import ChemicalCompound


class Reaction:
    """
    Represents a chemical reaction with reactants, products, and kinetic parameters.
    """
    
    def __init__(self, reactants: Dict[ChemicalCompound, int], 
                 products: Dict[ChemicalCompound, int],
                 rate_constant: float,
                 reaction_order: int = 1):
        """
        Initialize a chemical reaction.
        
        Args:
            reactants (Dict[ChemicalCompound, int]): Reactants and their stoichiometric coefficients
            products (Dict[ChemicalCompound, int]): Products and their stoichiometric coefficients
            rate_constant (float): Reaction rate constant (k)
            reaction_order (int): Overall reaction order (default: 1)
        """
        self.reactants = reactants
        self.products = products
        self.rate_constant = rate_constant
        self.reaction_order = reaction_order
    
    def calculate_rate(self, concentrations: Dict[ChemicalCompound, float]) -> float:
        """
        Calculate the reaction rate based on current concentrations.
        
        Args:
            concentrations (Dict[ChemicalCompound, float]): Current concentrations in mol/L
            
        Returns:
            float: Reaction rate in mol/L/s
        """
        rate = self.rate_constant
        
        # For simplicity, assume rate depends on first reactant concentration
        # In reality, this would depend on the specific rate law
        for compound, coeff in self.reactants.items():
            if compound in concentrations:
                concentration = concentrations[compound]
                rate *= (concentration ** coeff)
            else:
                return 0.0  # No reaction if reactant is not present
        
        return rate
    
    def get_stoichiometry_matrix(self) -> Dict[ChemicalCompound, int]:
        """
        Get the stoichiometry matrix (net change in each compound).
        
        Returns:
            Dict[ChemicalCompound, int]: Net stoichiometric coefficients
        """
        stoichiometry = {}
        
        # Reactants have negative coefficients (consumed)
        for compound, coeff in self.reactants.items():
            stoichiometry[compound] = -coeff
        
        # Products have positive coefficients (produced)
        for compound, coeff in self.products.items():
            stoichiometry[compound] = coeff
        
        return stoichiometry
    
    def __str__(self):
        reactant_str = " + ".join([f"{coeff}{compound.formula}" if coeff > 1 else compound.formula 
                                  for compound, coeff in self.reactants.items()])
        product_str = " + ".join([f"{coeff}{compound.formula}" if coeff > 1 else compound.formula 
                                 for compound, coeff in self.products.items()])
        return f"{reactant_str} → {product_str}"


class ReactionSystem:
    """
    Represents a system of chemical reactions that can be simulated over time.
    """
    
    def __init__(self, reactions: List[Reaction]):
        """
        Initialize a reaction system.
        
        Args:
            reactions (List[Reaction]): List of reactions in the system
        """
        self.reactions = reactions
        self.all_compounds = set()
        
        # Collect all compounds from all reactions
        for reaction in reactions:
            self.all_compounds.update(reaction.reactants.keys())
            self.all_compounds.update(reaction.products.keys())
    
    def simulate(self, initial_concentrations: Dict[ChemicalCompound, float], 
                 time_points: List[float]) -> Dict[ChemicalCompound, List[float]]:
        """
        Simulate the reaction system over time using Euler's method.
        
        Args:
            initial_concentrations (Dict[ChemicalCompound, float]): Initial concentrations in mol/L
            time_points (List[float]): Time points to simulate (in seconds)
            
        Returns:
            Dict[ChemicalCompound, List[float]]: Concentrations at each time point
        """
        # Initialize concentration arrays
        concentrations = {}
        for compound in self.all_compounds:
            concentrations[compound] = [initial_concentrations.get(compound, 0.0)]
        
        # Simple Euler integration
        for i in range(1, len(time_points)):
            dt = time_points[i] - time_points[i-1]
            current_conc = {compound: concentrations[compound][-1] 
                           for compound in self.all_compounds}
            
            # Calculate rate of change for each compound
            rate_changes = {compound: 0.0 for compound in self.all_compounds}
            
            for reaction in self.reactions:
                reaction_rate = reaction.calculate_rate(current_conc)
                stoichiometry = reaction.get_stoichiometry_matrix()
                
                for compound, stoich_coeff in stoichiometry.items():
                    rate_changes[compound] += stoich_coeff * reaction_rate
            
            # Update concentrations
            for compound in self.all_compounds:
                new_conc = current_conc[compound] + rate_changes[compound] * dt
                # Ensure concentrations don't go negative
                new_conc = max(0.0, new_conc)
                concentrations[compound].append(new_conc)
        
        return concentrations