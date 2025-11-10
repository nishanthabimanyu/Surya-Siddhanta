"""
Critical tests for the fixed Surya Siddhanta implementation
"""

import pytest
import math
from surya_siddhanta.angle_utils import *
from surya_siddhanta.time_utils import *
from surya_siddhanta.chapter3_mean_motions import MeanMotionCalculator
from surya_siddhanta.chapter4_manda_correction import MandaCorrectionCalculator

class TestCriticalFixes:
    
    def test_ahargana_epoch(self):
        """Test that Ahargana is 0 at Kali Yuga epoch."""
        ahargana = calculate_precise_ahargana(-3101, 2, 18)
        assert abs(ahargana) < 1e-6, f"Ahargana at epoch should be 0, got {ahargana}"
    
    def test_ahargana_known_dates(self):
        """Test Ahargana against known JDN differences."""
        # Test J2000 epoch (January 1, 2000)
        ahargana_2000 = calculate_precise_ahargana(2000, 1, 1)
        jdn_2000 = 2451557  # JDN for J2000 in proleptic Julian calendar (midnight)
        expected_ahargana = jdn_2000 - KALI_YUGA_EPOCH_JDN
        assert abs(ahargana_2000 - expected_ahargana) < 1.0
    
    def test_normalize_angle(self):
        """Test angle normalization handles negatives and large values."""
        assert normalize_angle(361.5) == 1.5
        assert normalize_angle(-45.0) == 315.0
        assert normalize_angle(720.0) == 0.0
        assert normalize_angle(-180.0) == 180.0
    
    def test_circular_difference(self):
        """Test circular difference calculation."""
        assert circular_difference(350, 10) == 20.0  # Straddles 0°
        assert circular_difference(10, 350) == 20.0  # Symmetric
        assert circular_difference(90, 270) == 180.0  # Maximum difference
        assert circular_difference(0, 0) == 0.0  # Same angle
    
    def test_manda_correction_physics(self):
        """Test Manda correction follows correct physical behavior."""
        manda_calc = MandaCorrectionCalculator()
        physics_test = manda_calc.test_manda_physics()
        
        assert physics_test['all_correct'], \
            f"Manda physics test failed: {physics_test}"
    
    def test_mean_motion_verification(self):
        """Test mean motion verification is non-circular."""
        motion_calc = MeanMotionCalculator()
        verification = motion_calc.verify_against_modern()
        
        # Check that we have real errors (not zero)
        for planet, results in verification.items():
            assert results['daily_motion_error'] > 0, \
                f"Circular verification detected for {planet}"
            assert results['period_error'] > 0, \
                f"Circular verification detected for {planet}"
    
    def test_unit_conversions(self):
        """Test degree/arcminute conversions are precise."""
        test_degrees = [0, 1, 45.5, 90, 180, 360]
        
        for deg in test_degrees:
            arcmin = degrees_to_arcminutes(deg)
            back_to_deg = arcminutes_to_degrees(arcmin)
            assert abs(deg - back_to_deg) < 1e-10, \
                f"Unit conversion not reversible for {deg} degrees"
    
    def test_dms_conversions(self):
        """Test DMS to decimal conversions."""
        # Test positive angles
        decimal = dms_to_decimal(45, 30, 15)
        assert abs(decimal - 45.5041666667) < 1e-6
        
        d, m, s = decimal_to_dms(45.5041666667)
        assert d == 45 and m == 30 and abs(s - 15) < 0.1
        
        # Test negative angles
        decimal = dms_to_decimal(-45, 30, 15)
        assert abs(decimal - (-45.5041666667)) < 1e-6

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
