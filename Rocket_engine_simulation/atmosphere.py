import numpy as np

# constants
g0 = 9.80665
R = 287.05

# ISA layers (altitude, base temperature, lapse rate)
ISA_layers = [
    (0,      288.15, -0.0065),
    (11000,  216.65,  0.0),
    (20000,  216.65,  0.001),
    (32000,  228.65,  0.0028),
    (47000,  270.65,  0.0),
    (51000,  270.65, -0.0028),
    (71000,  214.65, -0.002),
    (86000,  186.87,  0.0),
]

# a list of pressures at the bottom of each layer
Base_pressures = [101325.0]

for i in range(len(ISA_layers)-1):
    h0, T0, L = ISA_layers[i]
    h1, T1, _ = ISA_layers[i+1]
    P0 = Base_pressures[-1]
    dh = h1 - h0
    if L == 0.0:
        P1 = P0 * np.exp(-g0 * dh / (R * T0))
    else:
        P1 = P0 * (T1 / T0) ** (-g0 / (R * L))
    Base_pressures.append(float(P1))

def get_ambient_pressure(altitude):
    if altitude > 86000:
        return 0.0
    else:
        #altitude = max(altitude, 0)
        layer_idx = 0
        for i in range(len(ISA_layers) - 1):
            if altitude >= ISA_layers[i][0]:
                layer_idx = i
        h0, T0, L = ISA_layers[layer_idx]
        P0 = Base_pressures[layer_idx]
        dh = altitude - h0
        T  = T0 + L * dh
        if L == 0.0:
            P1 = P0 * np.exp(-g0 * dh / (R * T0))
            return P1
        else:
            P1 = P0 * (T / T0) ** (-g0 / (R * L))
            return P1