import os
from together import Together
from dotenv import load_dotenv
from flask import Flask, request, render_template

app = Flask(__name__)
load_dotenv()
client = Together(api_key=os.getenv('TOGETHER_API_KEY'))


# Initialize the stream variable
stream = None

@app.route('/', methods=['GET', 'POST'])
def index():
    #global stream
    stream = ''
    output = ''
    if request.method == 'POST':
        prompt = 'An html landing page with less than 300 words about ' + request.form['prompt'] + ' as a properly formated HTML file with nice CSS formating. Do not provide a summary of what you did just raw HTML and CSS.'
        stream = client.chat.completions.create(
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

        with open("templates/generated.html", "w") as file:
            file.write(output)

        return render_template('index.html', prompt=prompt, stream=output)
    return render_template('index.html', stream=stream)


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
    app.run(debug=True)