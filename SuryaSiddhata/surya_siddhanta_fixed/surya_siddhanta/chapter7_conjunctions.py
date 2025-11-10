"""
Chapter 7: Planetary Conjunctions & Special Configurations
Fixed: Robust circular window detection, stable interpolation, proper thresholds
"""

import math
from typing import Dict, Any, List, Tuple
from itertools import combinations

from .angle_utils import (normalize_angle, circular_difference, circular_mean, 
                         calculate_angular_separation_exact
                         )
from .constants import CONJUNCTION_LIMITS
from .correction_logger import global_logger, CorrectionType


class ConjunctionCalculator:
    """
    Calculate planetary conjunctions and special configurations.
    Fixed: Robust algorithms for circular statistics and configuration detection.
    """
    
    def __init__(self):
        self.limits = CONJUNCTION_LIMITS
    
    def check_conjunction(self, planet1_data: Dict[str, float], 
                         planet2_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Check for conjunction between two planets.
        Fixed: Uses exact angular separation calculation.
        """
        lon1, lat1 = planet1_data['longitude'], planet1_data.get('latitude', 0)
        lon2, lat2 = planet2_data['longitude'], planet2_data.get('latitude', 0)
        
        separation = calculate_angular_separation_exact(lon1, lat1, lon2, lat2)
        lon_diff = circular_difference(lon1, lon2)
        lat_diff = abs(lat1 - lat2) if lat1 is not None and lat2 is not None else 0
        
        is_exact_conjunction = (separation <= self.limits['Exact_Conjunction'] and
                              lat_diff <= self.limits['Exact_Conjunction'])
        
        is_close_conjunction = separation <= self.limits['Close_Conjunction']
        
        result = {
            'separation': separation,
            'longitude_difference': lon_diff,
            'latitude_difference': lat_diff,
            'is_exact_conjunction': is_exact_conjunction,
            'is_close_conjunction': is_close_conjunction,
            'planets': [planet1_data.get('name', 'Unknown'), 
                       planet2_data.get('name', 'Unknown')]
        }
        
        if is_exact_conjunction or is_close_conjunction:
            global_logger.log_correction(
                chapter=7,
                correction_type=CorrectionType.CONJUNCTION,
                planet=f"{planet1_data.get('name')}-{planet2_data.get('name')}",
                input_values={
                    "planet1_longitude": lon1,
                    "planet2_longitude": lon2,
                    "planet1_latitude": lat1,
                    "planet2_latitude": lat2
                },
                output_values=result,
                units="degrees"
            )
        
        return result
    
    def check_planetary_group(self, planets_data: Dict[str, Dict[str, float]], 
                            min_planets: int = 3) -> Dict[str, Any]:
        """
        Detect planetary groups using robust circular statistics.
        Fixed: Proper handling of circular window around 0°.
        """
        if len(planets_data) < min_planets:
            return {'is_group': False, 'reason': f'Need at least {min_planets} planets'}
        
        longitudes = [data['longitude'] for data in planets_data.values()]
        
        # Robust circular window detection
        sorted_lons = sorted(longitudes)
        
        # Check all possible circular windows
        min_range = float('inf')
        
        # Duplicate the array to handle circular cases
        extended_lons = sorted_lons + [lon + 360 for lon in sorted_lons]
        
        for i in range(len(sorted_lons)):
            window_end = i + len(sorted_lons) - 1
            if window_end >= len(extended_lons):
                continue
                
            window_range = extended_lons[window_end] - extended_lons[i]
            if window_range < min_range:
                min_range = window_range
        
        is_group = min_range <= self.limits['Planetary_Group']
        
        result = {
            'is_group': is_group,
            'group_size': len(planets_data),
            'min_longitude_range': min_range,
            'group_limit': self.limits['Planetary_Group'],
            'planet_names': list(planets_data.keys())
        }
        
        if is_group:
            global_logger.log_correction(
                chapter=7,
                correction_type=CorrectionType.CONJUNCTION,
                planet="GROUP",
                input_values={"longitudes": longitudes},
                output_values=result,
                units="degrees"
            )
        
        return result
    
    def check_special_configurations(self, planet1_data: Dict[str, float],
                                   planet2_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Check for special planetary configurations.
        """
        lon1, lat1 = planet1_data['longitude'], planet1_data.get('latitude', 0)
        lon2, lat2 = planet2_data['longitude'], planet2_data.get('latitude', 0)
        
        lon_diff = circular_difference(lon1, lon2)
        
        is_opposition = abs(lon_diff - 180) <= self.limits['Opposition']
        is_quadrature_90 = abs(lon_diff - 90) <= self.limits['Quadrature']
        is_quadrature_270 = abs(lon_diff - 270) <= self.limits['Quadrature']
        is_quadrature = is_quadrature_90 or is_quadrature_270
        
        conjunction_check = self.check_conjunction(planet1_data, planet2_data)
        is_conjunction = conjunction_check['is_exact_conjunction']
        
        configuration_type = "None"
        if is_conjunction:
            configuration_type = "Conjunction"
        elif is_opposition:
            configuration_type = "Opposition"
        elif is_quadrature:
            configuration_type = "Quadrature"
        
        result = {
            'configuration_type': configuration_type,
            'is_opposition': is_opposition,
            'is_quadrature': is_quadrature,
            'is_conjunction': is_conjunction,
            'longitude_difference': lon_diff,
            'separation': conjunction_check['separation']
        }
        
        if configuration_type != "None":
            global_logger.log_correction(
                chapter=7,
                correction_type=CorrectionType.CONJUNCTION,
                planet=f"{planet1_data.get('name')}-{planet2_data.get('name')}",
                input_values={
                    "planet1_longitude": lon1,
                    "planet2_longitude": lon2,
                    "longitude_difference": lon_diff
                },
                output_values=result,
                units="degrees"
            )
        
        return result
    
    def refine_conjunction_time(self, time_points: List[float], 
                              separation_values: List[float]) -> float:
        """
        Refine conjunction timing using stable Lagrange interpolation.
        Fixed: Replaces unstable quadratic fitting.
        """
        from .chapter5_sighra_correction import SighraCorrectionCalculator
        
        sighra_calc = SighraCorrectionCalculator()
        return sighra_calc.refine_minimum_time_lagrange(time_points, separation_values)
    
    def analyze_all_conjunctions(self, planets_data: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """
        Analyze all possible planetary conjunctions and configurations.
        """
        conjunctions = []
        planet_names = list(planets_data.keys())
        
        for i, name1 in enumerate(planet_names):
            for j, name2 in enumerate(planet_names):
                if i >= j:  # Avoid duplicates and self-comparison
                    continue
                
                data1 = planets_data[name1]
                data2 = planets_data[name2]
                
                conjunction = self.check_conjunction(data1, data2)
                special_config = self.check_special_configurations(data1, data2)
                
                if (conjunction['is_exact_conjunction'] or 
                    conjunction['is_close_conjunction'] or
                    special_config['configuration_type'] != "None"):
                    
                    result = {
                        'planet1': name1,
                        'planet2': name2,
                        'conjunction': conjunction,
                        'special_configuration': special_config
                    }
                    conjunctions.append(result)
        
        return conjunctions