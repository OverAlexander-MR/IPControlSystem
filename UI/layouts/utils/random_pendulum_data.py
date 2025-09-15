"""random_pendulum_data.py

Simulación física del péndulo invertido montado sobre un carro.

Provee la clase `RandomPendulumData` (por compatibilidad con la API previa) que
implementa una simulación realista mediante integración numérica (RK4) de las
ecuaciones dinámicas del sistema.

API principal:
    sim = RandomPendulumData()            # instancia con parámetros por defecto
    state = sim.next(dt)                  # avanza dt segundos y retorna (x_norm, x_dot, theta, theta_dot)

Opciones de configuración (al crear la instancia):
    RandomPendulumData(M=1.0, m=0.1, l=0.5, track_half_range=2.0, ...)

- x_norm está normalizado en [-1,1] respecto a track_half_range (metros).
- theta está en radianes, con 0 = vertical hacia arriba.

Se permite pasar una función control_func(state, t) que devuelva la fuerza F (N)
aplicada al carro en cada paso; por defecto F=0 (sin control).

"""

from math import sin, cos
from typing import Callable, Optional, Tuple


class RandomPendulumData:
    """Simulador físico de péndulo invertido con integración RK4.

    Parámetros relevantes:
        M: masa del carro (kg)
        m: masa del péndulo (kg)
        l: longitud al centro de masa del péndulo (m)
        g: gravedad (m/s^2)
        b: fricción viscosa del carro (N/m/s)
        track_half_range: distancia a cada lado que corresponde a x_norm = +-1 (m)
        control_func: función opcional control_func(state, t) -> F (N)
    """

    def __init__(
        self,
        M: float = 1.0,
        m: float = 0.1,
        l: float = 0.5,
        g: float = 9.81,
        b: float = 0.0,
        track_half_range: float = 2.0,
        control_func: Optional[
            Callable[[Tuple[float, float, float, float], float], float]
        ] = None,
    ):
        # physical parameters
        self.M = float(M)
        self.m = float(m)
        self.l = float(l)
        self.g = float(g)
        self.b = float(b)

        # clipping / normalization
        self.track_half_range = float(track_half_range)

        # controller (callable(state, t) -> force)
        self.control_func = control_func

        # initial state: x, x_dot, theta, theta_dot
        # theta = small angle near vertical (0 = up)
        self.x = 0.0
        self.x_dot = 0.0
        self.theta = 0.05  # small initial tilt (radians)
        self.theta_dot = 0.0

        # internal time
        self.t = 0.0

    def _derivatives(self, state, t, F):
        """Calcula las derivadas (x_dot, x_ddot, theta_dot, theta_ddot)"""
        x, x_dot, theta, theta_dot = state
        M = self.M
        m = self.m
        l = self.l
        g = self.g
        b = self.b

        # Useful shorthands
        sin_t = sin(theta)
        cos_t = cos(theta)

        # Denominator for theta_ddot formula
        denom = l * (4.0 / 3.0 - (m * cos_t * cos_t) / (M + m))

        # Compute theta_ddot following standard inverted pendulum on a cart dynamics
        # (derived from Lagrange) -- see control texts.
        theta_num = g * sin_t + cos_t * (
            (-F - m * l * theta_dot * theta_dot * sin_t + b * x_dot) / (M + m)
        )
        theta_ddot = theta_num / denom

        # x_ddot
        x_ddot = (
            F + m * l * (theta_dot * theta_dot * sin_t - theta_ddot * cos_t) - b * x_dot
        ) / (M + m)

        return (x_dot, x_ddot, theta_dot, theta_ddot)

    def _rk4_step(self, dt):
        state0 = (self.x, self.x_dot, self.theta, self.theta_dot)
        t0 = self.t

        # control at t0
        F0 = self.control_func(state0, t0) if self.control_func is not None else 0.0
        k1 = self._derivatives(state0, t0, F0)

        s1 = tuple(state0[i] + 0.5 * dt * k1[i] for i in range(4))
        F1 = (
            self.control_func(s1, t0 + 0.5 * dt)
            if self.control_func is not None
            else 0.0
        )
        k2 = self._derivatives(s1, t0 + 0.5 * dt, F1)

        s2 = tuple(state0[i] + 0.5 * dt * k2[i] for i in range(4))
        F2 = (
            self.control_func(s2, t0 + 0.5 * dt)
            if self.control_func is not None
            else 0.0
        )
        k3 = self._derivatives(s2, t0 + 0.5 * dt, F2)

        s3 = tuple(state0[i] + dt * k3[i] for i in range(4))
        F3 = self.control_func(s3, t0 + dt) if self.control_func is not None else 0.0
        k4 = self._derivatives(s3, t0 + dt, F3)

        new_state = [0.0] * 4
        for i in range(4):
            new_state[i] = state0[i] + (dt / 6.0) * (
                k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]
            )

        # Unpack
        self.x, self.x_dot, self.theta, self.theta_dot = new_state
        self.t += dt

        # Normalize theta to [-pi, pi] for numerical stability
        from math import pi

        while self.theta > pi:
            self.theta -= 2 * pi
        while self.theta < -pi:
            self.theta += 2 * pi

    def next(self, dt: float = 0.02):
        """Avanza la simulación dt segundos y retorna (x_norm, x_dot, theta, theta_dot).

        x_norm es x mapeado a [-1,1] usando track_half_range.
        """
        # Integrate (we may substep for stability if dt is large)
        max_substep = 0.02
        steps = max(1, int(dt / max_substep))
        sub_dt = dt / steps
        for _ in range(steps):
            self._rk4_step(sub_dt)

        # Convert to normalized position
        x_norm = self.x / self.track_half_range
        if x_norm < -1.0:
            x_norm = -1.0
        elif x_norm > 1.0:
            x_norm = 1.0

        return x_norm, self.x_dot, self.theta, self.theta_dot


# # Small demo when run as script
# if __name__ == "__main__":
#     import time

#     sim = RandomPendulumData()
#     print("Starting simulation (press Ctrl+C to stop).")
#     try:
#         while True:
#             state = sim.next(0.02)
#             print(
#                 f"x_norm={state[0]:+.3f}, x_dot={state[1]:+.3f}, theta={state[2]:+.3f}, theta_dot={state[3]:+.3f}"
#             )
#             time.sleep(0.02)
#     except KeyboardInterrupt:
#         print("Stopped.")
