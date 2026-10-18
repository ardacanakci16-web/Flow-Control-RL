"""
Reinforcement-Learning-Based Active Flow Control with Sensor Noise
Physics of Fluids Paper: Robustness and Sample Efficiency under Gaussian Sensor Noise
"""
from .sensor_noise_wrapper import GaussianSensorNoiseWrapper
from .pinball_env import FluidicPinballEnvironment

__all__ = ["GaussianSensorNoiseWrapper", "FluidicPinballEnvironment"]
