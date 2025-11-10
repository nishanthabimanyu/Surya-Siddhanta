"""
Chapter 5: Sighra Correction (Geocentric)
Fixed: Unit consistency, correct Karna formula, stable interpolation
"""

import math
from typing import Dict, Any, List, Tuple

from .angle_utils import normalize_angle, degrees_to_arcminutes, circular_difference
from .constants import SINE_RADIUS, SIGHRA_PARIDHI, PLANET_TYPES
from .correction_logger import global_logger, CorrectionType

class SighraCorrectionCalculator:
    """
    Apply Sighra correction with proper spherical trigonometry.
    Fixed: Correct Karna formula, unit consistency, stable algorithms.
    """
    
    def __init__(self):
        self.R = SINE_RADIUS  # Sine radius in arcminutes
    
    def calculate_sighra_kendra(self, planet_type: str, planet_longitude: float, 
                               sun_longitude: float) -> float:
        """
        Calculate Sighra Kendra (elongation) based on planet type.
        """
        if planet_type == 'superior':
            # For superior planets: SK = Planet - Sun
            sighra_kendra = normalize_angle(planet_longitude - sun_longitude)
        else:  # inferior
            # For inferior planets: SK = Sun - Planet  
            sighra_kendra = normalize_angle(sun_longitude - planet_longitude)
        
        return sighra_kendra
    
    def calculate_sighra_karna(self, planet: str, sighra_kendra: float) -> float:
        """
        Calculate Sighra Karna (hypotenuse) using correct spherical trigonometry.
        Fixed: Uses Law of Cosines for the Earth-Sun-Planet triangle.
        """
        if planet not in SIGHRA_PARIDHI:
            raise ValueError(f"Unknown planet for Sighra correction: {planet}")
        
        # Convert to consistent units (arcminutes)
        sighra_paridhi_arcmin = degrees_to_arcminutes(SIGHRA_PARIDHI[planet])
        sighra_kendra_rad = math.radians(sighra_kendra)
        
        # CORRECT FORMULA: Law of Cosines for the triangle
        # Karna² = R² + SP² + 2 × R × SP × cos(SK)
        karna_squared = (self.R ** 2 + 
                        sighra_paridhi_arcmin ** 2 + 
                        2 * self.R * sighra_paridhi_arcmin * math.cos(sighra_kendra_rad))
        
        sighra_karna = math.sqrt(karna_squared)
        
        return sighra_karna
    
    def calculate_sighra_phala(self, planet: str, sighra_kendra: float, 
                              sighra_karna: float) -> float:
        """
        Calculate Sighra Phala (correction angle).
        Fixed: Uses arcsine with proper unit handling.
        """
        sighra_paridhi_arcmin = degrees_to_arcminutes(SIGHRA_PARIDHI[planet])
        sighra_kendra_rad = math.radians(sighra_kendra)
        
        # Calculate argument for arcsine
        numerator = sighra_paridhi_arcmin * math.sin(sighra_kendra_rad)
        argument = numerator / sighra_karna
        
        # Ensure argument is within valid range for arcsine
        argument = max(min(argument, 1.0), -1.0)
        
        # Calculate Sighra Phala in radians, then convert to degrees
        sighra_phala_rad = math.asin(argument)
        sighra_phala_deg = math.degrees(sighra_phala_rad)
        
        return sighra_phala_deg
    
    def apply_sighra_correction(self, planet: str, manda_corrected_longitude: float,
                               sun_longitude: float) -> Dict[str, Any]:
        """
        Apply complete Sighra correction.
        Fixed: Proper handling for both superior and inferior planets.
        """
        if planet not in PLANET_TYPES:
            raise ValueError(f"Unknown planet type: {planet}")
        
        planet_type = PLANET_TYPES[planet]
        
        # Calculate Sighra parameters
        sighra_kendra = self.calculate_sighra_kendra(planet_type, manda_corrected_longitude, sun_longitude)
        sighra_karna = self.calculate_sighra_karna(planet, sighra_kendra)
        sighra_phala = self.calculate_sighra_phala(planet, sighra_kendra, sighra_karna)
        
        # Apply correction based on planet type
        if planet_type == 'superior':
            true_longitude = normalize_angle(manda_corrected_longitude + sighra_phala)
        else:
            # For inferior planets, use simplified approach (mark as approximate)
            true_longitude = normalize_angle(sun_longitude + sighra_phala)
        
        result = {
            'true_longitude': true_longitude,
            'sighra_kendra': sighra_kendra,
            'sighra_karna': sighra_karna,
            'sighra_phala': sighra_phala,
            'planet_type': planet_type,
            'is_approximate': planet_type == 'inferior'
        }
        
        # Log the correction
        global_logger.log_correction(
            chapter=5,
            correction_type=CorrectionType.SIGHRA_CORRECTION,
            planet=planet,
            input_values={
                "manda_corrected_longitude": manda_corrected_longitude,
                "sun_longitude": sun_longitude,
                "planet_type": planet_type,
                "sighra_kendra": sighra_kendra
            },
            output_values=result,
            units="degrees",
            metadata={"formula": "law_of_cosines"}
        )
        
        return result
    
    def refine_minimum_time_lagrange(self, time_points: List[float], 
                                   separation_values: List[float]) -> float:
        """
        Refine minimum time using stable Lagrange interpolation.
        Fixed: Replaces unstable quadratic fitting.
        """
        if len(time_points) != 3 or len(separation_values) != 3:
            raise ValueError("Need exactly 3 points for Lagrange interpolation")
        
        t0, t1, t2 = time_points
        s0, s1, s2 = separation_values
        
        # Lagrange interpolation for minimum finding
        # More stable than direct quadratic coefficients
        A = t0 * (s2 - s1) + t1 * (s0 - s2) + t2 * (s1 - s0)
        B = (t0 * t0) * (s1 - s2) + (t1 * t1) * (s2 - s0) + (t2 * t2) * (s0 - s1)
        
        if abs(A) < 1e-12:
            # Fallback to simple minimum if unstable
            min_index = separation_values.index(min(separation_values))
            return time_points[min_index]
        
        refined_time = -B / (2 * A)
        return refined_time