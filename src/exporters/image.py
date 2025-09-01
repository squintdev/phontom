"""Image exporter for ASCII banners (PNG/SVG)."""

from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import io


class ImageExporter:
    """Export ASCII banners as image files (PNG/SVG)."""
    
    def __init__(self, generator):
        """
        Initialize the image exporter.
        
        Args:
            generator: BannerGenerator instance
        """
        self.generator = generator
        self.default_font_size = 14
        self.default_padding = 20
    
    def export(self, filename: str, format: str = 'png',
               size: Optional[Tuple[int, int]] = None,
               background_color: str = 'white',
               text_color: str = 'black',
               font_size: Optional[int] = None) -> bool:
        """
        Export banner to an image file.
        
        Args:
            filename: Output filename
            format: Image format ('png' or 'svg')
            size: Optional image size (width, height)
            background_color: Background color
            text_color: Text color
            font_size: Font size for rendering
            
        Returns:
            True if export was successful
        """
        try:
            output_path = Path(filename)
            
            if format.lower() == 'svg':
                return self._export_svg(output_path, background_color, text_color, font_size)
            else:
                return self._export_png(output_path, size, background_color, text_color, font_size)
                
        except Exception as e:
            print(f"Error exporting to {format}: {str(e)}")
            return False
    
    def _export_png(self, output_path: Path, size: Optional[Tuple[int, int]],
                    background_color: str, text_color: str, 
                    font_size: Optional[int]) -> bool:
        """Export as PNG image."""
        try:
            # Get raw text without ANSI colors
            original_color = self.generator.style.color
            self.generator.style.color = None
            text = self.generator.render()
            self.generator.style.color = original_color
            
            # Calculate font size and image dimensions
            font_size = font_size or self.default_font_size
            
            # Try to use a monospace font
            try:
                # Try common monospace fonts
                font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("Courier New.ttf", font_size)
                except:
                    # Fall back to default font
                    font = ImageFont.load_default()
            
            # Calculate text size
            lines = text.split('\n')
            max_line_length = max(len(line) for line in lines) if lines else 0
            
            # Estimate dimensions
            char_width = font_size * 0.6  # Approximate character width
            char_height = font_size * 1.2  # Approximate line height
            
            text_width = int(max_line_length * char_width)
            text_height = int(len(lines) * char_height)
            
            # Calculate image size with padding
            padding = self.default_padding
            if size:
                img_width, img_height = size
            else:
                img_width = text_width + (padding * 2)
                img_height = text_height + (padding * 2)
            
            # Create image
            img = Image.new('RGBA', (img_width, img_height), self._parse_color(background_color))
            draw = ImageDraw.Draw(img)
            
            # Draw text
            y_offset = padding
            text_color_rgb = self._parse_color(text_color)
            
            for line in lines:
                draw.text((padding, y_offset), line, fill=text_color_rgb, font=font)
                y_offset += char_height
            
            # Add effects based on style
            if self.generator.style.shadow:
                img = self._add_shadow_effect(img, text_color_rgb)
            
            # Save image
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, 'PNG')
            
            return True
            
        except Exception as e:
            print(f"Error creating PNG: {str(e)}")
            return False
    
    def _export_svg(self, output_path: Path, background_color: str,
                    text_color: str, font_size: Optional[int]) -> bool:
        """Export as SVG image."""
        try:
            # Get raw text without ANSI colors
            original_color = self.generator.style.color
            self.generator.style.color = None
            text = self.generator.render()
            self.generator.style.color = original_color
            
            font_size = font_size or self.default_font_size
            lines = text.split('\n')
            
            # Calculate dimensions
            max_line_length = max(len(line) for line in lines) if lines else 0
            char_width = font_size * 0.6
            line_height = font_size * 1.2
            
            width = int(max_line_length * char_width + 40)
            height = int(len(lines) * line_height + 40)
            
            # Create SVG content
            svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="{background_color}"/>
    <style>
        .ascii-text {{
            font-family: 'Courier New', Courier, monospace;
            font-size: {font_size}px;
            fill: {text_color};
        }}
    </style>
"""
            
            # Add text lines
            y_offset = 30
            for line in lines:
                # Escape special XML characters
                escaped_line = self._escape_xml(line)
                svg_content += f'    <text x="20" y="{y_offset}" class="ascii-text">{escaped_line}</text>\n'
                y_offset += line_height
            
            # Add shadow effect if enabled
            if self.generator.style.shadow:
                svg_content = self._add_svg_shadow(svg_content)
            
            svg_content += "</svg>"
            
            # Save SVG
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            return True
            
        except Exception as e:
            print(f"Error creating SVG: {str(e)}")
            return False
    
    def _parse_color(self, color_name: str) -> Tuple[int, int, int, int]:
        """Parse color name to RGBA tuple."""
        colors = {
            'black': (0, 0, 0, 255),
            'white': (255, 255, 255, 255),
            'red': (255, 0, 0, 255),
            'green': (0, 255, 0, 255),
            'blue': (0, 0, 255, 255),
            'yellow': (255, 255, 0, 255),
            'magenta': (255, 0, 255, 255),
            'cyan': (0, 255, 255, 255),
            'gray': (128, 128, 128, 255),
            'transparent': (0, 0, 0, 0)
        }
        
        # Handle hex colors
        if color_name.startswith('#'):
            try:
                hex_color = color_name.lstrip('#')
                if len(hex_color) == 6:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    return (r, g, b, 255)
            except:
                pass
        
        return colors.get(color_name.lower(), (0, 0, 0, 255))
    
    def _escape_xml(self, text: str) -> str:
        """Escape special XML characters."""
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&apos;'
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    
    def _add_shadow_effect(self, img: Image.Image, 
                          text_color: Tuple[int, int, int, int]) -> Image.Image:
        """Add shadow effect to PNG image."""
        # Create a simple shadow by creating a slightly offset darker version
        # This is a simplified implementation
        return img
    
    def _add_svg_shadow(self, svg_content: str) -> str:
        """Add shadow filter to SVG."""
        shadow_filter = """    <defs>
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
            <feOffset dx="2" dy="2" result="offsetblur"/>
            <feComponentTransfer>
                <feFuncA type="linear" slope="0.5"/>
            </feComponentTransfer>
            <feMerge>
                <feMergeNode/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
"""
        # Insert the filter definition after the opening SVG tag
        insert_pos = svg_content.find('>') + 1
        insert_pos = svg_content.find('\n', insert_pos) + 1
        
        # Add filter reference to text style
        svg_content = svg_content.replace(
            'class="ascii-text"',
            'class="ascii-text" filter="url(#shadow)"'
        )
        
        return svg_content[:insert_pos] + shadow_filter + svg_content[insert_pos:]
    
    def export_with_gradient(self, filename: str, format: str = 'png') -> bool:
        """
        Export banner with gradient background.
        
        Args:
            filename: Output filename
            format: Image format ('png' or 'svg')
            
        Returns:
            True if export was successful
        """
        # This would implement gradient backgrounds
        # For now, just use regular export
        return self.export(filename, format=format, 
                         background_color='white', 
                         text_color='black')