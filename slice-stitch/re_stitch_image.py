import os
from PIL import Image

def restitch_image(input_folder, output_image_path, tile_size=512):
    # Get all tile file names
    tile_files = sorted(f for f in os.listdir(input_folder) if f.endswith(".jpg"))

    if not tile_files:
        print("No tiles found in the input folder.")
        return

    # Filter out filenames that don't match the expected format
    valid_tiles = []
    for tile_file in tile_files:
        try:
            row, col = tile_file.split("_")
            row = int(row)
            col = int(col.split(".")[0])  # Remove file extension and parse
            valid_tiles.append((row, col, tile_file))
        except (ValueError, IndexError):
            print(f"Skipping invalid tile: {tile_file}")

    if not valid_tiles:
        print("No valid tiles found after filtering.")
        return

    # Determine grid size from valid tiles
    rows = max(row for row, _, _ in valid_tiles)
    cols = max(col for _, col, _ in valid_tiles)

    # Create a blank image for re-stitching
    output_width = cols * tile_size
    output_height = rows * tile_size
    stitched_image = Image.new("RGB", (output_width, output_height))

    for row, col, tile_file in valid_tiles:
        tile_path = os.path.join(input_folder, tile_file)
        tile = Image.open(tile_path)

        # Calculate where to paste this tile
        left = (col - 1) * tile_size
        upper = (row - 1) * tile_size
        stitched_image.paste(tile, (left, upper))

    # Save the final image
    stitched_image.save(output_image_path)
    print(f"Re-stitching complete. Output saved to '{output_image_path}'.")

# Example usage
if __name__ == "__main__":
    input_folder = "processed_images"
    output_image_path = "restitched_image.jpg"
    restitch_image(input_folder, output_image_path)
