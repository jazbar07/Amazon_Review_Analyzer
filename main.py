from flask import Flask, render_template
from google.cloud import storage
import csv

app = Flask(__name__)

bucket_name = 'amazon_electric_reviews'
csv_file_name = 'ratings_Electronics (1).csv'
local_csv_file_path = '/Users/jazminebarnett/Documents/csv_file.csv'

client = storage.Client()



bucket = client.get_bucket(bucket_name)
blob = bucket.blob(csv_file_name)

with open(local_csv_file_path, 'wb') as file_obj:
    blob.download_to_file(file_obj)


@app.route('/')
def main():
    product_ratings = {}
    
    # start by grouping the data by productId
    with open(local_csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # catch to make sure there is enough data in each line so no IndexError
            if len(row) >= 3:
                productId, rating = row[1], float(row[2])
                if productId in product_ratings:
                    product_ratings[productId]['ratings'].append(rating)
                else:
                    product_ratings[productId] = {'ratings': [rating]}

    # calculate the average rating for each product
    for productId in product_ratings:
        ratings = product_ratings[productId]['ratings']
        product_ratings[productId]['avg_rating'] = sum(ratings) / len(ratings)

    # Sort the products by average rating and return the highest rated product
    sorted_products = sorted(product_ratings.items(), key=lambda x: x[1]['avg_rating'], reverse=True)
    highest_rated_product = sorted_products[0]



    return render_template('index.html', product_rate_list = sorted_products, highest_rated = highest_rated_product[0], average_rating = highest_rated_product[1]['avg_rating'])

if __name__ == '__main__':
    app.run()