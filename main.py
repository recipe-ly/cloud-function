from openai import OpenAI
import base64
import os
from pydantic import BaseModel

class Ingredient(BaseModel):
    name: str
    type: str
    amount: str
    unit: str

class IngredientsList(BaseModel):
    ingredients: list[Ingredient]


def main(context):

    base_url =  os.environ["API_URL"] or "https://api.openai.com/v1"
    
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=base_url)

    if not context.req.body:
        return context.res.json({"error": "No image provided"}, status_code=400)

    try:
        image_data = context.req.body

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an ingredient analyzer. Check the follow picture and return the list of ingredients based on everything you can see on the picture, i want you to return all the products, fruits and vegetables.
i want you want to return everything in the structure of a json list of ingredients. Each Ingredient should have a name, type, amount and unit. the name will be the label it has on it if any,
the type should be a simple name of what that ingredient is like is it pea or is some type of meat, in the case of spices please return a coma separated list of all the spices that the one in the picture might match.
for the amount, please return a number, and unit return one from the standard units""",
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
        
        return context.res.json({"recipes": suggestions.content})
    except Exception as e:
        context.log(e)
        return context.res.json({"error": str(e)})