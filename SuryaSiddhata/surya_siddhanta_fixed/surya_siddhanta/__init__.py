"""
Surya Siddhanta Astronomy - Complete Fixed Implementation

A rigorously validated Python implementation of the ancient Indian 
astronomical text Surya Siddhanta, with all critical mathematical 
and algorithmic fixes applied.
"""

__version__ = "1.0.0"
__author__ = "Surya Siddhanta Project"
__email__ = "surya-siddhanta @example.com"

from .calculator import SuryaSiddhantaCalculator
from .chapter3_mean_motions import MeanMotionCalculator
from .chapter4_manda_correction import MandaCorrectionCalculator
from .chapter5_sighra_correction import SighraCorrectionCalculator
from .chapter6_lunar_theory import LunarTheoryCalculator
from .chapter7_conjunctions import ConjunctionCalculator

__all__ = [
    "SuryaSiddhantaCalculator",
    "MeanMotionCalculator",
    "MandaCorrectionCalculator", 
    "SighraCorrectionCalculator",
    "LunarTheoryCalculator",
    "ConjunctionCalculator",
]