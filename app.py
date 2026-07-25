from flask import Flask, render_template, request

from decision_engine import ExperimentInputs, evaluate_experiment


app = Flask(__name__)


def parse_optional_boolean(field_name: str) -> bool | None:
    value = request.form.get(field_name)

    if value == "yes":
        return True

    if value == "no":
        return False

    return None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    try:
        conversion_drop = float(request.form["conversion_drop"])

        inputs = ExperimentInputs(
            statistically_significant=(
                request.form["statistically_significant"] == "yes"
            ),
            conversion_drop_percent=conversion_drop,
            segment_concentrated=parse_optional_boolean(
                "segment_concentrated"
            ),
            qualitative_friction=parse_optional_boolean(
                "qualitative_friction"
            ),
            issue_fixable=parse_optional_boolean("issue_fixable"),
            primary_metric_valuable=parse_optional_boolean(
                "primary_metric_valuable"
            ),
            longer_term_redesign=parse_optional_boolean(
                "longer_term_redesign"
            ),
        )

        result = evaluate_experiment(inputs)

    except (KeyError, TypeError, ValueError) as error:
        return render_template(
            "index.html",
            error=f"Please check the information entered: {error}",
        )

    return render_template(
        "result.html",
        result=result,
        inputs=inputs,
    )


if __name__ == "__main__":
    app.run(debug=True)