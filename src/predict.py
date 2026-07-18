@app.get("/predict")
def predict():

    df = pd.read_csv("data/creditcard.csv")

    sample = df.drop("Class", axis=1).iloc[[0]]

    prediction = int(model.predict(sample)[0])

    save_prediction(
        prediction=prediction,
        model_version="v1"
    )

    return {
        "prediction": prediction
    }