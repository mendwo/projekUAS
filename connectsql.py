import psycopg2
from psycopg2 import Error,sql

def connect():
    connection = psycopg2.connect(
    user="postgres",
    password="123",
    host = "127.0.0.1",
    port = "5432",
    database="Projek 3")
    cursor = connection.cursor()
    return cursor