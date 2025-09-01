# PHONTOM ASCII Banner Generator

A feature-rich Python application that generates beautiful ASCII art banners from text with multiple fonts, styles, and export formats.

```
#########################################################################
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                    ____  _   _  ___  _   _ _____ ___  __  __          #
#                   |  _ \| | | |/ _ \| \ | |_   _/ _ \|  \/  |         #
#                   | |_) | |_| | | | |  \| | | || | | | |\/| |         #
#                   |  __/|  _  | |_| | |\  | | || |_| | |  | |         #
#                   |_|   |_| |_|\___/|_| \_| |_| \___/|_|  |_|         #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#########################################################################
```

## Features

- **500+ Fonts**: Access to a vast library of ASCII art fonts via pyfiglet
- **Rich Styling**: Colors, gradients, borders, shadows, and padding options
- **Multiple Export Formats**: Text, HTML, PNG, SVG, and JSON
- **Interactive Mode**: User-friendly interface for creating banners
- **Template System**: Pre-defined styles for quick banner creation
- **CLI & Library**: Use as a command-line tool or Python library
- **Font Management**: Browse, search, and preview fonts by category

## Installation

```bash
# Clone the repository
git clone https://github.com/squintdev/phontom.git
cd phontom

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### Command Line Usage

```bash
# Simple banner
python -m src.cli.app generate "Hello World"

# With styling
python -m src.cli.app generate "Welcome" --font slant --color blue --border double

# Using templates
python -m src.cli.app generate "AWESOME" --template retro

# Export to file
python -m src.cli.app generate "Banner" --output banner.html --format html

# Interactive mode
python -m src.cli.app interactive
```

**Note**: After running `pip install -e .`, you can use `phontom` directly instead of `python -m src.cli.app`.

### Python Library Usage

```python
from src import BannerGenerator, Style, BorderStyle

# Simple usage
banner = BannerGenerator("Hello World")
print(banner.render())

# With custom style
style = Style(
    font="3-d",
    color="gradient:blue-cyan",
    border=BorderStyle.DOUBLE,
    padding=2,
    shadow=True
)
banner = BannerGenerator("EPIC", style=style)
print(banner.render())

# Export to different formats
from src.exporters import HTMLExporter, ImageExporter

# Export to HTML
html_exporter = HTMLExporter(banner)
html_exporter.export("banner.html")

# Export to PNG
img_exporter = ImageExporter(banner)
img_exporter.export("banner.png", format="png")
```

## CLI Commands

### `generate` - Create ASCII Banners

```bash
python -m src.cli.app generate [OPTIONS] TEXT

Options:
  -f, --font TEXT        Font to use (default: standard)
  -c, --color TEXT       Text color (e.g., red, gradient:blue-cyan)
  -b, --border TEXT      Border style (none|single|double|rounded|bold|ascii|star|hash)
  -p, --padding INT      Padding around text
  -w, --width INT        Maximum banner width
  -a, --align TEXT       Text alignment (left|center|right)
  -t, --template TEXT    Use predefined template
  -o, --output TEXT      Output file path
  --format TEXT          Output format (text|html|png|svg)
  --show-shadow          Add shadow effect
  --compact              Remove empty lines
```

### `fonts` - Browse Available Fonts

```bash
python -m src.cli.app fonts [OPTIONS]

Options:
  -c, --category TEXT    Filter by category (standard|slanted|3d|digital|decorative)
  -s, --search TEXT      Search fonts by name
  --sample              Show sample rendering
  --sample-text TEXT    Custom sample text
```

### `preview` - Preview Text in Multiple Fonts

```bash
python -m src.cli.app preview [OPTIONS] [TEXT]

Options:
  -f, --fonts TEXT      Specific fonts to preview (can be repeated)
  -c, --category TEXT   Preview fonts from category
  -m, --max INT        Maximum fonts to preview
```

### `templates` - List Available Templates

```bash
python -m src.cli.app templates
```

Available templates:
- **corporate**: Professional look with double borders
- **retro**: 3D font with star borders and gradients
- **minimal**: Clean and simple
- **fancy**: Slanted text with rounded borders
- **terminal**: Digital font with terminal aesthetics
- **banner**: Banner font with double borders and yellow color
- **matrix**: Green text on black, Matrix-style
- **neon**: Bright colors with glow effects

### `interactive` - Interactive Banner Creation

```bash
python -m src.cli.app interactive
```

Step-by-step wizard for creating banners with live previews.

## Styling Options

### Colors

Basic colors:
- `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- Bright variants: `bright_red`, `bright_green`, etc.

Gradients:
- `gradient:red-yellow`
- `gradient:blue-cyan`
- `gradient:magenta-cyan`

### Border Styles

- `none`: No border
- `single`: ┌─┐│└┘
- `double`: ╔═╗║╚╝
- `rounded`: ╭─╮│╰╯
- `bold`: ┏━┓┃┗┛
- `ascii`: +-+|+-+
- `star`: ****
- `hash`: ####

### Font Categories

- **standard**: Basic readable fonts
- **slanted**: Italic and slanted styles
- **3d**: Three-dimensional effect fonts
- **digital**: Computer and tech themed
- **decorative**: Ornamental and fancy
- **retro**: Vintage and classic styles
- **compact**: Space-efficient fonts
- **artistic**: Creative and unique designs

## Examples

### Create a Welcome Banner

```bash
python -m src.cli.app generate "WELCOME" \
  --font banner \
  --color gradient:blue-cyan \
  --border double \
  --padding 2 \
  --align center
```

### Generate Documentation Header

```bash
python -m src.cli.app generate "API DOCS" \
  --template corporate \
  --output docs/header.txt
```

### Create Social Media Image

```bash
python -m src.cli.app generate "Follow Me!" \
  --font slant \
  --color gradient:magenta-cyan \
  --border rounded \
  --output social.png \
  --format png
```

### Batch Process Multiple Banners

```python
from src import BannerGenerator, Style

texts = ["Chapter 1", "Chapter 2", "Chapter 3"]
style = Style.load_from_template("corporate")

for text in texts:
    banner = BannerGenerator(text, style)
    filename = f"{text.lower().replace(' ', '_')}.txt"
    with open(filename, 'w') as f:
        f.write(banner.render())
```

## Advanced Usage

### Custom Templates

Create your own templates in `src/templates/styles/`:

```yaml
# my_style.yaml
font: "3-d"
color: "gradient:purple-pink"
border: "double"
padding: 3
alignment: "center"
shadow: true
```

### Font Management

```python
from src.core.fonts import FontManager

fm = FontManager()

# Get fonts for headers
header_fonts = fm.get_recommended_fonts("headers")

# Search for specific fonts
space_fonts = fm.search_fonts("space")

# Get font information
info = fm.get_font_info("standard")
print(f"Height: {info['height']}, Width: {info['approx_width']}")
```

### Export with Custom Settings

```python
from src.exporters import HTMLExporter

# Export with animation
html_exporter = HTMLExporter(banner)
html_exporter.export_with_animation("animated.html")

# Export with specific theme
html_exporter.export("themed.html", theme="neon")
```

## Requirements

- Python 3.8+
- pyfiglet >= 1.0.2
- colorama >= 0.4.6
- rich >= 13.7.0
- click >= 8.1.7
- Pillow >= 10.2.0
- jinja2 >= 3.1.3
- PyYAML >= 6.0.1

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built on top of [pyfiglet](https://github.com/pwaller/pyfiglet) for ASCII art generation
- Inspired by classic UNIX banner programs
- Font library from FIGlet community
