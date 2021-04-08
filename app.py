from flask import Flask, flash, request, render_template, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

KEY = "Qs"

debug = DebugToolbarExtension(app)

@app.route('/')
def render_start():
    return render_template("landing.html", survey=survey)

@app.route('/begin', methods=["POST"])
def start():
    session[KEY] = []
    return redirect("/question/0")

@app.route("/question/<int:i>")
def render_questions(i):
    responses = session.get(KEY)

    if responses == None:
        return redirect("/")
    if len(responses) == len(survey.questions):
        return redirect("/complete")
    if len(responses) != i:
        flash(f"Error: Invalid Question Number")
        return redirect(f"/question/{len(responses)}")

    question = survey.questions[i]
    return render_template("question.html", question=question, question_num=i)

@app.route('/answer', methods=["POST"])
def answer_questions():
    answer = request.form['answer']

    responses = session[KEY]
    responses.append(answer)
    session[KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/question/{len(responses)}")

@app.route('/complete')
def done():
    return render_template("done.html")