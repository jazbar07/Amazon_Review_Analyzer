from flask import Flask, render_template
from google.cloud import storage
import csv

app = Flask(__name__)

bucket_name = 'atozreviews'
csv_file_name = 'amazon_co-ecommerce_sample.csv'
local_csv_file_path = './csv_file.csv'

client = storage.Client()

bucket = client.get_bucket(bucket_name)
blob = bucket.blob(csv_file_name)

with open(local_csv_file_path, 'wb') as file_obj:
    blob.download_to_file(file_obj)


@app.route('/')
def main():
    with open(local_csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        datas = [row for row in reader]

    # Filter the rows to include only those with a 5.0 rating in the 9th column
    # filtered_data = [row for row in data if row[8] = '5.0 out of 5 stars']

    # Pass the filtered data to the template for display
    return render_template('index.html', datas=datas)

if __name__ == '__main__':
    app.run()