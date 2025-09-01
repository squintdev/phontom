"""Font management for ASCII banners."""

import pyfiglet
from typing import List, Dict, Optional, Set
from pathlib import Path
import json


class FontManager:
    """Manages fonts for ASCII banner generation."""
    
    # Popular fonts categorized by style
    FONT_CATEGORIES = {
        "standard": ["standard", "small", "big", "banner", "block"],
        "slanted": ["slant", "lean", "italic", "script"],
        "3d": ["3-d", "3x5", "isometric1", "isometric2", "isometric3", "isometric4"],
        "digital": ["digital", "binary", "hex", "octal", "morse"],
        "decorative": ["bubble", "bulbhead", "colossal", "epic", "graceful"],
        "retro": ["doom", "larry3d", "alligator", "calvin", "cosmic"],
        "compact": ["mini", "small", "smscript", "smshadow", "smslant"],
        "wide": ["banner3", "colossal", "doh", "univers"],
        "artistic": ["starwars", "trek", "weird", "fantasy", "gothic"]
    }
    
    # Fonts good for specific use cases
    RECOMMENDED_FONTS = {
        "headers": ["banner", "big", "colossal", "epic"],
        "titles": ["standard", "slant", "3-d", "doom"],
        "code": ["digital", "small", "standard", "mono9"],
        "logos": ["3-d", "larry3d", "isometric1", "block"],
        "fun": ["starwars", "bubble", "bulbhead", "weird"]
    }
    
    def __init__(self, custom_font_dir: Optional[Path] = None):
        """
        Initialize the font manager.
        
        Args:
            custom_font_dir: Optional directory containing custom .flf font files
        """
        self.custom_font_dir = custom_font_dir or Path(__file__).parent.parent.parent / "fonts"
        self._font_cache = {}
        self._available_fonts = None
        self._font_metadata = {}
        self._load_font_metadata()
    
    def get_available_fonts(self) -> List[str]:
        """
        Get list of all available fonts.
        
        Returns:
            Sorted list of font names
        """
        if self._available_fonts is None:
            # Get pyfiglet fonts
            figlet_fonts = set(pyfiglet.FigletFont.getFonts())
            
            # Add custom fonts if directory exists
            custom_fonts = set()
            if self.custom_font_dir.exists():
                custom_fonts = {
                    f.stem for f in self.custom_font_dir.glob("*.flf")
                }
            
            self._available_fonts = sorted(figlet_fonts | custom_fonts)
        
        return self._available_fonts
    
    def get_fonts_by_category(self, category: str) -> List[str]:
        """
        Get fonts by category.
        
        Args:
            category: Category name (e.g., 'standard', '3d', 'decorative')
            
        Returns:
            List of font names in the category
        """
        available = set(self.get_available_fonts())
        category_fonts = self.FONT_CATEGORIES.get(category, [])
        return [f for f in category_fonts if f in available]
    
    def get_recommended_fonts(self, use_case: str) -> List[str]:
        """
        Get recommended fonts for a specific use case.
        
        Args:
            use_case: Use case (e.g., 'headers', 'titles', 'logos')
            
        Returns:
            List of recommended font names
        """
        available = set(self.get_available_fonts())
        recommended = self.RECOMMENDED_FONTS.get(use_case, [])
        return [f for f in recommended if f in available]
    
    def search_fonts(self, query: str) -> List[str]:
        """
        Search for fonts by name.
        
        Args:
            query: Search query (partial font name)
            
        Returns:
            List of matching font names
        """
        query_lower = query.lower()
        return [
            font for font in self.get_available_fonts()
            if query_lower in font.lower()
        ]
    
    def get_font_info(self, font_name: str) -> Dict[str, any]:
        """
        Get information about a specific font.
        
        Args:
            font_name: Name of the font
            
        Returns:
            Dictionary with font information
        """
        if font_name not in self.get_available_fonts():
            raise ValueError(f"Font '{font_name}' not found")
        
        info = {
            "name": font_name,
            "available": True,
            "categories": [],
            "recommended_for": []
        }
        
        # Find categories this font belongs to
        for category, fonts in self.FONT_CATEGORIES.items():
            if font_name in fonts:
                info["categories"].append(category)
        
        # Find use cases this font is recommended for
        for use_case, fonts in self.RECOMMENDED_FONTS.items():
            if font_name in fonts:
                info["recommended_for"].append(use_case)
        
        # Add metadata if available
        if font_name in self._font_metadata:
            info.update(self._font_metadata[font_name])
        
        # Try to get font dimensions
        try:
            fig = pyfiglet.Figlet(font=font_name)
            sample = fig.renderText("A")
            lines = sample.strip().split('\n')
            info["height"] = len(lines)
            info["approx_width"] = max(len(line) for line in lines)
        except:
            pass
        
        return info
    
    def validate_font(self, font_name: str) -> bool:
        """
        Check if a font is available.
        
        Args:
            font_name: Name of the font to validate
            
        Returns:
            True if font is available, False otherwise
        """
        return font_name in self.get_available_fonts()
    
    def get_font_sample(self, font_name: str, text: str = "SAMPLE") -> str:
        """
        Get a sample of text rendered in a specific font.
        
        Args:
            font_name: Name of the font
            text: Text to render (default: "SAMPLE")
            
        Returns:
            Rendered ASCII art text
        """
        if not self.validate_font(font_name):
            raise ValueError(f"Font '{font_name}' not found")
        
        try:
            fig = pyfiglet.Figlet(font=font_name)
            return fig.renderText(text)
        except Exception as e:
            return f"Error rendering font '{font_name}': {str(e)}"
    
    def get_all_categories(self) -> List[str]:
        """
        Get all available font categories.
        
        Returns:
            List of category names
        """
        return list(self.FONT_CATEGORIES.keys())
    
    def get_all_use_cases(self) -> List[str]:
        """
        Get all font use cases.
        
        Returns:
            List of use case names
        """
        return list(self.RECOMMENDED_FONTS.keys())
    
    def _load_font_metadata(self) -> None:
        """Load font metadata from file if it exists."""
        metadata_file = self.custom_font_dir / "font_metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    self._font_metadata = json.load(f)
            except:
                self._font_metadata = {}
    
    def add_custom_font(self, font_path: Path, metadata: Optional[Dict] = None) -> bool:
        """
        Add a custom font file.
        
        Args:
            font_path: Path to the .flf font file
            metadata: Optional metadata about the font
            
        Returns:
            True if font was added successfully
        """
        if not font_path.exists() or font_path.suffix != '.flf':
            return False
        
        # Copy font to custom fonts directory
        self.custom_font_dir.mkdir(parents=True, exist_ok=True)
        target_path = self.custom_font_dir / font_path.name
        
        try:
            import shutil
            shutil.copy2(font_path, target_path)
            
            # Add metadata if provided
            if metadata:
                font_name = font_path.stem
                self._font_metadata[font_name] = metadata
                self._save_font_metadata()
            
            # Reset cache
            self._available_fonts = None
            return True
        except Exception:
            return False
    
    def _save_font_metadata(self) -> None:
        """Save font metadata to file."""
        metadata_file = self.custom_font_dir / "font_metadata.json"
        try:
            with open(metadata_file, 'w') as f:
                json.dump(self._font_metadata, f, indent=2)
        except:
            pass