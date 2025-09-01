"""Core ASCII banner generator module."""

import pyfiglet
from typing import Optional, Dict, Any, List
from .styles import Style, BorderStyle
from .fonts import FontManager


class BannerGenerator:
    """Main ASCII banner generator class."""
    
    def __init__(self, text: str, style: Optional[Style] = None):
        """
        Initialize the banner generator.
        
        Args:
            text: The text to convert to ASCII art
            style: Optional style configuration
        """
        self.text = text
        self.style = style or Style()
        self.font_manager = FontManager()
        self._ascii_art = None
        self._styled_output = None
    
    def render(self, **kwargs) -> str:
        """
        Render the banner with the current style.
        
        Args:
            **kwargs: Override style parameters for this render
            
        Returns:
            The rendered ASCII banner as a string
        """
        # Merge kwargs with existing style
        render_style = self.style.copy()
        render_style.update(**kwargs)
        
        # Generate base ASCII art
        self._generate_ascii_art(render_style)
        
        # Apply styling
        self._apply_styling(render_style)
        
        return self._styled_output
    
    def _generate_ascii_art(self, style: Style) -> None:
        """Generate the base ASCII art using pyfiglet."""
        try:
            figlet = pyfiglet.Figlet(
                font=style.font,
                width=style.width,
                justify=style.alignment
            )
            self._ascii_art = figlet.renderText(self.text)
        except pyfiglet.FontNotFound:
            # Fallback to standard font
            figlet = pyfiglet.Figlet(font='standard')
            self._ascii_art = figlet.renderText(self.text)
    
    def _apply_styling(self, style: Style) -> None:
        """Apply styling to the generated ASCII art."""
        lines = self._ascii_art.split('\n')
        
        # Remove empty lines if compact mode
        if style.compact:
            lines = [line for line in lines if line.strip()]
        
        # Apply padding
        if style.padding:
            lines = self._apply_padding(lines, style.padding)
        
        # Apply border
        if style.border != BorderStyle.NONE:
            lines = self._apply_border(lines, style)
        
        # Apply colors
        if style.color:
            lines = self._apply_colors(lines, style)
        
        self._styled_output = '\n'.join(lines)
    
    def _apply_padding(self, lines: List[str], padding: int) -> List[str]:
        """Apply padding around the text."""
        padded_lines = []
        
        # Add vertical padding
        for _ in range(padding):
            padded_lines.append('')
        
        # Add horizontal padding
        for line in lines:
            padded_lines.append(' ' * padding + line + ' ' * padding)
        
        # Add vertical padding
        for _ in range(padding):
            padded_lines.append('')
        
        return padded_lines
    
    def _apply_border(self, lines: List[str], style: Style) -> List[str]:
        """Apply border around the text."""
        if not lines:
            return lines
        
        # Calculate max width
        max_width = max(len(line) for line in lines)
        
        # Get border characters based on style
        border_chars = style.get_border_chars()
        
        bordered_lines = []
        
        # Top border
        bordered_lines.append(
            border_chars['tl'] + 
            border_chars['h'] * (max_width + 2) + 
            border_chars['tr']
        )
        
        # Content with side borders
        for line in lines:
            padded_line = line.ljust(max_width)
            bordered_lines.append(
                border_chars['v'] + ' ' + 
                padded_line + ' ' + 
                border_chars['v']
            )
        
        # Bottom border
        bordered_lines.append(
            border_chars['bl'] + 
            border_chars['h'] * (max_width + 2) + 
            border_chars['br']
        )
        
        return bordered_lines
    
    def _apply_colors(self, lines: List[str], style: Style) -> List[str]:
        """Apply colors to the text."""
        from colorama import Fore, Back, Style as ColoramaStyle
        import colorama
        
        # Initialize colorama
        colorama.init()
        
        colored_lines = []
        color_map = {
            'black': Fore.BLACK,
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'bright_black': Fore.LIGHTBLACK_EX,
            'bright_red': Fore.LIGHTRED_EX,
            'bright_green': Fore.LIGHTGREEN_EX,
            'bright_yellow': Fore.LIGHTYELLOW_EX,
            'bright_blue': Fore.LIGHTBLUE_EX,
            'bright_magenta': Fore.LIGHTMAGENTA_EX,
            'bright_cyan': Fore.LIGHTCYAN_EX,
            'bright_white': Fore.LIGHTWHITE_EX,
        }
        
        # Handle gradient colors
        if style.color.startswith('gradient:'):
            colors = style.color.replace('gradient:', '').split('-')
            return self._apply_gradient(lines, colors, color_map)
        
        # Apply single color
        color_code = color_map.get(style.color, '')
        for line in lines:
            colored_lines.append(color_code + line + ColoramaStyle.RESET_ALL)
        
        return colored_lines
    
    def _apply_gradient(self, lines: List[str], colors: List[str], color_map: Dict) -> List[str]:
        """Apply gradient coloring to lines."""
        from colorama import Style as ColoramaStyle
        
        gradient_lines = []
        num_lines = len(lines)
        
        if num_lines == 0:
            return lines
        
        # Simple two-color gradient
        if len(colors) == 2 and all(c in color_map for c in colors):
            start_color = color_map[colors[0]]
            end_color = color_map[colors[1]]
            
            for i, line in enumerate(lines):
                # Alternate between colors for simple gradient effect
                if i < num_lines // 2:
                    gradient_lines.append(start_color + line + ColoramaStyle.RESET_ALL)
                else:
                    gradient_lines.append(end_color + line + ColoramaStyle.RESET_ALL)
        else:
            # Fallback to first color if gradient not supported
            color = color_map.get(colors[0], '')
            for line in lines:
                gradient_lines.append(color + line + ColoramaStyle.RESET_ALL)
        
        return gradient_lines
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export the banner configuration as a dictionary.
        
        Returns:
            Dictionary containing banner configuration
        """
        return {
            'text': self.text,
            'style': self.style.to_dict(),
            'output': self._styled_output
        }
    
    def get_available_fonts(self) -> List[str]:
        """
        Get list of available fonts.
        
        Returns:
            List of font names
        """
        return self.font_manager.get_available_fonts()
    
    def preview_fonts(self, sample_text: Optional[str] = None) -> str:
        """
        Preview text in multiple fonts.
        
        Args:
            sample_text: Text to preview (defaults to self.text)
            
        Returns:
            String showing the text in different fonts
        """
        text = sample_text or self.text
        previews = []
        
        # Get a selection of popular fonts
        preview_fonts = ['standard', 'slant', '3-d', 'banner', 'big', 'block', 'bubble', 'digital']
        
        for font_name in preview_fonts:
            if font_name in self.get_available_fonts():
                previews.append(f"\n=== {font_name.upper()} ===")
                try:
                    fig = pyfiglet.Figlet(font=font_name)
                    previews.append(fig.renderText(text))
                except:
                    previews.append(f"(Unable to render {font_name})")
        
        return '\n'.join(previews)