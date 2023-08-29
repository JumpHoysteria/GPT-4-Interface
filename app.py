import os
from dotenv import load_dotenv
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
BROWSER_LINE_ENDING = b'<br>'

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
path = "C:\\Users\\Alex\\Documents\\GPT-4\\GPT-4-Interface/response.txt"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["question"]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                {"role": "user", "content": prompt},
                
                ],
                temperature=0.6,
            )
            response = response.choices[0].message.content
            with open(path, "w+") as file1:
                file1.write(response)

            return redirect(url_for("index"))
        except openai.error.RateLimitError:
            print("Model is overloaded")
            return redirect(url_for("index", result = f"ERROR: Model is overloaded \n {prompt}"))
            
    with open(path, "rb") as file1:
        result = file1.read()
        result = result.replace(WINDOWS_LINE_ENDING, BROWSER_LINE_ENDING)
        #result = result.decode()
    return render_template("index.html", result=result)
