import psycopg2
from psycopg2 import Error, sql
from prettytable import from_db_cursor
from macro import *

def connect():
    connection = psycopg2.connect(
    user="postgres",
    password="123",
    host = "127.0.0.1",
    port = "5432",
    database="Projek")
    cursor = connection.cursor()
    return cursor

def showtable(entity):
    cursor = connect()
    cursor.execute(f"SELECT * FROM {entity}")

    mytable = from_db_cursor(cursor)
    print(mytable)

    # records= cursor.fetchall()
    # for row in records:
    #     print(row)

def regis():
    while True:
        try:
            username = input("Masukkan username dengan jumlah 4-16 karakter ")
            passw = passbintang("Masukkan password dengan jumlah 4-16 karakter ")
            if len(username) <= 16 and len(username) >= 4 and  len(passw) <= 16 and len(passw) >= 4 :
                nama= input("Masukkan nama lengkap anda ")
                telp= input("Masukkan nomer telepon anda ")
                email= input ("Masukkan email anda ")
                cursor = connect()
                cursor.execute("INSERT INTO pengguna(is_admin,nama_lengkap,username,passwords,no_telpon,email,is_delete) VALUES (True,%s, %s,%s,%s,%s,False)", (nama,username, passw,telp,email))
                cursor.connection.commit()
                break
            else:
                print("jumlah karakter username atau password tidak memenuhi syarat")
        except (Exception,Error) as error:
            print(error)

def login():
    print("test")

    connection = psycopg2.connect(
    user="postgres",
    password="123",
    host = "127.0.0.1",
    port = "5432",
    database="Projek")
    cursor = connection.cursor()
    username= input("masukkan username ")
    passw= passbintang("masukkan password ")

    cursor.execute("SELECT * FROM pengguna")
    records = cursor.fetchall()
    index = None
    for index,row in enumerate(records):
        if username == row[3] and passw == row[4]:
            print ("berhasil")
            print (index)
            return row
    if index is None:
        print("Salah")

def MenuUtama():
    print("""
1. Data akun (melihat dan mengedit)
2. Membuat Pesanan
3. Status pesanan (melihat dan )
4. Log out / keluar
""")

def MenuUtamaAdmin():
    print("""
1. Data akun (melihat mengedit akun admin, melihat akun pengguna)
2. Katalog menu (melihat,mengedit)
4. Status pesanan (melihat,mengedit status)
5. Laporan penjualan (melihat,menambah)
6. Log out / keluar
""")

def ShowAkun():
    print("Nama: ",data_user[2])
    print("Username: ",data_user[3])
    print("Password: ",data_user[4])
    print("No. telepon :",data_user[5])
    print("Email: ",data_user[6])

def ShowAkunAll():
    cursor= connect()
    cursor.execute("SELECT * FROM pengguna")


################################################################

while True:
    print("""Menu :
1. Registrasi
2. Login
3. Show Tabel""")
    pilihanmenu= inputint("Masukkan menu yang ingin dipilih: ")
    if pilihanmenu == 1:
        clear()
        regis()
    elif pilihanmenu == 2:  
        clear()
        data_user = login()
        print(data_user)
        getch()
        clear()
        break
    elif pilihanmenu == 3 :
        clear()
        temp= input("Masukkan tabel yang ingin ditampilkan ")
        showtable(temp)
        getch()
        # clear()
    elif pilihanmenu == 0:
        exit()

try:
    if data_user[1] is False: # Menu penjual
        clear()
        MenuUtama()
        temp = inputint("Masukkan menu yang diinginkan")
        if temp == 1:
            ShowAkun()
        elif temp == 2:
            pass
        elif temp == 3 :
            pass
        elif temp == 4 :
            exit

    elif data_user[1] is True: # Menu admin
        clear()
        MenuUtamaAdmin()
        temp =inputint("Masukkan angka ")
        if temp == 1:
            print("1. Data user \n" 
            "2. Data admin")
            temp = inputint("Masukkan angka ")
            if temp == 1:
                ShowAkunAll()

    
except :
    print('Error, Silahkan kontak admin(Error 001)')