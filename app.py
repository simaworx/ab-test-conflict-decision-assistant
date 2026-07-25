import os
from typing import Any

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from decision_engine import (
    RESULTS,
    follow_branch,
    get_question,
    get_result,
    is_result,
)


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-change-before-deployment",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    session.clear()
    session["current_node"] = "significance"
    session["path"] = []

    return redirect(
        url_for("question", node_id="significance")
    )


@app.route("/question/<node_id>", methods=["GET", "POST"])
def question(node_id: str):
    session["current_node"] = node_id
    question_node = get_question(node_id)

    if request.method == "POST":
        selected_answer = request.form.get("answer")

        if not selected_answer:
            return render_template(
                "question.html",
                node_id=node_id,
                question=question_node,
                path=session.get("path", []),
                error="Please select an answer.",
            )

        try:
            next_node = follow_branch(
                node_id=node_id,
                answer=selected_answer,
            )
        except ValueError as error:
            return render_template(
                "question.html",
                node_id=node_id,
                question=question_node,
                path=session.get("path", []),
                error=str(error),
            )

        selected_label = next(
            option.label
            for option in question_node.options
            if option.value == selected_answer
        )

        path: list[dict[str, Any]] = session.get("path", [])

        path.append(
            {
                "node_id": node_id,
                "question": question_node.question,
                "answer": selected_label,
            }
        )

        session["path"] = path
        session["current_node"] = next_node

        if is_result(next_node):
            return redirect(
                url_for("result", result_id=next_node)
            )

        return redirect(
            url_for("question", node_id=next_node)
        )

    return render_template(
        "question.html",
        node_id=node_id,
        question=question_node,
        path=session.get("path", []),
    )


@app.route("/result/<result_id>")
def result(result_id: str):
    if result_id not in RESULTS:
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        result=get_result(result_id),
        path=session.get("path", []),
    )


@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("start"))


if __name__ == "__main__":
    app.run(debug=True)