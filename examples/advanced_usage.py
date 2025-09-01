#!/usr/bin/env python3
"""Advanced usage examples for ASCII Banner Generator."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import BannerGenerator, Style, BorderStyle
from src.core.fonts import FontManager
from src.exporters import TextExporter, HTMLExporter, ImageExporter


def font_discovery():
    """Demonstrate font discovery and management."""
    print("=" * 60)
    print("FONT DISCOVERY")
    print("=" * 60)
    
    fm = FontManager()
    
    # Get fonts by category
    print("\n3D Fonts:")
    three_d_fonts = fm.get_fonts_by_category("3d")
    print(", ".join(three_d_fonts[:5]))
    
    # Get recommended fonts for specific use cases
    print("\nRecommended for Headers:")
    header_fonts = fm.get_recommended_fonts("headers")
    print(", ".join(header_fonts))
    
    # Search for fonts
    print("\nFonts containing 'star':")
    star_fonts = fm.search_fonts("star")
    print(", ".join(star_fonts))
    
    # Get font information
    print("\nFont Info for 'standard':")
    info = fm.get_font_info("standard")
    print(f"  Categories: {', '.join(info['categories'])}")
    print(f"  Recommended for: {', '.join(info['recommended_for'])}")
    if 'height' in info:
        print(f"  Dimensions: {info['height']}h x {info['approx_width']}w")


def export_examples():
    """Demonstrate various export formats."""
    print("=" * 60)
    print("EXPORT EXAMPLES")
    print("=" * 60)
    
    # Create a banner
    style = Style(
        font="slant",
        color="gradient:blue-cyan",
        border=BorderStyle.DOUBLE,
        padding=2
    )
    banner = BannerGenerator("EXPORT", style)
    
    # Create output directory
    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True)
    
    # Text export
    text_exporter = TextExporter(banner)
    text_exporter.export(output_dir / "banner.txt")
    print("\n✓ Exported to banner.txt")
    
    # Text with metadata
    text_exporter.export_with_metadata(output_dir / "banner_with_meta.txt")
    print("✓ Exported to banner_with_meta.txt (with metadata)")
    
    # JSON export
    text_exporter.export_json(output_dir / "banner.json")
    print("✓ Exported to banner.json")
    
    # HTML export
    html_exporter = HTMLExporter(banner)
    html_exporter.export(output_dir / "banner.html", theme="neon")
    print("✓ Exported to banner.html (neon theme)")
    
    # HTML with animation
    html_exporter.export_with_animation(output_dir / "banner_animated.html")
    print("✓ Exported to banner_animated.html (animated)")
    
    # Image exports
    img_exporter = ImageExporter(banner)
    
    # PNG export
    img_exporter.export(
        output_dir / "banner.png",
        format="png",
        background_color="white",
        text_color="blue"
    )
    print("✓ Exported to banner.png")
    
    # SVG export
    img_exporter.export(
        output_dir / "banner.svg",
        format="svg",
        background_color="#f0f0f0",
        text_color="#333333"
    )
    print("✓ Exported to banner.svg")


def batch_processing():
    """Generate multiple banners in batch."""
    print("=" * 60)
    print("BATCH PROCESSING")
    print("=" * 60)
    
    # Chapter headers
    chapters = [
        "Introduction",
        "Getting Started",
        "Advanced Topics",
        "Conclusion"
    ]
    
    style = Style(
        font="banner",
        color="blue",
        border=BorderStyle.DOUBLE,
        padding=1,
        alignment="center"
    )
    
    output_dir = Path("examples/output/chapters")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, chapter in enumerate(chapters, 1):
        banner = BannerGenerator(f"Chapter {i}", style)
        
        # Save as text
        filename = output_dir / f"chapter_{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"# {chapter}\n\n")
            f.write(banner.render())
        
        print(f"✓ Generated {filename.name}")


def font_preview():
    """Preview text in multiple fonts."""
    print("=" * 60)
    print("FONT PREVIEW")
    print("=" * 60)
    
    text = "DEMO"
    fonts = ["standard", "slant", "3-d", "banner", "big", "digital"]
    
    for font_name in fonts:
        print(f"\n--- Font: {font_name} ---")
        banner = BannerGenerator(text, Style(font=font_name))
        print(banner.render())


def custom_style_builder():
    """Build complex custom styles programmatically."""
    print("=" * 60)
    print("CUSTOM STYLE BUILDER")
    print("=" * 60)
    
    # Start with a base style
    style = Style(font="standard")
    
    # Progressively add features
    print("\n1. Base text:")
    banner = BannerGenerator("STYLE", style)
    print(banner.render())
    
    # Add color
    style.color = "cyan"
    print("\n2. With color:")
    banner = BannerGenerator("STYLE", style)
    print(banner.render())
    
    # Add border
    style.border = BorderStyle.SINGLE
    print("\n3. With border:")
    banner = BannerGenerator("STYLE", style)
    print(banner.render())
    
    # Add padding
    style.padding = 1
    print("\n4. With padding:")
    banner = BannerGenerator("STYLE", style)
    print(banner.render())
    
    # Add shadow
    style.shadow = True
    print("\n5. With shadow:")
    banner = BannerGenerator("STYLE", style)
    print(banner.render())


def multi_line_banner():
    """Create banners with multiple lines of text."""
    print("=" * 60)
    print("MULTI-LINE BANNER")
    print("=" * 60)
    
    lines = ["WELCOME", "TO THE", "FUTURE"]
    
    style = Style(
        font="big",
        color="gradient:magenta-cyan",
        border=BorderStyle.DOUBLE,
        padding=2,
        alignment="center"
    )
    
    for line in lines:
        banner = BannerGenerator(line, style)
        print(banner.render())


def main():
    """Run all advanced examples."""
    examples = [
        font_discovery,
        export_examples,
        batch_processing,
        font_preview,
        custom_style_builder,
        multi_line_banner
    ]
    
    for example in examples:
        try:
            example()
            print("\n" * 2)
        except Exception as e:
            print(f"Error in {example.__name__}: {str(e)}")
            print("\n" * 2)
    
    print("=" * 60)
    print("Advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()