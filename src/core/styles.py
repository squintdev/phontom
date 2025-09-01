"""Style definitions and management for ASCII banners."""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
import yaml
from pathlib import Path


class BorderStyle(Enum):
    """Border style options."""
    NONE = "none"
    SINGLE = "single"
    DOUBLE = "double"
    ROUNDED = "rounded"
    BOLD = "bold"
    ASCII = "ascii"
    STAR = "star"
    HASH = "hash"


class Alignment(Enum):
    """Text alignment options."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class ColorScheme(Enum):
    """Predefined color schemes."""
    DEFAULT = "default"
    RAINBOW = "rainbow"
    OCEAN = "ocean"
    FIRE = "fire"
    FOREST = "forest"
    SUNSET = "sunset"
    NEON = "neon"
    MONOCHROME = "monochrome"


@dataclass
class Style:
    """Style configuration for ASCII banners."""
    
    font: str = "standard"
    color: Optional[str] = None
    background_color: Optional[str] = None
    border: BorderStyle = BorderStyle.NONE
    border_color: Optional[str] = None
    padding: int = 0
    width: int = 80
    alignment: str = "left"
    compact: bool = False
    shadow: bool = False
    shadow_color: Optional[str] = "bright_black"
    bold: bool = False
    italic: bool = False
    underline: bool = False
    
    def __post_init__(self):
        """Validate and convert style parameters."""
        if isinstance(self.border, str):
            self.border = BorderStyle(self.border)
        
        if isinstance(self.alignment, str):
            # Handle both string and Alignment enum
            self.alignment = self.alignment.lower()
            if self.alignment not in ['left', 'center', 'right']:
                self.alignment = 'left'
    
    def copy(self) -> 'Style':
        """Create a copy of the style."""
        return Style(**asdict(self))
    
    def update(self, **kwargs) -> None:
        """Update style parameters."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert style to dictionary."""
        data = asdict(self)
        # Convert enums to strings
        if isinstance(data.get('border'), BorderStyle):
            data['border'] = data['border'].value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Style':
        """Create style from dictionary."""
        # Convert border string to enum if needed
        if 'border' in data and isinstance(data['border'], str):
            try:
                data['border'] = BorderStyle(data['border'])
            except ValueError:
                data['border'] = BorderStyle.NONE
        return cls(**data)
    
    def get_border_chars(self) -> Dict[str, str]:
        """Get border characters based on style."""
        borders = {
            BorderStyle.NONE: {
                'tl': '', 'tr': '', 'bl': '', 'br': '',
                'h': '', 'v': ''
            },
            BorderStyle.SINGLE: {
                'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘',
                'h': '─', 'v': '│'
            },
            BorderStyle.DOUBLE: {
                'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝',
                'h': '═', 'v': '║'
            },
            BorderStyle.ROUNDED: {
                'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
                'h': '─', 'v': '│'
            },
            BorderStyle.BOLD: {
                'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛',
                'h': '━', 'v': '┃'
            },
            BorderStyle.ASCII: {
                'tl': '+', 'tr': '+', 'bl': '+', 'br': '+',
                'h': '-', 'v': '|'
            },
            BorderStyle.STAR: {
                'tl': '*', 'tr': '*', 'bl': '*', 'br': '*',
                'h': '*', 'v': '*'
            },
            BorderStyle.HASH: {
                'tl': '#', 'tr': '#', 'bl': '#', 'br': '#',
                'h': '#', 'v': '#'
            }
        }
        return borders.get(self.border, borders[BorderStyle.NONE])
    
    @classmethod
    def load_from_template(cls, template_name: str) -> 'Style':
        """Load style from a template file."""
        template_dir = Path(__file__).parent.parent / "templates" / "styles"
        template_file = template_dir / f"{template_name}.yaml"
        
        if not template_file.exists():
            # Try to find in default templates
            default_templates = cls._get_default_templates()
            if template_name in default_templates:
                return cls.from_dict(default_templates[template_name])
            raise FileNotFoundError(f"Template '{template_name}' not found")
        
        with open(template_file, 'r') as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data)
    
    @staticmethod
    def _get_default_templates() -> Dict[str, Dict[str, Any]]:
        """Get default template configurations."""
        return {
            "corporate": {
                "font": "standard",
                "border": "double",
                "color": "blue",
                "padding": 2,
                "alignment": "center"
            },
            "retro": {
                "font": "3-d",
                "border": "star",
                "color": "gradient:magenta-cyan",
                "shadow": True,
                "padding": 1
            },
            "minimal": {
                "font": "small",
                "border": "none",
                "color": "white",
                "compact": True
            },
            "fancy": {
                "font": "slant",
                "border": "rounded",
                "color": "gradient:blue-cyan",
                "padding": 2,
                "shadow": True
            },
            "terminal": {
                "font": "digital",
                "border": "single",
                "color": "green",
                "padding": 1,
                "width": 100
            },
            "banner": {
                "font": "banner",
                "border": "double",
                "color": "yellow",
                "padding": 1,
                "alignment": "center"
            },
            "matrix": {
                "font": "digital",
                "color": "bright_green",
                "background_color": "black",
                "border": "none",
                "shadow": True
            },
            "neon": {
                "font": "big",
                "color": "gradient:magenta-cyan",
                "border": "rounded",
                "shadow": True,
                "shadow_color": "bright_magenta"
            }
        }
    
    def apply_color_scheme(self, scheme: ColorScheme) -> None:
        """Apply a predefined color scheme."""
        schemes = {
            ColorScheme.RAINBOW: {
                "color": "gradient:red-yellow",
                "border_color": "magenta"
            },
            ColorScheme.OCEAN: {
                "color": "gradient:blue-cyan",
                "border_color": "blue",
                "shadow_color": "bright_blue"
            },
            ColorScheme.FIRE: {
                "color": "gradient:red-yellow",
                "border_color": "red",
                "shadow_color": "bright_red"
            },
            ColorScheme.FOREST: {
                "color": "gradient:green-bright_green",
                "border_color": "green",
                "shadow_color": "green"
            },
            ColorScheme.SUNSET: {
                "color": "gradient:magenta-yellow",
                "border_color": "magenta"
            },
            ColorScheme.NEON: {
                "color": "gradient:bright_magenta-bright_cyan",
                "border_color": "bright_magenta",
                "shadow": True
            },
            ColorScheme.MONOCHROME: {
                "color": "white",
                "border_color": "bright_black",
                "shadow_color": "bright_black"
            }
        }
        
        if scheme in schemes:
            self.update(**schemes[scheme])