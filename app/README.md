Simplified API service that allows the creation and deletion of resources that live in a MongoDB (inmemory):

## Endpoints
### InsertUser

`POST /api/v1.0/user`

#### Example HTTP Request
```
POST /api/v1.0/user HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 366

{
    "name": "A Martinez",
    "description": "Adolph Larrue Martinez III.",
    "mbti": "ISFJ",
    "enneagram": "9w3",
    "variant": "sp/so",
    "tritype": 725,
    "socionics": "SEE",
    "sloan": "RCOEN",
    "psyche": "FEVL",
    "temperaments": "Phlegmatic [Dominant]",
    "image": "https://cdn.pixabay.com/photo/2017/02/23/13/05/avatar-2092113_1280.png"
}
```

#### Example Response
```json
{
    "id": "65bc7bc191563e032e184fc0"
}
```

### GetUser

`GET /api/v1.0/user`

#### Example HTTP Request
```
GET /api/v1.0/user/65bc7bc191563e032e184fc0 HTTP/1.1
Host: localhost:8000
```

#### Example Response
```json
{
    "_id": "65bc7bc191563e032e184fc0",
    "description": "Adolph Larrue Martinez III.",
    "enneagram": "9w3",
    "image": "https://cdn.pixabay.com/photo/2017/02/23/13/05/avatar-2092113_1280.png",
    "mbti": "ISFJ",
    "name": "A Martinez",
    "psyche": "FEVL",
    "sloan": "RCOEN",
    "socionics": "SEE",
    "temperaments": "Phlegmatic [Dominant]",
    "tritype": 725,
    "variant": "sp/so"
}
```

### PostComment

`POST /api/v1.0/user/<user_id>/comment`

#### Example HTTP Request
```
POST /api/v1.0/user/65bc7bc191563e032e184fc0/comment HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 108

{
    "from_user_id": "65bc16d9de8ff7fcb049541b",
    "mbti": "INTP",
    "body": "A sample comment"
}
```
```
POST /api/v1.0/user/65bc7bc191563e032e184fc0/comment HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 108

{
    "from_user_id": "65bc16d9de8ff7fcb049542b",
    "mbti": "INTJ",
    "body": "Another sample comment"
}
```

#### Example Response
`HTTP 201`

### GetComments

`GET /api/v1.0/user/<user_id>/comments`

#### Example HTTP Request
```
GET /api/v1.0/user/65bc7bc191563e032e184fc0/comments HTTP/1.1
Host: localhost:8000
```

#### Example Response
```json
{
    "comments": [
        {
            "body": "A sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049541b",
            "id": "65bc7bcb91563e032e184fc1",
            "likes_count": 0,
            "mbti": "INTP"
        },
        {
            "body": "Another sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049542b",
            "id": "65bc7bd291563e032e184fc2",
            "likes_count": 0,
            "mbti": "INTJ"
        }
    ]
}
```

#### Example Response (after generating likes on comments)
```json
{
    "comments": [
        {
            "body": "A sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049541b",
            "id": "65bca4ef31f4a27f2f8b58dd",
            "likes_count": 0,
            "mbti": "INTJ"
        },
        {
            "body": "Another sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049542b",
            "id": "65bca4fc31f4a27f2f8b58de",
            "likes": [
                {
                    "from_user_id": "65bc5752b845ce653fae6d1b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d2b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d3b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d4b"
                }
            ],
            "likes_count": 4,
            "mbti": "INTP"
        },
        {
            "body": "One more sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049543b",
            "id": "65bca50a31f4a27f2f8b58df",
            "likes": [
                {
                    "from_user_id": "65bc5752b845ce653fae6d1b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d2b"
                }
            ],
            "likes_count": 2,
            "mbti": "INTJ"
        }
    ]
}
```
---
#### Example Request (sorting)
```
GET /api/v1.0/user/65bca4da31f4a27f2f8b58dc/comments?sort=best HTTP/1.1
Host: localhost:8000
```

#### Example Response
```
{
    "comments": [
        {
            "body": "Another sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049542b",
            "id": "65bca4fc31f4a27f2f8b58de",
            "likes": [
                {
                    "from_user_id": "65bc5752b845ce653fae6d1b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d2b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d3b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d4b"
                }
            ],
            "likes_count": 4,
            "mbti": "INTP"
        },
        {
            "body": "One more sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049543b",
            "id": "65bca50a31f4a27f2f8b58df",
            "likes": [
                {
                    "from_user_id": "65bc5752b845ce653fae6d1b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d2b"
                }
            ],
            "likes_count": 2,
            "mbti": "INTJ"
        },
        {
            "body": "A sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049541b",
            "id": "65bca4ef31f4a27f2f8b58dd",
            "likes_count": 0,
            "mbti": "INTJ"
        }
    ]
}
```
---
#### Example HTTP Request (with filtering)
```
GET /api/v1.0/user/65bca4da31f4a27f2f8b58dc/comments?filter=INTP HTTP/1.1
Host: localhost:8000
```

#### Example Response
```json
{
    "comments": [
        {
            "body": "Another sample comment",
            "from_user_id": "65bc16d9de8ff7fcb049542b",
            "id": "65bca4fc31f4a27f2f8b58de",
            "likes": [
                {
                    "from_user_id": "65bc5752b845ce653fae6d1b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d2b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d3b"
                },
                {
                    "from_user_id": "65bc5752b845ce653fae6d4b"
                }
            ],
            "likes_count": 4,
            "mbti": "INTP"
        }
    ]
}
```

### LikeComment

`POST /api/v1.0/user/<user_id>/comment/<comment_id>`

#### Example HTTP Request
```
POST /api/v1.0/user/65bc7bc191563e032e184fc0/comment/65bc7bcb91563e032e184fc1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 50

{
    "from_user_id": "65bc5752b845ce653fae6d3b"
}
```

#### Example Response
```json
`HTTP 201`
```

### UnlikeComment

`DELETE /api/v1.0/user/<user_id>/comment/<comment_id>`

#### Example HTTP Request
```
DELETE /api/v1.0/user/65bc7bc191563e032e184fc0/comment/65bc7bcb91563e032e184fc1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 50

{
    "from_user_id": "65bc5752b845ce653fae6d3b"
}
```

#### Example Response
```json
`HTTP 200`
```


## How to run and test the service

- Create an environment and run `pip install -r requirements.txt` to install all dependencies.
- Run with `python app.py`
- To run tests, execute `python -m unittest test.test_app -v`