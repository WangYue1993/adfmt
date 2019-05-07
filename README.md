# adfmt
adfmt is used for generating annotations automated.

It's designed for apidoc.

usage:
```python
>>> import adfmt
>>>
>>> # request an api
>>> r = adfmt.DocUnit.get('/books/', json=dict(limit=3)) 
>>> r.output
'''
class ApiDocBooks(object):
    @staticmethod
    def books_get():
        """
        @api {get} /books/ get books data.
        @apiGroup Book
        @apiParam {Number} limit the numbers of books.
        @apiSuccess {String} name name of book.
        @apiSuccess {String} id book primary-key.
        """
'''
```
