from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ascii-banner-generator",
    version="1.0.0",
    author="ASCII Banner Generator",
    description="A feature-rich ASCII art banner generator with multiple export formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ascii-banner-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Topic :: Artistic Software",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ascii-banner=src.cli.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["templates/styles/*.yaml", "fonts/*.flf"],
    },
)