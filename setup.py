from setuptools import setup, find_packages

setup(
    name="ultimateminecraftlib",
    version="0.1.0",
    description="A library for interacting with Minecraft mod platforms (Modrinth and CurseForge)",
    author="Alex",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.6"
)