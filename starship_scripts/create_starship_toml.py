from pathlib import Path
from re import match

# Function to check the format of the colors is correct and there are enough colors
def ensure_color_palette_format(colors: list[str]) -> bool:
    if not len(colors) >= 5:
        print("Color palette file does not have enough colors/lines, min 5. Exiting...")
        exit(0)

    for color in colors:
        if not match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            print("The colors are not the correct format. Use '#xxxxxx' or '#xxx'")
            exit(0)
    
# Function to handle overwriting existing starship.toml
def write_or_overwrite_starshiptoml_with_permission(template: str):
    response = not Path("starship.toml").exists() or input("starship.toml already exists. Overwrite? (Y/n):").lower().strip()
    if response in (True, "y", "yes", ""):
        Path("starship.toml").write_text(template)
        print("Wrote starship.toml! Copy or move it to ~/.config/starship.toml")
        exit(0)
    elif response in ("n", "no"):
        print("Exiting...")
        exit(0)
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        write_or_overwrite_starshiptoml_with_permission()

# Get the color palette
color_palette_path: str = "./color_palettes/" + input("Enter color palette filename (./color_palettes/___): ")

while not Path(color_palette_path).exists():
    color_palette_path = "./color_palettes/" + input("File not found. Must be in './color_palettes': ")
color_palette: list[str] = Path(color_palette_path).read_text().splitlines()

for i, color in enumerate(color_palette):
    color_palette[i] = color.strip()

ensure_color_palette_format(color_palette)

# Get the template
template_path = Path("template.toml")
if not template_path.exists():
    print(f"Could not find '{template_path.name}'. Exiting...")
    exit(0)
template: str = template_path.read_text()

# Replace color placeholders in the template
for i, color in enumerate(color_palette):
    template = template.replace(f"$COLOR{i}", color)

write_or_overwrite_starshiptoml_with_permission(template)