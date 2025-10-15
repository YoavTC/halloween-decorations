import json
import csv
import os

def recipe_output_to_loot_table(recipe_data):
    """
    Converts Minecraft recipe output to a loot table JSON.
    """
    result = recipe_data.get("result", {})
    item_id = result.get("id", "minecraft:air")
    item_count = result.get("count", 1)
    components = result.get("components", {})

    entry = {
        "type": "minecraft:item",
        "name": item_id,
    }
    functions = []
    if components:
        functions.append({
            "function": "minecraft:set_components",
            "components": components
        })
    if item_count > 1:
        functions.append({
            "function": "minecraft:set_count",
            "count": item_count
        })
    if functions:
        entry["functions"] = functions

    loot_table = {
        "pools": [
            {
                "rolls": 1,
                "entries": [entry]
            }
        ]
    }
    return loot_table

def load_original_keys(item_id, original_recipe_dir):
    """Load the original key mappings, custom name, and deco_id from existing recipe file"""
    original_file = os.path.join(original_recipe_dir, f'{item_id}.json')
    if os.path.exists(original_file):
        with open(original_file, 'r', encoding='utf-8') as f:
            original_recipe = json.load(f)
            return {
                'keys': original_recipe.get('key', {}),
                'custom_name': original_recipe['result']['components']['minecraft:custom_name']['text'],
                'deco_id': original_recipe['result']['components']['minecraft:custom_data']['deco_id']
            }
    return None

def numeric_to_pattern(numeric_pattern, keys):
    """Convert numeric pattern back to recipe pattern with keys"""
    # Create mapping of numbers to keys
    key_list = list(keys.keys())
    num_to_key = {str(idx): key for idx, key in enumerate(key_list, 1)}
    num_to_key['0'] = ' '
    
    # Determine pattern dimensions based on length
    pattern_length = len(numeric_pattern)
    if pattern_length == 6:  # 2x3 pattern
        rows = 2
        cols = 3
    elif pattern_length == 9:  # 3x3 pattern
        rows = 3
        cols = 3
    else:
        # Try to infer dimensions
        rows = (pattern_length + 2) // 3  # Round up division
        cols = 3
    
    # Convert numeric string to pattern
    pattern = []
    for i in range(rows):
        row = ''
        for j in range(cols):
            idx = i * cols + j
            if idx < len(numeric_pattern):
                row += num_to_key.get(numeric_pattern[idx], ' ')
            else:
                row += ' '
        pattern.append(row)
    
    return pattern

def create_recipe_json(item_id, recipe_keys, recipe_pattern, texture, hitbox, author, url, original_data=None):
    """Create a recipe JSON structure from CSV data"""
    # Parse recipe keys
    key_items = [k.strip() for k in recipe_keys.split(',')]
    
    # Add minecraft: prefix if not present
    key_items = [f'minecraft:{item}' if not item.startswith('minecraft:') and not item.startswith('#') else item for item in key_items]
    
    # Use original keys if available, otherwise create new mapping
    if original_data and 'keys' in original_data:
        keys = original_data['keys']
    else:
        # Create key mapping
        # Standard single character keys
        key_chars = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        keys = {}
        for i, item in enumerate(key_items):
            if i < len(key_chars):
                keys[key_chars[i]] = item
    
    # Convert numeric pattern to recipe pattern
    pattern = numeric_to_pattern(recipe_pattern, keys)
    
    # Parse hitbox into width and height
    hitbox_parts = hitbox.split(',')
    width = float(hitbox_parts[0].strip())
    height = float(hitbox_parts[1].strip())
    
    # Use original custom name if available, otherwise generate from item_id
    if original_data and 'custom_name' in original_data:
        custom_name = original_data['custom_name']
    else:
        custom_name = f"{item_id.replace('_', ' ').title()} Decoration"
    
    # Use original deco_id if available, otherwise use item_id
    if original_data and 'deco_id' in original_data:
        deco_id = original_data['deco_id']
    else:
        deco_id = item_id
    
    # Create the full recipe structure
    recipe = {
        "type": "minecraft:crafting_shaped",
        "key": keys,
        "pattern": pattern,
        "result": {
            "components": {
                "minecraft:profile": {
                    "properties": [
                        {
                            "name": "textures",
                            "value": texture
                        }
                    ]
                },
                "minecraft:attribute_modifiers": [
                    {
                        "type": "minecraft:block_interaction_range",
                        "id": "block_interaction_range",
                        "amount": -5,
                        "operation": "add_multiplied_total",
                        "slot": "hand"
                    }
                ],
                "minecraft:tooltip_display": {
                    "hidden_components": [
                        "minecraft:attribute_modifiers"
                    ]
                },
                "minecraft:equippable": {
                    "slot": "chest",
                    "equip_sound": "minecraft:ui.cartography_table.take_result",
                    "allowed_entities": "minecraft:armor_stand"
                },
                "minecraft:custom_data": {
                    "deco": True,
                    "deco_id": deco_id,
                    "deco_width": width,
                    "deco_height": height
                    # "deco_size": deco_size
                },
                "minecraft:custom_name": {
                    "text": custom_name,
                    "color": "#ffbf00",
                    "bold": False,
                    "italic": False
                },
                "minecraft:lore": [
                    [
                        {
                            "text": f"Model by {author}",
                            "color": "dark_gray",
                            "bold": False,
                            "italic": False
                        }
                    ],
                    [
                        {
                            "text": url,
                            "color": "dark_gray",
                            "bold": False,
                            "italic": False
                        }
                    ]
                ]
            },
            "count": 1,
            "id": "minecraft:player_head"
        },
        "show_notification": False
    }
    
    return recipe

