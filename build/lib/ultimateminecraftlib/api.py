from requests import get

base_url_modrinth = "https://api.modrinth.com/v2/"
base_url_curseforge = "https://api.curseforge.com/v1/"
curseforge_key = "$2a$10$wuAJuNZuted3NORVmpgUC.m8sI.pv1tOPKZyBgLFGjxFp/br0lZCC"

def search(query : str, version : str = None, modloader : str = None, project_type : str = None, categories : list = None) -> list:
    """
    Search for mods on modrinth or curseforge.
    :param query: The search query.
    :param version: The version of the game.
    :param modloader: The modloader to search for.
    :param project_type: The type of project to search for.
    :param categories: The categories to search for.
    :return: A list of mods in a dictionary format.
    :rtype: list

    The dictionary format is as follows:
    {
        "name": str,
        "id": str,
        "slug": str,
        "origin": str,
        "description": str,
        "categories": list,
        "downloads": int,
        "authors": list,
        "icon_url": str,
        "project_url": str,
        "modloader": list,
        "version": list
    }
    """

    return search_modrinth(query, version, modloader, project_type, categories) + search_curseforge(query, version, modloader, project_type, categories)
    
def search_curseforge(query: str, version: str = None, modloader: str = None, project_type: str = None, categories: list = None) -> list:
    url = f"{base_url_curseforge}mods/search"
    headers = {"x-api-key": curseforge_key}
    params = {
        "gameId": 432,  # Minecraft game ID
        "searchFilter": query,
        "sortOrder": "desc"
    }

    # Map project types to CurseForge class IDs
    project_type_map = {
        "mod": 6,  # Mods
        "modpack": 4471,  # Modpacks
        "resourcepack": 12,  # Resource Packs
        "world": 17,  # Worlds
        "shader": 6552,  # Shaders
    }

    if version:
        params["gameVersion"] = version
    if modloader:
        params["modLoaderType"] = modloader
    if project_type and project_type.lower() in project_type_map:
        params["classId"] = project_type_map[project_type.lower()]
    if categories:
        params["categoryIds"] = ",".join(map(str, categories))

    response = get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json().get("data", [])
    else:
        response.raise_for_status()
    
    translated_results = []
    for project in results:
        translated_results.append(translate_from_curseforge(project))
    
    return translated_results

def search_modrinth(query : str, version : str = None, modloader : str = None, project_type : str = None, categories : list = None) -> list:
    url = f"{base_url_modrinth}search?q={query}"

    if version or modloader or project_type or categories:
        facets = []

        if version:
            facets.append([f"versions:{version}"])
        if modloader:
            facets.append([f"categories:{modloader}"])
        if project_type:
            facets.append([f"project_type:{project_type}"])
        if categories:
            for categorie in categories:
                facets.append([f"categories:{categorie}"])
        
        url = f"{url}&facets={facets}"

    url = url.replace("'", '"')

    request = get(url)
    results = request.json()

    translated_results = []
    for project in results["hits"]:
        translated_results.append(translate_from_modrinth(project))
        
    return translated_results

def translate_from_curseforge(project: dict) -> dict:
    all_versions = []
    all_modloaders = []
    
    for file_index in project.get("latestFilesIndexes", []):
        if file_index.get("gameVersion"):
            all_versions.append(file_index["gameVersion"])
        if file_index.get("modLoader"):
            modloader = file_index["modLoader"]
            if modloader == 4:
                modloader = "fabric"
            elif modloader == 5:
                modloader = "quilt"
            elif modloader == 6:
                modloader = "neoforge"

            all_modloaders.append(modloader)
    
    deduplicated_modloaders = []
    for modloader in all_modloaders:
        if modloader not in deduplicated_modloaders:
            deduplicated_modloaders.append(modloader)
    
    return {
        "name": project["name"],
        "id": project["id"],
        "slug": project["slug"],
        "origin": "curseforge",
        "description": project.get("summary", ""),
        "categories": [category["name"] for category in project.get("categories", [])],
        "downloads": project.get("downloadCount", 0),
        "authors": [author["name"] for author in project.get("authors", [])],
        "icon_url": project.get("logo", {}).get("thumbnailUrl", ""),
        "project_url": project.get("links", {}).get("websiteUrl", ""),
        "modloader": deduplicated_modloaders,
        "version": sorted(list(set(all_versions))),
    }

