"""
Main Surya Siddhanta Calculator
Fixed: Integrates all chapters with consistent Ahargana and unit handling
"""

from typing import Dict, Any, List

from .time_utils import calculate_precise_ahargana
from .chapter3_mean_motions import MeanMotionCalculator
from .chapter4_manda_correction import MandaCorrectionCalculator
from .chapter5_sighra_correction import SighraCorrectionCalculator
from .chapter6_lunar_theory import LunarTheoryCalculator
from .chapter7_conjunctions import ConjunctionCalculator
from .correction_logger import global_logger, CorrectionType

class SuryaSiddhantaCalculator:
    """
    Complete Surya Siddhanta implementation with all critical fixes.
    """
    
    def __init__(self, enable_logging: bool = True):
        self.enable_logging = enable_logging
        global_logger.enabled = enable_logging
        
        # Initialize all chapter calculators
        self.mean_motion = MeanMotionCalculator()
        self.manda_correction = MandaCorrectionCalculator()
        self.sighra_correction = SighraCorrectionCalculator()
        self.lunar_theory = LunarTheoryCalculator()
        self.conjunctions = ConjunctionCalculator()
        
        # Planetary data cache
        self._position_cache = {}
    
    def calculate_planetary_position(self, planet: str, year: int, 
                                   month: int = 1, day: int = 1) -> Dict[str, Any]:
        """
        Calculate complete planetary position with all corrections.
        Fixed: Single Ahargana source, proper correction chaining.
        """
        # Use precise Ahargana exclusively
        ahargana = calculate_precise_ahargana(year, month, day)
        
        global_logger.log_correction(
            chapter=2,
            correction_type=CorrectionType.AHARGANA,
            planet=planet,
            input_values={"year": year, "month": month, "day": day},
            output_values={"ahargana": ahargana},
            units="days"
        )
        
        # Calculate mean longitude
        mean_longitude = self.mean_motion.calculate_mean_longitude(planet, ahargana)
        
        # Apply Manda correction
        manda_corrected = self.manda_correction.apply_manda_correction(planet, mean_longitude)
        
        result = {
            'planet': planet,
            'date': f"{year}-{month:02d}-{day:02d}",
            'ahargana': ahargana,
            'mean_longitude': mean_longitude,
            'manda_corrected': manda_corrected,
            'true_longitude': manda_corrected,  # Default for Sun/Moon
            'corrections_applied': ['mean_motion', 'manda']
        }
        
        # Apply Sighra correction for planets (not Sun/Moon)
        if planet in ['Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            sun_mean = self.mean_motion.calculate_mean_longitude('Sun', ahargana)
            sun_true = self.manda_correction.apply_manda_correction('Sun', sun_mean)
            
            sighra_result = self.sighra_correction.apply_sighra_correction(
                planet, manda_corrected, sun_true
            )
            
            result.update({
                'true_longitude': sighra_result['true_longitude'],
                'sighra_kendra': sighra_result['sighra_kendra'],
                'sighra_phala': sighra_result['sighra_phala'],
                'sighra_karna': sighra_result['sighra_karna'],
                'is_approximate': sighra_result.get('is_approximate', False)
            })
            result['corrections_applied'].append('sighra')
        
        # Cache the result
        cache_key = f"{planet}_{year}_{month}_{day}"
        self._position_cache[cache_key] = result
        
        return result
    
    def calculate_lunar_phenomena(self, year: int, month: int = 1, 
                                day: int = 1) -> Dict[str, Any]:
        """
        Calculate lunar positions and phenomena.
        """
        # Get lunar and solar positions
        moon_data = self.calculate_planetary_position('Moon', year, month, day)
        sun_data = self.calculate_planetary_position('Sun', year, month, day)
        rahu_data = self.calculate_planetary_position('Moon_Node', year, month, day)
        
        moon_long = moon_data['true_longitude']
        sun_long = sun_data['true_longitude']
        rahu_long = rahu_data['true_longitude']
        
        # Calculate lunar phenomena
        latitude_result = self.lunar_theory.calculate_lunar_latitude(moon_long, rahu_long)
        tithi_result = self.lunar_theory.calculate_tithi(moon_long, sun_long)
        
        solar_eclipse = self.lunar_theory.check_solar_eclipse_conditions(
            moon_long, sun_long, rahu_long, latitude_result['latitude']
        )
        lunar_eclipse = self.lunar_theory.check_lunar_eclipse_conditions(
            moon_long, sun_long, rahu_long, latitude_result['latitude']
        )
        
        return {
            'date': f"{year}-{month:02d}-{day:02d}",
            'moon_longitude': moon_long,
            'sun_longitude': sun_long,
            'rahu_longitude': rahu_long,
            'lunar_latitude': latitude_result,
            'tithi': tithi_result,
            'solar_eclipse': solar_eclipse,
            'lunar_eclipse': lunar_eclipse
        }
    
    def analyze_conjunctions(self, year: int, month: int = 1, 
                           day: int = 1) -> Dict[str, Any]:
        """
        Analyze planetary conjunctions for given date.
        """
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        positions = {}
        
        # Get all planetary positions
        for planet in planets:
            data = self.calculate_planetary_position(planet, year, month, day)
            positions[planet] = {
                'name': planet,
                'longitude': data['true_longitude'],
                'latitude': 0.0  # Simplified - would need actual latitude
            }
        
        # Analyze conjunctions
        all_conjunctions = self.conjunctions.analyze_all_conjunctions(positions)
        group_check = self.conjunctions.check_planetary_group(positions)
        
        return {
            'date': f"{year}-{month:02d}-{day:02d}",
            'planetary_positions': positions,
            'conjunctions': all_conjunctions,
            'planetary_groups': group_check
        }
    
    def validate_implementation(self) -> Dict[str, Any]:
        """
        Run comprehensive validation of the implementation.
        """
        validation_results = {}
        
        # Validate epoch calculation
        from .time_utils import validate_epoch_calculation
        validation_results['epoch_validation'] = validate_epoch_calculation()
        
        # Validate mean motions against modern values
        validation_results['mean_motion_validation'] = self.mean_motion.verify_against_modern()
        
        # Validate Manda correction physics
        validation_results['manda_physics_validation'] = self.manda_correction.test_manda_physics()
        
        # Test known dates
        test_dates = [
            (2000, 1, 1, "J2000 epoch"),
            (2024, 1, 1, "Current year"),
        ]
        
        position_tests = {}
        for year, month, day, description in test_dates:
            sun_pos = self.calculate_planetary_position('Sun', year, month, day)
            moon_pos = self.calculate_planetary_position('Moon', year, month, day)
            position_tests[description] = {
                'sun_longitude': sun_pos['true_longitude'],
                'moon_longitude': moon_pos['true_longitude']
            }
        
        validation_results['position_tests'] = position_tests
        
        return validation_results
    
    def save_correction_logs(self, filename: str = "surya_siddhanta_corrections.jsonl"):
        """Save all correction logs to file."""
        if self.enable_logging:
            global_logger.save_to_file(filename)
    
    def get_correction_summary(self) -> Dict[str, Any]:
        """Get summary of all corrections applied."""
        return global_logger.get_summary()