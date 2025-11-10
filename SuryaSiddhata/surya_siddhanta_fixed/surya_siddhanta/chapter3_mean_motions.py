"""
Chapter 3: Mean Motions of Planets
Fixed: Precision handling, modular arithmetic, non-circular verification
"""

import math
from typing import Dict

from .angle_utils import normalize_angle, reduce_angle_magnitude, dms_to_decimal
from .time_utils import calculate_precise_ahargana
from .constants import (
    CIVIL_DAYS_IN_MAHAYUGA, 
    PLANETARY_REVOLUTIONS,
    INITIAL_LONGITUDES,
    MODERN_SIDEREAL_PERIODS
)
from .correction_logger import global_logger, CorrectionType

class MeanMotionCalculator:
    """
    Calculate mean planetary motions with precision considerations.
    Fixed: Uses modular arithmetic to minimize floating-point error.
    """
    
    def __init__(self):
        self.daily_motions = self._calculate_daily_motions()
        self.initial_longitudes_deg = self._convert_initial_longitudes()
        self.periods_days = self._calculate_periods()
    
    def _calculate_daily_motions(self) -> Dict[str, float]:
        """Calculate exact daily motions from Mahayuga revolutions."""
        motions = {}
        for planet, revolutions in PLANETARY_REVOLUTIONS.items():
            daily_motion = (revolutions * 360.0) / CIVIL_DAYS_IN_MAHAYUGA
            motions[planet] = daily_motion
        
        # Log the calculation for verification
        global_logger.log_correction(
            chapter=2,
            correction_type=CorrectionType.MEAN_MOTION,
            planet="ALL",
            input_values={"civil_days_mahayuga": CIVIL_DAYS_IN_MAHAYUGA},
            output_values={"daily_motions": motions},
            units="degrees_per_day"
        )
        
        return motions
    
    def _convert_initial_longitudes(self) -> Dict[str, float]:
        """Convert initial longitudes from DMS to decimal degrees."""
        longitudes = {}
        for planet, dms in INITIAL_LONGITUDES.items():
            longitudes[planet] = dms_to_decimal(*dms)
        return longitudes
    
    def _calculate_periods(self) -> Dict[str, float]:
        """Calculate planetary periods in days."""
        periods = {}
        for planet, revolutions in PLANETARY_REVOLUTIONS.items():
            periods[planet] = CIVIL_DAYS_IN_MAHAYUGA / revolutions
        return periods
    
    def calculate_mean_longitude(self, planet: str, ahargana: float) -> float:
        """
        Calculate mean longitude with precision handling.
        Fixed: Uses modular arithmetic to reduce floating-point error.
        """
        if planet not in self.daily_motions:
            raise ValueError(f"Unknown planet: {planet}")
        
        # Reduce ahargana modulo period to minimize magnitude
        period_days = self.periods_days[planet]
        reduced_ahargana = reduce_angle_magnitude(ahargana, period_days)
        
        daily_motion = self.daily_motions[planet]
        total_motion = daily_motion * reduced_ahargana
        
        initial_longitude = self.initial_longitudes_deg[planet]
        mean_longitude = normalize_angle(initial_longitude + total_motion)
        
        # Log the calculation
        global_logger.log_correction(
            chapter=3,
            correction_type=CorrectionType.MEAN_MOTION,
            planet=planet,
            input_values={
                "ahargana": ahargana,
                "reduced_ahargana": reduced_ahargana,
                "daily_motion": daily_motion,
                "initial_longitude": initial_longitude
            },
            output_values={"mean_longitude": mean_longitude},
            units="degrees"
        )
        
        return mean_longitude
    
    def verify_against_modern(self) -> Dict[str, Dict[str, float]]:
        """
        Verify Surya Siddhanta periods against modern values.
        Fixed: Non-circular verification using independent modern data.
        """
        verification_results = {}
        
        for planet, ss_daily_motion in self.daily_motions.items():
            if planet not in MODERN_SIDEREAL_PERIODS:
                continue
                
            modern_period = MODERN_SIDEREAL_PERIODS[planet]
            modern_daily_motion = 360.0 / modern_period
            
            ss_period = 360.0 / ss_daily_motion
            
            error_daily = abs(ss_daily_motion - modern_daily_motion)
            error_period = abs(ss_period - modern_period)
            
            verification_results[planet] = {
                'ss_daily_motion': ss_daily_motion,
                'modern_daily_motion': modern_daily_motion,
                'ss_period': ss_period,
                'modern_period': modern_period,
                'daily_motion_error': error_daily,
                'period_error': error_period
            }
        
        return verification_results
    
    def calculate_for_date(self, planet: str, year: int, month: int = 1, day: int = 1) -> float:
        """Convenience method to calculate mean longitude for a specific date."""
        ahargana = calculate_precise_ahargana(year, month, day)
        return self.calculate_mean_longitude(planet, ahargana)