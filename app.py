from flask import Flask, render_template, request, session, redirect, url_for
import requests
import random
import html
import time

app = Flask(__name__)
app.secret_key = "testkey"

genres = {
    "general": "9",
    "movies": "11",
    "music": "12",
    "video games": "15",
    "anime/manga": "31"
    }

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/genre.html", methods=["GET", "POST"])
def trivia_genre():
    session["count"] = request.form["quantity"]
    session["genre"] = genres[request.form["selected_genre"]]
    response = requests.get(
        "https://opentdb.com/api.php?amount="
        + str(session["count"])
        + "&category="
        + session["genre"]
    ).json()
    count = f"Number of questions: {session["count"]}"
    category = f"Category: {request.form["selected_genre"].capitalize()}"
    session["current"] = 0
    session["questions"] = response["results"]
    return render_template("genre.html", count=count, category=category)

@app.route("/trivia.html", methods=["GET", "POST"])
    
def question():

    if session["current"] >= len(session["questions"]):
        return render_template("finalscore.html", score=session["score"])
    
    current = session["current"]
    result = session["questions"][current]
    trivia_question = html.unescape(result["question"])
    session["correct"] = result["correct_answer"]

    if result["type"] == "multiple":
        answers = [
            html.unescape(result["correct_answer"]),
            html.unescape(result["incorrect_answers"][0]),
            html.unescape(result["incorrect_answers"][1]),
            html.unescape(result["incorrect_answers"][2]),
        ]
        random.shuffle(answers)
    elif result["type"] == "boolean":
        answers = [
            "True",
            "False"
        ]

    return render_template(
        "trivia.html",
        question_number=current + 1,
        answers=answers,
        trivia_question=trivia_question,
        total=len(session["questions"])
        )

@app.route("/answer.html", methods=["GET", "POST"])
def answer():
    selected = request.form["answer"]
    correct = session["correct"]
    session["current"] += 1

    if selected == correct:
        session["score"] += 1
        score = f"Score: {session["score"]}"
        return render_template("correct.html", score=score)
    else:
        correct=f"Correct Answer: {html.unescape(session["correct"])}"
        score = f"Score: {session["score"]}"
        return render_template(
            "incorrect.html",
            score=score,
            correct=correct)


@app.route("/restart", methods=["POST"])
def restart():
    session.clear()
    session["score"] = 0
    return redirect(url_for("index"))
