from sklearn.feature_extraction.text import CountVectorizer
import joblib
import os

model = joblib.load(os.path.abspath("gender_detect.pkl"))
vectorizer = CountVectorizer()


def predict_gender(name):
    vocabulary = joblib.load(os.path.abspath("vocabulary.pkl"))
    vectorizer.vocabulary_ = vocabulary

    name_vectorized = vectorizer.transform([name])
    predicted_gender = model.predict(name_vectorized)[0]
    return predicted_gender

