"""Text exporter for ASCII banners."""

from pathlib import Path
from typing import Optional
import json


class TextExporter:
    """Export ASCII banners as text files with optional ANSI colors."""
    
    def __init__(self, generator):
        """
        Initialize the text exporter.
        
        Args:
            generator: BannerGenerator instance
        """
        self.generator = generator
    
    def export(self, filename: str, include_colors: bool = True, 
               include_metadata: bool = False) -> bool:
        """
        Export banner to a text file.
        
        Args:
            filename: Output filename
            include_colors: Whether to include ANSI color codes
            include_metadata: Whether to include metadata as comments
            
        Returns:
            True if export was successful
        """
        try:
            output_path = Path(filename)
            
            # Generate banner
            if include_colors:
                content = self.generator.render()
            else:
                # Render without colors
                original_color = self.generator.style.color
                self.generator.style.color = None
                content = self.generator.render()
                self.generator.style.color = original_color
            
            # Add metadata if requested
            if include_metadata:
                metadata = self._generate_metadata()
                content = metadata + "\n" + content
            
            # Write to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error exporting to text: {str(e)}")
            return False
    
    def export_plain(self, filename: str) -> bool:
        """
        Export banner as plain text without any styling.
        
        Args:
            filename: Output filename
            
        Returns:
            True if export was successful
        """
        return self.export(filename, include_colors=False, include_metadata=False)
    
    def export_with_metadata(self, filename: str) -> bool:
        """
        Export banner with metadata comments.
        
        Args:
            filename: Output filename
            
        Returns:
            True if export was successful
        """
        return self.export(filename, include_colors=True, include_metadata=True)
    
    def get_raw_output(self) -> str:
        """
        Get the raw text output without colors.
        
        Returns:
            Plain text banner
        """
        original_color = self.generator.style.color
        self.generator.style.color = None
        content = self.generator.render()
        self.generator.style.color = original_color
        return content
    
    def get_colored_output(self) -> str:
        """
        Get the text output with ANSI colors.
        
        Returns:
            Colored text banner
        """
        return self.generator.render()
    
    def _generate_metadata(self) -> str:
        """
        Generate metadata comments for the banner.
        
        Returns:
            Metadata as comment lines
        """
        metadata_lines = [
            "# ASCII Banner Generator Output",
            f"# Text: {self.generator.text}",
            f"# Font: {self.generator.style.font}",
        ]
        
        if self.generator.style.color:
            metadata_lines.append(f"# Color: {self.generator.style.color}")
        
        if self.generator.style.border != "none":
            metadata_lines.append(f"# Border: {self.generator.style.border.value}")
        
        if self.generator.style.padding > 0:
            metadata_lines.append(f"# Padding: {self.generator.style.padding}")
        
        metadata_lines.append("# " + "=" * 60)
        
        return "\n".join(metadata_lines)
    
    def export_json(self, filename: str) -> bool:
        """
        Export banner data as JSON.
        
        Args:
            filename: Output filename
            
        Returns:
            True if export was successful
        """
        try:
            output_path = Path(filename)
            
            data = {
                "text": self.generator.text,
                "style": self.generator.style.to_dict(),
                "output": {
                    "plain": self.get_raw_output(),
                    "colored": self.get_colored_output()
                },
                "metadata": {
                    "font": self.generator.style.font,
                    "available_fonts": self.generator.get_available_fonts()
                }
            }
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting to JSON: {str(e)}")
            return False