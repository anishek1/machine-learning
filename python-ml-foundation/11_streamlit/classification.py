import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


@ st.cache_data
def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["species"] = iris.target
    return df, iris


df, iris = load_data()

st.title("Iris Classifier — Streamlit")
st.write("Small demo app: train a RandomForest on the Iris dataset and make predictions.")

if st.checkbox("Show raw data"):
    st.dataframe(df)

# Sidebar: hyperparameters and test size
st.sidebar.header("Model hyperparameters")
n_estimators = st.sidebar.slider("n_estimators", 10, 500, 100)
max_depth = st.sidebar.slider("max_depth (None=0)", 0, 50, 5)
test_size_pct = st.sidebar.slider("Test set size (%)", 10, 50, 30)
random_state = st.sidebar.number_input("random_state", value=42, step=1)

X = df.iloc[:, :-1]
y = df["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=(test_size_pct / 100.0), random_state=int(random_state), stratify=y
)

model = RandomForestClassifier(
    n_estimators=int(n_estimators), max_depth=(None if int(max_depth) == 0 else int(max_depth)), random_state=int(random_state)
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

st.sidebar.subheader("Evaluation")
st.sidebar.write(f"Test accuracy: {acc:.3f}")

st.subheader("Make a prediction")
defaults = X.mean()
col1, col2 = st.columns(2)
with col1:
    sepal_length = st.number_input(
        "sepal length (cm)", float(X["sepal length (cm)"].min()), float(X["sepal length (cm)"].max()), float(defaults["sepal length (cm)"])
    )
    sepal_width = st.number_input(
        "sepal width (cm)", float(X["sepal width (cm)"].min()), float(X["sepal width (cm)"].max()), float(defaults["sepal width (cm)"])
    )
with col2:
    petal_length = st.number_input(
        "petal length (cm)", float(X["petal length (cm)"].min()), float(X["petal length (cm)"].max()), float(defaults["petal length (cm)"])
    )
    petal_width = st.number_input(
        "petal width (cm)", float(X["petal width (cm)"].min()), float(X["petal width (cm)"].max()), float(defaults["petal width (cm)"])
    )

if st.button("Predict"):
    sample = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    pred = model.predict(sample)[0]
    proba = model.predict_proba(sample).max()
    st.success(f"Predicted species: {iris.target_names[pred]} (probability {proba:.3f})")

st.subheader("Feature importances")
feat_imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
st.bar_chart(feat_imp)

st.write("---")
st.write("To run: in this folder run `streamlit run classification.py`")

