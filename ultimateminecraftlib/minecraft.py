import minecraft_launcher_lib as mll

def install_minecraft(path: str, version: str, modloader: str, modloader_version: str):
    if "-loader" in modloader:
        modloader = modloader.split("-")[0]

    print(f"Installing Minecraft {version} with {modloader} {modloader_version} to {path}")

    if modloader == "fabric":
        mll.fabric.install_fabric(version, path, modloader_version)
    if modloader == "forge":
        mll.forge.install_forge(version, path, modloader_version)
    if modloader == "neoforge":
        mll.forge.install_forge(version, path, modloader_version)
    if modloader == "quilt":
        mll.quilt.install_quilt(version, path, modloader_version)
    if modloader == None or modloader == "" or modloader.lower() == "none" or modloader == "vanilla":
        mll.minecraft.install_minecraft(version, path)

def launch_minecraft(path: str):
    with open(f"{path}/version", "r") as f:
        version = f.read()

    print(f"Launching Minecraft {version} from {path}")
    command = mll.command.get_minecraft_command(version, path)
    print(command)