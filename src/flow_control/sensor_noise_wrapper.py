"""
Gaussian Sensor Noise Observation Wrapper
Implements Equation (1) from the Physics of Fluids paper:
o_tilde_i = o_i + N(0, (level * |o_i|)^2)
"""
import numpy as np

class GaussianSensorNoiseWrapper:
    """
    Corrupts observation vector with Gaussian noise proportional to its own magnitude.
    Ground-truth physical CFD state remains unaffected.
    """
    def __init__(self, env, noise_level=0.10, seed=None):
        self.env = env
        self.noise_level = float(noise_level)
        self.rng = np.random.default_rng(seed)

    def set_noise_level(self, level):
        self.noise_level = float(level)

    def wrap_observation(self, obs):
        if self.noise_level <= 0.0:
            return obs.copy()
        
        # Relative noise proportional to each component's absolute magnitude
        scale = self.noise_level * np.abs(obs)
        noise = self.rng.normal(loc=0.0, scale=scale, size=obs.shape)
        return obs + noise

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        return self.wrap_observation(obs)

    def step(self, action):
        clean_obs, reward, done, info = self.env.step(action)
        noisy_obs = self.wrap_observation(clean_obs)
        # Store true physical drag in info for unbiased evaluation
        info["true_cd"] = float(np.sum(clean_obs[1::2]))
        info["clean_obs"] = clean_obs
        return noisy_obs, reward, done, info
