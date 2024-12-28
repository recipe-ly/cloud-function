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


class Ingredient(BaseModel):
    name: str
    product: str
    type: str
    amount: int
    unit: Unit

class IngredientsList(BaseModel):
    ingredients: list[Ingredient]


def main(context):
    
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    if not context.req.body:
        return context.res.json({"error": "No image provided"}, status_code=400)

    try:
        image_data = context.req.body

        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an ingredient analyzer. Check the follow picture and return the list of ingredients based on everything you can see on the picture, i want you to return all the products, fruits and vegetables.
i want you want to return everything in the structure of a json list of ingredients. Each Ingredient should have a name, product, type, amount and unit. the name will be the label it has on it if any,
the product should be a simple name of what that ingredient is like is it pea or precisely what that item is this needs to precise, in the case of spices please return a coma separated list of all the spices that the one in the picture might match.
for the amount, please return a number, and unit return one from the standard units. please make sure to accurately get the type of the item to the precise thing it is.""",
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
            temperature=0.0

        )

        suggestions = response.choices[0]
        context.log(suggestions)
        
        return context.res.json({"recipes": suggestions.message.parsed.dict()})
    except Exception as e:
        context.log(e)
        return context.res.json({"error": str(e)})