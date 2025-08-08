"""
Setup script for Binance Futures Trading Bot
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="binance-futures-bot",
    version="1.0.0",
    author="Amrun Khakim",
    author_email="amrun.dev@gmail.com",
    description="Advanced Binance Futures Trading Bot with Technical Analysis and Risk Management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amvst/binance-futures-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "binance-futures-bot=main:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "web": [
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "jinja2>=3.1.0",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords="binance futures trading bot cryptocurrency technical-analysis risk-management",
    project_urls={
        "Bug Reports": "https://github.com/amvst/binance-futures-bot/issues",
        "Source": "https://github.com/amvst/binance-futures-bot",
        "Documentation": "https://github.com/amvst/binance-futures-bot#readme",
    },
)
