import psycopg2
from psycopg2 import Error,sql

def connect():
    connection = psycopg2.connect(
    user="postgres",
<<<<<<< HEAD
    password="qwerty",
    host = "127.0.0.1",
    port = "5432",
    database="daffaprojeks")
=======
    password="acil123",
    host = "localhost",
    port = "5432",
    database="coffe")
>>>>>>> 4617cd8da548801ebeacb09e9cef41e261588654
    cursor = connection.cursor()
    return cursor