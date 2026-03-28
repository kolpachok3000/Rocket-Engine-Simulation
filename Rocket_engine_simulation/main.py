import numpy as np
import matplotlib.pyplot as plt
from engine_model import performance_vs_altitude
import os

# create folder for plots
os.makedirs("plots", exist_ok=True)

# engine = "Merlin 1D"
Pc = 10.8e6
Tc = 3900.0
At = 0.0401
expansion_ratio = 16.0 #Ae/At

# propellant = "LOX/RP-1"
gamma = 1.2
R = 355.0     

expansion_ratios = [10.0, 16.0, 25.0]

altitudes = np.linspace(0, 100000, 200)

all_results = []

for expansion_ratio in expansion_ratios:
    altitude_array, Pa_array, Pe_array, ve_array, Me_array, thrust_array, Isp_array = performance_vs_altitude(Pc, Tc, At, expansion_ratio, gamma, R, altitudes)

    all_results.append((
        expansion_ratio,
        altitude_array,
        Pa_array,
        Pe_array,
        ve_array,
        Me_array,
        thrust_array,
        Isp_array
    ))

# using the middle expansion ratio as a reference
reference_result = all_results[1]

expansion_ratio = reference_result[0]
altitude_array = reference_result[1]
Pa_array = reference_result[2]
Pe_array = reference_result[3]
ve_array = reference_result[4]
Me_array = reference_result[5]
thrust_array = reference_result[6]
Isp_array = reference_result[7]

print("Sample results for expansion ratio =", expansion_ratio)
print("Thrust at sea level:", round(thrust_array[0], 2), "N")
print("Isp at sea level:", round(Isp_array[0], 2), "s")
print("Thrust at 100 km:", round(thrust_array[-1], 2), "N")
print("Isp at 100 km:", round(Isp_array[-1], 2), "s")
print("Exit Mach number:", round(Me_array[0], 4))
print("Exit pressure:", round(Pe_array[0], 2), "Pa")
print("Exit velocity:", round(ve_array[0], 2), "m/s")

# Plot 1: Ambient pressure vs altitude
plt.figure()
plt.plot(altitude_array / 1000, Pa_array/1000)
plt.xlabel("Altitude [km]")
plt.ylabel("Ambient pressure [kPa]")
plt.title("Ambient pressure vs altitude")
plt.grid(True)
plt.savefig("plots/ambient_pressure_vs_altitude.png", dpi=300, bbox_inches="tight")

# Plot 2: Thrust vs altitude
plt.figure()
for result in all_results:
    expansion_ratio = result[0]
    altitude_array = result[1]
    thrust_array = result[6]
    plt.plot(altitude_array / 1000, thrust_array/1000, label="Ae/At = " + str(expansion_ratio))

plt.xlabel("Altitude [km]")
plt.ylabel("Thrust [kN]")
plt.title("Rocket thrust vs altitude")
plt.legend()
plt.grid(True)
plt.savefig("plots/thrust_vs_altitude.png", dpi=300, bbox_inches="tight")

# Plot 3: Specific impulse vs altitude
plt.figure()
for result in all_results:
    expansion_ratio = result[0]
    altitude_array = result[1]
    Isp_array = result[7]
    plt.plot(altitude_array / 1000, Isp_array, label="Ae/At = " + str(expansion_ratio))

plt.xlabel("Altitude [km]")
plt.ylabel("Specific impulse [s]")
plt.title("Specific impulse vs altitude")
plt.legend()
plt.grid(True)
plt.savefig("plots/isp_vs_altitude.png", dpi=300, bbox_inches="tight")

plt.show()