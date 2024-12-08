import os
from PIL import Image

def slice_image(input_image_path, output_folder, tile_size=512):
    # Open the image
    img = Image.open(input_image_path)
    width, height = img.size
    
    # Calculate the number of tiles needed in each direction
    cols = (width + tile_size - 1) // tile_size
    rows = (height + tile_size - 1) // tile_size

    # Create output directory
    os.makedirs(output_folder, exist_ok=True)

    for row in range(1, rows + 1):  # Start at 1
        for col in range(1, cols + 1):  # Start at 1
            # Calculate the tile coordinates
            left = (col - 1) * tile_size
            upper = (row - 1) * tile_size
            right = min(left + tile_size, width)
            lower = min(upper + tile_size, height)

            # Create the tile
            tile = img.crop((left, upper, right, lower))

            # Add black padding if necessary
            if tile.size != (tile_size, tile_size):
                padded_tile = Image.new("RGB", (tile_size, tile_size), (0, 0, 0))
                padded_tile.paste(tile, (0, 0))
                tile = padded_tile

            # Save the tile with the naming convention
            tile_filename = f"{row:03}_{col:03}.jpg"
            tile.save(os.path.join(output_folder, tile_filename))

    print(f"Slicing complete. Tiles saved in '{output_folder}'.")

# Example usage
if __name__ == "__main__":
    input_image_path = "input_image.jpg"  # Replace with your input image path
    output_folder = "sliced_images"
    slice_image(input_image_path, output_folder)
