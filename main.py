import psycopg2
from psycopg2 import Error, sql
from prettytable import from_db_cursor, PrettyTable
from macro import *
from connectsql import *

### Note : Sisa fitur sedang menunggu konfirmasi dari basda benar atau tidak. Daripada kerja dua kali

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
        if jumlah[0] % 5 == 0:
            page = jumlah[0]//5
        else:
            page = jumlah[0]//5+1
        for x in range(page):
            print("Halaman ke ",x+1)
            record = cursor.fetchmany(5)
            columns = [x[0] for x in cursor.description]
            mytable = PrettyTable(columns)
            for y in record:
                zz = []
                for z in y:
                    if z is None:
                        zz.append("-")
                    else:
                        zz.append(z)
                mytable.add_row(zz)
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
    if jumlah[0] % 5 == 0:
        page = jumlah[0]//5
    else:
        page = jumlah[0]//5+1
    for x in range(page):
        print("Halaman ke ",x+1)
        record = cursor.fetchmany(5)
        columns = [x[0] for x in cursor.description]
        mytable = PrettyTable(columns)
        for y in record:
            zz = []
            for z in y:
                if z is None:
                    zz.append("-")
                else:
                    zz.append(z)
            mytable.add_row(zz)
        print(mytable)
        getch_()

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
                cursor.execute("SELECT id_pengguna from pengguna ORDER BY id_pengguna desc")
                record = cursor.fetchone()
                id = record[0] + 1
                cursor.execute("INSERT INTO pengguna(id_pengguna,is_admin,nama_lengkap,username,passwords,no_telpon,email,is_delete) VALUES (%s,False,%s, %s,%s,%s,%s,False)", (id,nama,username, passw,telp,email))
                cursor.connection.commit()
                clear()
                print("Berhasil registrasi")
                getch_()
                clear()
                break
            else:
                print("jumlah karakter username atau password tidak memenuhi syarat...")
                getch_()
        except (Exception,Error) as error:
            print(error)

def login_user():
    username= input("masukkan username ")
    passw= passbintang("masukkan password ")
    return username, passw

def login(username, passw):
    cursor = connect()
    try :
        cursor.execute(f"SELECT * FROM pengguna")
        records = cursor.fetchall()
    except psycopg2.Error as Error:
        print("Salah")
    index = None
    for index,row in enumerate(records):
        if username == row[3] and passw == row[4]:
            print ("berhasil")
            print (index)
            return row
            # return row
    if index is None:
        print("Salah")

def login_refresh(id_user):
    cursor = connect()
    try :
        cursor.execute(f"SELECT * FROM pengguna where id_pengguna = {id_user}")
        records = cursor.fetchone()
    except psycopg2.Error as Error:
        print("Salah")
    return records


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
        getch_()
    else:
        clear()
        print("Data tidak jadi diubah")
        getch_()

def ChangeAkunSelf(id_):## jumlah karakter atau len harus disesuaikan dengan query nanti

    count = 0
    cursor = connect()
    cursor.execute(f"Select * from pengguna where id_pengguna = {id_}")
    records = cursor.fetchone()
    query = "Update pengguna Set "
    while True:
        nama = input("Masukkan nama baru, kosongkan jika sama ")
        if not nama == "":
            if len(nama) > 3 and len(nama) < 33:
                query = query + f" nama_lengkap = '{nama}'"
                count += 1
                break
            else:
                continue
        else:
            break
    while True:
        username = input ("Masukkan username baru, kosongkan jika sama ")
        if not username == "":
            if len(username) > 3 and len(username) < 17:
                if not count == 0:
                    query = query + ","
                query = query + f" username = '{username}'"
                count += 1
                break
        else:
            break
    while True:
        password = input("Masukkan password baru, kosongkan jika sama ")
        if not password == "":
            if len(password) > 3 and len(password) < 17:
                if not count == 0:
                    query = query + ","
                query = query + f" passwords = '{password}'"
                count += 1
                break
        else:
            break
    while True:
        no = input("Masukkan nomer telepon baru, kosongkan jika sama ")
        if not no == "":
            if all(x.isdigit() or x in "+-"  for x in no):
                if not count == 0:
                    query = query + ","
                count += 1
                query = query + f" no_telpon = '{no}'"
                break
            else:
                print("Maukkan input yang vaild")
                continue
        else:
            break
    while True:
        email = input("Masukkan email baru, kosongkan jika sama ")
        if not email == "":
            if email and "@" in email and "." in email:
                if not count == 0:
                    query = query + ","
                count += 1
                query = query + f" email = '{email}'"
                break
            else:
                continue
        else:
            break
                
    query = query + f" WHERE id_pengguna = {records[0]}"
    if count != 0:
        cursor.execute(query)
        cursor.connection.commit()
        clear()
        print(f"{count} data berhasil diubah...")
        getch_()
    else:
        clear()
        print("Data tidak jadi diubah")
        getch_()

