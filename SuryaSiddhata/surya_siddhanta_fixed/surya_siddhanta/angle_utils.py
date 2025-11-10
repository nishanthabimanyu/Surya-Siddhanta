"""
Centralized angle utilities for Surya Siddhanta calculations
Fixed: Consistent normalization, circular operations, and unit conversions
"""

import math
import numpy as np
from typing import Tuple, List

def normalize_angle(x: float) -> float:
    """Normalize angle to [0, 360) degrees with precise floating-point handling."""
    normalized = x % 360.0
    if normalized < 0:
        normalized += 360.0
    return normalized

def circular_difference(angle1: float, angle2: float) -> float:
    """Smallest circular difference between two angles in degrees [0, 180]."""
    diff = abs(angle1 - angle2) % 360.0
    return min(diff, 360.0 - diff)

def circular_mean(angles: List[float]) -> float:
    """Compute circular mean of angles in degrees."""
    if not angles:
        return 0.0
    
    angles_rad = [math.radians(angle) for angle in angles]
    sum_sin = sum(math.sin(angle) for angle in angles_rad)
    sum_cos = sum(math.cos(angle) for angle in angles_rad)
    
    if abs(sum_sin) < 1e-12 and abs(sum_cos) < 1e-12:
        return 0.0  # Undefined direction
    
    mean_rad = math.atan2(sum_sin, sum_cos)
    return normalize_angle(math.degrees(mean_rad))

def degrees_to_arcminutes(degrees: float) -> float:
    """Convert decimal degrees to arcminutes."""
    return degrees * 60.0

def arcminutes_to_degrees(arcminutes: float) -> float:
    """Convert arcminutes to decimal degrees."""
    return arcminutes / 60.0

def dms_to_decimal(degrees: int, minutes: int, seconds: float) -> float:
    """Convert degrees, minutes, seconds to decimal degrees."""
    sign = 1 if degrees >= 0 else -1
    return sign * (abs(degrees) + minutes/60.0 + seconds/3600.0)

def decimal_to_dms(decimal_degrees: float) -> Tuple[int, int, float]:
    """Convert decimal degrees to degrees, minutes, seconds."""
    sign = -1 if decimal_degrees < 0 else 1
    decimal_degrees = abs(decimal_degrees)
    
    degrees = int(decimal_degrees)
    minutes_decimal = (decimal_degrees - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    return (sign * degrees, minutes, seconds)

def reduce_angle_magnitude(angle: float, period: float) -> float:
    """Reduce angle magnitude using modular arithmetic to minimize floating-point error."""
    return angle % period

def calculate_angular_separation_exact(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the exact angular separation between two points on a sphere
    given their longitudes and latitudes (in degrees).
    Uses the Haversine formula for spherical distance.
    """
    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Convert back to degrees
    separation_degrees = math.degrees(c)
    return separation_degrees