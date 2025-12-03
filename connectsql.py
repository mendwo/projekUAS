import psycopg2
from psycopg2 import Error,sql

def connect():
    connection = psycopg2.connect(
    user="postgres",
    password="qwerty",
    host = "127.0.0.1",
    port = "5432",
    database="daffaprojeks")
    cursor = connection.cursor()
    return cursor