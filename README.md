# Rocket-Engine-Simulation
This project models the performance of a rocket engine as a function of altitude using Python. It computes important quantities such as ambient pressure, exit pressure, exit velocity, thrust, and specific impulse for different nozzle expansion ratios. 

The goal of the project is to study how engine performance changes from sea level to near-vacuum conditions and how nozzle geometry affects thrust and efficiency. The current version uses Merlin-1D engine from Falcon-9, although the obtained results do not perfectly match with published values as there is not all data available. To run the simulation for your own engine, change #engine, #propellant and expansion ratios sections at the top of main.py.

# Features

- Computes ambient pressure as a function of altitude
- Simulates rocket engine performance for a given set of chamber conditions
- Evaluates:
  - Exit Mach number
  - Exit pressure
  - Exit velocity
  - Thrust
  - Specific impulse
- Compares multiple nozzle expansion ratios
- Generates and saves plots in a separate folder

# Project Structure

ROCKET_ENGINE_SIMULATION

 - atmosphere.py        # Computes atmospheric properties versus altitude
 - engine_model.py      # Core rocket engine performance calculations
 - main.py              # Runs simulations and generates plots
 - plots/               # Saved output figures
 - README.md            # Project documentation

Assumptions:
1. Steady-state engine
2. Standard atmosphere (ISA) for Pa
3. Constant chamber pressure Pc
4. Constant chamber temperature Tc
5. Constant specific heat ratio gamma
6. Constant gas constant R
7. Fixed throat area At
8. Fixed exit area Ae
