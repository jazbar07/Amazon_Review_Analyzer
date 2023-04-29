from flask import Flask, render_template, request
from google.cloud import storage
import csv


app = Flask(__name__)

bucket_name = 'amazon_electric_reviews'
csv_file_name = 'amazon_co-ecommerce_sample.csv'
local_csv_file_path = './csv_file.csv'

client = storage.Client()

bucket = client.get_bucket(bucket_name)
blob = bucket.blob(csv_file_name)

csv_string = blob.download_as_string().decode("utf-8")

# Split the CSV file string into lines
lines = csv_string.split("\n")

# Remove the first line (header)
lines = lines[1:]

# Join the lines back into a string
csv_string = "\n".join(lines)


# Upload the modified CSV file back to the bucket
blob.upload_from_string(csv_string.encode("utf-8"))

with open(local_csv_file_path, 'wb') as file_obj:
    blob.download_to_file(file_obj)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        query = request.form['query']
        option = request.form['option']

        with open(local_csv_file_path, 'r', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            data = [row for row in reader if row and len(row) >= 3]

        filtered_data = []
        for i in range(len(data)):
            if option == '' or data[i][9] == option:
                if query == '' or query.lower() in data[i][2].lower():
                    filtered_data.append(data[i])

        return render_template('index.html', datas=filtered_data, len=len(filtered_data), x=1)

    else:
        with open(local_csv_file_path, 'r', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            datas = [row for row in reader if row and len(row) >= 3]

        # Pass the original data to the template for display
        return render_template('index.html', datas=datas, len=len(datas), x=1)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True) 