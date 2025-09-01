#!/usr/bin/env python3
"""CLI interface for ASCII Banner Generator."""

import click
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.generator import BannerGenerator
from src.core.styles import Style, BorderStyle, ColorScheme
from src.core.fonts import FontManager
from src.exporters.text import TextExporter
from src.exporters.html import HTMLExporter
from src.exporters.image import ImageExporter


console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', is_flag=True, help='Show version information')
def cli(ctx, version):
    """ASCII Banner Generator - Create beautiful ASCII art banners with style!"""
    if version:
        click.echo("ASCII Banner Generator v1.0.0")
        return
    
    if ctx.invoked_subcommand is None:
        # Show help if no subcommand
        click.echo(ctx.get_help())


@cli.command()
@click.argument('text')
@click.option('--font', '-f', default='standard', help='Font to use for the banner')
@click.option('--color', '-c', default=None, help='Text color (e.g., red, blue, gradient:red-yellow)')
@click.option('--border', '-b', default='none', 
              type=click.Choice(['none', 'single', 'double', 'rounded', 'bold', 'ascii', 'star', 'hash']),
              help='Border style')
@click.option('--padding', '-p', default=0, type=int, help='Padding around the text')
@click.option('--width', '-w', default=80, type=int, help='Maximum width of the banner')
@click.option('--align', '-a', default='left',
              type=click.Choice(['left', 'center', 'right']),
              help='Text alignment')
@click.option('--template', '-t', default=None, help='Use a predefined template')
@click.option('--output', '-o', default=None, help='Output file (auto-detect format from extension)')
@click.option('--format', default='text',
              type=click.Choice(['text', 'html', 'png', 'svg']),
              help='Output format')
@click.option('--show-shadow', is_flag=True, help='Add shadow effect')
@click.option('--compact', is_flag=True, help='Remove empty lines for compact output')
def generate(text, font, color, border, padding, width, align, template, output, format, show_shadow, compact):
    """Generate an ASCII banner from text."""
    
    # Create style
    if template:
        try:
            style = Style.load_from_template(template)
            console.print(f"[green]Using template: {template}[/green]")
        except FileNotFoundError:
            console.print(f"[red]Template '{template}' not found. Using default style.[/red]")
            style = Style()
    else:
        style = Style(
            font=font,
            color=color,
            border=BorderStyle(border),
            padding=padding,
            width=width,
            alignment=align,
            shadow=show_shadow,
            compact=compact
        )
    
    # Generate banner
    try:
        generator = BannerGenerator(text, style)
        result = generator.render()
        
        # Handle output
        if output:
            # Auto-detect format from extension if not specified
            if format == 'text' and output:
                ext = Path(output).suffix.lower()
                format_map = {
                    '.html': 'html',
                    '.png': 'png',
                    '.svg': 'svg',
                    '.txt': 'text'
                }
                format = format_map.get(ext, 'text')
            
            # Export to file
            if format == 'html':
                exporter = HTMLExporter(generator)
                exporter.export(output)
                console.print(f"[green]✓ Banner saved to {output} (HTML format)[/green]")
            elif format == 'png':
                exporter = ImageExporter(generator)
                exporter.export(output, format='png')
                console.print(f"[green]✓ Banner saved to {output} (PNG format)[/green]")
            elif format == 'svg':
                exporter = ImageExporter(generator)
                exporter.export(output, format='svg')
                console.print(f"[green]✓ Banner saved to {output} (SVG format)[/green]")
            else:
                exporter = TextExporter(generator)
                exporter.export(output)
                console.print(f"[green]✓ Banner saved to {output} (text format)[/green]")
        else:
            # Print to console
            if color:
                # Already colored by generator
                print(result)
            else:
                console.print(result)
                
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--category', '-c', default=None, help='Filter fonts by category')
@click.option('--search', '-s', default=None, help='Search fonts by name')
@click.option('--sample', is_flag=True, help='Show sample text for each font')
@click.option('--sample-text', default='SAMPLE', help='Text to use for samples')
def fonts(category, search, sample, sample_text):
    """List available fonts."""
    font_manager = FontManager()
    
    # Get fonts based on filters
    if category:
        fonts = font_manager.get_fonts_by_category(category)
        title = f"Fonts in category: {category}"
    elif search:
        fonts = font_manager.search_fonts(search)
        title = f"Fonts matching: {search}"
    else:
        fonts = font_manager.get_available_fonts()
        title = "Available Fonts"
    
    if not fonts:
        console.print("[yellow]No fonts found matching criteria.[/yellow]")
        return
    
    if sample:
        # Show samples
        for font_name in fonts[:10]:  # Limit to first 10 for readability
            console.print(Panel(
                font_manager.get_font_sample(font_name, sample_text),
                title=f"[bold cyan]{font_name}[/bold cyan]",
                border_style="blue"
            ))
    else:
        # Show list
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Font Name", style="cyan", no_wrap=True)
        table.add_column("Categories", style="green")
        table.add_column("Recommended For", style="yellow")
        
        for font_name in fonts:
            info = font_manager.get_font_info(font_name)
            categories = ", ".join(info.get("categories", []))
            recommended = ", ".join(info.get("recommended_for", []))
            table.add_row(font_name, categories or "-", recommended or "-")
        
        console.print(table)
        console.print(f"\n[dim]Total: {len(fonts)} fonts[/dim]")


