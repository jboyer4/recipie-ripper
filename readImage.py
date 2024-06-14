#!/usr/bin/env python3
# https://www.reddit.com/r/Python/comments/16f0yla/so_you_decided_to_extract_recipe_text_from_scans/
# https://www.reddit.com/r/Python/comments/18t726b/pure_recipe_is_a_cli_app_to_save_or_view_online/
# https://www.reddit.com/r/Python/comments/mga8xy/an_open_source_recipe_book_database_with_a_flask/
# https://www.reddit.com/r/Python/comments/s5yb6m/i_made_a_recipe_creatorfinder_in_python/
from imageProcessing import cleanImage
import pytesseract
import re

# These keywords are used to try to roughly identify recipie sections
ingredients_keyword = "ingredients"
instructions_keywords = ["instructions", "directions", "how to"]

# extract_text_from_image
# image_path: where to find the image we'd like to get a recipe from
# Send the image to imageProcessing.py to clean it up in opencv before trying to extract text with tesseract
def extract_text_from_image(image_path):
    prossedImage = cleanImage(image_path)
    text = pytesseract.image_to_string(prossedImage)
    
    return text

# extract_sections
# text: The raw text extracted from the image
# Here we'll split the text roughly into 2 sections for the ingredients and instructions. There may be extra text in each section at this stage
# but we'll worry about that later
def extract_sections(text):
    lower_text = text.lower()
    # Find the ingredients
    ingredients_start = lower_text.find(ingredients_keyword)
    ingredients_end = None

    if ingredients_start != -1:
        instructions_start = min([lower_text.find(kw) for kw in instructions_keywords if lower_text.find(kw) != -1], default=-1)
        # End the ingredients section at the start of the instructions
        if instructions_start != -1:
            ingredients_end = instructions_start
            ingredients_section = text[ingredients_start:ingredients_end]
        else:
            ingredients_section = text[ingredients_start:]

        # Extract the instructions section
        instructions_section = text[instructions_start:] if instructions_start != -1 else None
    else:
        #TODO: add more advance parsing if this fails and quit if that fails
        ingredients_section = None
        instructions_section = None

    return ingredients_section, instructions_section

# parse_ingredients
# ingredients_text: The section extracted associated with the ingredients keywords
# Returns an object contining a list of ingredients and possilby contianing the prep time, cook time, or servings 
def parse_ingredients(ingredients_text):
    # Ingredients must be split by line
    # TODO test performance without this restriction to consider allowing more flexibilty
    lines = ingredients_text.split('\n')

    # Initialize return object
    recipe_json = {
        "ingredients": [],
        "prepTime": None,
        "cookTime": None,
        "servings": None
    }

    for line in lines:
        line = line.strip().lower()
        if line and not line.startswith("ingredients"):
            # Check for ingredient pattern
            # Grep ingredient lines assuming it starts with a number, a fraction, or 'a'
            ingredient_pattern = re.compile(r'^(\d+|\d+/\d+|a)(\s|\s.*$)')
            if ingredient_pattern.match(line):
                recipe_json["ingredients"].append(line)
            
            # Check if the line contians the prep or cooktime
            elif "time" in line:
                if "cook" in line:
                    recipe_json["cookTime"] = line
                else:
                    recipe_json["prepTime"] = line
            # Check if the line contians the prep or cooktime
            elif "serving" in line:
                recipe_json["servings"] = line
    return recipe_json

# TODO I don't think I want this to be main
if __name__ == "__main__":
    image_path = "ingredients.jpg" #todo make this take input
    image_path2 = "proteinPancake.jpg"
    extracted_text = extract_text_from_image(image_path2)

    # testing: Print the extracted text
    print("Extracted Text:")
    print(extracted_text.lower())

    ingredients_section, instructions_section = extract_sections(extracted_text)
    print("Ingredients Section:\n", ingredients_section)
    print("Instructions Section:\n", instructions_section)

    # Parse ingredients
    ingredient_obj = parse_ingredients(ingredients_section)