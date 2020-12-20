# py-crud-example
User CRUD operations written in Python - With MariaDB & FastAPI.

## Used

  * [FastAPI](https://github.com/tiangolo/fastapi)
  * [Tortoise-ORM](https://github.com/tortoise/tortoise-orm/)
  * [Pydantic](https://github.com/samuelcolvin/pydantic/)
  * [PyJWT](https://github.com/jpadilla/pyjwt)
  * [bcrypt](https://github.com/pyca/bcrypt/)

## TODO

  - [ ] Test **API Endpoints**
  - [ ] Test **Database**
  - [ ] Add **docstrings** in [Sphinx](https://www.sphinx-doc.org) format
  - [ ] Lint
  - [ ] Optimize Docker build

## API Endpoints

### `/register` `POST`

```sh
curl -X POST localhost:8000/register \
-H "Content-Type: application/json" \
-d '{"first_name": "joHn ", "last_name": " dOE", "email": "john.doe@mail.me", "username": "asuperuser", "password": "Sup3rS@f3P@55w0rd"}'
```

### `/user/<user_id>` `GET | DELETE`

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
-d '{"username": "asuperuser", "current_password": "password", "new_password": "Password", "new_password_check": "Ultr@Sup3rS@f3P@55w0rd"}'
```
### `/login` `POST`

```sh
curl -X POST localhost:8000/login \
-H "Content-Type: application/json" \
-d '{"username": "asuperuser", "password": "Ultr@Sup3rS@f3P@55w0rd"}'
```

### `/logout` `GET`

```sh
curl -X GET localhost:8000/logout
```
