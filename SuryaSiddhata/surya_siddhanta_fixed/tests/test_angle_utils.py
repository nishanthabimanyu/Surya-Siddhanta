"""
Tests for angle utilities.
"""

import pytest
import math
from surya_siddhanta.angle_utils import *

def test_normalize_angle():
    """Test angle normalization."""
    assert normalize_angle(361.5) == 1.5
    assert normalize_angle(-45.0) == 315.0
    assert normalize_angle(720.0) == 0.0
    assert normalize_angle(0.0) == 0.0
    assert normalize_angle(360.0) == 0.0

def test_circular_difference():
    """Test circular difference calculation."""
    assert circular_difference(10, 350) == 20.0
    assert circular_difference(350, 10) == 20.0
    assert circular_difference(90, 270) == 180.0
    assert circular_difference(270, 90) == 180.0
    assert circular_difference(180, 180) == 0.0
    assert circular_difference(0, 180) == 180.0

def test_circular_mean():
    """Test circular mean calculation."""
    assert circular_difference(circular_mean([10, 350]), 0.0) < 1e-9
    assert abs(circular_mean([80, 100]) - 90.0) < 1e-9
    assert abs(circular_mean([170, 190]) - 180.0) < 1e-9
    assert abs(circular_mean([0, 0, 0]) - 0.0) < 1e-9
    assert circular_mean([]) == 0.0

def test_dms_conversion():
    """Test DMS to decimal and back."""
    d, m, s = 45, 30, 15
    decimal = dms_to_decimal(d, m, s)
    assert abs(decimal - 45.5041666667) < 1e-6
    
    rd, rm, rs = decimal_to_dms(decimal)
    assert rd == d and rm == m and abs(rs - s) < 0.1

    # Test negative angle
    d, m, s = -45, 30, 15
    decimal = dms_to_decimal(d, m, s)
    assert abs(decimal - (-45.5041666667)) < 1e-6
    
    rd, rm, rs = decimal_to_dms(decimal)
    assert rd == d and rm == m and abs(rs - s) < 0.1

def test_arcminutes_conversion():
    """Test degrees to arcminutes and back."""
    degrees = 10.5
    arcminutes = degrees_to_arcminutes(degrees)
    assert arcminutes == 630.0
    
    r_degrees = arcminutes_to_degrees(arcminutes)
    assert r_degrees == degrees

def test_reduce_angle_magnitude():
    """Test angle magnitude reduction."""
    assert abs(reduce_angle_magnitude(1000.0, 360.0) - 280.0) < 1e-9
    assert abs(reduce_angle_magnitude(8000.0, 180.0) - 80.0) < 1e-9

def test_calculate_angular_separation_exact():
    """Test angular separation calculation."""
    # Test 1: Same point
    assert calculate_angular_separation_exact(0, 0, 0, 0) == 0.0
    
    # Test 2: North pole to south pole
    assert abs(calculate_angular_separation_exact(0, 90, 0, -90) - 180.0) < 1e-9
    
    # Test 3: 90 degrees longitude difference on equator
    assert abs(calculate_angular_separation_exact(0, 0, 90, 0) - 90.0) < 1e-9
    
    # Test 4: A known distance (e.g., London to Paris)
    # London: 51.5074 N, 0.1278 W -> lat=51.5074, lon=-0.1278
    # Paris: 48.8566 N, 2.3522 E -> lat=48.8566, lon=2.3522
    # Expected distance is approx 344 km, which is about 3.09 degrees on Earth's surface.
    # This test is not about Earth distance, but angular separation.
    separation = calculate_angular_separation_exact(-0.1278, 51.5074, 2.3522, 48.8566)
    # Let's check with an online calculator.
    # https://www.movable-type.co.uk/scripts/latlong.html gives 3.09 degrees.
    assert abs(separation - 3.09) < 0.01

if __name__ == "__main__":
    pytest.main()