def TampilkanPesanan(id,mode=1):
    try:
        clear()
        cursor = connect()
        # cursor.execute(f"SELECT p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman FROM pesanan p where is_delete = '0' and id_pengguna = '{id}'")
        if mode == 1: #tanpa id
            cursor.execute(f"SELECT p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman, j.nama_jalan || ', ' || k.nama_kecamatan || ', ' || ka.nama_kabupaten AS Alamat FROM pesanan p, jalan j, kecamatan k, kabupaten ka, alamat_pengiriman a where is_delete = '0' and id_pengguna = '{id}' and p.id_alamat_pengiriman = a.id_alamat_pengiriman and a.id_jalan = j.id_jalan and j.id_kecamatan = k.id_kecamatan and k.id_kabupaten = ka.id_kabupaten")
        else:
            cursor.execute(f"SELECT p.id_pesanan, p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman, j.nama_jalan || ', ' || k.nama_kecamatan || ', ' || ka.nama_kabupaten AS Alamat FROM pesanan p, jalan j, kecamatan k, kabupaten ka, alamat_pengiriman a where is_delete = '0' and id_pengguna = '{id}' and p.id_alamat_pengiriman = a.id_alamat_pengiriman and a.id_jalan = j.id_jalan and j.id_kecamatan = k.id_kecamatan and k.id_kabupaten = ka.id_kabupaten")
        record = cursor.fetchall()
        # print("test")
        columns = [x[0] for x in cursor.description]
        mytable = PrettyTable(columns)
        if len(record) == 0:
            print("Anda belum melakukan pemesanan")
            return 1
        else:
            for y in record:
                zz = []
                for z in y:
                    if z is None:
                        zz.append("-")
                    else:
                        zz.append(z)
                mytable.add_row(zz)
            print(mytable)

            return 0

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
        if not tujuan == "":
            cursor = connect()
            cursor.execute(f"UPDATE pesanan SET is_delete = '1' WHERE id_pesanan = {tujuan}")
            cursor.connection.commit()
            print("Data berhasil dihapus")

    except (Exception,Error) as error:
        print(error)

    finally:
        if not tujuan == "" and cursor.connection:
            cursor.close()
            cursor.connection.close()