def main():
    # Paths (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    csv_file = os.path.join(script_dir, 'items.csv')
    recipe_output_dir = os.path.join(project_root, 'src', 'data', 'halloweendeco', 'recipe')
    loot_table_output_dir = os.path.join(project_root, 'src', 'data', 'halloweendeco', 'loot_table')
    function_output_dir = os.path.join(project_root, 'src', 'data', 'halloweendeco', 'function')
    spawn_function_dir = os.path.join(project_root, 'src', 'data', 'halloweendeco', 'function', 'spawn')
    original_recipe_dir = os.path.join(project_root, 'src', 'data', 'halloweendeco', 'recipe')
    
    # Create output directories
    os.makedirs(recipe_output_dir, exist_ok=True)
    os.makedirs(loot_table_output_dir, exist_ok=True)
    os.makedirs(function_output_dir, exist_ok=True)
    os.makedirs(spawn_function_dir, exist_ok=True)
    
    # List to store all recipe IDs for the mcfunction file
    recipe_ids = []
    
    # Read CSV and generate recipes
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        for row in reader:
            item_id = row['id']
            recipe_keys = row['recipe keys']
            recipe_pattern = row['recipe pattern']
            texture = row['texture']
            hitbox = row['hitbox']
            author = row['author']
            url = row['url']
            
            # Load original keys to preserve key letter mappings
            original_data = load_original_keys(item_id, original_recipe_dir)
            
            # Generate recipe JSON
            recipe = create_recipe_json(item_id, recipe_keys, recipe_pattern, texture, hitbox, author, url, original_data)
            
            # Write recipe to file
            recipe_output_file = os.path.join(recipe_output_dir, f'{item_id}.json')
            with open(recipe_output_file, 'w', encoding='utf-8') as out_f:
                json.dump(recipe, out_f, indent=2, ensure_ascii=False)
            
            # Generate loot table from recipe
            loot_table = recipe_output_to_loot_table(recipe)
            
            # Write loot table to file
            loot_table_output_file = os.path.join(loot_table_output_dir, f'{item_id}.json')
            with open(loot_table_output_file, 'w', encoding='utf-8') as out_f:
                json.dump(loot_table, out_f, indent=2, ensure_ascii=False)
            
            # Generate spawn function file if it doesn't exist
            spawn_function_file = os.path.join(spawn_function_dir, f'{item_id}.mcfunction')
            if not os.path.exists(spawn_function_file):
                with open(spawn_function_file, 'w', encoding='utf-8') as out_f:
                    out_f.write('')  # Create empty file
                print(f'Generated: spawn/{item_id}.mcfunction (empty)')
            
            # Add to recipe IDs list
            recipe_ids.append(item_id)
            
            print(f'Generated: {item_id}.json (recipe, loot table, and advancement)')
    
    # Generate grant_all_recipes.mcfunction file
    mcfunction_file = os.path.join(function_output_dir, 'give_all_recipes.mcfunction')
    with open(mcfunction_file, 'w', encoding='utf-8') as f:
        for recipe_id in recipe_ids:
            f.write(f'recipe give @a halloweendeco:{recipe_id}\n')
    
    print(f'Generated: give_all_recipes.mcfunction')
    print(f'\nRecipes generated in: {recipe_output_dir}')
    print(f'Loot tables generated in: {loot_table_output_dir}')
    print(f'Spawn functions generated in: {spawn_function_dir}')
    print(f'Function generated in: {function_output_dir}')
    
    # Process spawn function files to ensure Tags:[deco_parent] is present
    process_spawn_functions(spawn_function_dir)

def process_spawn_functions(spawn_function_dir):
    """Process all spawn function files to ensure summon commands have Tags:[deco_parent]"""
    import os
    import re
    
    print(f'\nProcessing spawn function files...')
    
    for filename in os.listdir(spawn_function_dir):
        if filename.endswith('.mcfunction'):
            filepath = os.path.join(spawn_function_dir, filename)
            
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip empty files
            if not content.strip():
                continue
            
            # Process each line that starts with summon
            lines = content.split('\n')
            modified = False
            
            for i, line in enumerate(lines):
                if line.strip().startswith('summon '):
                    # Check if Tags:[deco_parent] is already present
                    if 'Tags:[deco_parent]' not in line:
                        # Find the position after the coordinates (~ ~ ~) and before the opening brace
                        match = re.search(r'(summon\s+\S+\s+~\s+~\s+~\s+)(\{.*)', line)
                        if match:
                            prefix = match.group(1)
                            nbt_data = match.group(2)
                            
                            # Insert Tags:[deco_parent] at the beginning of NBT data
                            if nbt_data.startswith('{') and len(nbt_data) > 1:
                                # Insert after the opening brace
                                new_line = prefix + '{Tags:[deco_parent],' + nbt_data[1:]
                                lines[i] = new_line
                                modified = True
                                print(f'  Updated {filename}: Added Tags:[deco_parent]')
            
            # Write back if modified
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
    
    print('Spawn function processing complete.')

if __name__ == '__main__':
    main()
