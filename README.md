# UltimateMinecraftLib

A Python library for interacting with Minecraft mod platforms (Modrinth and CurseForge).

## Usage

### Searching for Mods

```python
from ultimateminecraftlib import search

# Basic search
results = search("jei")

# Advanced search with filters
results = search(
    query="jei",
    version="1.20.1",
    modloader="fabric",
    project_type="mod",
    categories=["utility"]
)
```

### Getting Download URLs

```python
from ultimateminecraftlib import get_download

# Using Modrinth mod ID
url = get_download(
    id="P7dR8mSH",  # JEI mod ID
    version="1.20.1",
    modloader="fabric",
    origin="modrinth"
)

# Using CurseForge mod ID
url = get_download(
    id="238222",  # JEI mod ID
    version="1.20.1",
    modloader="forge",
    origin="curseforge"
)
```

### Downloading Mods

```python
from ultimateminecraftlib import download_mod

# Download a mod directly
download_mod(
    id="P7dR8mSH",
    version="1.20.1",
    modloader="fabric",
    origin="modrinth"
)
```

### Checking Modloader Availability

```python
from ultimateminecraftlib import is_modloader_available

# Check if a mod is available for a specific modloader
available = is_modloader_available(
    id="P7dR8mSH",
    version="1.20.1",
    modloader="fabric",
    origin="modrinth"
)
```

## API Reference

### `search(query, version=None, modloader=None, project_type=None, categories=None)`
Searches for mods across both Modrinth and CurseForge platforms.

### `get_download(id=None, slug=None, version=None, modloader=None, origin=None)`
Gets the download URL for a specific mod version.

### `download_mod(id=None, slug=None, version=None, modloader=None, origin=None)`
Downloads a mod directly to the current directory.

### `is_modloader_available(id=None, slug=None, version=None, modloader=None, origin=None)`
Checks if a mod is available for a specific modloader and version.

### `search_modrinth(query, version=None, modloader=None, project_type=None, categories=None)`
Searches for mods on Modrinth only.

### `search_curseforge(query, version=None, modloader=None, project_type=None, categories=None)`
Searches for mods on CurseForge only.

## Requirements

- Python 3.6+
- requests >= 2.25.0

## License

MIT License