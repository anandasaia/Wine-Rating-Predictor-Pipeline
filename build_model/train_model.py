
import pandas as pd
import numpy as np
import click
import pickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from pathlib import Path


@click.command()
@click.option('--train-csv')
@click.option('--out-dir')
def build_model(train_csv, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    #reading csv file
    dp=pd.read_csv(train_csv)
    X = dp['description']
    y = dp['points_simplified'] 
    # Vectorizing model
    vectorizer = TfidfVectorizer()
    vectorizer.fit(X)
    X = vectorizer.transform(X)      
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=101)
    rfc = RandomForestClassifier()
    rfc.fit(X_train, y_train)
    predictions = rfc.predict(X_test)
    print(classification_report(y_test, predictions))
    report=classification_report(y_test, predictions,output_dict=True)
    evaluate = pd.DataFrame(report).transpose()
    evaluate.to_csv(out_dir/'report.csv')
    # Calculate the absolute errors
    errors = abs(predictions - y_test)
	# Calculate mean absolute percentage error (MAPE)
    mape = 100 * (errors / y_test)
	# Calculate and display accuracy
    accuracy = 100 - np.mean(mape)
    print('Accuracy:', round(accuracy, 2), '%')
#    evaluate = pd.DataFrame(report).transpose()
#    evaluate.to_csv(out_dir/'report.csv')


if __name__ == "__main__":
  # data_vector=pd.read_csv("../data_root/created_csv/transformed.csv")
   #vectorizing 
   train_data=build_model()
    
