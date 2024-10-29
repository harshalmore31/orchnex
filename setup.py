# setup.py
import subprocess
import sys
import os
from setuptools import setup, find_packages, Command
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

def read_requirements(filename):
    """Read requirements from requirements.txt"""
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read requirements
INSTALL_REQUIRES = read_requirements('requirements.txt')

class CustomInstallCommand(install):
    """Custom installation command"""
    def run(self):
        self.run_command('install_dependencies')
        install.run(self)

class CustomDevelopCommand(develop):
    """Custom development command"""
    def run(self):
        self.run_command('install_dependencies')
        develop.run(self)

class InstallDependenciesCommand(Command):
    """Command to install all dependencies"""
    description = 'Install all dependencies'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the installation"""
        try:
            # Ensure pip is up to date
            self.announce("Upgrading pip...", level=2)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

            # Install required packages
            self.announce("Installing required packages...", level=2)
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + INSTALL_REQUIRES)

            # Create necessary directories
            self.announce("Creating necessary directories...", level=2)
            os.makedirs("outputs", exist_ok=True)

            # Set up environment variables file if it doesn't exist
            if not os.path.exists('.env'):
                self.announce("Creating .env file...", level=2)
                with open('.env', 'w') as f:
                    f.write("""# Orchnex Environment Variables
GEMINI_API_KEY=your_gemini_api_key_here
NVIDIA_API_KEY=your_nvidia_api_key_here
""")

            self.announce("""
╔════════════════════════════════════════════════════════════════╗
║                   🌟 Orchnex Setup Complete! 🌟                ║
║                                                                ║
║  Next steps:                                                   ║
║  1. Configure your API keys in .env file                       ║
║  2. Run 'orchnex' to start the demo                           ║
║  3. Check documentation at docs/README.md                      ║
║                                                                ║
║  For issues: https://github.com/yourusername/orchnex/issues   ║
╚════════════════════════════════════════════════════════════════╝
            """, level=2)

        except Exception as e:
            self.announce(f"Error during setup: {str(e)}", level=2)
            raise

setup(
    name="orchnex",
    version="0.1.0",
    description="Multi-LLM Orchestration Platform",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Harshal More",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/orchnex",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'dev': [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "isort>=5.12.0",
            "mypy>=1.7.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'orchnex=orchnex.main:run_interactive_demo',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'install_dependencies': InstallDependenciesCommand,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)