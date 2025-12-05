import psycopg2
from psycopg2 import Error, sql
from prettytable import from_db_cursor, PrettyTable
from macro import *
from connectsql import *



def showtable(entity): #Tampilkan menu dengan fitur order jika diperlukan
    try:
        querydefault = f"SELECT * FROM {entity} ORDER BY id_{entity} asc"
        ordercount = 0
        query = querydefault
        orderlist = []
        orderlistasc = []
        
        while True:
            if not 'cursor' in locals() and globals(): # may not work/needed
                cursor = connect()
            cursor.execute(f"Select count(*) from {entity}")
            jumlah = cursor.fetchone()
            cursor.execute(query)
            if jumlah[0] == 0:
                page = 1
            elif jumlah[0] % 5 == 0:
                page = jumlah[0]//5
            else:
                page = jumlah[0]//5+1
            # print("Jumlah =",jumlah[0])
            index = 0
            for x in range(page):
                if jumlah[0] == 0:
                    clear()
                    print("Belum ada data ")
                    getch_()
                    clear()
                    return
                logprint(index)
                printlog(f"Halaman ke {x+1}")
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
                printlog(mytable)
                temp = input("Masukkan order jika ingin mengurutkan, enter jika ingin pergi ke halaman berikutnya \natau isi sembarang jika ingin pergi ke halaman terakhir... ")
                if temp != "":
                    break
                else:
                    index += 2
                    clear()
                    pass
                # getch_()
            # clear()
            query = querydefault
            if temp == "":
                break
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
    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def Showtablewithout(entity): #Tampilkan tabel tanpa order dll
    try:
        query = f"SELECT * FROM {entity} ORDER BY id_{entity} asc"

        if not 'cursor' in locals() and globals(): # may not work/needed
            cursor = connect()

        cursor.execute(f"Select count(*) from {entity}")
        jumlah = cursor.fetchone()
        cursor.execute(query)

        if jumlah[0] == 0:
            clear()
            print("Data tidak ada")
            getch_()
            clear()
            return
        elif jumlah[0] % 5 == 0:
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
        
    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def registrasi(): # Menu registrasi
    while True:
        try:
            cursor = connect()
            cursor.execute("SELECT * FROM pengguna")
            record = cursor.fetchall()

            username = input("Masukkan username dengan jumlah 4-16 karakter (kosongkan untuk keluar) ")
            if username == "":
                clear()
                break
            passw = passbintang("Masukkan password dengan jumlah 4-16 karakter ")

            if len(username) <= 16 and len(username) >= 4 and  len(passw) <= 16 and len(passw) >= 4 :
                index = 1
                while True : # Data diri dan check input
                    while True:
                        nama= inputlog("Masukkan nama lengkap anda ")
                        if nama and all(c.isalpha() or c.isspace() for c in nama):
                            index +=1
                            break
                        else:
                            print("Masukkan data yang valid yang berisi huruf dan spasi saja")
                            getch_()
                            clear()
                            logpop()
                            logprint(index)
                    while True:
                        telp= inputlog("Masukkan nomer telepon anda ")
                        if telp and all(c.isdigit() or c in "+-" for c in telp):
                            if not any(telp == x[5] for x in record):
                                index += 1
                                break
                            else:
                                print("Nomer sudah dipakai, silahkan masukkan nomer yang lainnya")
                                getch_()
                                clear()
                                logpop()
                                logprint(index)
                        else:
                            print("Masukkan data yang valid yang mengandung angka atau simbol +- saja ")
                            getch_()
                            clear()
                            logpop()
                            logprint(index)

                    while True:
                        email= inputlog("Masukkan email anda ")
                        if email and "@" in email and "." in email:
                            if not any(email == x[6] for x in record):
                                index += 1
                                break
                            else:
                                print("Email sudah dipakai, silahkan masukkan email yang lainnya")
                                getch_()
                                clear()
                                logpop()
                                logprint(index)
                        else:
                            print ("Masukkan data yang valid yang berisi email lengkap dengan @ dan . ")
                            getch_()
                            clear()
                            logpop()
                            logprint(index)
                    
                    clear()
                    print("Username:",username)
                    print("Password:",passw)
                    print("Nama:",nama)
                    print("No telepon:",telp)
                    print("Email:",email)
                    temp = input ("Apakah data sudah benar? ketik y jika benar ")
                    if temp == "y":
                        break
                    else:
                        clear()
                        return

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
                clear()

        except (Exception,Error) as error:
            print(error)
        finally:
            if connect():
                cursor.connection.close()
                cursor.close()

