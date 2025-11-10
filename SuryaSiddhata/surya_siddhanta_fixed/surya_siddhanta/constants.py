"""
Constants for Surya Siddhanta calculations
Fixed: Clear unit documentation and precise values
"""

import math
from typing import Dict, Tuple

# Time constants
CIVIL_DAYS_IN_MAHAYUGA = 1577917500
KALI_YUGA_START_YEAR = -3101  # Astronomical year for 3102 BCE

# Surya Siddhanta trigonometric constant
SINE_RADIUS = 3438  # R = 3438 minutes

# Planetary revolutions in Mahayuga (Chapter 2)
PLANETARY_REVOLUTIONS = {
    'Sun': 4320000,
    'Moon': 57753336,
    'Mercury': 17937000,
    'Venus': 7022388,
    'Mars': 2296824,
    'Jupiter': 364220,
    'Saturn': 146564,
    'Moon_Apogee': 488219,    # Mandocca
    'Moon_Node': 232226,      # Rahu
}

# Initial longitudes at Kali Yuga start (Chapter 3)
# Format: (degrees, minutes, seconds)
INITIAL_LONGITUDES = {
    'Sun': (0, 0, 0),
    'Moon': (0, 0, 0),
    'Mars': (164, 11, 34),
    'Mercury': (220, 2, 16),
    'Jupiter': (154, 1, 56),
    'Venus': (0, 0, 0),  # Approximately
    'Saturn': (249, 7, 3),
    'Moon_Apogee': (80, 0, 0),
    'Moon_Node': (0, 0, 0),
}

# Manda Paridhi (Epicycle circumference) in degrees (Chapter 4)
MANDA_PARIDHI = {
    'Sun': 13 + 40/60,      # 13°40'
    'Moon': 31 + 30/60,     # 31°30'
    'Mars': 70.0,           # 70°00'
    'Mercury': 28.0,        # 28°00'
    'Jupiter': 32.0,        # 32°00'
    'Venus': 11.0,          # 11°00'
    'Saturn': 48.0,         # 48°00'
}

# Mandocca (Apogee) positions at Kali Yuga start in degrees (Chapter 4)
MANDOCCA_POSITIONS = {
    'Sun': 80.0,      # Verse 4.3
    'Moon': 80.0,     # Verse 4.4
    'Mars': 130.0,    # Verse 4.5
    'Mercury': 220.0, # Verse 4.6
    'Jupiter': 160.0, # Verse 4.7
    'Venus': 80.0,    # Verse 4.8
    'Saturn': 240.0,  # Verse 4.8
}

# Sighra Paridhi (Epicycle radius) in degrees (Chapter 5)
SIGHRA_PARIDHI = {
    'Mars': 235.0,           # Verse 5.1
    'Mercury': 131 + 30/60,  # 131°30' - Verse 5.2
    'Jupiter': 72.0,         # Verse 5.3
    'Venus': 260.0,          # Verse 5.4
    'Saturn': 39.0,          # Verse 5.5
}

# Planet types for Sighra correction
PLANET_TYPES = {
    'Mars': 'superior',
    'Jupiter': 'superior', 
    'Saturn': 'superior',
    'Mercury': 'inferior',
    'Venus': 'inferior'
}

# Lunar constants (Chapter 6)
LUNAR_CONSTANTS = {
    'Max_Inclination': 4.5,  # degrees (Verse 6.1)
    'Solar_Eclipse_Limit': 12.0,  # degrees
    'Lunar_Eclipse_Limit': 10.0,  # degrees
}

# Modern astronomical constants for validation
MODERN_SIDEREAL_PERIODS = {
    'Sun': 365.256363,      # Sidereal year (days)
    'Moon': 27.321661,      # Sidereal month (days)
    'Mercury': 87.969257,   # Sidereal period (days)
    'Venus': 224.7008,      # Sidereal period (days)
    'Mars': 686.98,         # Sidereal period (days)
    'Jupiter': 4332.59,     # Sidereal period (days)
    'Saturn': 10746.94,     # Sidereal period (days)
}

# Conjunction and configuration limits (Chapter 7)
CONJUNCTION_LIMITS = {
    'Exact_Conjunction': 1.0,      # degrees
    'Close_Conjunction': 5.0,      # degrees  
    'Graha_Yuddha_Longitude': 1.0, # degrees
    'Graha_Yuddha_Latitude': 1.0,  # degrees
    'Planetary_Group': 30.0,       # degrees
    'Opposition': 5.0,             # degrees
    'Quadrature': 5.0,             # degrees
}