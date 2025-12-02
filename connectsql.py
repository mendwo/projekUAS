import psycopg2
from psycopg2 import Error,sql

def connect():
    connection = psycopg2.connect(
    user="postgres",
    password="acil123",
    host = "localhost",
    port = "5432",
    database="tembakau")
    cursor = connection.cursor()
    return cursor