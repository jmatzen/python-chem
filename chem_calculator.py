#!/usr/bin/env python3
"""
Chemical Reaction Calculator

Main application for calculating chemical reactions over time.
This module provides the command-line interface and main application logic.
"""

import argparse
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from chemical_compound import ChemicalCompound
from reaction import Reaction, ReactionSystem


class ChemicalCalculator:
    """
    Main calculator class for chemical reaction simulations.
    """
    
    def __init__(self):
        """Initialize the calculator."""
        self.compounds = {}
        self.reactions = []
    
    def add_compound(self, formula: str, name: str = None, concentration: float = 0.0) -> ChemicalCompound:
        """
        Add a chemical compound to the system.
        
        Args:
            formula (str): Chemical formula
            name (str): Common name (optional)
            concentration (float): Initial concentration in mol/L
            
        Returns:
            ChemicalCompound: The created compound
        """
        compound = ChemicalCompound(formula, name)
        compound.calculate_molar_mass()
        self.compounds[formula] = {
            'compound': compound,
            'concentration': concentration
        }
        return compound
    
    def add_reaction(self, reactant_formulas: List[str], reactant_coeffs: List[int],
                    product_formulas: List[str], product_coeffs: List[int],
                    rate_constant: float) -> Reaction:
        """
        Add a chemical reaction to the system.
        
        Args:
            reactant_formulas (List[str]): List of reactant formulas
            reactant_coeffs (List[int]): Stoichiometric coefficients for reactants
            product_formulas (List[str]): List of product formulas
            product_coeffs (List[int]): Stoichiometric coefficients for products
            rate_constant (float): Reaction rate constant
            
        Returns:
            Reaction: The created reaction
        """
        reactants = {}
        products = {}
        
        # Build reactants dictionary
        for formula, coeff in zip(reactant_formulas, reactant_coeffs):
            if formula not in self.compounds:
                self.add_compound(formula)
            reactants[self.compounds[formula]['compound']] = coeff
        
        # Build products dictionary
        for formula, coeff in zip(product_formulas, product_coeffs):
            if formula not in self.compounds:
                self.add_compound(formula)
            products[self.compounds[formula]['compound']] = coeff
        
        reaction = Reaction(reactants, products, rate_constant)
        self.reactions.append(reaction)
        return reaction
    
    def simulate_reactions(self, time_end: float, time_steps: int = 1000) -> Tuple[List[float], Dict]:
        """
        Simulate all reactions over time.
        
        Args:
            time_end (float): End time for simulation (seconds)
            time_steps (int): Number of time steps
            
        Returns:
            Tuple[List[float], Dict]: Time points and concentration data
        """
        if not self.reactions:
            raise ValueError("No reactions defined. Add reactions before simulating.")
        
        # Create time points
        time_points = np.linspace(0, time_end, time_steps).tolist()
        
        # Prepare initial concentrations
        initial_concentrations = {}
        for formula, data in self.compounds.items():
            initial_concentrations[data['compound']] = data['concentration']
        
        # Create reaction system and simulate
        reaction_system = ReactionSystem(self.reactions)
        results = reaction_system.simulate(initial_concentrations, time_points)
        
        return time_points, results
    
    def plot_results(self, time_points: List[float], concentrations: Dict, 
                    output_file: str = None):
        """
        Plot the concentration vs time results.
        
        Args:
            time_points (List[float]): Time points
            concentrations (Dict): Concentration data
            output_file (str): Optional output file for saving plot
        """
        plt.figure(figsize=(10, 6))
        
        for compound, conc_data in concentrations.items():
            plt.plot(time_points, conc_data, label=str(compound), linewidth=2)
        
        plt.xlabel('Time (s)')
        plt.ylabel('Concentration (mol/L)')
        plt.title('Chemical Reaction Simulation')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {output_file}")
        else:
            plt.show()
    
    def load_from_config(self, config_file: str):
        """
        Load compounds and reactions from a JSON configuration file.
        
        Args:
            config_file (str): Path to configuration file
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Load compounds
            if 'compounds' in config:
                for compound_data in config['compounds']:
                    self.add_compound(
                        compound_data['formula'],
                        compound_data.get('name'),
                        compound_data.get('concentration', 0.0)
                    )
            
            # Load reactions
            if 'reactions' in config:
                for reaction_data in config['reactions']:
                    self.add_reaction(
                        reaction_data['reactants']['formulas'],
                        reaction_data['reactants']['coefficients'],
                        reaction_data['products']['formulas'],
                        reaction_data['products']['coefficients'],
                        reaction_data['rate_constant']
                    )
            
            print(f"Loaded configuration from {config_file}")
            
        except Exception as e:
            print(f"Error loading configuration: {e}")
            sys.exit(1)
    
    def print_system_info(self):
        """Print information about the current system."""
        print("\n=== Chemical Reaction System ===")
        print(f"Compounds ({len(self.compounds)}):")
        for formula, data in self.compounds.items():
            compound = data['compound']
            concentration = data['concentration']
            molar_mass = compound.calculate_molar_mass()
            print(f"  {compound} - {concentration:.3f} mol/L - MW: {molar_mass:.2f} g/mol")
        
        print(f"\nReactions ({len(self.reactions)}):")
        for i, reaction in enumerate(self.reactions, 1):
            print(f"  {i}. {reaction} (k = {reaction.rate_constant})")


def create_example_config():
    """Create an example configuration file."""
    example_config = {
        "compounds": [
            {"formula": "A", "name": "Reactant A", "concentration": 1.0},
            {"formula": "B", "name": "Reactant B", "concentration": 0.5},
            {"formula": "C", "name": "Product C", "concentration": 0.0}
        ],
        "reactions": [
            {
                "reactants": {
                    "formulas": ["A", "B"],
                    "coefficients": [1, 1]
                },
                "products": {
                    "formulas": ["C"],
                    "coefficients": [1]
                },
                "rate_constant": 0.1
            }
        ]
    }
    
    with open('example_config.json', 'w') as f:
        json.dump(example_config, f, indent=2)
    print("Created example_config.json")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description='Chemical Reaction Calculator')
    parser.add_argument('--config', '-c', type=str, help='Configuration file (JSON)')
    parser.add_argument('--time', '-t', type=float, default=100.0, 
                       help='Simulation time (seconds, default: 100)')
    parser.add_argument('--steps', '-s', type=int, default=1000,
                       help='Number of time steps (default: 1000)')
    parser.add_argument('--output', '-o', type=str, 
                       help='Output file for plot (optional)')
    parser.add_argument('--example', action='store_true',
                       help='Create example configuration file')
    
    args = parser.parse_args()
    
    if args.example:
        create_example_config()
        return
    
    calculator = ChemicalCalculator()
    
    if args.config:
        calculator.load_from_config(args.config)
    else:
        # Default example: A + B → C
        print("No configuration file provided. Using default example reaction: A + B → C")
        calculator.add_compound("A", "Reactant A", 1.0)
        calculator.add_compound("B", "Reactant B", 0.5)
        calculator.add_compound("C", "Product C", 0.0)
        calculator.add_reaction(["A", "B"], [1, 1], ["C"], [1], 0.1)
    
    calculator.print_system_info()
    
    # Run simulation
    print(f"\nRunning simulation for {args.time} seconds with {args.steps} steps...")
    try:
        time_points, concentrations = calculator.simulate_reactions(args.time, args.steps)
        
        # Print final concentrations
        print("\nFinal concentrations:")
        for compound, conc_data in concentrations.items():
            print(f"  {compound}: {conc_data[-1]:.6f} mol/L")
        
        # Plot results
        calculator.plot_results(time_points, concentrations, args.output)
        
    except Exception as e:
        print(f"Simulation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()