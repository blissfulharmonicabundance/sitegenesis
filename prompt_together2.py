import os

from together import Together
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, render_template, stream_with_context, Response
from supabase import create_client, Client
# from supabase_auth import SyncGoTrueClient


app = Flask(__name__)
load_dotenv()

# Initialize Together AI
together_ai = Together(api_key=os.getenv('TOGETHER_API_KEY'))


# Initialize Supabase
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


# @app.route('/sign_up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             user = supabase.auth.sign_up({ "email": email, "password": password })
#             return redirect(url_for('sign_in'))
#         except supabase.auth.AuthApiError:
#             return render_template('sign_up.html')
#     return render_template('sign_up.html')

# @app.route('/sign_in', methods=['GET', 'POST'])
# def sign_in():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         try:
#             user = supabase.auth.sign_in_with_password({ "email": email, "password": password })
#             return redirect(url_for('index'))
#         except:
#             return redirect(url_for('sign_up'))     
#     return render_template('sign_in.html')

# @app.route('/sign_out')
# def sign_out():
#     try:
#         res = supabase.auth.sign_out()
#     except:
#         pass
#     finally:    
#         return redirect(url_for('index'))

# Initialize the stream variable
stream = None

@app.route('/', methods=['GET', 'POST'])
def index():
    #global stream
    stream = ''
    output = ''
    if request.method == 'POST':
        prompt = 'An html landing page with less than 300 words about ' + request.form['prompt'] + ' as a properly formated HTML file with nice CSS formating. Do not provide a summary of what you did just raw HTML and CSS. Remove markdown decorators i.e. ```.'
        stream = together_ai.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>"],
            stream=True
        )
        output = ''
        for chunk in stream:
            output += chunk.choices[0].delta.content or ""

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
    return render_template('index.html', stream=stream)



@app.route('/groq', methods=['GET', 'POST'])
def groq_stream():
    global streaming_response
    api_key = os.getenv('GROK_API_KEY')
    
    if request.method == 'POST':
        query = 'A full html landing page complete with text and images about ' + request.form['prompt'] + ' as a properly formated HTML file with nice CSS formating. Do not provide a summary of what you did just raw HTML and CSS combined. Remove markdown decorators i.e. ```.'
        
        streaming_response = request.post(
            "https://api.crew.ai/v1/groq",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"query": query},
            stream=True
        )

def generate_response():
    for chunk in streaming_response.iter_content(chunk_size=1024):
        yield chunk

    return Response(stream_with_context(generate_response()), mimetype='application/json')

@app.route('/stream', methods=['GET'])
def stream():
    global stream
    if stream:
        for chunk in stream.json():
            yield chunk['choices'][0]['delta']['content'] + '\n'
    else:
        yield ''


@app.route('/generated', methods=['GET', 'POST'])
def generated():    
    return render_template('generated.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)