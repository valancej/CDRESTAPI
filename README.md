# CDRESTAPI

- Developed using Python, Flask, MySQL, and sqlalchemy
- Ensure MySQL, flask, and Flask-SQLAlchemy are properly installed
- Create database, create two tables: doctors and reviews
- Doctors table will consist of an id INT NOT NULL PRIMARY KEY, and a name VARCHAR NOT NULL
- Reviews table will consist of an id INT NOT NULL PRIMARY KEY, a doctorId INT NOT NULL, and a description TEXT NOT NULL.
- Configure doctorReview_db.conf to match values setup in your database.
- Start hitting endpoints

Tested using Postman and CURL

Example:

```
curl -XDELETE -H ‘Content-Type: application/json’  http://localhost:3000/doctors/1
```
