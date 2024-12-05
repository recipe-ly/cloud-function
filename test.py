from appwrite.client import Client
from appwrite.services.functions import Functions

IMAGE_PATH = "path/to/your/image.jpg"


client = Client()


client.set_endpoint('https://cloud.appwrite.io/v1')  
client.set_project('6744a0f700127fd3f71b')  
client.set_key('standard_e1c779b6c0200f820f42b5cf86faad2a0a47a939b8368612e28ad7e1c104b3e9333e29c72d9dc54966ebe7f10218d083feb5f862f8783e8f9a567f71848da0a61268cdd34c1e984f16792cf25815c92d44d0f8853be574048c8c6dd069fe680b59f121530bcf949c61637a549b6e0acab0ba809a5b8dfa389aa650f506c180df')  

functions = Functions(client)

try:
    function_id = '6751bcd50020deca844e'  
    response = functions.create_execution(function_id, data='{"key":"value"}')  
    print(f'Function Execution Response: {response}')
except Exception as e:
    print(f'Error calling function: {e}')
