import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv('final.csv')

X = data['Name']
y = data['Gender']

vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)
joblib.dump(vectorizer.vocabulary_, 'vocabulary.pkl')

X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


joblib.dump(classifier, 'gender_detect.pkl')


def predict_gender(name):
    name_vectorized = vectorizer.transform([name])
    gender = classifier.predict(name_vectorized)[0]
    return gender
print(predict_gender("Moiz"))

# Save the trained model




