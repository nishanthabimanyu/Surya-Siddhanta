"""
Precise time utilities using Julian Day Number exclusively
Fixed: Single authoritative Ahargana calculation with proleptic Julian calendar
"""

import math
from typing import Tuple
import jdcal

def is_julian_leap_year(year: int) -> bool:
    """
    Check if year is leap in proleptic Julian calendar.
    Astronomical year numbering: year 0 = 1 BCE
    """
    return year % 4 == 0

def _days_in_month(year: int, month: int) -> int:
    """
    Returns the number of days in a given month for a given year (Julian calendar).
    """
    if month == 2:
        return 29 if is_julian_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def jdn_from_date(year: int, month: int, day: int) -> int:
    """
    Convert date to Julian Day Number (proleptic Julian calendar).
    Uses astronomical year numbering: year 0 = 1 BCE, year -1 = 2 BCE, etc.
    Uses jdcal.jcal2jd for robust conversion, adjusted for midnight.
    
    Args:
        year: Astronomical year (0 = 1 BCE, -1 = 2 BCE, etc.)
        month: Month (1-12)
        day: Day (1-31)
    
    Returns:
        Julian Day Number
    
    Raises:
        ValueError: If the month or day is invalid.
    """
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")
    
    max_day = _days_in_month(year, month)
    if not (1 <= day <= max_day):
        raise ValueError(f"Invalid day: {day} for month {month} in year {year}. Day must be between 1 and {max_day}.")

    jd1, jd2 = jdcal.jcal2jd(year, month, day)
    return int(jd1 + jd2 - 0.5)

# Epoch: Kali Yuga start, February 18, 3102 BCE (astronomical year -3101)
KALI_YUGA_EPOCH_JDN = 588465

def calculate_precise_ahargana(year: int, month: int = 1, day: int = 1) -> float:
    """
    Calculate Ahargana using precise JDN difference.
    This is the SINGLE authoritative Ahargana calculation.
    
    Args:
        year: Astronomical year (0 = 1 BCE, -1 = 2 BCE, etc.)
        month: Month (1-12)
        day: Day (1-31)
    
    Returns:
        Ahargana (elapsed days since Kali Yuga start)
    """
    target_jdn = jdn_from_date(year, month, day)
    ahargana = target_jdn - KALI_YUGA_EPOCH_JDN
    
    # Verify we get integer days for known dates
    if year == -3101 and month == 2 and day == 18:
        assert abs(ahargana) < 1e-6, f"Epoch Ahargana should be 0, got {ahargana}"
    
    return ahargana

def jdn_to_date(jdn: int) -> Tuple[int, int, int]:
    """
    Convert Julian Day Number back to date (proleptic Julian calendar).
    Returns (year, month, day) in astronomical year numbering.
    Uses jdcal.jd2jcal for robust conversion, adjusted for midnight JDN input.
    """
    year, month, day, fractional_day = jdcal.jd2jcal(jdn + 0.5, 0.0) # Adjust JDN to JD for noon
    return (year, month, day)

def validate_epoch_calculation():
    """Validate that our epoch calculation is correct."""
    epoch_jdn = KALI_YUGA_EPOCH_JDN # Use the hardcoded JDN
    reconstructed_date = jdn_to_date(epoch_jdn)
    
    assert reconstructed_date == (-3101, 2, 18), \
        f"Epoch date reconstruction failed: {reconstructed_date}"
    
    # Also check that jdn_from_date for the original date gives the expected JDN
    calculated_jdn_from_date = jdn_from_date(-3101, 2, 18)
    assert calculated_jdn_from_date == KALI_YUGA_EPOCH_JDN, \
        f"jdn_from_date for epoch date is incorrect: {calculated_jdn_from_date}"
    
    ahargana = calculate_precise_ahargana(-3101, 2, 18)
    assert abs(ahargana) < 1e-6, f"Epoch Ahargana not zero: {ahargana}"
    
    return True
