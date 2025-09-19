# Python-Chem: Chemical Reaction Calculator

A Python application that takes a list of chemical compounds and calculates reactions over time using numerical integration of kinetic equations.

## Features

- Define chemical compounds with molecular formulas
- Set up chemical reactions with reactants, products, and rate constants
- Simulate reaction kinetics over time using Euler's method
- Visualize concentration changes with matplotlib plots
- Load reaction systems from JSON configuration files
- Command-line interface for easy usage

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jmatzen/python-chem.git
cd python-chem
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install as a package:
```bash
pip install -e .
```

## Usage

### Command Line Interface

Run the calculator with default example reaction:
```bash
python chem_calculator.py
```

Use a configuration file:
```bash
python chem_calculator.py --config examples/simple_reaction.json
```

Specify simulation parameters:
```bash
python chem_calculator.py --config examples/enzyme_reaction.json --time 50 --steps 500
```

Save plot to file:
```bash
python chem_calculator.py --config examples/realistic_chemistry.json --output reaction_plot.png
```

Generate example configuration:
```bash
python chem_calculator.py --example
```

### Configuration File Format

Create JSON files to define your reaction system:

```json
{
  "compounds": [
    {
      "formula": "A",
      "name": "Reactant A",
      "concentration": 1.0
    },
    {
      "formula": "B",
      "name": "Reactant B", 
      "concentration": 0.5
    },
    {
      "formula": "C",
      "name": "Product C",
      "concentration": 0.0
    }
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
```

### Programming Interface

```python
from chem_calculator import ChemicalCalculator

# Create calculator instance
calc = ChemicalCalculator()

# Add compounds
calc.add_compound("A", "Reactant A", 1.0)
calc.add_compound("B", "Reactant B", 0.5) 
calc.add_compound("C", "Product C", 0.0)

# Add reaction: A + B → C
calc.add_reaction(["A", "B"], [1, 1], ["C"], [1], 0.1)

# Run simulation
time_points, concentrations = calc.simulate_reactions(100.0, 1000)

# Plot results
calc.plot_results(time_points, concentrations)
```

## Examples

The `examples/` directory contains several demonstration files:

- `simple_reaction.json` - Basic A + B → C reaction
- `enzyme_reaction.json` - Enzyme kinetics (E + S ⇌ ES → E + P)
- `realistic_chemistry.json` - Real chemical reaction (H₂ + I₂ → 2HI)

## Theory

The application simulates chemical kinetics using:

1. **Rate Laws**: Reaction rates calculated from concentrations and rate constants
2. **Mass Balance**: Conservation of mass through stoichiometric coefficients  
3. **Numerical Integration**: Euler's method for time evolution
4. **Kinetic Equations**: dc/dt = Σ(νᵢ × rᵢ) where νᵢ is stoichiometric coefficient and rᵢ is reaction rate

## Requirements

- Python 3.7+
- NumPy >= 1.20.0
- Matplotlib >= 3.3.0

## License

This project is open source and available under the MIT License.