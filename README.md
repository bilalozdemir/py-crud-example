# py-crud-example
User CRUD Operations written in Python - With Redis &amp; MySQL &amp; JWT


## API Endpoints

### `/register` `POST`

```sh
curl -X POST localhost:8000/register \
-H "Content-Type: application/json" \
-d '{"first_name": "a", "last_name": "b", "email": "a@b.c", "username": "abcde", "password": "P@ssword"}'
```

### `/user/<user_id>` `GET/DELETE`

```sh
curl -X [GET|DELETE] localhost:8000/user/{user_id}
```

### `/users` `GET`

```sh
curl -X GET localhost:8000/users
```

### `/change-password` `PUT`

```sh
curl -X PUT localhost:8000/change-password \
-H "Content-Type: application/json" \
-d '{"username": "abcde", "current_password": "password", "new_password": "Password", "new_password_check": "Password"}'
```
### `/login` `POST`

```sh
curl -X POST localhost:8000/login \
-H "Content-Type: application/json" \
-d '{"username": "abcde", "password": "Password"}'
```

### `/logout` `GET`

```sh
curl -X GET localhost:8000/logout
```
