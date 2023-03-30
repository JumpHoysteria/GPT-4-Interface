import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = "To Be Inserted"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["question"]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
            {"role": "user", "content": prompt}
            ],
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)