"""HTML exporter for ASCII banners."""

from pathlib import Path
from typing import Optional, Dict
import html


class HTMLExporter:
    """Export ASCII banners as HTML files with CSS styling."""
    
    def __init__(self, generator):
        """
        Initialize the HTML exporter.
        
        Args:
            generator: BannerGenerator instance
        """
        self.generator = generator
    
    def export(self, filename: str, include_css: bool = True,
               standalone: bool = True, theme: str = "default") -> bool:
        """
        Export banner to an HTML file.
        
        Args:
            filename: Output filename
            include_css: Whether to include CSS styling
            standalone: Whether to create a complete HTML document
            theme: CSS theme to use
            
        Returns:
            True if export was successful
        """
        try:
            output_path = Path(filename)
            
            # Generate HTML content
            if standalone:
                content = self._generate_standalone_html(include_css, theme)
            else:
                content = self._generate_html_snippet(include_css, theme)
            
            # Write to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error exporting to HTML: {str(e)}")
            return False
    
    def _generate_standalone_html(self, include_css: bool, theme: str) -> str:
        """Generate a complete HTML document."""
        css = self._generate_css(theme) if include_css else ""
        banner_html = self._generate_banner_html()
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCII Banner - {html.escape(self.generator.text)}</title>
    {css}
</head>
<body>
    <div class="ascii-banner-container">
        {banner_html}
    </div>
</body>
</html>"""
    
    def _generate_html_snippet(self, include_css: bool, theme: str) -> str:
        """Generate just the banner HTML snippet."""
        css = self._generate_css(theme) if include_css else ""
        banner_html = self._generate_banner_html()
        
        if include_css:
            return f"{css}\n{banner_html}"
        return banner_html
    
    def _generate_banner_html(self) -> str:
        """Generate the banner HTML."""
        # Get raw output without ANSI colors
        original_color = self.generator.style.color
        self.generator.style.color = None
        raw_output = self.generator.render()
        self.generator.style.color = original_color
        
        # Escape HTML and preserve formatting
        escaped = html.escape(raw_output)
        
        # Wrap in pre tag to preserve ASCII art formatting
        return f'<pre class="ascii-banner" data-font="{self.generator.style.font}">{escaped}</pre>'
    
    def _generate_css(self, theme: str) -> str:
        """Generate CSS styling."""
        themes = self._get_themes()
        theme_css = themes.get(theme, themes["default"])
        
        base_css = """<style>
    .ascii-banner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px;
        box-sizing: border-box;
    }
    
    .ascii-banner {
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.2;
        white-space: pre;
        margin: 0;
        padding: 20px;
        border-radius: 8px;
        overflow-x: auto;
    }
"""
        
        return base_css + theme_css + "\n</style>"
    
    def _get_themes(self) -> Dict[str, str]:
        """Get available CSS themes."""
        color_map = self._get_color_for_style()
        
        themes = {
            "default": f"""
    body {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }}
    .ascii-banner {{
        background: rgba(255, 255, 255, 0.95);
        color: #333;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }}""",
            
            "dark": f"""
    body {{
        background: #1a1a1a;
    }}
    .ascii-banner {{
        background: #2d2d2d;
        color: {color_map.get('text', '#00ff00')};
        border: 1px solid #444;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.1);
    }}""",
            
            "terminal": """
    body {
        background: #000;
    }
    .ascii-banner {
        background: #000;
        color: #00ff00;
        border: 1px solid #00ff00;
        text-shadow: 0 0 3px #00ff00;
    }""",
            
            "paper": """
    body {
        background: #f5f5f5;
    }
    .ascii-banner {
        background: white;
        color: #222;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }""",
            
            "neon": f"""
    body {{
        background: linear-gradient(45deg, #000428 0%, #004e92 100%);
    }}
    .ascii-banner {{
        background: rgba(0, 0, 0, 0.8);
        color: {color_map.get('text', '#00ffff')};
        border: 2px solid {color_map.get('border', '#ff00ff')};
        box-shadow: 0 0 30px {color_map.get('border', '#ff00ff')}, inset 0 0 30px rgba(0, 255, 255, 0.1);
        text-shadow: 0 0 10px currentColor;
    }}""",
            
            "retro": """
    body {
        background: linear-gradient(180deg, #2d1b69 0%, #0f0c29 100%);
    }
    .ascii-banner {
        background: #1a1a2e;
        color: #f39c12;
        border: 3px double #f39c12;
        box-shadow: 0 0 20px rgba(243, 156, 18, 0.3);
    }"""
        }
        
        return themes
    
    def _get_color_for_style(self) -> Dict[str, str]:
        """Map style colors to CSS colors."""
        color_map = {
            'black': '#000000',
            'red': '#ff0000',
            'green': '#00ff00',
            'yellow': '#ffff00',
            'blue': '#0000ff',
            'magenta': '#ff00ff',
            'cyan': '#00ffff',
            'white': '#ffffff',
            'bright_black': '#808080',
            'bright_red': '#ff6666',
            'bright_green': '#66ff66',
            'bright_yellow': '#ffff66',
            'bright_blue': '#6666ff',
            'bright_magenta': '#ff66ff',
            'bright_cyan': '#66ffff',
            'bright_white': '#ffffff',
        }
        
        style_color = self.generator.style.color
        if style_color and not style_color.startswith('gradient:'):
            text_color = color_map.get(style_color, '#333333')
        else:
            text_color = '#333333'
        
        border_color = color_map.get(self.generator.style.border_color, text_color) if self.generator.style.border_color else text_color
        
        return {
            'text': text_color,
            'border': border_color
        }
    
    def export_with_animation(self, filename: str) -> bool:
        """
        Export banner with CSS animation effects.
        
        Args:
            filename: Output filename
            
        Returns:
            True if export was successful
        """
        try:
            output_path = Path(filename)
            
            banner_html = self._generate_banner_html()
            animated_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animated ASCII Banner - {html.escape(self.generator.text)}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(270deg, #667eea, #764ba2, #f093fb, #f5576c);
            background-size: 800% 800%;
            animation: gradientShift 10s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .ascii-banner {{
            font-family: 'Courier New', Courier, monospace;
            line-height: 1.2;
            white-space: pre;
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: float 3s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}
    </style>
</head>
<body>
    <div class="ascii-banner-container">
        {banner_html}
    </div>
</body>
</html>"""
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(animated_html)
            
            return True
            
        except Exception as e:
            print(f"Error exporting animated HTML: {str(e)}")
            return False