@cli.command()
@click.argument('text', default='PREVIEW')
@click.option('--fonts', '-f', multiple=True, help='Specific fonts to preview (can be used multiple times)')
@click.option('--category', '-c', default=None, help='Preview fonts from a specific category')
@click.option('--max', '-m', default=5, type=int, help='Maximum number of fonts to preview')
def preview(text, fonts, category, max):
    """Preview text in multiple fonts."""
    font_manager = FontManager()
    
    # Get fonts to preview
    if fonts:
        preview_fonts = list(fonts)
    elif category:
        preview_fonts = font_manager.get_fonts_by_category(category)[:max]
    else:
        # Default preview fonts
        preview_fonts = ['standard', 'slant', '3-d', 'banner', 'big']
    
    # Generate previews
    for font_name in preview_fonts:
        if font_manager.validate_font(font_name):
            try:
                generator = BannerGenerator(text, Style(font=font_name))
                result = generator.render()
                
                console.print(Panel(
                    result,
                    title=f"[bold cyan]{font_name}[/bold cyan]",
                    border_style="blue"
                ))
            except Exception as e:
                console.print(f"[red]Error with font '{font_name}': {str(e)}[/red]")
        else:
            console.print(f"[yellow]Font '{font_name}' not available[/yellow]")


@cli.command()
def templates():
    """List available templates."""
    templates = Style._get_default_templates()
    
    table = Table(title="Available Templates", show_header=True, header_style="bold magenta")
    table.add_column("Template", style="cyan", no_wrap=True)
    table.add_column("Font", style="green")
    table.add_column("Border", style="yellow")
    table.add_column("Color", style="blue")
    table.add_column("Features", style="white")
    
    for name, config in templates.items():
        features = []
        if config.get('shadow'):
            features.append('shadow')
        if config.get('padding'):
            features.append(f"padding:{config['padding']}")
        if config.get('alignment') == 'center':
            features.append('centered')
        if config.get('compact'):
            features.append('compact')
        
        table.add_row(
            name,
            config.get('font', 'standard'),
            config.get('border', 'none'),
            config.get('color', '-'),
            ', '.join(features) if features else '-'
        )
    
    console.print(table)
    console.print("\n[dim]Use with: ascii-banner generate \"text\" --template <name>[/dim]")


@cli.command()
def interactive():
    """Interactive mode for creating banners."""
    console.print("[bold cyan]ASCII Banner Generator - Interactive Mode[/bold cyan]\n")
    
    # Get text
    text = click.prompt("Enter text for banner", default="HELLO")
    
    # Show font categories
    font_manager = FontManager()
    categories = font_manager.get_all_categories()
    console.print("\n[yellow]Font Categories:[/yellow]")
    for i, cat in enumerate(categories, 1):
        console.print(f"  {i}. {cat}")
    
    cat_choice = click.prompt("Select category (number) or press Enter for all", default="", type=str)
    
    # Get fonts
    if cat_choice and cat_choice.isdigit():
        idx = int(cat_choice) - 1
        if 0 <= idx < len(categories):
            fonts = font_manager.get_fonts_by_category(categories[idx])
        else:
            fonts = font_manager.get_available_fonts()[:10]
    else:
        fonts = ['standard', 'slant', '3-d', 'banner', 'big']
    
    # Preview fonts
    console.print("\n[yellow]Select a font:[/yellow]")
    for i, font in enumerate(fonts[:10], 1):
        sample = font_manager.get_font_sample(font, text[:10])
        console.print(f"\n{i}. [cyan]{font}[/cyan]")
        console.print(Panel(sample, border_style="dim"))
    
    font_choice = click.prompt("Select font (number)", type=int, default=1)
    selected_font = fonts[min(font_choice - 1, len(fonts) - 1)]
    
    # Border selection
    console.print("\n[yellow]Border Styles:[/yellow]")
    borders = ['none', 'single', 'double', 'rounded', 'bold', 'ascii', 'star', 'hash']
    for i, border in enumerate(borders, 1):
        console.print(f"  {i}. {border}")
    
    border_choice = click.prompt("Select border (number)", type=int, default=1)
    selected_border = borders[min(border_choice - 1, len(borders) - 1)]
    
    # Color selection
    colors = ['none', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 
              'gradient:red-yellow', 'gradient:blue-cyan', 'gradient:magenta-cyan']
    console.print("\n[yellow]Color Options:[/yellow]")
    for i, color in enumerate(colors, 1):
        if color == 'none':
            console.print(f"  {i}. No color")
        else:
            console.print(f"  {i}. {color}")
    
    color_choice = click.prompt("Select color (number)", type=int, default=1)
    selected_color = None if color_choice == 1 else colors[min(color_choice - 1, len(colors) - 1)]
    
    # Other options
    padding = click.prompt("Padding", type=int, default=0)
    add_shadow = click.confirm("Add shadow effect?", default=False)
    
    # Generate final banner
    console.print("\n[green]Generating banner...[/green]\n")
    
    style = Style(
        font=selected_font,
        color=selected_color,
        border=BorderStyle(selected_border),
        padding=padding,
        shadow=add_shadow,
        alignment='center' if padding > 0 else 'left'
    )
    
    generator = BannerGenerator(text, style)
    result = generator.render()
    
    console.print(Panel(
        result,
        title="[bold green]Your Banner[/bold green]",
        border_style="green"
    ))
    
    # Save option
    if click.confirm("\nSave banner to file?", default=False):
        filename = click.prompt("Filename", default="banner.txt")
        format = click.prompt("Format (text/html/png)", default="text")
        
        if format == 'html':
            from src.exporters.html import HTMLExporter
            exporter = HTMLExporter(generator)
            exporter.export(filename)
        elif format == 'png':
            from src.exporters.image import ImageExporter
            exporter = ImageExporter(generator)
            exporter.export(filename, format='png')
        else:
            from src.exporters.text import TextExporter
            exporter = TextExporter(generator)
            exporter.export(filename)
        
        console.print(f"[green]✓ Banner saved to {filename}[/green]")


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()