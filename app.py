from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction_text = ""
    result_class = ""

    glucose = ""
    insulin = ""
    bmi = ""
    age = ""

    if request.method == "POST":
        try:
            glucose = float(request.form["glucose"])
            insulin = float(request.form["insulin"])
            bmi = float(request.form["bmi"])
            age = float(request.form["age"])

            input_data = pd.DataFrame(
                [[glucose, insulin, bmi, age]],
                columns=["Glucose", "Insulin", "BMI", "Age"]
            )

            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)

            if prediction[0] == 1:
                prediction_text = "The person is likely to have Diabetes."
                result_class = "danger"
            else:
                prediction_text = "The person is not likely to have Diabetes."
                result_class = "success"

        except Exception as e:
            prediction_text = "Unable to process the input. Please check the values and try again."
            result_class = "danger"

    return render_template(
        "index.html",
        prediction_text=prediction_text,
        result_class=result_class,
        glucose=glucose,
        insulin=insulin,
        bmi=bmi,
        age=age
    )


if __name__ == "__main__":
    app.run(debug=True)