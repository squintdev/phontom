#!/usr/bin/env python3
"""Basic usage examples for ASCII Banner Generator."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import BannerGenerator, Style, BorderStyle, ColorScheme


def simple_banner():
    """Create a simple banner with default settings."""
    print("=" * 60)
    print("SIMPLE BANNER")
    print("=" * 60)
    
    banner = BannerGenerator("Hello World")
    print(banner.render())


def styled_banner():
    """Create a banner with custom styling."""
    print("=" * 60)
    print("STYLED BANNER")
    print("=" * 60)
    
    style = Style(
        font="slant",
        color="cyan",
        border=BorderStyle.DOUBLE,
        padding=2,
        alignment="center"
    )
    
    banner = BannerGenerator("STYLED", style)
    print(banner.render())


def gradient_banner():
    """Create a banner with gradient colors."""
    print("=" * 60)
    print("GRADIENT BANNER")
    print("=" * 60)
    
    style = Style(
        font="3-d",
        color="gradient:magenta-cyan",
        border=BorderStyle.ROUNDED,
        padding=1
    )
    
    banner = BannerGenerator("GRADIENT", style)
    print(banner.render())


def template_banner():
    """Create banners using predefined templates."""
    print("=" * 60)
    print("TEMPLATE BANNERS")
    print("=" * 60)
    
    templates = ["corporate", "retro", "minimal", "neon"]
    
    for template_name in templates:
        print(f"\n--- Template: {template_name} ---")
        style = Style.load_from_template(template_name)
        banner = BannerGenerator("TEMPLATE", style)
        print(banner.render())


def color_scheme_banner():
    """Create banners with different color schemes."""
    print("=" * 60)
    print("COLOR SCHEMES")
    print("=" * 60)
    
    schemes = [ColorScheme.OCEAN, ColorScheme.FIRE, ColorScheme.FOREST]
    
    for scheme in schemes:
        print(f"\n--- Color Scheme: {scheme.value} ---")
        style = Style(font="standard", border=BorderStyle.SINGLE)
        style.apply_color_scheme(scheme)
        banner = BannerGenerator(scheme.value.upper(), style)
        print(banner.render())


def shadow_banner():
    """Create a banner with shadow effect."""
    print("=" * 60)
    print("SHADOW EFFECT")
    print("=" * 60)
    
    style = Style(
        font="big",
        color="yellow",
        border=BorderStyle.BOLD,
        shadow=True,
        shadow_color="bright_black",
        padding=1
    )
    
    banner = BannerGenerator("SHADOW", style)
    print(banner.render())


def compact_banner():
    """Create a compact banner without empty lines."""
    print("=" * 60)
    print("COMPACT BANNER")
    print("=" * 60)
    
    style = Style(
        font="small",
        compact=True,
        border=BorderStyle.ASCII
    )
    
    banner = BannerGenerator("COMPACT", style)
    print(banner.render())


def main():
    """Run all examples."""
    examples = [
        simple_banner,
        styled_banner,
        gradient_banner,
        template_banner,
        color_scheme_banner,
        shadow_banner,
        compact_banner
    ]
    
    for example in examples:
        example()
        print("\n" * 2)
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()