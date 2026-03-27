import numpy as np
from atmosphere import get_ambient_pressure

# Constants
g0 = 9.80665  # m/s^2


def area_mach_relation(M, gamma):
    
    # Computes Ae/At for a given Mach number M using the isentropic area-Mach relation.
    
    Ae_At = (1.0 / M) * ((2.0 / (gamma + 1.0) * (1.0 + (gamma - 1.0) / 2.0 * M**2))** ((gamma + 1.0) / (2.0 * (gamma - 1.0))))
    return Ae_At
print("f_low:", area_mach_relation(1.0001, 1.22)-16)
print("f_mid:", area_mach_relation(10.05, 1.22)-16)
def solve_exit_mach(expansion_ratio, gamma, threshold=1e-6, iterations=200):
    
    # Solves for the supersonic exit Mach number from the nozzle expansion ratio Ae/At.
    # Uses recursive bisection on the supersonic branch.
    
    # set bounds
    low = 1.0001
    high = 20.0

    for iteration in range(iterations):
        mid = 0.5 * (low + high)

        f_low = area_mach_relation(low, gamma) - expansion_ratio
        f_mid = area_mach_relation(mid, gamma) - expansion_ratio

        if abs(f_mid) < threshold:
            return mid

        if f_low * f_mid < 0:
            high = mid
        else:
            low = mid

    return mid


def get_mass_flow_rate(Pc, Tc, At, gamma, R):
    """
    Computes choked nozzle mass flow rate.

    Parameters:
        Pc     chamber pressure [Pa]
        Tc     chamber temperature [K]
        At     throat area [m^2]
        gamma  specific heat ratio [-]
        R      gas constant of exhaust gases [J/(kg*K)]
    """
    m_dot = At * Pc * np.sqrt(gamma / (R * Tc)) * (2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (2.0 * (gamma - 1.0)))
    return m_dot


def get_exit_conditions(Pc, Tc, expansion_ratio, gamma, R):
    """
    Computes exit Mach number, temperature, pressure and velocity.

    Returns:
        Me  exit Mach number [-]
        Te  exit temperature [K]
        Pe  exit pressure [Pa]
        ve  exit velocity [m/s]
    """
    Me = solve_exit_mach(expansion_ratio, gamma)

    Te = Tc / (1.0 + (gamma - 1.0) / 2.0 * Me**2)

    Pe = Pc * (1.0 + (gamma - 1.0) / 2.0 * Me**2) ** (-gamma / (gamma - 1.0))

    ve = Me * np.sqrt(gamma * R * Te)

    return Me, Te, Pe, ve


def rocket_performance(Pc, Tc, At, expansion_ratio, gamma, R, altitude):
    """
    Computes rocket thrust and specific impulse at a given altitude.

    Returns:
        altitude, Pa, m_dot, Ae, Me, Te, Pe, ve, thrust, Isp
    """
    Pa = get_ambient_pressure(altitude)
    Ae = expansion_ratio * At

    m_dot = get_mass_flow_rate(Pc, Tc, At, gamma, R)
    Me, Te, Pe, ve = get_exit_conditions(Pc, Tc, expansion_ratio, gamma, R)

    thrust = m_dot * ve + (Pe - Pa) * Ae
    Isp = thrust / (m_dot * g0)

    return altitude, Pa, m_dot, Ae, Me, Te, Pe, ve, thrust, Isp


def performance_vs_altitude(Pc, Tc, At, expansion_ratio, gamma, R, altitudes):
    """
    Computes rocket performance over multiple altitudes.

    Returns:
        altitude_array, Pa_array, Pe_array, ve_array, Me_array, thrust_array, Isp_array
    """
    altitudes = np.asarray(altitudes, dtype=float)

    pa_list = []
    pe_list = []
    ve_list = []
    me_list = []
    thrust_list = []
    isp_list = []

    for h in altitudes:
        altitude, Pa, m_dot, Ae, Me, Te, Pe, ve, thrust, Isp = rocket_performance(Pc, Tc, At, expansion_ratio, gamma, R, h)

        pa_list.append(Pa)
        pe_list.append(Pe)
        ve_list.append(ve)
        me_list.append(Me)
        thrust_list.append(thrust)
        isp_list.append(Isp)

    Pa_array = np.array(pa_list)
    Pe_array = np.array(pe_list)
    ve_array = np.array(ve_list)
    Me_array = np.array(me_list)
    thrust_array = np.array(thrust_list)
    Isp_array = np.array(isp_list)

    return altitudes, Pa_array, Pe_array, ve_array, Me_array, thrust_array, Isp_array