import json
import os
from pathlib import Path
from pprint import pprint
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import JSONLoader

openai_key = os.getenv('OPENAI_API_KEY')
file_path = './recipes_raw_nosource_fn.json'

# loader = JSONLoader(file_path=file_path, jq_schema='.[]', text_content=False)
with open(file_path, 'r') as file:
    data = json.load(file)

def get_embedding_function():
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    return embeddings

def prepare_metadata(recipe):
    metadata = recipe.copy()
    
    # Use .get() to avoid KeyError and provide a default value if 'ingredients' is missing
    ingredients_list = metadata.get('ingredients', [])  # Default to an empty list if 'ingredients' is missing
    
    # Convert the ingredients list to a single string
    metadata['ingredients'] = ', '.join(ingredients_list) if ingredients_list else 'No ingredients provided'
    
    # Handle other None values in metadata by converting them to empty strings
    for key, value in metadata.items():
        if value is None:
            metadata[key] = ""  # Replace None with an empty string or a default value
    
    return metadata

def prepare_recipe_text(recipe):
    title = recipe.get('title ', 'Untitled Recipe')  # Default to 'Untitled Recipe' if 'title' is missing
    ingredients = ', '.join(recipe.get('ingredients', []))  # Default to empty list if 'ingredients' is missing
    instructions = recipe.get('instructions', 'No instructions provided.')  # Default to a message if missing
    combined_text = f"Recipe title: {title}\nIngredients: {ingredients}\nInstructions: {instructions}"
    return combined_text

recipes_to_add = list(data.items())[1982:]
count = 1982    #Stopped at 12182!!
total = len(data)
for recipe_id, recipe_data in data.items():
    combined_text = prepare_recipe_text(recipe_data)
    metadata = prepare_metadata(recipe_data)
    db = Chroma(persist_directory= 'chroma', embedding_function=get_embedding_function())
    db.add_texts(texts=[combined_text], metadatas=[metadata], ids=[recipe_id])
    count += 1
    print(f"Added recipe to the database. {count}/{total}")


