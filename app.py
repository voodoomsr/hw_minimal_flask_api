from flask import Flask, jsonify, Response, json
from flask import request
import settings


books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 986546546
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 978654654
    }
]


print(__name__)


@app.route('/books')
def get_books():
    return jsonify({'books': books})


def validate_book_object(book_object):
    valid_properties = ['name', 'price', 'isbn'] 
    return len(valid_properties) == len(book_object.keys()) and set(valid_properties) == set(book_object.keys())


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validate_book_object(request_data)):
        books.insert(0, request_data)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['isbn'])
        return response
    else:
        error_message = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data doesnt conform with the contract'
        }
        return Response(json.dumps(error_message), 400, mimetype='application/json')

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    

    return Response('', 200) 


def _get_book_by_isbn(isbn):
    return [ book for book in books if book['isbn'] == isbn][0]
        

@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book(isbn):
    request_data = request.get_json()
    book = _get_book_by_isbn(isbn)
    for k in request_data.keys():
        book[k] = request_data[k]
    response = Response('', status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    books.pop(_get_book_by_isbn(isbn))
    return Response('', 200)

if __name__ == '__main__':
    app.run(port=5000)