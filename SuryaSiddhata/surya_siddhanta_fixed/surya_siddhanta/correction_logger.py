"""
Structured logging for all astronomical corrections
Fixed: Comprehensive logging with unit tracking
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class CorrectionType(Enum):
    AHARGANA = "ahargana"
    MEAN_MOTION = "mean_motion"
    MANDA_CORRECTION = "manda_correction"
    SIGHRA_CORRECTION = "sighra_correction"
    LUNAR_LATITUDE = "lunar_latitude"
    TITHI = "tithi"
    ECLIPSE_CHECK = "eclipse_check"
    CONJUNCTION = "conjunction"

@dataclass
class CorrectionEntry:
    timestamp: str
    chapter: int
    correction_type: str
    planet: str
    input_values: Dict[str, Any]
    output_values: Dict[str, Any]
    units: str
    metadata: Optional[Dict[str, Any]] = None

class CorrectionLogger:
    """
    Structured logger for tracking all astronomical corrections.
    Essential for debugging and validation.
    """
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.entries: List[CorrectionEntry] = []
    
    def log_correction(self, 
                      chapter: int,
                      correction_type: CorrectionType,
                      planet: str,
                      input_values: Dict[str, Any],
                      output_values: Dict[str, Any],
                      units: str = "degrees",
                      metadata: Optional[Dict[str, Any]] = None):
        """
        Log a correction step with full context.
        
        Args:
            chapter: Surya Siddhanta chapter number
            correction_type: Type of correction being applied
            planet: Planet or body being calculated
            input_values: Input parameters for the calculation
            output_values: Output results of the calculation
            units: Units used in the calculation
            metadata: Additional context information
        """
        if not self.enabled:
            return
            
        entry = CorrectionEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            chapter=chapter,
            correction_type=correction_type.value,
            planet=planet,
            input_values=input_values,
            output_values=output_values,
            units=units,
            metadata=metadata or {}
        )
        
        self.entries.append(entry)
    
    def get_entries(self) -> List[Dict[str, Any]]:
        """Get all log entries as JSON-serializable dictionaries."""
        return [asdict(entry) for entry in self.entries]
    
    def save_to_file(self, filename: str):
        """Save logs to JSONL file (one entry per line)."""
        if not self.enabled:
            return
            
        with open(filename, 'w', encoding='utf-8') as f:
            for entry_dict in self.get_entries():
                f.write(json.dumps(entry_dict, ensure_ascii=False) + '\n')
    
    def clear(self):
        """Clear all log entries."""
        self.entries.clear()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of logged corrections."""
        if not self.entries:
            return {}
        
        by_chapter = {}
        by_planet = {}
        by_type = {}
        
        for entry in self.entries:
            # Count by chapter
            by_chapter[entry.chapter] = by_chapter.get(entry.chapter, 0) + 1
            
            # Count by planet
            by_planet[entry.planet] = by_planet.get(entry.planet, 0) + 1
            
            # Count by type
            by_type[entry.correction_type] = by_type.get(entry.correction_type, 0) + 1
        
        return {
            "total_entries": len(self.entries),
            "by_chapter": by_chapter,
            "by_planet": by_planet,
            "by_type": by_type,
            "time_range": {
                "first": self.entries[0].timestamp if self.entries else None,
                "last": self.entries[-1].timestamp if self.entries else None
            }
        }

# Global logger instance
global_logger = CorrectionLogger(enabled=True)
