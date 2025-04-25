import pandas as pd
import json


df = pd.read_csv('BooksDataset.csv')
df.to_json('books.json', orient='records')


with open('books.json', 'r') as file:
    books = json.load(file)

for i in range(100):
    book = books[i]
    print(book)
    break
