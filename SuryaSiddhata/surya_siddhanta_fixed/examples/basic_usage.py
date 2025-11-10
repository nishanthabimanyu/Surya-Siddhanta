```
"""
Basic usage example for the fixed Surya Siddhanta implementation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from surya_siddhanta.calculator import SuryaSiddhantaCalculator

def main():
    """Demonstrate basic usage of the fixed implementation."""
    print("Surya Siddhanta Astronomy - Fixed Implementation")
    print("=" * 50)
    
    # Create calculator with logging enabled
    calculator = SuryaSiddhantaCalculator(enable_logging=True)
    
    # Run validation
    print("\n1. VALIDATION RESULTS:")
    validation = calculator.validate_implementation()
    
    print("✓ Epoch validation:", validation['epoch_validation'])
    print("✓ Manda physics:", validation['manda_physics_validation']['all_correct'])
    
    # Calculate positions for current date
    print("\n2. PLANETARY POSITIONS for 2024-01-15:")
    planets = ['Sun', 'Moon', 'Mars', 'Jupiter']
    
    for planet in planets:
        position = calculator.calculate_planetary_position(planet, 2024, 1, 15)
        print(f"  {planet:8}: {position['true_longitude']:6.2f}°")
    
    # Calculate lunar phenomena
    print("\n3. LUNAR PHENOMENA for 2024-01-15:")
    lunar_data = calculator.calculate_lunar_phenomena(2024, 1, 15)
    
    tithi = lunar_data['tithi']
    print(f"  Tithi: {tithi['tithi_number']} ({tithi['tithi_fraction']*100:.1f}% complete)")
    print(f"  Solar Eclipse: {lunar_data['solar_eclipse']['eclipse_occurring']}")
    print(f"  Lunar Eclipse: {lunar_data['lunar_eclipse']['eclipse_occurring']}")
    
    # Analyze conjunctions
    print("\n4. CONJUNCTION ANALYSIS for 2024-01-15:")
    conjunctions = calculator.analyze_conjunctions(2024, 1, 15)
    
    if conjunctions['conjunctions']:
        for conj in conjunctions['conjunctions']:
            p1, p2 = conj['planet1'], conj['planet2']
            sep = conj['conjunction']['separation']
            print(f"  {p1}-{p2}: {sep:.2f}° separation")
    else:
        print("  No significant conjunctions")
    
    # Save correction logs
    calculator.save_correction_logs("example_corrections.jsonl")
    summary = calculator.get_correction_summary()
    print(f"\n5. CORRECTION SUMMARY: {summary['total_entries']} entries logged")
    
    print("\n✓ All calculations completed successfully!")

if __name__ == "__main__":
    main()
```