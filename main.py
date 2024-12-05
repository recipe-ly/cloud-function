from openai import OpenAI 
import base64
import json
import os



def main(context):

    client = OpenAI()


    openai.api_key = os.environ['OPENAI_API_KEY']

    if not context.req.body:
        return context.res.json({"error": "No image provided"}, status_code=400)

    try:
        image_data = context.req.body.decode()

       response=client.chat.completions.create(
        model="gpt-4o-mini", messages=[
        {
        'role': 'system',
        'content': "Analyze this image and get recipes based on it",
      },
      {
        'role': 'user',
        'content': [
          {
            'type': 'image_url',
            'image_url': {
              'url':
                  f'data:image/jpeg;base64,{image_data}',
              'detail': 'low'
            }
          }
        ],
      }]
        )

        suggestions = response.get('choices', [{}])[0].get('text', 'No suggestions available')

        return context.res.json({"recipes": suggestions})
    except Exception as e:
        return context.res.json({"error": str(e)}, status_code=500)