def translate_from_modrinth(project: dict) -> dict:
    modloader_categories = ["forge", "fabric", "quilt", "neoforge", "rift", "liteloader"]
    
    modloaders = [cat for cat in project.get("categories", []) 
                 if cat.lower() in modloader_categories]
    
    categories = [cat for cat in project.get("categories", []) 
                 if cat.lower() not in modloader_categories]
    
    return {
        "name": project["title"],
        "id": project["project_id"],
        "slug": project["slug"],
        "origin": "modrinth",
        "description": project.get("description", ""),
        "categories": sorted(categories),
        "downloads": project.get("downloads", 0),
        "authors": [project.get("author", "")],
        "icon_url": project.get("icon_url", ""),
        "project_url": f"https://modrinth.com/mod/{project['slug']}",
        "modloader": sorted(modloaders),
        "version": sorted(project.get("versions", [])),
    }

def get_download_modrinth(id: str = None, slug: str = None, version: str = None, modloader: str = None):
    if not id and not slug:
        raise ValueError("Either 'id' or 'slug' must be provided")
    if id:
        url = f"{base_url_modrinth}project/{id}/version"
    else:
        url = f"{base_url_modrinth}project/{slug}/version"
    
    response = get(url)
    response.raise_for_status()
    versions = response.json()
    
    for ver in versions:
        if not version in ver["game_versions"]:
            continue
        if not modloader in ver["loaders"]:
            continue

        return ver["files"][0]["url"]

def get_download_curseforge(id: int = None, slug: str = None, version: str = None, modloader: str = None):
    if not id and not slug:
        raise ValueError("Either 'id' or 'slug' must be provided")
    
    if modloader == "fabric":
        modloader = "Fabric"
    elif modloader == "forge":
        modloader = "Forge"
    elif modloader == "neoforge":
        modloader = "NeoForge"
    
    headers = {"x-api-key": curseforge_key}
    
    if id:
        url = f"{base_url_curseforge}mods/{id}/files"
    else:
        url = f"{base_url_curseforge}mods/search?gameId=432&slug={slug}"
        response = get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data["data"]:
            raise ValueError("Mod not found")
        id = data["data"][0]["id"]
        url = f"{base_url_curseforge}mods/{id}/files"

    response = get(url, headers=headers)
    response.raise_for_status()
    files = response.json()
    versions = files["data"]
    
    for ver in versions:
        if not version in ver["gameVersions"]:
            continue
        if not modloader in ver["gameVersions"]:
            continue
        
        return ver["downloadUrl"]

def get_download(id: str = None, slug: str = None, version: str = None, modloader: str = None, origin: str = None):
    if origin == "curseforge":
        return get_download_curseforge(int(id), slug, version, modloader)
    elif origin == "modrinth":
        return get_download_modrinth(id, slug, version, modloader)
    else:
        raise ValueError("Invalid origin")

def download(url: str, path: str):
    response = get(url, stream=True)
    response.raise_for_status()
    with open(path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def download_mod(id: int = None, slug: str = None, version: str = None, modloader: str = None, origin: str = None, path: str = None):
    url = get_download(id, slug, version, modloader, origin)
    download(url, url.split("/")[-1])

def is_modloader_available_curseforge(id: int, slug: str, version: str, modloader: str):
    return get_download_curseforge(id, slug, version, modloader) is not None

def is_modloader_available_modrinth(id: str, slug: str, version: str, modloader: str):
    return get_download_modrinth(id, slug, version, modloader) is not None

def is_modloader_available(id: int = None, slug: str = None, version: str = None, modloader: str = None, origin: str = None):
    if origin == "curseforge":
        return is_modloader_available_curseforge(id, slug, version, modloader)
    elif origin == "modrinth":
        return is_modloader_available_modrinth(id, slug, version, modloader)
    else:
        raise ValueError("Invalid origin")