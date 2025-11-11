from pathlib import Path
from re import match

STARSHIP_TOML_PATH = Path("../starship.toml")
COLOR_PALETTE_FOLDER_PATH = Path("./color_palettes/")
TEMPLATE_PATH = Path("./template.toml")

# Function to check the format of the colors is correct and there are enough colors
def ensure_color_palette_format(colors: list[str]) -> bool:
    if not len(colors) >= 5:
        print("Color palette file does not have enough colors/lines, the minimum is 5. Exiting...")
        exit(1)

    for color in colors:
        if not match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            print("The colors are not the correct format. Use '#xxxxxx' or '#xxx'")
            exit(1)
    
# Function to handle overwriting existing starship.toml
def write_or_overwrite_starshiptoml_with_permission(template: str):
    response = not STARSHIP_TOML_PATH.exists() or input("starship.toml already exists. Overwrite? (Y/n):").lower().strip()
    if response in (True, "y", "yes", ""):
        STARSHIP_TOML_PATH.write_text(template)
        print("Wrote starship.toml! Copy or move it to ~/.config/starship.toml")
        exit(0)
    elif response in ("n", "no"):
        print("Exiting...")
        exit(0)
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        write_or_overwrite_starshiptoml_with_permission()

# Get the color palette
color_palette_path: str = str(COLOR_PALETTE_FOLDER_PATH) + "/" + input("Enter color palette filename (./color_palettes/___): ")

while not color_palette_path.exists():
    color_palette_path = str(COLOR_PALETTE_FOLDER_PATH) + "/" + input("File not found. Must be in './color_palettes': ")
color_palette: list[str] = Path(color_palette_path).read_text().splitlines()

for i, color in enumerate(color_palette):
    color_palette[i] = color.strip()

ensure_color_palette_format(color_palette)

# Get the template
if not TEMPLATE_PATH.exists():
    print(f"Could not find '{TEMPLATE_PATH.name}'. Exiting...")
    exit(1)
template: str = TEMPLATE_PATH.read_text()

# Replace color placeholders in the template
for i, color in enumerate(color_palette):
    template = template.replace(f"$COLOR{i}", color)

write_or_overwrite_starshiptoml_with_permission(template)