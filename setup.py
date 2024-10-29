# setup.py
from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="orchnex",
    version="0.1.0",
    description="Multi-LLM Orchestration Platform",
    author="Harshal More",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Core Dependencies
        "openai>=1.0.0",          # OpenAI API
        "google-generativeai>=0.3.0",  # Google Gemini API
        "nvidia-triton-client>=2.40.0",  # NVIDIA Triton
        "transformers>=4.36.0",   # Hugging Face Transformers
        "torch>=2.0.0",           # PyTorch
        
        # UI and Console
        "rich>=13.7.0",           # Rich text and formatting
        "typer>=0.9.0",          # CLI interface
        
        # Utility Libraries
        "python-dotenv>=1.0.0",   # Environment variable management
        "requests>=2.31.0",       # HTTP requests
        "pydantic>=2.5.0",        # Data validation
        "tenacity>=8.2.0",        # Retry mechanism
        
        # Output and Logging
        "loguru>=0.7.0",          # Logging
        "pandas>=2.1.0",          # Data manipulation
        "PyYAML>=6.0.1",          # YAML file handling
        
        # Development Dependencies
        "pytest>=7.4.0",          # Testing
        "black>=23.11.0",         # Code formatting
        "isort>=5.12.0",          # Import sorting
        "mypy>=1.7.0",            # Type checking
    ],
    extras_require={
        'dev': [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "isort>=5.12.0",
            "mypy>=1.7.0",
            "flake8>=6.1.0",
            "pre-commit>=3.5.0",
        ],
        'docs': [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'orchnex=orchnex.main:run_interactive_demo',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    project_urls={
        "Homepage": "https://github.com/harshalmore31/orchnex",
        "Bug Reports": "https://github.com/harshalmore31/orchnex/issues",
    },
)