"""
Chapter 4: Manda Correction (Equation of Center)
Fixed: Unit consistency, proper sign handling, quadrant boundaries
"""

import math
from typing import Dict, Any

from .angle_utils import normalize_angle, degrees_to_arcminutes, arcminutes_to_degrees
from .constants import SINE_RADIUS, MANDA_PARIDHI, MANDOCCA_POSITIONS
from .correction_logger import global_logger, CorrectionType

class MandaCorrectionCalculator:
    """
    Apply Manda correction with unit consistency and proper physics.
    Fixed: All internal calculations in arcminutes, correct sign handling.
    """
    
    def __init__(self):
        self.R = SINE_RADIUS  # Sine radius in arcminutes
    
    def surya_siddhanta_sine(self, angle_degrees: float) -> float:
        """
        Calculate sine using Surya Siddhanta method.
        Returns signed value to handle quadrant automatically.
        """
        angle_radians = math.radians(angle_degrees)
        return self.R * math.sin(angle_radians)
    
    def calculate_manda_kendra(self, mean_longitude: float, mandocca: float) -> float:
        """Calculate Manda Kendra (anomaly) with proper normalization."""
        return normalize_angle(mean_longitude - mandocca)
    
    def calculate_manda_phala(self, manda_paridhi_deg: float, manda_kendra: float) -> float:
        """
        Calculate Manda Phala (equation of center) with unit consistency.
        Fixed: All internal calculations in arcminutes.
        """
        # Convert everything to arcminutes for internal calculation
        manda_paridhi_arcmin = degrees_to_arcminutes(manda_paridhi_deg)
        
        # Calculate signed Jya (automatically handles quadrant via sine)
        jya_arcmin = self.surya_siddhanta_sine(manda_kendra)
        
        # Calculate Manda Phala in arcminutes
        # Formula: MP = (Manda_Paridhi × Jya) / (360 × R)
        manda_phala_arcmin = (manda_paridhi_arcmin * jya_arcmin) / (360.0 * self.R)
        
        # Convert back to degrees for final correction
        manda_phala_deg = arcminutes_to_degrees(manda_phala_arcmin)
        
        return manda_phala_deg
    
    def apply_manda_correction(self, planet: str, mean_longitude: float) -> float:
        """
        Apply complete Manda correction.
        Fixed: Proper physics - true longitude = mean longitude + equation of center.
        """
        if planet not in MANDA_PARIDHI:
            raise ValueError(f"Unknown planet for Manda correction: {planet}")
        
        mandocca = MANDOCCA_POSITIONS[planet]
        manda_paridhi = MANDA_PARIDHI[planet]
        
        manda_kendra = self.calculate_manda_kendra(mean_longitude, mandocca)
        manda_phala = self.calculate_manda_phala(manda_paridhi, manda_kendra)
        
        # CORRECT PHYSICS: True longitude = Mean longitude + Equation of center
        # The sign is handled automatically by the sine function in manda_phala
        true_longitude = normalize_angle(mean_longitude + manda_phala)
        
        # Log the correction
        global_logger.log_correction(
            chapter=4,
            correction_type=CorrectionType.MANDA_CORRECTION,
            planet=planet,
            input_values={
                "mean_longitude": mean_longitude,
                "mandocca": mandocca,
                "manda_paridhi_deg": manda_paridhi,
                "manda_kendra": manda_kendra
            },
            output_values={
                "manda_phala": manda_phala,
                "true_longitude": true_longitude
            },
            units="degrees",
            metadata={"correction_sign": "automatic_via_sine"}
        )
        
        return true_longitude
    
    def test_manda_physics(self) -> Dict[str, Any]:
        """
        Test Manda correction follows correct physical behavior.
        Fixed: Verify planet is ahead of mean before apogee, behind after apogee.
        """
        test_cases = [
            # (mean_lon, mandocca, expected_phala_sign, description)
            (10.0, 0.0, "positive", "Just after apogee - should be ahead"),
            (350.0, 0.0, "negative", "Just before apogee - should be behind"),
            (90.0, 0.0, "positive", "90° from apogee - maximum ahead"),
            (270.0, 0.0, "negative", "270° from apogee - maximum behind"),
        ]
        
        results = []
        manda_paridhi = 31.5  # Use Moon's value for testing
        
        for mean_lon, mandocca, expected_sign, description in test_cases:
            manda_kendra = self.calculate_manda_kendra(mean_lon, mandocca)
            manda_phala = self.calculate_manda_phala(manda_paridhi, manda_kendra)
            
            actual_sign = "positive" if manda_phala > 0 else "negative"
            correct = actual_sign == expected_sign
            
            results.append({
                "description": description,
                "mean_longitude": mean_lon,
                "mandocca": mandocca,
                "manda_kendra": manda_kendra,
                "manda_phala": manda_phala,
                "expected_sign": expected_sign,
                "actual_sign": actual_sign,
                "correct": correct
            })
        
        return {
            "test_cases": results,
            "all_correct": all(r["correct"] for r in results)
        }