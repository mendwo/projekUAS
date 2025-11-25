import psycopg2
from psycopg2 import Error, sql
from prettytable import from_db_cursor, PrettyTable
from macro import *
from connectsql import *

### Note : Sisa fitur sedang menunggu konfirmasi benar atau tidak. Daripada kerja dua kali

def showtable(entity):
    querydefault = f"SELECT * FROM {entity}"
    ordercount = 0
    query = querydefault
    orderlist = []
    orderlistasc = []
    # offset = 0
    # limit = f" limit 10 "
    while True:
        # print("query= ", query)
        if not 'cursor' in locals() and globals(): # may not work/needed
            cursor = connect()
        cursor.execute(f"Select count(*) from {entity}")
        jumlah = cursor.fetchone()
        cursor.execute(query)
        for x in range((jumlah[0]//5)+1):
            print("Halaman ke ",x+1)
            record = cursor.fetchmany(5)
            columns = [x[0] for x in cursor.description]
            mytable = PrettyTable(columns)
            for y in record:
                mytable.add_row(y)
            print(mytable)
            temp = input("Masukkan opsi (join, where, group, having, order,)\n(enter untuk next page,isi sembarang untuk skip) ")
            if temp != "":
                break
            else:
                pass
            clear()
        query = querydefault
        if temp == "":
            break
        elif temp == "join":
            pass
        elif temp == "where":
            pass
        elif temp == "group":
            pass
        elif temp == "having":
            pass
        elif temp == "order":
            ordercount += 1
            order= input("Masukkan order by kolom apa ")
            orderlist.append(order)
            asc = input("Enter jika asc")
            orderlistasc.append(asc)
            for x in range(ordercount):
                if x == 0 :
                    query = query + f" ORDER BY {orderlist[x]}"
                else:
                    query = query + f", {orderlist[x]}"
                if orderlistasc[x] == "":
                    query = query + " asc"
                else:
                    query = query + " desc"
        else:
            break

def Showtablewithout(entity):
    query = f"SELECT * FROM {entity}"
    # offset = 0
    # limit = f" limit 10 "
    
    # print("query= ", query)
    if not 'cursor' in locals() and globals(): # may not work/needed
        cursor = connect()
    cursor.execute(f"Select count(*) from {entity}")
    jumlah = cursor.fetchone()
    cursor.execute(query)
    for x in range((jumlah[0]//5)+1):
        print("Halaman ke ",x+1)
        record = cursor.fetchmany(5)
        columns = [x[0] for x in cursor.description]
        mytable = PrettyTable(columns)
        for y in record:
            mytable.add_row(y)
        print(mytable)
        getch()

def regis():
    while True:
        try:
            username = input("Masukkan username dengan jumlah 4-16 karakter (kosongkan untuk keluar) ")
            if username == "":
                clear()
                break
            passw = passbintang("Masukkan password dengan jumlah 4-16 karakter ")
            if len(username) <= 16 and len(username) >= 4 and  len(passw) <= 16 and len(passw) >= 4 :
                inputvalid = 0
                while inputvalid < 3 : # Data diri dan check input
                    inputvalid = 0
                    nama= input("Masukkan nama lengkap anda ")
                    if nama and all(c.isalpha() or c.isspace() for c in nama):
                        inputvalid +=1
                    telp= input("Masukkan nomer telepon anda ")
                    if telp and all(c.isdigit() or c in "+-" for c in telp):
                        inputvalid += 1
                    email= input ("Masukkan email anda ")
                    if email and "@" in email and "." in email:
                        inputvalid += 1
                    if inputvalid < 3 : 
                        print ("Masukkan data yang valid")
                        clear()
                    else:
                        break
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
    cursor = connect()
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


def ShowAkun():
    print("Nama: ",data_user[2])
    print("Username: ",data_user[3])
    print("Password: ",data_user[4])
    print("No. telepon :",data_user[5])
    print("Email: ",data_user[6])

def ShowAkunAll():
    # cursor= connect()
    # cursor.execute("SELECT * FROM pengguna")
    showtable("pengguna")

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

def TampilkanPesanan(id,mode=1):
    try:
        cursor = connect()
        # cursor.execute(f"SELECT p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman FROM pesanan p where is_delete = '0' and id_pengguna = '{id}'")
        if mode == 1:
            cursor.execute(f"SELECT p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman, j.nama_jalan || ' ' || k.nama_kecamatan || ' ' || ka.nama_kabupaten AS Alamat FROM pesanan p, jalan j, kecamatan k, kabupaten ka, alamat_pengiriman a where is_delete = '0' and id_pengguna = '{id}' and p.id_alamat_pengiriman = a.id_alamat_pengiriman and a.id_jalan = j.id_jalan and j.id_kecamatan = k.id_kecamatan and k.id_kabupaten = ka.id_kabupaten")
        else:
            cursor.execute(f"SELECT p.id_pesanan, p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman, j.nama_jalan || ' ' || k.nama_kecamatan || ' ' || ka.nama_kabupaten AS Alamat FROM pesanan p, jalan j, kecamatan k, kabupaten ka, alamat_pengiriman a where is_delete = '0' and id_pengguna = '{id}' and p.id_alamat_pengiriman = a.id_alamat_pengiriman and a.id_jalan = j.id_jalan and j.id_kecamatan = k.id_kecamatan and k.id_kabupaten = ka.id_kabupaten")
        record = cursor.fetchall()
        print("test")
        columns = [x[0] for x in cursor.description]
        mytable = PrettyTable(columns)
        for y in record:
            mytable.add_row(y)
        print(mytable)

    except (Exception,Error) as error:
        print(error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()
            
def HapusPesanan(id):
    try:
        TampilkanPesanan(id,2)
        tujuan = input("Masukkan id yang ingin dihapus ")
        cursor = connect()
        cursor.execute(f"UPDATE pesanan SET is_delete = '1' WHERE id_pesanan = {tujuan}")
        cursor.connection.commit()
        print("Data berhasil dihapus")

    except (Exception,Error) as error:
        print(error)

    finally:
        if cursor.connection:
            cursor.close()
            cursor.connection.close()


def BuatPesanan(id):
    try:
        Showtablewithout('katalog')
        cursor = connect()
        while True:
            katalog = inputint("Masukkan id barang yang ingin dibeli ")
            cursor.execute("SELECT id_katalog, stok_menu, soft_delete from katalog where stok > 0 and soft_delete = 0")
            record = cursor.fetchall()
            if any(katalog == x for x in record[0]):
                break
            else:
                print("Masukkan id katalog yang benar")
        jalan = input ("Masukkan nama jalan tujuan ")
        kecamatan = input ("Masukkan nama kecamatan tujuan ")
        kabupaten = input("Masukkan nama kabupaten tujuan ")
        while True:
            jumlah = inputint("Masukkan jumlah barang yang ingin dibeli ")
            cursor.execute(f"SELECT id_katalog,stok_menu from katalog where id_katalog = '{katalog}'")
            record = cursor.fetchall()
            if jumlah <= record[1] and jumlah > 0:
                break
            else:
                print("Masukkan jumlah yang benar")
        cursor.execute("SELECT nama_kabupaten from kabupaten")
        record = cursor.fetchall()
        if any(kabupaten.lower() == x.lower() for x in record[0]):
            print("1")
            # pass
        else:
            print("2")
            cursor.execute(f"INSERT INTO kabupaten(nama_kabupaten) Values('{kabupaten}')")
            # cursor.execute(f"SELECT id_kabupaten, nama_kabupaten from kabupaten where lower(nama_kabupaten) ilike '{kabupaten}'")
            # record = cursor.fetchone()
            # cursor.execute(f"INSERT INTO kecamatan(nama_kecamatan,id_kabupaten) Values('{kecamatan}',{record[0]})")
            # cursor.execute(f"SELECT id_kecamatan, nama_kecamatan from kecamatan where lower(nama_kecamatan) ilike '{kecamatan}'")
            # record = cursor.fetchone()
            # cursor.execute(f"INSERT INTO jalan(nama_jalan, id_kecamatan) Values('{jalan}',{cursor[0]})")
            # cursor.execute(f"SELECT id_jalan,nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
            # record = cursor.fetchone()
            # cursor.execute(f"INSERT INTO alamat_pengiriman(id_jalan) Values({record[0]})")
        cursor.execute("SELECT nama_kecamatan from kecamatan")
        record = cursor.fetchall()
        if any(kecamatan.lower() == x.lower() for x in record[0]):
            print("3")
            # pass
        else:
            print("4")
            cursor.execute(f"SELECT id_kabupaten, nama_kabupaten from kabupaten where lower(nama_kabupaten) ilike '{kabupaten}'")
            record = cursor.fetchone()
            cursor.execute(f"INSERT INTO kecamatan(nama_kecamatan,id_kabupaten) Values('{kecamatan}','{record[0]}')")
        #     cursor.execute(f"SELECT id_kecamatan, nama_kecamatan from kecamatan where lower(nama_kecamatan) ilike '{kecamatan}'")
        #     record = cursor.fetchone()
        #     cursor.execute(f"INSERT INTO jalan(nama_jalan, id_kecamatan) Values('{jalan}',{cursor[0]})")
        #     cursor.execute(f"SELECT id_jalan,nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
        #     record = cursor.fetchone()
        #     cursor.execute(f"INSERT INTO alamat_pengiriman(id_jalan) Values({record[0]})")
        cursor.execute("SELECT nama_jalan from jalan")
        record = cursor.fetchall()
        if any(jalan.lower() == x.lower() for x in record[0]):
            print("5")
            # pass
        else:
            print("6")
            cursor.execute(f"SELECT id_kecamatan, nama_kecamatan from kecamatan where lower(nama_kecamatan) ilike '{kecamatan}'")
            record = cursor.fetchone()
            print(record)
            cursor.execute(f"INSERT INTO jalan(nama_jalan, id_kecamatan) Values('{jalan}','{record[0]}')")
            print("insert berhasil ")
        #     cursor.execute(f"SELECT id_jalan, nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
        #     record = cursor.fetchone()
        #     print(record)
        #     cursor.execute(f"INSERT INTO alamat_pengiriman(id_jalan) Values('{record[0]}')")
        cursor.execute(f"SELECT id_jalan, nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
        record = cursor.fetchone()
        cursor.execute("SELECT id_jalan from alamat_pengiriman")
        record1 = cursor.fetchall()
        if any (record[0] == x for x in record1[0]):
            print("7")
            # pass
        else:
            print("8")
            cursor.execute(f"SELECT id_jalan,nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
            record = cursor.fetchone()
            cursor.execute(f"INSERT INTO alamat_pengiriman(id_jalan) Values('{record[0]}')")
        # cursor.connection.commit()

        cursor.execute(f"SELECT id_alamat_pengiriman, id_jalan from alamat_pengiriman where id_jalan = '{record[0]}'")
        record = cursor.fetchone()
        cursor.execute(f"INSERT INTO pesanan(tanggal_pesanan, status_pesanan, tanggal_pengiriman, is_delete, id_pengguna, id_alamat_pengiriman) VALUES (now() :: DATE, 'diproses', now() :: DATE, '0', {id}, {record[0]})")
        cursor.execute(f"SELECT id_pesanan, id_alamat_pengiriman from pesanan where id_alamat_pengiriman = '{record[0]}'")
        record = cursor.fetchone()
        cursor.execute(f"INSERT INTO detail_pesanan(jumlah_pesanan, subtotal, id_katalog, id_pesanan) VALUES ({jumlah}, 0, {katalog}, {record[0]})")
        cursor.connection.commit()

    except (Exception,Error) as error:
        print(error)


def StatusPesanan():
    pass

def Katalog():
    pass

def Laporan():
    pass

################################################################

login_status= 0
clear()

while True:
#     print("""Menu :
# 1. Registrasi
# 2. Login
# 3. Show Tabel
# 0. Keluar""")
    # pilihanmenu= inputint("Masukkan menu yang ingin dipilih: ")
    pilihanmenu = select("Registrasi \nLogin \nShow tabel \nKeluar")
    if pilihanmenu == 1:
        clear()
        regis()
    elif pilihanmenu == 2:  
        clear()
        data_user = login()
        print(data_user)
        if not data_user is None:
            login_status = 1
            clear()
            break
        print("Username atau passsword salah")
        getch()
        clear()
    elif pilihanmenu == 3 :
        clear()
        temp= input("Masukkan tabel yang ingin ditampilkan ")
        if not temp == "":
            showtable(temp)
        # getch()
        clear()
    elif pilihanmenu == 4 or pilihanmenu== 0:
        exit()

while login_status == 1:
    try:
        if data_user[1] is False: # Menu pembeli
            clear()
            print("""
1. Data akun (melihat dan mengedit)
2. Membuat Pesanan
3. Status pesanan (melihat dan menghapus)
4. Log out / keluar
""")
            temp = inputint("Masukkan menu yang diinginkan ")
            if temp == 1:
                clear()
                ShowAkun()
                temp = input("Tekan enter untuk keluar atau masukkan sembarang huruf untuk mengedit ")
                if temp != "":
                    ChangeAkunSelf(data_user[0])
            elif temp == 2:
                BuatPesanan(data_user[0])
                getch()
            elif temp == 3 :
                TampilkanPesanan(data_user[0])
                pilihan = input("Enter jika lanjut, masukkan sembarang huruf jika ingin menghapus data")
                if not pilihan == "":
                    clear()
                    HapusPesanan(data_user[0])
            elif temp == 4 :
                clear()
                temp = input("Apakah kamu yakin ingin keluar?\nketik y jika yakin ingin keluar ")
                if temp == "y":
                    login_status = 0

##################################################################################
        
        elif data_user[1] is True: # Menu admin
            clear()
            print("""
1. Data akun (melihat mengedit akun admin, melihat akun pengguna)
2. Katalog menu (melihat,mengedit)
3. Status pesanan (melihat,mengedit status)
4. Laporan penjualan (melihat,menambah)
5. Log out / keluar
""")
            temp =inputint("Masukkan angka ")
            if temp == 1:
                print("1. Data user\n" 
                "2. Data admin")
                temp = inputint("Masukkan angka ")
                if temp == 1: #Data all
                    ShowAkunAll()
                    temp= input("Tekan enter untuk keluar atau isi dengan sembarang huruf untuk mengedit ")
                    clear()
                    if temp == "":
                        pass
                    else :
                        ChangeAkunAll()
                elif temp == 2: #Data sendiri
                    clear()
                    ShowAkun()
                    temp = input("Tekan enter untuk keluar atau isi dengan sembarang huruf untuk mengedit ")
                    if temp != "":
                        ChangeAkunSelf(data_user[0])
            elif temp == 2:
                Katalog()
            elif temp == 3 :
                StatusPesanan()
            elif temp == 4 :
                Laporan()
            elif temp == 5 :
                clear()
                temp = input("Apakah kamu yakin ingin keluar?\nketik y jika yakin ingin keluar ")
                if temp == "y":
                    login_status = 0
        
    except :
        # print('Error, Silahkan kontak admin(Error 001)')
        print(Error)
        print("Error 123")


# # if connection:
# #     cursor.close()
# #     connection.close()



# showtable("pengguna")
# # ChangeAkunAll()