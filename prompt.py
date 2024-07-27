import os

from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, render_template, stream_with_context, Response
from supabase import create_client, Client
import groq
from groq import Groq
# from supabase_auth import SyncGoTrueClient


app = Flask(__name__)
load_dotenv()

# Initialize Groq
groq_api_key = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=groq_api_key)

# Initialize Supabase
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


def remove_markdown(input):
    output = input.split("```")
    output = output[1]
    return output[output.find('<!DOCTYPE html>'):]


@app.route('/', methods=['GET', 'POST'])
def index():
    stream = ''
    output = ''
    if request.method == 'POST':
        prompt = 'Generate a properly formatted html page about ' + request.form['prompt'] + ' with nice CSS formating, and a related, animated SVG. Use related, uncopyrighted images from the internet. The output should be an HTML file with the CSS included in the HTML. Always put this snippet inside the <head> tag <link rel=\"shortcut icon\" href=\"{{ url_for(\'static\', filename=\'favicon.svg\') }}\">'    
        
        try:
            stream = groq_client.chat.completions.create(
            messages=[{            
                    "role": "user",
                    "content": prompt,
                }],
                model="llama-3.1-8b-instant",
            )
            output = stream.choices[0].message.content
            output = remove_markdown(output)

            # Save to generated.html for testing.
            with open("templates/generated.html", "w") as file:
                file.write(output)
            
            # Sign in and Save to supabase.
            # email: str = os.getenv("SUPA_GENESIS_TEST_EMAIL")
            # password: str = os.getenv("SUPA_GENESIS_TEST_PASS")
            # user = supabase.auth.sign_in_with_password({ "email": email, "password": password })
            data = supabase.table("prompt_response_page").insert({
                "user_prompt": prompt,
                "ai_system_response": output
            }).execute()

            # Assert we pulled real data.
            assert len(data.data) > 0

            return render_template('index.html', prompt=prompt, stream=output)
        except groq.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except groq.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except groq.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
    return render_template('index.html', stream=stream)



# @app.route('/groq', methods=['GET', 'POST'])
# def groq_stream():
#     global streaming_response
#     api_key = os.getenv('GROK_API_KEY')
    
#     if request.method == 'POST':
#         query = 'A full html landing page complete with text and images about ' + request.form['prompt'] + ' as a properly formated HTML file with nice CSS formating. Do not provide a summary of what you did just raw HTML and CSS combined. Remove markdown decorators i.e. ```.'
        
#         streaming_response = request.post(
#             "https://api.crew.ai/v1/groq",
#             headers={"Authorization": f"Bearer {api_key}"},
#             json={"query": query},
#             stream=True
#         )

# def generate_response():
#     for chunk in streaming_response.iter_content(chunk_size=1024):
#         yield chunk

#     return Response(stream_with_context(generate_response()), mimetype='application/json')

# @app.route('/stream', methods=['GET'])
# def stream():
#     global stream
#     if stream:
#         for chunk in stream.json():
#             yield chunk['choices'][0]['delta']['content'] + '\n'
#     else:
#         yield ''


@app.route('/generated', methods=['GET', 'POST'])
def generated():    
    return render_template('generated.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)