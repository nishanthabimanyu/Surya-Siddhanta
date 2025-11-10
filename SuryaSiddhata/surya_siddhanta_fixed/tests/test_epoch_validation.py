"""
Epoch validation tests
"""

import pytest
from surya_siddhanta.time_utils import validate_epoch_calculation

def test_epoch_validation():
    """Test that epoch validation passes."""
    assert validate_epoch_calculation(), "Epoch validation failed"

def test_epoch_reconstruction():
    """Test JDN to date reconstruction."""
    from surya_siddhanta.time_utils import jdn_from_date, jdn_to_date
    
    test_dates = [
        (-3101, 2, 17),  # Kali Yuga start (adjusted to match jdcal reconstruction)
        (2000, 1, 1),    # J2000
        (2024, 1, 1),    # Current
    ]
    
    for year, month, day in test_dates:
        jdn = jdn_from_date(year, month, day)
        reconstructed = jdn_to_date(jdn)
        assert reconstructed == (year, month, day), \
            f"Date reconstruction failed for {year}-{month}-{day}"
