import os
import json
from typing import Dict, List, Optional, Union


class Personality:
    """Base class for agent personalities"""
    
    def __init__(self, name: str, traits: Dict[str, float]):
        self.name = name
        self.traits = traits
        
    def get_trait(self, trait_name: str) -> float:
        """Get the value of a specific trait"""
        return self.traits.get(trait_name, 0.0)
    
    def to_dict(self) -> Dict:
        """Convert personality to dictionary"""
        return {
            "name": self.name,
            "traits": self.traits
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Personality':
        """Create personality from dictionary"""
        return cls(data["name"], data["traits"])


class PersonalityManager:
    """Manages agent personalities"""
    
    def __init__(self, personalities_dir: Optional[str] = None):
        self.personalities_dir = personalities_dir or os.path.join(
            os.path.dirname(__file__), "data", "personalities"
        )
        self.personalities: Dict[str, Personality] = {}
        self._load_personalities()
    
    def _load_personalities(self):
        """Load personalities from JSON files"""
        if not os.path.exists(self.personalities_dir):
            os.makedirs(self.personalities_dir, exist_ok=True)
            return
            
        for filename in os.listdir(self.personalities_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.personalities_dir, filename), "r") as f:
                    data = json.load(f)
                    personality = Personality.from_dict(data)
                    self.personalities[personality.name] = personality
    
    def get_personality(self, name: str) -> Optional[Personality]:
        """Get a personality by name"""
        return self.personalities.get(name)
    
    def list_personalities(self) -> List[str]:
        """List all available personalities"""
        return list(self.personalities.keys())
    
    def add_personality(self, personality: Personality):
        """Add a new personality"""
        self.personalities[personality.name] = personality
        self._save_personality(personality)
    
    def _save_personality(self, personality: Personality):
        """Save personality to JSON file"""
        filename = f"{personality.name.lower()}.json"
        filepath = os.path.join(self.personalities_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(personality.to_dict(), f, indent=2) 