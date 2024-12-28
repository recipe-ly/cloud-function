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
                    "content": os.environ["INGREDIENTS_PROMPT"],
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