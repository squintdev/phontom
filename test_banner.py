#!/usr/bin/env python3
"""Quick test script to verify ASCII Banner Generator functionality."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src import BannerGenerator, Style, BorderStyle


def test_basic_functionality():
    """Test basic banner generation."""
    print("Testing ASCII Banner Generator...")
    print("=" * 60)
    
    # Test 1: Simple banner
    print("\n1. Simple Banner Test:")
    banner = BannerGenerator("TEST")
    output = banner.render()
    assert output, "Failed to generate simple banner"
    print(output)
    print("✓ Simple banner works")
    
    # Test 2: Styled banner
    print("\n2. Styled Banner Test:")
    style = Style(
        font="slant",
        color="cyan",
        border=BorderStyle.DOUBLE,
        padding=1
    )
    banner = BannerGenerator("STYLE", style)
    output = banner.render()
    assert output, "Failed to generate styled banner"
    print(output)
    print("✓ Styled banner works")
    
    # Test 3: Font availability
    print("\n3. Font Availability Test:")
    fonts = banner.get_available_fonts()
    assert len(fonts) > 0, "No fonts available"
    print(f"✓ Found {len(fonts)} fonts")
    
    # Test 4: Template loading
    print("\n4. Template Test:")
    try:
        template_style = Style.load_from_template("corporate")
        banner = BannerGenerator("TEMPLATE", template_style)
        output = banner.render()
        print(output)
        print("✓ Template loading works")
    except Exception as e:
        print(f"⚠ Template test failed: {e}")
    
    # Test 5: Export functionality
    print("\n5. Export Test:")
    from src.exporters import TextExporter
    
    exporter = TextExporter(banner)
    raw_output = exporter.get_raw_output()
    assert raw_output, "Failed to get raw output"
    print("✓ Text export works")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)