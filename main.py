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
    if not 'cursor' in locals() or globals(): # may not work/needed
        cursor = connect()
    cursor.execute(f"SELECT * FROM {entity}")

    mytable = from_db_cursor(cursor)
    print(mytable)

def regis():
    while True:
        try:
            username = input("Masukkan username dengan jumlah 4-16 karakter (kosongkan untuk keluar) ")
            if username == "":
                clear()
                break
            passw = passbintang("Masukkan password dengan jumlah 4-16 karakter ")
            if len(username) <= 16 and len(username) >= 4 and  len(passw) <= 16 and len(passw) >= 4 :
                nama= input("Masukkan nama lengkap anda ")
                telp= input("Masukkan nomer telepon anda ")
                email= input ("Masukkan email anda ")
                cursor = connect()
                cursor.execute("INSERT INTO pengguna(is_admin,nama_lengkap,username,passwords,no_telpon,email,is_delete) VALUES (False,%s, %s,%s,%s,%s,False)", (nama,username, passw,telp,email))
                cursor.connection.commit()
                clear()
                print("Berhasil registrasi")
                getch()
                clear()
                break
            else:
                print("jumlah karakter username atau password tidak memenuhi syarat...")
                getch()
        except (Exception,Error) as error:
            print(error)

def login():
    connection = psycopg2.connect(
    user="postgres",
    password="123",
    host = "127.0.0.1",
    port = "5432",
    database="Projek")
    cursor = connection.cursor()
    username= input("masukkan username ")
    passw= passbintang("masukkan password ")
    try :
        cursor.execute("SELECT * FROM pengguna")
        records = cursor.fetchall()
    except psycopg2.Error as Error:
        print("Salah")
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

def ChangeAkunAll():
    cursor = connect()
    showtable("pengguna")
    id_= inputint("Masukkan id yg ingin diubah ")
    cursor.execute(f"Select * from pengguna where id_pengguna = {id_}")
    records = cursor.fetchone()
    # print(records)
    query = "Update pengguna Set "
    nama = input("Masukkan nama baru, kosongkan jika sama ")
    count = 0
    if not nama == "":
        query = query + f" nama_lengkap = '{nama}'"
        count += 1
    username = input ("Masukkan username baru, kosongkan jika sama ")
    if not username == "":
        if not count == 0:
            query = query + ","
        query = query + f" username = '{username}'"
        count += 1
    password = input("Masukkan password baru, kosongkan jika sama ")
    if not password == "":
        if not count == 0:
            query = query + ","
        query = query + f" passwords = '{password}'"
        count += 1
    no = input("Masukkan nomer telepon baru, kosongkan jika sama ")
    if not no == "":
        if not count == 0:
            query = query + ","
        count += 1
        query = query + f" no_telpon = '{no}'"
    email = input("Masukkan email baru, kosongkan jika sama ")
    if not email == "":
        if not count == 0:
            query = query + ","
        count += 1
        query = query + f" email = '{email}'"
    query = query + f" WHERE id_pengguna = {records[0]}"
    if count != 0:
        cursor.execute(query)
        cursor.connection.commit()
        clear()
        print(f"{count} data berhasil diubah...")
        getch()
    else:
        clear()
        print("Data tidak jadi diubah")
        getch()

def ChangeAkunSelf(id_):
    cursor = connect()
    cursor.execute(f"Select * from pengguna where id_pengguna = {id_}")
    records = cursor.fetchone()
    # print(records)
    query = "Update pengguna Set "
    nama = input("Masukkan nama baru, kosongkan jika sama ")
    count = 0
    if not nama == "":
        query = query + f" nama_lengkap = '{nama}'"
        count += 1
    username = input ("Masukkan username baru, kosongkan jika sama ")
    if not username == "":
        if not count == 0:
            query = query + ","
        query = query + f" username = '{username}'"
        count += 1
    password = input("Masukkan password baru, kosongkan jika sama ")
    if not password == "":
        if not count == 0:
            query = query + ","
        query = query + f" passwords = '{password}'"
        count += 1
    no = input("Masukkan nomer telepon baru, kosongkan jika sama ")
    if not no == "":
        if not count == 0:
            query = query + ","
        count += 1
        query = query + f" no_telpon = '{no}'"
    email = input("Masukkan email baru, kosongkan jika sama ")
    if not email == "":
        if not count == 0:
            query = query + ","
        count += 1
        query = query + f" email = '{email}'"
    query = query + f" WHERE id_pengguna = {records[0]}"
    if count != 0:
        cursor.execute(query)
        cursor.connection.commit()
        clear()
        print(f"{count} data berhasil diubah...")
        getch()
    else:
        clear()
        print("Data tidak jadi diubah")
        getch()

################################################################

login_status= 0
clear()

while True:
    print("""Menu :
1. Registrasi
2. Login
3. Show Tabel
0. Keluar""")
    pilihanmenu= inputint("Masukkan menu yang ingin dipilih: ")
    if pilihanmenu == 1:
        clear()
        regis()
    elif pilihanmenu == 2:  
        clear()
        data_user = login()
        print(data_user)
        getch()
        if not data_user is None:
            login_status = 1
        clear()
        break
    elif pilihanmenu == 3 :
        clear()
        temp= input("Masukkan tabel yang ingin ditampilkan ")
        showtable(temp)
        getch()
        clear()
    elif pilihanmenu == 0:
        exit()

try:
    if login_status == 1 and data_user[1] is False: # Menu penjual
        clear()
        MenuUtama()
        temp = inputint("Masukkan menu yang diinginkan ")
        if temp == 1:
            clear()
            ShowAkun()
            temp = input("Tekan enter untuk keluar atau masukkan sembarang huruf untuk mengedit ")
            if temp != "":
                ChangeAkunSelf(data_user[0])
        elif temp == 2:
            pass
        elif temp == 3 :
            pass
        elif temp == 4 :
            exit

    elif login_status == 1 and data_user[1] is True: # Menu admin
        clear()
        MenuUtamaAdmin()
        temp =inputint("Masukkan angka ")
        if temp == 1:
            print("1. Data user \n" 
            "2. Data admin")
            temp = inputint("Masukkan angka ")
            if temp == 1:
                ShowAkunAll()
                temp= input("Enter jika ingin keluar,isi dengan angka apa saja jika ingin mengedit ")
                clear()
                if temp == "":
                    pass
                else :
                    ChangeAkunAll()
            elif temp == 2:
                clear()
                ShowAkun()
                temp = input("Tekan enter untuk keluar atau masukkan sembarang huruf untuk mengedit ")
                if temp != "":
                    ChangeAkunSelf(data_user[0])
    
except :
    # print('Error, Silahkan kontak admin(Error 001)')
    print(Error)
    print("Error 123")


# if connection:
#     cursor.close()
#     connection.close()



# showtable("pengguna")
# ChangeAkunAll()