def BuatPesanan(id):
    try:
        Showtablewithout('katalog')
        cursor = connect()
        cursor.execute("SELECT id_pesanan from pesanan ORDER BY id_pesanan desc")
        record = cursor.fetchone()
        # id_pesanan = record[0] + 1
        kataloglist = []
        jumlahlist = []
        while True:
            katalog = input("Masukkan id barang yang ingin dibeli, kosongkan jika ingin selesai ")
            if katalog == "":
                break
            elif katalog.isdigit():
                katalog = int(katalog)
            jumlah = inputint("Masukkan jumlah yang ingin dipesan ")
            cursor.execute("SELECT id_katalog, stok_menu, soft_delete from katalog where stok_menu > 0 and soft_delete = '0'")
            record = cursor.fetchall()
            if any(katalog == x[0] for x in record):
                if any(jumlah <= y[1] for y in record):
                    kataloglist.append(katalog)
                    jumlahlist.append(jumlah)
                else:
                    print("Masukkan jumlah yang benar")
            else:
                print("Masukkan id katalog yang benar")
        if len(kataloglist) == 0 :
            return
        jalan = input ("Masukkan nama jalan tujuan ")
        kecamatan = input ("Masukkan nama kecamatan tujuan ")
        kabupaten = input("Masukkan nama kabupaten tujuan ")
        # while True:
        #     jumlah = inputint("Masukkan jumlah barang yang ingin dibeli ")
        #     cursor.execute(f"SELECT id_katalog,stok_menu from katalog where id_katalog = '{katalog}'")
        #     record = cursor.fetchone()
        #     print("asidj",record)
        #     if jumlah <= record[1] and jumlah > 0:
        #         break
        #     else:
        #         print("Masukkan jumlah yang benar")
        cursor.execute("SELECT nama_kabupaten from kabupaten")
        record = cursor.fetchall()
        print("test789")
        if any(kabupaten.lower() == x[0].lower() for x in record):
            print("1")
            # pass
        else:
            print("2")
            cursor.execute("SELECT id_kabupaten from kabupaten ORDER BY id_kabupaten desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"INSERT INTO kabupaten(id_kabupaten,nama_kabupaten) Values('{id_}','{kabupaten}')")
            # cursor.execute(f"SELECT id_kabupaten, nama_kabupaten from kabupaten where lower(nama_kabupaten) ilike '{kabupaten}'")
            # record = cursor.fetchone()
            # cursor.execute(f"INSERT INTO kecamatan(nama_kecamatan,id_kabupaten) Values('{kecamatan}',{record[0]})")
            # cursor.execute(f"SELECT id_kecamatan, nama_kecamatan from kecamatan where lower(nama_kecamatan) ilike '{kecamatan}'")
            # record = cursor.fetchone()
            # cursor.execute(f"INSERT INTO jalan(nama_jalan, id_kecamatan) Values('{jalan}',{cursor[0]})")
            # cursor.execute(f"SELECT id_jalan,nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
            # record = cursor.fetchone()
            # cursor.execute(f"INSERT INTO alamat_pengiriman(id_jalan) Values({record[0]})")
        print("test6732")
        cursor.execute("SELECT nama_kecamatan from kecamatan")
        record = cursor.fetchall()
        if any(kecamatan.lower() == x[0].lower() for x in record):
            print("3")
            # pass
        else:
            print("4")
            cursor.execute("SELECT id_kecamatan from kecamatan ORDER BY id_kecamatan desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"SELECT id_kabupaten, nama_kabupaten from kabupaten where lower(nama_kabupaten) ilike '{kabupaten}'")
            record = cursor.fetchone()
            cursor.execute(f"INSERT INTO kecamatan(id_kecamatan,nama_kecamatan,id_kabupaten) Values('{id_}','{kecamatan}','{record[0]}')")
        #     cursor.execute(f"SELECT id_kecamatan, nama_kecamatan from kecamatan where lower(nama_kecamatan) ilike '{kecamatan}'")
        #     record = cursor.fetchone()
        #     cursor.execute(f"INSERT INTO jalan(nama_jalan, id_kecamatan) Values('{jalan}',{cursor[0]})")
        #     cursor.execute(f"SELECT id_jalan,nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
        #     record = cursor.fetchone()
        #     cursor.execute(f"INSERT INTO alamat_pengiriman(id_jalan) Values({record[0]})")
        print("hdashadsd")
        cursor.execute("SELECT nama_jalan from jalan")
        record = cursor.fetchall()
        if any(jalan.lower() == x[0].lower() for x in record):
            print("5")
            # pass
        else:
            print("6")
            cursor.execute("SELECT id_jalan from jalan ORDER BY id_jalan desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"SELECT id_kecamatan, nama_kecamatan from kecamatan where lower(nama_kecamatan) ilike '{kecamatan}'")
            record = cursor.fetchone()
            print(record)
            cursor.execute(f"INSERT INTO jalan(id_jalan,nama_jalan, id_kecamatan) Values('{id_}','{jalan}','{record[0]}')")
            print("insert berhasil ")
        #     cursor.execute(f"SELECT id_jalan, nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
        #     record = cursor.fetchone()
        #     print(record)
        #     cursor.execute(f"INSERT INTO alamat_pengiriman(id_jalan) Values('{record[0]}')")
        # cursor.execute("SELECT id_pesanan from pesanan ORDER BY id_pesanan desc")
        # record = cursor.fetchone()
        # id = record[0] + 1
        cursor.execute(f"SELECT id_jalan, nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
        record = cursor.fetchone()
        cursor.execute("SELECT id_jalan from alamat_pengiriman")
        record1 = cursor.fetchall()
        if any (record[0] == x[0] for x in record1):
            print("7")
            # pass
        else:
            print("8")
            cursor.execute("SELECT id_alamat_pengiriman from alamat_pengiriman ORDER BY id_alamat_pengiriman desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"SELECT id_jalan,nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
            record = cursor.fetchone() #id_jalan
            cursor.execute(f"INSERT INTO alamat_pengiriman(id_alamat_pengiriman,id_jalan) Values('{id_}','{record[0]}')")
        # cursor.connection.commit()

        print("9")
        cursor.execute("SELECT id_pesanan from pesanan ORDER BY id_pesanan desc")
        record2 = cursor.fetchone()
        print(record2)
        if record2 == None:
            id_= 1
        else:
            id_ = record2[0] + 1 #id_pesanan
        cursor.execute(f"SELECT id_alamat_pengiriman, id_jalan from alamat_pengiriman where id_jalan = '{record[0]}'")
        record = cursor.fetchone() #id_alamat
        id_alamat = record[0]
        print("10")
        getch_()
        clear()
        while True:
            print("1. Tunai\n2. Non tunai")
            metode = input("Masukkan metode pembayaran ")
            if metode == "1" :
                metode = "tunai"
                break
            elif metode == "2":
                metode = "non tunai"
                break
            else:
                print("Masukkan pilihan yang benar")
        cursor.execute("SELECT id_transaksi from transaksi ORDER BY id_transaksi desc")
        record = cursor.fetchone()
        if record == None :
            id_transaksi = 1
        else:
            id_transaksi = record[0] + 1 #id_transaksi
        cursor.execute(f"INSERT INTO transaksi Values ({id_transaksi}, '{metode}', 'belum membayar', '0')")
        print("890")
        cursor.execute(f"INSERT INTO pesanan(id_pesanan,tanggal_pesanan, status_pesanan, is_delete, id_pengguna, id_transaksi, id_alamat_pengiriman) VALUES ('{id_}',now() :: DATE, 'belum bayar', '0', {id}, {id_transaksi}, '{id_alamat}')")
        cursor.execute("SELECT id_detail_pesanan from detail_pesanan ORDER BY id_detail_pesanan desc")
        record = cursor.fetchone()
        if record == None:
            id_ = 1
        else:
            id_ = record[0] + 1 #id_detail_pesanan
        print("11")
        cursor.execute(f"SELECT id_pesanan, id_alamat_pengiriman from pesanan where id_alamat_pengiriman = '{id_alamat}' ORDER BY id_pesanan desc")
        record = cursor.fetchone() #id_pesanan
        index= 0
        for x in kataloglist: #belum harga satuan
            cursor.execute(f"SELECT id_katalog, harga_menu from katalog where id_katalog = {x}")
            record_harga = cursor.fetchone()
            cursor.execute(f"INSERT INTO detail_pesanan(id_detail_pesanan,jumlah_pesanan, harga_satuan, id_pesanan, id_katalog) VALUES ('{id_}',{jumlahlist[index]},{record_harga[1]}, {record[0]}, {x})")
            id_ += 1
            index += 1
        cursor.connection.commit()
        
        return

    except (Exception,Error) as error:
        print(error)
        return

def StatusPesanan():
    pass

def Katalog():
    pass

def Laporan():
    pass

def Pembayaran(id):
    #WIP, nunggu basda jadi
    TampilkanPesanan(id,2)
    cursor = connect()
    cursor.execute(f"SELECT * from pesanan where id_pengguna = '{id}'")
    record = cursor.fetchall()
    # print("test07")
    # print(record)
    if len(record) == 0:
        print("Anda belum melakukan pemesanan")
        return 1
    while True:
        id_ = inputint("Masukkan id yang ingin dibayar ")
        if any(id_ == x[0] for x in record):
            cursor.execute(f"SELECT id_transaksi FROM pesanan where id_pesanan = '{id_}'")
            id_transaksi = cursor.fetchone()
            break
        elif id_ == "":
            return
        else:
            print("Masukkan id yang benar")
            getch_()
            continue
    
    cursor.execute(f"SELECT jumlah_pesanan*harga_satuan FROM detail_pesanan where id_pesanan = {id_}")
    record = cursor.fetchall()
    harga = 0
    for x in record:
        harga += x[0]
    while True:
        print("Harga yang harus dibayar adalah ",harga)
        bayar = inputint("Uang yang dibayar :")
        if bayar == harga:
            pilihbayar = input("Apakah anda yakin? ketik y jika anda yakin ")
            if pilihbayar == "y":
                cursor.execute(f"UPDATE transaksi SET status_pembayaran = 'sudah membayar' where id_transaksi = '{id_transaksi[0]}'")
                print("Pesanan berhasil dibayar")
                getch_()
                break
        elif bayar < harga:
            print("Nominal anda kurang ")
            getch_()
            clear()
        elif bayar > harga:
            print("Nominal anda terlalu banyak")
            getch_()
            clear()


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
        username,password = login_user()
        data_user = login(username, password)
        # print(data_user)
        if not data_user is None:
            login_status = 1
            clear()
            break
        else:
            print("Username atau passsword salah")
            getch_()
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
        id_user = data_user[0]
        data_user = login_refresh(id_user)
        if data_user[1] is False: # Menu pembeli
            clear()
            print("""
1. Data akun (melihat dan mengedit)
2. Membuat Pesanan
3. Status pesanan (melihat dan menghapus)
4. Pembayaran
5. Log out / keluar
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
                getch_()
            elif temp == 3 :
                pilih = TampilkanPesanan(data_user[0])
                if pilih == 0:
                    pilihan = input("Enter jika lanjut, masukkan sembarang huruf jika ingin menghapus data ")
                    if not pilihan == "":
                        clear()
                        HapusPesanan(data_user[0])
                else:
                        getch_()
            elif temp == 4:
                Pembayaran(data_user[0])
            elif temp == 5 :
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
        
    except (Exception,Error) as error:
        # print('Error, Silahkan kontak admin(Error 001)')
        print(error)
        print("Error 123")
        break
    # finally:
    #     if cursor.connection():
    #         cursor.close()
    #         cursor.connectio.closen()


# # if connection:
# #     cursor.close()
# #     connection.close()



# showtable("pengguna")
# # ChangeAkunAll()