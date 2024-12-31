from typing import Optional
from openai import OpenAI
import base64
import os
from pydantic import BaseModel
from enum import Enum


class Unit(Enum):
    GRAM = "g"
    KILOGRAM = "kg"
    LITER = "l"
    MILLILITER = "ml"
    CUP = "cup"
    TABLESPOON = "tbsp"
    TEASPOON = "tsp"
    OUNCE = "oz"
    POUND = "lb"
    PIECE = "pcs"


class IngredientType(Enum):
    fruit = "fruit"
    vegetable = "vegetable"
    spice = "spice"
    legume = "legume"
    herb = "herb"
    grain = "grain"
    nut = "nut"
    dairy = "dairy"
    meat = "meat"
    seafood = "seafood"
    oil = "oil"


class Ingredient(BaseModel):
    name: Optional[str]
    product: str
    type: IngredientType
    amount: int
    unit: Unit


class IngredientsList(BaseModel):
    ingredients: list[Ingredient]


class RecipeStep(BaseModel):
    number: int
    description: str


class Recipe(BaseModel):
    name: str
    ingredients: list[Ingredient]
    steps: list[RecipeStep]


class RecipeList(BaseModel):
    recipes: list[Recipe]


def get_ingredients(context, client):
    if not context.req.body:
        return context.res.json({"error": "No image provided"}, status_code=400)

    try:
        image_data = context.req.body

        response = client.beta.chat.completions.parse(
            model=os.environ["OPENAI_MODEL"],
            messages=[
                {
                    "role": "system",
                    "content": """You are an ingredient analyzer. Review the following picture and return a list of ingredients based on everything you can identify in the image, focusing only on products, fruits, and vegetables.
For each ingredient, return a JSON list with the following fields:
name: The label or any specific identifier visible on the ingredient (if applicable).
product: A precise description of what the ingredient is (e.g., "pea," "apple," or "carrot"). Avoid any brand names.
type: The category of the ingredient (e.g., "fruit," "vegetable," "spice," etc.).
amount: The numeric quantity of the ingredient if visible or estimable.
unit: The standard unit of measurement (e.g., "grams," "kilograms," "pieces," "cups," etc.).
If you encounter spices, return a comma-separated list of all spices that the ingredient might correspond to. Please make sure to identify each item with accuracy, providing its exact type and form as seen in the image.""",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data,
                                "detail": "low",
                            },
                        }
                    ],
                },
            ],
            response_format=IngredientsList,
            temperature=0.0,
        )

        suggestions = response.choices[0]
        context.log(suggestions.message)

        return context.res.json(suggestions.message.content)
    except Exception as e:
        context.log(e)
        return context.res.json({"error": str(e)})


def get_recipes(context, client):
    try:
        ingredients_data = context.req.body

        response = client.beta.chat.completions.parse(
            model=os.environ["OPENAI_MODEL"],
            messages=[
                {
                    "role": "system",
                    "content": """You are a highly skilled and imaginative chef. I will provide you with a list of ingredients in JSON format, and your task is to create 3 unique, flavorful and different recipes using these ingredients. The recipes should be creative, well-structured, and easy to follow.  
For each ingredient, return a JSON list:
For each recipe return a JSON list with the following fields:
For each step return a JSON list with the following fields:
name: If no name already exists generate one yourself.
number: The step numbers counting from one.
description: The description of how to perform the step.
All fields are essential, please don't omit any.
""",
                },
                {"role": "user", "content": ingredients_data},
            ],
            response_format=RecipeList,
            temperature=0.0,
        )

        suggestions = response.choices[0]
        context.log(suggestions)

        return context.res.json(suggestions.message.parsed.json())
    except Exception as e:
        context.log(e)
        return context.res.json({"error": str(e)})


def main(context):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    if context.req.path == "/get/ingredients":
        return get_ingredients(context, client)
    if context.req.path == "/get/recipes":
        return get_recipes(context, client)