def login_user(): #Engga kepake
    username= input("masukkan username ")
    passw= passbintang("masukkan password ")
    return username, passw

def login(username, passw): #Fitur login
    cursor = connect()
    try :
        cursor.execute(f"SELECT * FROM pengguna")
        records = cursor.fetchall()
        index = None
        for row in records:
            if username == row[3] and passw == row[4]:
                print ("berhasil")
                return row
        if index is None:
            print("Salah")

    except psycopg2.Error as Error:
        print("Salah")
    finally:
        if connect():
            cursor.connection.close()
            cursor.close()
        

def login_refresh(id_user): #Refresh data login jika diubah
    try :
        cursor = connect()
        cursor.execute(f"SELECT * FROM pengguna where id_pengguna = {id_user}")
        records = cursor.fetchone()

    except psycopg2.Error as error:
        print("Salah", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

    return records


def ShowAkun(): #Lihat data diri sendiri
    print("Nama: ",data_user[2])
    print("Username: ",data_user[3])
    print("Password: ",data_user[4])
    print("No. telepon :",data_user[5])
    print("Email: ",data_user[6])

def ShowAkunAll():#Engga dipake
    # cursor= connect()
    # cursor.execute("SELECT * FROM pengguna")
    showtable("pengguna")

def ChangeAkunAll():
    try:
        cursor = connect()
        Showtablewithout("pengguna")
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

    except(Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def ChangeAkunSelf(id_):## jumlah karakter atau len harus disesuaikan dengan query nanti
    try:
        clear()
        ShowAkun()
        print("")
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

    except(Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def TampilkanPesanan(id,mode=1):
    try:
        clear()
        cursor = connect()

        if mode == 1:
            cursor.execute(f"SELECT p.tanggal_pesanan, p.status_pesanan, t.nominal, p.tanggal_pengiriman, m.nama_metode_transaksi, j.nama_jalan || ', ' || k.nama_kecamatan || ', ' || ka.nama_kabupaten AS Alamat FROM pesanan p, jalan j, kecamatan k, kabupaten ka, alamat_pengiriman a, transaksi t, metode_transaksi m where p.is_delete = '0' and id_pengguna = '{id}' and p.id_alamat_pengiriman = a.id_alamat_pengiriman and a.id_jalan = j.id_jalan and j.id_kecamatan = k.id_kecamatan and k.id_kabupaten = ka.id_kabupaten and p.id_transaksi = t.id_transaksi and t.id_metode_transaksi = m.id_metode_transaksi")
        else:
            cursor.execute(f"SELECT p.id_pesanan, p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman, j.nama_jalan || ' ' || k.nama_kecamatan || ' ' || ka.nama_kabupaten AS Alamat FROM pesanan p, jalan j, kecamatan k, kabupaten ka, alamat_pengiriman a where is_delete = '0' and id_pengguna = '{id}' and p.id_alamat_pengiriman = a.id_alamat_pengiriman and a.id_jalan = j.id_jalan and j.id_kecamatan = k.id_kecamatan and k.id_kabupaten = ka.id_kabupaten")
        record = cursor.fetchall()

        if len(record) == 0:
            print("Anda belum memiliki pesanan ")
            getch_()
            return 0
        
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

    except (Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def BuatPesanan(id):
    try:
        Showtablewithout('katalog')
        cursor = connect()
        kataloglist = []
        jumlahlist = []

        while True: # Memasukkan barang dan jumlah ke keranjang
            katalog = input("Masukkan id barang yang ingin dibeli, kosongkan jika ingin selesai ")
            if katalog == "":
                if len(kataloglist) == 0:
                    print("Anda tidak memesan apapun....")
                    getch_()
                    return
                break
            elif katalog.isdigit():
                katalog = int(katalog)
            jumlah = inputint("Masukkan jumlah yang ingin dipesan ")
            cursor.execute("SELECT id_katalog, stok_menu, is_delete from katalog where stok_menu > 0 and is_delete = '0'")
            record = cursor.fetchall()
            if any(katalog == x[0] for x in record):
                if any(jumlah <= y[1] for y in record):
                    kataloglist.append(katalog)
                    jumlahlist.append(jumlah)
                else:
                    print("Masukkan jumlah yang benar")
            else:
                print("Masukkan id katalog yang benar")
        
        while True: # Masukkan alamat
            jalan = input ("Masukkan nama jalan tujuan ")
            if not jalan == "":
                if all(x.isalpha or x.isspace for x in jalan):
                    break
        while True:
            no_alamat = input ("Masukkan no alamat tujuan ")
            if not no_alamat == "":
                break
        while True:
            kecamatan = input ("Masukkan nama kecamatan tujuan ")
            if not kecamatan == "":
                break
        while True:
            kabupaten = input("Masukkan nama kabupaten tujuan ")
            if not kabupaten == "":
                break

        cursor.execute("SELECT nama_kabupaten from kabupaten") # Memasukkan data alamat ke databse
        record = cursor.fetchall()
        if any(kabupaten.lower() == x[0].lower() for x in record):
            pass
        else:
            cursor.execute("SELECT id_kabupaten from kabupaten ORDER BY id_kabupaten desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"INSERT INTO kabupaten(id_kabupaten,nama_kabupaten) Values('{id_}','{kabupaten}')")

        cursor.execute("SELECT nama_kecamatan from kecamatan")
        record = cursor.fetchall()
        if any(kecamatan.lower() == x[0].lower() for x in record):
            pass
        else:
            cursor.execute("SELECT id_kecamatan from kecamatan ORDER BY id_kecamatan desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"SELECT id_kabupaten, nama_kabupaten from kabupaten where lower(nama_kabupaten) ilike '{kabupaten}'")
            record = cursor.fetchone()
            cursor.execute(f"INSERT INTO kecamatan(id_kecamatan,nama_kecamatan,id_kabupaten) Values('{id_}','{kecamatan}','{record[0]}')")

        cursor.execute("SELECT nama_jalan from jalan")
        record = cursor.fetchall()
        if any(jalan.lower() == x[0].lower() for x in record):
            pass
        else:
            cursor.execute("SELECT id_jalan from jalan ORDER BY id_jalan desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"SELECT id_kecamatan, nama_kecamatan from kecamatan where lower(nama_kecamatan) ilike '{kecamatan}'")
            record = cursor.fetchone()
            # print(record)
            cursor.execute(f"INSERT INTO jalan(id_jalan,nama_jalan, id_kecamatan) Values('{id_}','{jalan}','{record[0]}')")

        cursor.execute(f"SELECT id_jalan, nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
        record = cursor.fetchone()
        cursor.execute("SELECT id_jalan from alamat_pengiriman")
        record1 = cursor.fetchall()
        if any (record[0] == x[0] for x in record1):
            pass
        else:
            cursor.execute("SELECT id_alamat_pengiriman from alamat_pengiriman ORDER BY id_alamat_pengiriman desc")
            record = cursor.fetchone()
            if record == None:
                id_ = 1
            else:
                id_ = record[0] + 1
            cursor.execute(f"SELECT id_jalan,nama_jalan from jalan where lower(nama_jalan) ilike '{jalan}'")
            record = cursor.fetchone() #id_jalan
            cursor.execute(f"INSERT INTO alamat_pengiriman(id_alamat_pengiriman, no_alamat, id_jalan) Values('{id_}', '{no_alamat}','{record[0]}')")

        cursor.execute("SELECT id_pesanan from pesanan ORDER BY id_pesanan desc")
        record2 = cursor.fetchone()
        if record2 == None:
            id_pesanan= 1
        else:
            id_pesanan = record2[0] + 1 #id_pesanan
        cursor.execute(f"SELECT id_alamat_pengiriman, id_jalan from alamat_pengiriman where id_jalan = '{record[0]}'")
        record = cursor.fetchone() #id_alamat
        id_alamat = record[0]
        clear()

        while True: # Memasukkan metode pembayaran
            print("1. Tunai\n2. Non tunai")
            metode = inputint("Masukkan metode pembayaran ")
            if metode == 1 or metode == 2:
                break
            else:
                print("Masukkan pilihan yang benar")

        cursor.execute("SELECT id_transaksi from transaksi ORDER BY id_transaksi desc")
        record = cursor.fetchone()
        id_transaksi = record[0] + 1
        cursor.execute(f"SELECT jumlah_detail_pesanan*harga_satuan FROM detail_pesanan where id_pesanan = {id_}")
        record = cursor.fetchall()
        harga = 0
        indexJumlah = 0

        for x in kataloglist: # Memasukkan pesanan dan transaksi ke database
            cursor.execute(f"SELECT harga_menu FROM katalog where id_katalog = {x}")
            hargabarang = cursor.fetchone()
            harga += hargabarang[0] * jumlahlist[indexJumlah]
            indexJumlah += 1
        cursor.execute(f"INSERT INTO transaksi Values ({id_transaksi}, {harga}, '{metode}')")
        cursor.execute(f"INSERT INTO pesanan(id_pesanan,tanggal_pesanan, status_pesanan, is_delete, id_pengguna, id_transaksi, id_alamat_pengiriman) VALUES ('{id_pesanan}',now() :: DATE, 'diproses', '0', '{id}', '{id_transaksi}','{id_alamat}')")
        
        cursor.execute("SELECT id_detail_pesanan from detail_pesanan ORDER BY id_detail_pesanan desc")
        record = cursor.fetchone()
        if record == None:
            id_ = 1
        else:
            id_ = record[0] + 1 #id_detail_pesanan

        index = 0
        for x in kataloglist: # Memasukkan detail transaksi ke database
            cursor.execute(f"SELECT id_katalog, harga_menu from katalog where id_katalog = {x}")
            record_harga = cursor.fetchone()
            cursor.execute(f"INSERT INTO detail_pesanan(id_detail_pesanan,jumlah_detail_pesanan, harga_satuan, id_pesanan, id_katalog) VALUES ('{id_}',{jumlahlist[index]},{record_harga[1]}, {id_pesanan}, {x})")
            id_ += 1
            index += 1

        cursor.execute(f"SELECT nama_metode_transaksi from metode_transaksi where id_metode_transaksi = {metode}")
        nama_metode = cursor.fetchone()
        while True: # Konfirmasi pembayaran
            temp = input(f"Harga yang harus dibayarkan adalah {harga} melalui metode {nama_metode[0]} \nMasukkan huruf y jika benar ")
            if temp == "y":
                break
            else:
                return

        indexJumlah = 0
        for x in kataloglist: #Update stok setelah pembelian
            cursor.execute(f"SELECT stok_menu FROM katalog where id_katalog = {x}")
            stok_awal = cursor.fetchone()
            stok = stok_awal[0] - jumlahlist[indexJumlah]
            cursor.execute(f"UPDATE katalog SET stok_menu = '{stok}' where id_katalog = {x}")
            indexJumlah += 1

        cursor.connection.commit()
        
        return

    except(Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()


def Katalog():
    try:
        Showtablewithout('katalog')
        cursor = connect()
        pilihan = input("Enter jika ingin keluar, masukkan sembarang jika ingin mengubah ")
        if pilihan == "":
            return
        clear()
        Showtablewithout('katalog')
        cursor.execute("SELECT * FROM katalog")
        record = cursor.fetchall()
        while True:
            id_ = inputint("Masukkan id yang ingin diubah ")
            if any(id_ == x[0] for x in record):
                cursor.execute(f"SELECT * FROM katalog where id_katalog = '{id_}'")
                katalog = cursor.fetchone()
                break
            elif pilihan == "":
                return
        query = "UPDATE katalog SET "
        count = 0
        while True:
            nama = input("Masukkan nama baru, kosongkan jika sama ")
            if not nama == "":
                query = query + f" nama_menu = '{nama}'"
                count += 1
                break
            else:
                break
        while True:
            jumlahstok = input("Masukkan stok baru, enter jika ingin sama ")
            if not jumlahstok == "":
                if jumlahstok.isdigit() :
                    jumlahstok = int(jumlahstok)
                    if not count == 0:
                        query = query + ","
                    query = query + f" stok_menu = '{jumlahstok}'"
                    count += 1
                    break
                else:
                    break
            else:
                break
        while True:
            harga = input("Masukkan harga baru, kosongkan jika sama ")
            if not harga == "":
                if not count == 0:
                    query = query + ","
                query = query + f" harga_menu = '{harga}'"
                count += 1
                break
            else:
                break
        while True:
            deskripsi = input("Masukkan deskripsi baru, kosongkan jika sama ")
            if not deskripsi == "":
                if not count == 0:
                    query = query + ","
                query = query + f" deskripsi_menu = '{deskripsi}'"
                count += 1
                break
            else:
                break
        while True:
            hapus = input("Apakah data dihapus,enter jika tidak, isi jika iya ")
            if not hapus == "":
                if katalog [5] == False:
                    if not count == 0:
                        query = query + ","
                    query = query + f" is_delete = '1'"
                    count += 1
                break
            else:
                if katalog [5] == True:
                    if not count == 0:
                        query = query + ","
                    query = query + f" is_delete = '0'"
                    count += 1
                break
                    
        query = query + f" WHERE id_katalog = {id_}"
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
    
    except(Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def statusPesanan(id_pengguna):
    clear()
    try:
        cursor = connect() #mencoba terhubung
        cursor.execute(f"""
                      SELECT p.id_pesanan, p.tanggal_pesanan, p.status_pesanan, p.tanggal_pengiriman
                      FROM pesanan p
                      WHERE p.id_pengguna = {id_pengguna} AND p.is_delete = '0' 
                      ORDE BY p.id_pesanan ASC
                      """)
        record = cursor.fetchall()

        while True:
            if len(record) == 0:
                print("anda belum punya pesanan")
            else:
                columns = [x[0] for x in cursor.description]
                mytable = PrettyTable(columns)
                for a in record:
                    ab = []
                    for b in a:
                        ab.append("-" if b is None else b)
                    mytable.add_row(ab)
                print(mytable)
            pilih = input("tekan Enter untu keluar")
            if pilih =="":
                break
    except(Exception, Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if cursor.connection:
            cursor.close()
            cursor.connection.close()

def UbahStatusPesanan(id_pesanan = None):
   
    try:
        clear()
        Showtablewithout('pesanan') 
        cursor = connect() #mecoba terhubung

        pilih = input("Enter untuk keluar, ketik sembarang untuk mengubah:")
        if pilih == "":
            return
        
        clear()
        Showtablewithout('pesanan')
        cursor.execute("SELECT * FROM pesanan WHERE is_delete = '0' ")
        record = cursor.fetchall() 

        while True:
            id_pesanan = input("Masukkan ID pesanan yang ingin diubah:")

            if id_pesanan == "":
                return
            elif id_pesanan.isdigit():
                id_pesanan = int(id_pesanan)
            else:
                continue
            
            ada = False
            for a in record:
                if id_pesanan == a[0]:
                    ada = True
            if not ada :
                print("Maaf, pesanan tidak ditemukan.")
                continue
            elif ada :
                break

        ddl = "UPDATE pesanan SET "
        count = 0

        cursor.execute(f"SELECT status_pesanan from pesanan where id_pesanan = {id_pesanan}")
        record = cursor.fetchone()
        piltus = record[0]
       
        if piltus == "diproses":                         # piltus = pilihan status 
            staru = "dikirirm"                          # staru = status baru
        elif piltus == "dikirim":
            staru = "selesai"
        elif piltus == "selesai":
            staru = "selesai"
        
        while True:
            clear()
            print("Status sekarang adalah",record[0])
            temp = input(f"Ubah status menjadi {staru}?(y jika iya, hapus jika menghapus pesanan) ")
            if temp == "y" or temp == "hapus":
                break
            else:
                print("Masukkan input yang benar")
                getch_()

        if temp == "y":
            if piltus == "diproses":
                ddl = ddl + "status_pesanan = 'dikirim', tanggal_pengiriman = now()::DATE "
            elif piltus == "dikirim":
                ddl = ddl + "status_pesanan = 'selesai' "
            elif piltus == "selesai":
                ddl = ddl + "status_pesanan = 'selesai' "

        elif temp == "hapus":
            ddl = ddl + "status_pesanan = 'dibatalkan', is_delete = True "

        ddl = ddl + f"WHERE id_pesanan = {id_pesanan}"
        cursor.execute(ddl)
        cursor.connection.commit()

        clear()
        if temp == "hapus":
            print("Data berhasil dihapus")
        else:
            print(f"Status pesanan {id_pesanan} berhasil diubah menjadi {staru}")
        getch_()      
            
    except(Exception, Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if cursor.connection:
            cursor.close()
            cursor.connection.close()

def laporan_bulanan(tahun):
    cursor = connect()
    try:
        if tahun :
            query = f"""
                SELECT 
                    EXTRACT(MONTH FROM p.tanggal_pesanan) AS "Bulan",
                    SUM(t.nominal) AS "Total Penjualan",
                    COUNT(p.id_pesanan) AS "Jumlah Transaksi"
                FROM pesanan p
                JOIN transaksi t ON p.id_transaksi = t.id_transaksi
                WHERE EXTRACT(YEAR FROM p.tanggal_pesanan) = {tahun}
                AND p.is_delete = '0'
                GROUP BY 1
                ORDER BY 1;
            """
        elif not tahun :
            query = (f"SELECT TO_CHAR(p.tanggal_pesanan, 'YYYY') as \"Tahun\",TO_CHAR(p.tanggal_pesanan, 'mm') as \"Bulan\", COUNT(p.id_pesanan) as \"Jumlah pesanan\", SUM(t.nominal) as \"Jumlah nominal\" from pesanan p, transaksi t where p.id_transaksi = t.id_transaksi GROUP BY 1,2 ORDER BY 1 desc,2 desc")
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print(f"Tidak ada data untuk tahun {tahun}")
            return
        
        columns = [x[0] for x in cursor.description]
        table = PrettyTable(columns)
        for r in rows:
            table.add_row(r)

        print("\n=== LAPORAN PENJUALAN BULANAN ===")
        print(table)

    except(Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def laporan_quartal(tahun):
    cursor = connect()
    try:
        if tahun:
            query = f"""
                SELECT
                    CEILING((EXTRACT(MONTH FROM p.tanggal_pesanan)::numeric) / 3) AS "Kuartal",
                    SUM(t.nominal) AS "Total Penjualan",
                    COUNT(p.id_pesanan) AS "Jumlah Transaksi"
                FROM pesanan p
                JOIN transaksi t ON p.id_transaksi = t.id_transaksi
                WHERE EXTRACT(YEAR FROM p.tanggal_pesanan) = {tahun}
                AND p.is_delete = '0'
                GROUP BY 1
                ORDER BY 1;
            """
        elif not tahun:
            query = (f"SELECT TO_CHAR(p.tanggal_pesanan, 'YYYY') as \"Tahun\", TO_CHAR(p.tanggal_pesanan, '\"Q\"Q') as \"Kuartal\", COUNT(p.id_pesanan) as \"Jumlah pesanan\", SUM(t.nominal) as \"Jumlah nominal\" from pesanan p, transaksi t where p.id_transaksi = t.id_transaksi GROUP BY 1,2 ORDER BY 1 desc,2 desc")
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print(f"Tidak ada data untuk tahun {tahun}")
            return
        columns = [x[0] for x in cursor.description]
        table = PrettyTable(columns)
        for r in rows:
            table.add_row(r)

        print("\n=== LAPORAN PENJUALAN QUARTAL ===")
        print(table)

    except(Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

def laporan_tahunan():
    cursor = connect()
    try:
        query = """
            SELECT
                EXTRACT(YEAR FROM p.tanggal_pesanan) AS "Tahun",
                SUM(t.nominal) AS "Total penjualan",
                COUNT(p.id_pesanan) AS "Jumlah Transaksi"
            FROM pesanan p
            JOIN transaksi t ON p.id_transaksi = t.id_transaksi
            WHERE p.is_delete = '0'
            GROUP BY 1
            ORDER BY 1;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("Tidak ada data tahunan")
            return
        
        columns = [x[0] for x in cursor.description]
        table = PrettyTable(columns)
        for r in rows:
            table.add_row(r)

        print("\n=== LAPORAN PENJUALAN TAHUNAN ===")
        print(table)

    except(Exception,Error) as error:
        print("Terdapat kesalahan: ", error)

    finally:
        if connect():
            cursor.connection.close()
            cursor.close()

################################################################
################################################################
################################################################

login_status= 0
clear()

print("SELAMAT DATANG DI TRACRCOFFE \n \nAplikasi Sistem Informasi Penjualan dan \nPengelolaan Biji Kopi Berbasis Digital\n")
print("Pencet apa saja untuk memasuki aplikasi.....",end='',flush=True)
getch_() #Bug(?)
clear()
while True:
    pilihanmenu = select("Registrasi \nLogin \nKeluar","---TRACRCOFFE---")
    if pilihanmenu == 1:
        clear()
        registrasi()
    elif pilihanmenu == 2:  
        clear()
        username = input("masukkan username ")
        password = passbintang("masukkan password ")
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
    elif pilihanmenu == 3:
        exit()



while login_status == 1:
    try:
        id_user = data_user[0]
        data_user = login_refresh(id_user)

        if data_user[1] is False: # Menu pembeli
            clear()
            temp = select("""Data akun (melihat dan mengedit)
Membuat Pesanan
Status pesanan
Log out / keluar
""")
            
            if temp == 1:
                clear()
                ShowAkun()
                print("Tekan enter untuk keluar atau masukkan sembarang huruf untuk mengedit ")
                temp = getch_(ascii=1)
                if temp != 13:
                    ChangeAkunSelf(data_user[0])
            elif temp == 2:
                BuatPesanan(data_user[0])
                getch_()
            elif temp == 3 :
                pesanan = TampilkanPesanan(data_user[0])
                getch_()
            elif temp == 4 :
                clear()
                print("Apakah kamu yakin ingin keluar?\nketik y jika yakin ingin keluar ")
                temp = getch_(ascii=1)
                if temp == 121:
                    clear()
                    login_status = 0

##################################################################################
        
        elif data_user[1] is True: # Menu admin
            clear()
            temp = select("""Data akun (melihat mengedit akun admin, melihat akun pengguna)
Katalog menu (melihat,mengedit)
Status pesanan (melihat,mengedit status)
Laporan penjualan (melihat,menambah)
Log out / keluar
""")
            if temp == 1:
                temp = select("Data user \nData admin")
                if temp == 1: #semua data
                    showtable("pengguna")
                    temp= input("Tekan enter untuk keluar atau isi dengan sembarang huruf untuk mengedit ")
                    clear()

                    if temp == "":
                        pass
                    else :
                        ChangeAkunAll()

                elif temp == 2: #Data sendiri (admin)
                    clear()
                    ShowAkun()
                    temp = input("Tekan enter untuk keluar atau isi dengan sembarang huruf untuk mengedit ")
                    if temp != "":
                        ChangeAkunSelf(data_user[0])

            elif temp == 2:
                Katalog()

            elif temp == 3 :
                UbahStatusPesanan()

            elif temp == 4 :
                temp_ = select("Laporan per bulan \nLaporan per kuartal \nLaporan per tahun")
                if temp_ == 1:
                    tahun = input("Masukkan tahun, kosongkan untuk menampilkan semua: ")
                    laporan_bulanan(tahun)
                    getch_()
                elif temp_ == 2:
                    tahun = input("Masukkan tahun: ")
                    laporan_quartal(tahun)
                    getch_()
                elif temp_ == 3:
                    laporan_tahunan()
                    getch_()

            elif temp == 5 :
                clear()
                temp = input("Apakah kamu yakin ingin keluar?\nketik y jika yakin ingin keluar ")
                if temp == "y":
                    login_status = 0
        
    except (Exception,Error) as error:
        print("Telah terjadi eror",error)
        break
