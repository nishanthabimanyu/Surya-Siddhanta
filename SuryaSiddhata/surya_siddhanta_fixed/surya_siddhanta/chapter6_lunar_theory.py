"""
Chapter 6: Lunar Theory & Eclipses
Fixed: Proper eclipse conditions, latitude calculation, threshold handling
"""

import math
from typing import Dict, Any, List

from .angle_utils import normalize_angle, circular_difference
from .constants import LUNAR_CONSTANTS
from .correction_logger import global_logger, CorrectionType

class LunarTheoryCalculator:
    """
    Calculate lunar phenomena with proper eclipse conditions.
    Fixed: Realistic thresholds, proper geometry for eclipse detection.
    """
    
    def __init__(self):
        self.max_inclination = LUNAR_CONSTANTS['Max_Inclination']
        self.solar_eclipse_limit = LUNAR_CONSTANTS['Solar_Eclipse_Limit']
        self.lunar_eclipse_limit = LUNAR_CONSTANTS['Lunar_Eclipse_Limit']
    
    def calculate_lunar_latitude(self, moon_longitude: float, 
                               rahu_longitude: float) -> Dict[str, float]:
        """
        Calculate lunar latitude using Surya Siddhanta formula.
        β = i × sin(λ_moon - λ_rahu)
        """
        argument = normalize_angle(moon_longitude - rahu_longitude)
        argument_rad = math.radians(argument)
        
        latitude = self.max_inclination * math.sin(argument_rad)
        
        result = {
            'latitude': latitude,
            'argument': argument,
            'max_inclination': self.max_inclination
        }
        
        global_logger.log_correction(
            chapter=6,
            correction_type=CorrectionType.LUNAR_LATITUDE,
            planet="Moon",
            input_values={
                "moon_longitude": moon_longitude,
                "rahu_longitude": rahu_longitude,
                "argument": argument
            },
            output_values=result,
            units="degrees"
        )
        
        return result
    
    def calculate_tithi(self, moon_longitude: float, sun_longitude: float) -> Dict[str, Any]:
        """
        Calculate Tithi (lunar day) and time to next Tithi.
        Tithi = (λ_moon - λ_sun) / 12°
        """
        elongation = normalize_angle(moon_longitude - sun_longitude)
        
        tithi_decimal = elongation / 12.0
        tithi_number = int(tithi_decimal) + 1
        tithi_fraction = tithi_decimal - int(tithi_decimal)
        
        # Calculate time to next Tithi (simplified)
        moon_daily_motion = 13.176396  # degrees/day
        sun_daily_motion = 0.985647    # degrees/day
        relative_motion = moon_daily_motion - sun_daily_motion
        
        time_to_next_tithi_days = (1 - tithi_fraction) * 12.0 / relative_motion
        
        result = {
            'elongation': elongation,
            'tithi_decimal': tithi_decimal,
            'tithi_number': tithi_number,
            'tithi_fraction': tithi_fraction,
            'time_to_next_tithi_days': time_to_next_tithi_days,
            'time_to_next_tithi_hours': time_to_next_tithi_days * 24
        }
        
        global_logger.log_correction(
            chapter=6,
            correction_type=CorrectionType.TITHI,
            planet="Moon",
            input_values={
                "moon_longitude": moon_longitude,
                "sun_longitude": sun_longitude,
                "elongation": elongation
            },
            output_values=result,
            units="degrees_and_days"
        )
        
        return result
    
    def check_solar_eclipse_conditions(self, moon_longitude: float, sun_longitude: float,
                                     rahu_longitude: float, moon_latitude: float) -> Dict[str, Any]:
        """
        Check conditions for solar eclipse with realistic thresholds.
        Fixed: Proper syzygy and node proximity conditions.
        """
        # Condition 1: New Moon (conjunction)
        elongation = circular_difference(moon_longitude, sun_longitude)
        new_moon_threshold = 1.0  # degrees
        
        # Condition 2: Proximity to node
        node_distance = circular_difference(moon_longitude, rahu_longitude)
        
        is_new_moon = elongation <= new_moon_threshold
        is_near_node = (node_distance <= self.solar_eclipse_limit or 
                       abs(moon_latitude) <= 2.0)
        
        eclipse_occurring = is_new_moon and is_near_node
        
        # Calculate qualitative magnitude
        if eclipse_occurring:
            magnitude = 1.0 - (node_distance / self.solar_eclipse_limit)
            magnitude = max(0.0, min(1.0, magnitude))
        else:
            magnitude = 0.0
        
        result = {
            'eclipse_occurring': eclipse_occurring,
            'eclipse_type': 'solar',
            'magnitude': magnitude,
            'elongation': elongation,
            'node_distance': node_distance,
            'is_new_moon': is_new_moon,
            'is_near_node': is_near_node,
            'moon_latitude': moon_latitude
        }
        
        global_logger.log_correction(
            chapter=6,
            correction_type=CorrectionType.ECLIPSE_CHECK,
            planet="Moon",
            input_values={
                "moon_longitude": moon_longitude,
                "sun_longitude": sun_longitude,
                "rahu_longitude": rahu_longitude,
                "moon_latitude": moon_latitude
            },
            output_values=result,
            units="degrees"
        )
        
        return result
    
    def check_lunar_eclipse_conditions(self, moon_longitude: float, sun_longitude: float,
                                     rahu_longitude: float, moon_latitude: float) -> Dict[str, Any]:
        """
        Check conditions for lunar eclipse.
        """
        opposition_longitude = normalize_angle(sun_longitude + 180)
        elongation = circular_difference(moon_longitude, opposition_longitude)
        full_moon_threshold = 1.0  # degrees
        
        node_distance = circular_difference(moon_longitude, rahu_longitude)
        
        is_full_moon = elongation <= full_moon_threshold
        is_near_node = (node_distance <= self.lunar_eclipse_limit or 
                       abs(moon_latitude) <= 2.0)
        
        eclipse_occurring = is_full_moon and is_near_node
        
        if eclipse_occurring:
            magnitude = 1.0 - (node_distance / self.lunar_eclipse_limit)
            magnitude = max(0.0, min(1.0, magnitude))
        else:
            magnitude = 0.0
        
        result = {
            'eclipse_occurring': eclipse_occurring,
            'eclipse_type': 'lunar',
            'magnitude': magnitude,
            'elongation': elongation,
            'node_distance': node_distance,
            'is_full_moon': is_full_moon,
            'is_near_node': is_near_node,
            'moon_latitude': moon_latitude
        }
        
        global_logger.log_correction(
            chapter=6,
            correction_type=CorrectionType.ECLIPSE_CHECK,
            planet="Moon",
            input_values={
                "moon_longitude": moon_longitude,
                "sun_longitude": sun_longitude,
                "rahu_longitude": rahu_longitude,
                "moon_latitude": moon_latitude
            },
            output_values=result,
            units="degrees"
        )
        
        return result
    
    def predict_eclipse_season(self, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """
        Predict potential eclipse seasons for a range of years.
        """
        eclipses = []
        
        for year in range(start_year, end_year + 1):
            # Simplified: check every new and full moon
            for month in range(1, 13):
                for day in [1, 15]:  # Approximate new and full moons
                    # This would need actual lunar/solar positions
                    # Placeholder for actual implementation
                    pass
        
        return eclipses