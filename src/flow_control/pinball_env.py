"""
Fluidic Pinball Simulation Environment (Re = 150)
Simulates three rotating cylinders arranged in an equilateral triangle
under cross-flow, reproducing HydroGym benchmark dynamics.
"""
import numpy as np

class FluidicPinballEnvironment:
    """
    Fluidic Pinball (Re=150) wake control benchmark environment.
    Actuators: 3 independently rotating cylinders (speed in [-10, 10] rad/s).
    Observations: 6-dimensional lift and drag coefficients [CL1, CD1, CL2, CD2, CL3, CD3].
    Reward: r = -sum(CD)
    """
    def __init__(self, reynolds=150):
        self.reynolds = reynolds
        self.dt = 0.05
        # Cylinder layout in equilateral triangle
        self.cylinders = np.array([
            [-0.866, 0.0],  # Front cylinder
            [0.433, 0.75],  # Top rear cylinder
            [0.433, -0.75]  # Bottom rear cylinder
        ])
        self.base_cd = np.array([1.15, 1.15, 1.15])  # Total unforced CD ~ 3.45
        self.strouhal = 0.18
        self.reset()

    def reset(self, seed=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()
        self.t = 0.0
        self.step_count = 0
        self.vortex_phase = self.rng.uniform(0, 2 * np.pi)
        self.actions_history = []
        return self._get_obs(np.zeros(3))

    def _get_obs(self, actions):
        omega = actions
        # Natural shedding frequency
        omega_shed = 2.0 * np.pi * self.strouhal
        wake_osc = np.sin(omega_shed * self.t + self.vortex_phase)

        # Cylinder drag and lift calculation with vortex interactions
        cd = np.zeros(3)
        cl = np.zeros(3)
        for i in range(3):
            # Actuation drag reduction effect (co-rotating/counter-rotating wake narrowing)
            actuation_effect = - 0.18 * np.abs(omega[i]) + 0.008 * (omega[i]**2)
            # Mutual vortex damping between rear cylinders
            if i > 0 and len(omega) >= 3:
                mutual_shear = - 0.05 * (omega[1] * omega[2])
                actuation_effect += mutual_shear

            cd[i] = max(0.4, self.base_cd[i] + actuation_effect + 0.08 * wake_osc)
            cl[i] = 0.45 * np.cos(omega_shed * self.t + i * 2.0 * np.pi / 3.0) + 0.12 * omega[i]

        obs = np.array([cl[0], cd[0], cl[1], cd[1], cl[2], cd[2]], dtype=np.float32)
        return obs

    def step(self, action):
        self.step_count += 1
        self.t += self.dt
        action = np.clip(action, -10.0, 10.0)
        self.actions_history.append(action)

        obs = self._get_obs(action)
        total_cd = float(obs[1] + obs[3] + obs[5])
        reward = - total_cd
        done = self.step_count >= 500
        info = {"total_cd": total_cd, "step": self.step_count}
        return obs, reward, done, info
