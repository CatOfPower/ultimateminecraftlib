# UltimateMinecraftLib

A Python library for interacting with Modrinth and CurseForge in a unified way.

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

# Platform specific searches
from ultimateminecraftlib import search_modrinth, search_curseforge

modrinth_results = search_modrinth("jei")
curseforge_results = search_curseforge("jei")
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

### Working with Modpacks

```python
from ultimateminecraftlib import load_modrinth_pack, load_curseforge_pack

# Load a Modrinth modpack
load_modrinth_pack("modpack.mrpack")

# Load a CurseForge modpack
load_curseforge_pack("modpack.zip")
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

### Core Functions

#### search
```python
search(query, version=None, modloader=None, project_type=None, categories=None)
```
Searches for mods across both Modrinth and CurseForge platforms.

#### get_download
```python
get_download(id=None, slug=None, version=None, modloader=None, origin=None)
```
Gets the download URL for a specific mod version.

#### download_mod
```python
download_mod(id=None, slug=None, version=None, modloader=None, origin=None)
```
Downloads a mod directly to the current directory.

### Platform Specific Functions

#### search_modrinth / search_curseforge
```python
search_modrinth(query, version=None, modloader=None, project_type=None, categories=None)
search_curseforge(query, version=None, modloader=None, project_type=None, categories=None)
```
Search for mods on a specific platform.

#### load_modrinth_pack / load_curseforge_pack
```python
load_modrinth_pack(path)
load_curseforge_pack(path)
```
Load and parse modpack files from either platform.