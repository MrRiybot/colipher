from PIL import Image
import math

def hex_to_decimal(hex_color):
    """Converts a hex color to decimal."""
    return int(hex_color[1:], 16)

def group_all_hex_colors(n_groups):
    """Groups all possible hex colors into n groups."""
    # Maximum decimal value for a color
    max_color_value = 256**3
    # Size of each group
    group_size = max_color_value / n_groups
    
    # Dictionary to hold the groups
    groups = {i: [] for i in range(n_groups)}
    
    for i in range(max_color_value):
        # Convert the current index to a hex color
        hex_color = '#' + format(i, '06x')
        # Determine the group for this color
        group_index = int(i // group_size)
        # Append the color to the appropriate group
        groups[group_index].append(hex_color)
    
    return groups

# Example usage: Be careful with large values of n_groups; generating all hex colors is impractical


# Defining a comprehensive list of Arabic characters and Tashkeel to ensure accurate mapping
arabic_chars_list =['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'َ', 'ي', 'ر', 'إ', 'ه', 'ط', 'م', 'ئ', 'ص', 'ج', 'ظ', 'ح', 'ث', 'ض', ' ', 'د', 'ن', 'ا', 'ة', 'ش', 'أ', 'ف', 'ِ', 'ى', 'ٍ', 'ب', 'آ', 'ّ', 'ٌ', 'ك', 'ء', 'س', 'ق', 'ُ', 'ز', 'خ', 'ع', 'ذ', 'غ', 'و', 'ل', 'ٌ', 'ً', 'ت', 'ْ', 'ؤ']
print(len(arabic_chars_list))
n_groups = group_all_hex_colors(len(arabic_chars_list))

def prep_value_index(n_groups):
    # Step 1: Preprocess to create a value-to-index mapping
    value_to_index_map = {}
    for index, group in enumerate(n_groups):
        for value in n_groups[index]:
            value_to_index_map[value] = index
    return value_to_index_map

value_to_index = prep_value_index(n_groups)



# Create mappings based on the ordered list
char_to_id_mapping = {char: index for index, char in enumerate(arabic_chars_list)}
id_to_char_mapping = {index: char for index, char in enumerate(arabic_chars_list)}

def text_to_arabic_char_ids(text):
    return [char_to_id_mapping.get(char, None) for char in text if char in char_to_id_mapping]

def arabic_char_ids_to_text(ids):
    return ''.join(id_to_char_mapping.get(id, '') for id in ids)

def string_to_unicode_indices(input_string):
    # Convert each character in the string to its Unicode code point
    unicode_indices = [ord(char) for char in input_string]
    return unicode_indices

# Example usage
sample_text = "Hello, World!"
unicode_indices = string_to_unicode_indices(sample_text)
print(unicode_indices)
def unicode_indices_to_string(indices):
    # Convert each Unicode code point in the list to its corresponding character
    characters = [chr(index) for index in indices]
    return ''.join(characters)

def filter_chars_by_max_colipher_decimal(max_value, text):
    return ''.join(char if char in arabic_chars_list else ' ' for char in text)
    
def find_value_index(groups, value):
    for index, group in enumerate(groups):
        if value in groups[index]:
            return index
    return None


def int_to_hex(int_list):
    hex_list = []
    for i in int_list:
        hex_list.append(n_groups[i][int(len(n_groups[i])/2)])
    return hex_list

def hex_to_int_optimized(hex_list, value_to_index_map):
    return [(value_to_index_map[h]) for h in hex_list]

    

def create_color_blocks_image(hex_colors, block_size=10,colors_per_row=5):
    # Determine the image dimensions
    # Adjust as needed
    img_width = colors_per_row * block_size
    img_height = ((len(hex_colors) - 1) // colors_per_row + 1) * block_size
    
    # Create a new image
    image = Image.new('RGB', (img_width, img_height), 'white')
    
    # Draw the color blocks
    for i, hex_color in enumerate(hex_colors):
        x = (i % colors_per_row) * block_size
        y = (i // colors_per_row) * block_size
        for dx in range(block_size):
            for dy in range(block_size):
                image.putpixel((x+dx, y+dy), tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
    
    return image

def image_to_hex_codes(image_path, colors_per_col=None,block_size=10, colors_per_row=5):
    
    # Load the image
    image = Image.open(image_path)
    
    
    # Determine the number of rows and columns
    img_width, img_height = image.size
    if(colors_per_col!=None):
        print("hmm")
        block_size = img_height // colors_per_col
        print(block_size)
    num_rows = int(img_height // block_size)
    num_cols = min(colors_per_row, img_width // block_size)
    
    hex_colors = []
    
    # Iterate over each block
    for row in range(num_rows):
        for col in range(num_cols):
            # Calculate the starting pixel of the block
            x = col * block_size
            y = row * block_size
            
            # Sample a pixel from the block
            pixel = image.getpixel((x + block_size//2, y + block_size//2))
            
            # Convert the pixel to hex
            hex_color = '#{0:02x}{1:02x}{2:02x}'.format(pixel[0], pixel[1], pixel[2])
            hex_colors.append(hex_color)
            
            # Break if we have collected enough colors per the input image's size and parameters
            if len(hex_colors) >= num_rows * num_cols:
                break
    
    return hex_colors


def colipher(text,image_path):
    text = text.lower()
    color_per_row = int(math.sqrt(len(text)))
    text = filter_chars_by_max_colipher_decimal(150, text)
    indices = text_to_arabic_char_ids(text)
    print(indices)
    hex_list = int_to_hex(indices)
    im = create_color_blocks_image(hex_list,block_size=30,colors_per_row=color_per_row)
    im.save(image_path)

def decolipher(image_path,blocks_count,colors_per_row):
    hex_codes = image_to_hex_codes(image_path,block_size=30,colors_per_row=colors_per_row,colors_per_col=blocks_count)
    int_list = hex_to_int_optimized(hex_codes, value_to_index)
    print(int_list)
    message = arabic_char_ids_to_text(int_list)
    return message