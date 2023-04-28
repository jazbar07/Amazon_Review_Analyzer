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


@app.route('/')
def main():
    with open(local_csv_file_path, 'r',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        datas = [row for row in reader if row and len(row) >= 3]

    # Pass the filtered data to the template for display
    return render_template('index.html', datas=datas, len=len(datas), x=1)

@app.route('/search')
def search():
    selected_option = request.args.get('selected')
    search_query = request.args.get('query')

    with open(local_csv_file_path, 'r',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        datas = [row for row in reader if row and len(row) >= 3]

        for row in datas:
            if selected_option == 'All Products':
                data = datas
                break
            elif selected_option == 'Product Name':
                data = {}
                for rowbyrow in row[rowbyrow][2]:
                    check_input = rowbyrow.split('<')
                    if check_input.startswith(search_query):
                        data.append(rowbyrow[0])
                    else:
                        continue 
            elif selected_option == 'Rating':
                data = {}
                for rowbyrow in row[rowbyrow][8]:
                    check_input = rowbyrow.split('out')
                    if check_input.startswith(search_query):
                        data.append(rowbyrow[0])
                    else:
                        continue
            elif selected_option == 'Description':
                data = {}
                for rowbyrow in row[rowbyrow][11]:
                    if search_query in rowbyrow:
                        data.append(rowbyrow)
                    else:
                        continue
            elif selected_option == 'Category':
                data = {}
                for rowbyrow in row[rowbyrow][9]:
                   check_input = rowbyrow.split('>')
                   if check_input.startswith(search_query):
                        data.append(rowbyrow[0])
                   else:
                       continue
            else:
                break
    return render_template('search_results.html', datas=data, len=len(data), x=0)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True) 