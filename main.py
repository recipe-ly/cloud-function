import openai
import base64
import json
import os



def main(context):
    openai.api_key = os.environ['OPENAI_API_KEY']

    if not context.req.body:
        return context.res.json({"error": "No image provided"}, status_code=400)

    try:
        image_data = context.req.body.decode()

        response = openai.Image.create(
            prompt="Analyze this image and suggest recipes based on it",
            image=image_data,
            model="gpt-4o-mini",
        )

        suggestions = response.get('choices', [{}])[0].get('text', 'No suggestions available')

        return context.res.json({"recipes": suggestions})
    except Exception as e:
        return context.res.json({"error": str(e)}, status_code=500)

