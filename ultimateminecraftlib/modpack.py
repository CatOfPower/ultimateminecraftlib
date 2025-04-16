import json
import os
import zipfile

def load_modrinth_pack(path: str):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(path[:-7])
    
    with open(path[:-7] + "/modrinth.index.json", 'r') as file:
        modrinth_data = json.load(file)

    data = {
        "name" : modrinth_data["name"],
        "modpackVersion" : modrinth_data["versionId"],
        "minecraftVersion" : modrinth_data["dependencies"]["minecraft"],
        "modloader" : list(modrinth_data["dependencies"].keys())[1],
        "modloaderVersion" : modrinth_data["dependencies"][list(modrinth_data["dependencies"].keys())[1]],
        "mods" : [],
        "resourcepacks" : [],
    }

    for resource in modrinth_data["files"]:
        url = resource["downloads"][0]
        resource_type = resource["path"].split("/")[0][:-1]
        resource_name = resource["path"].split("/")[1]
        resource_path = resource["path"]
        
        resource = {
            "name" : resource_name,
            "url" : url,
            "path" : resource_path,
        }

        if resource_type == "mod":
            data["mods"].append(resource)
        elif resource_type == "resourcepack":
            data["resourcepacks"].append(resource)
    
    with open(path[:-7] + "/modpack.json", 'w') as file:
        json.dump(data, file, indent=4)
    
    os.remove(path[:-7] + "/modrinth.index.json")

def load_curseforge_pack(path):
    from .api import get_curseforge_project_files

    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(path[:-4])
    
    with open(path[:-4] + "/manifest.json", 'r') as file:
        curseforge_data = json.load(file)
    
    data = {
        "name" : curseforge_data["name"],
        "modpackVersion" : curseforge_data["version"],
        "minecraftVersion" : curseforge_data["minecraft"]["version"],
        "modloader" : curseforge_data["minecraft"]["modLoaders"][0]["id"].split("-")[0],
        "modloaderVersion" : curseforge_data["minecraft"]["modLoaders"][0]["id"].split("-")[1],
        "mods" : [],
        "resourcepacks" : [],
    }

    for file in curseforge_data["files"]:
        project_id = file["projectID"]
        file_id = file["fileID"]
        project_files = get_curseforge_project_files(project_id, file_id)
        url = project_files["data"]["downloadUrl"]
        if project_files["data"]["fileName"].split(".")[-1] == "jar":
            resource_type = "mod"
        elif project_files["data"]["fileName"].split(".")[-1] == "zip":
            resource_type = "resourcepack"
        
        resource_name = project_files["data"]["fileName"]
        resource_path = resource_type + "s/" + project_files["data"]["fileName"]

        resource = {
            "name" : resource_name,
            "url" : url,
            "path" : resource_path,
        }

        if resource_type == "mod":
            data["mods"].append(resource)
        elif resource_type == "resourcepack":
            data["resourcepacks"].append(resource)
        
    with open(path[:-4] + "/modpack.json", 'w') as file:
        json.dump(data, file, indent=4)
    os.remove(path[:-4] + "/manifest.json")
    os.remove(path[:-4] + "/modlist.html")

def install_modpack(path: str):
    with open(path+"/modpack.json", 'r') as file:
        modpack_data = json.load(file)