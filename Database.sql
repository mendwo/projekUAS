create table pengguna(
id_pengguna SERIAL PRIMARY KEY,
is_admin BOOLEAN NOT NULL,
nama_lengkap VARCHAR (30) NOT NULL,
username VARCHAR (25) NOT NULL,
passwords VARCHAR (30) NOT NULL,
no_telpon VARCHAR (30) NOT NULL UNIQUE,
email VARCHAR (30) NOT NULL UNIQUE,
is_delete BOOLEAN NOT NULL
);

drop table pengguna

create table pesanan(
id_pesanan SERIAL PRIMARY KEY,
tanggal_pesanan DATE NOT NULL,
status_pesanan VARCHAR (30) NOT NULL,
tanggal_pengiriman DATE,
is_delete BOOLEAN NOT NULL,
id_pengguna INTEGER REFERENCES pengguna (id_pengguna),
id_transaksi INTEGER REFERENCES transaksi (id_transaksi),
id_alamat_pengiriman INTEGER REFERENCES alamat_pengiriman (id_alamat_pengiriman)
);

drop table pesanan

create table katalog(
id_katalog serial primary key,
nama_menu VARCHAR (30) NOT NULL,
stok_menu NUMERIC (10,2) NOT NULL,
harga_menu INTEGER NOT NULL,
jenis_menu VARCHAR (30) NOT NULL,
deskripsi_menu VARCHAR (30),
is_delete BOOLEAN NOT null
);

drop table katalog

create table transaksi(
id_transaksi SERIAL PRIMARY KEY,
nominal INTEGER NOT NULL,
id_metode_transaksi INTEGER REFERENCES metode_transaksi (id_metode_transaksi)
);

drop table transaksi

create table metode_transaksi(
id_metode_transaksi SERIAL PRIMARY KEY,
nama_metode_transaksi VARCHAR (25)
);

drop table metode_transaksi

create table detail_pesanan(
id_detail_pesanan SERIAL PRIMARY KEY,
jumlah_detail_pesanan INTEGER NOT NULL,
harga_satuan INTEGER NOT NULL,
id_pesanan INTEGER REFERENCES pesanan (id_pesanan),
id_katalog INTEGER REFERENCES katalog (id_katalog)
);

drop table detail_pesanan

create table alamat_pengiriman(
id_alamat_pengiriman SERIAL PRIMARY KEY,
no_alamat VARCHAR (25) NOT NULL,
id_jalan INTEGER REFERENCES jalan (id_jalan)
);

drop table alamat_pengiriman

create table jalan(
id_jalan SERIAL PRIMARY KEY,
nama_jalan VARCHAR (30) NOT NULL,
id_kecamatan INTEGER REFERENCES kecamatan (id_kecamatan)
);

drop table jalan

create table kecamatan(
id_kecamatan SERIAL PRIMARY KEY,
nama_kecamatan VARCHAR (30),
id_kabupaten INTEGER REFERENCES kabupaten (id_kabupaten)
);

drop table kecamatan

create table kabupaten(
id_kabupaten SERIAL PRIMARY KEY,
nama_kabupaten VARCHAR (30)
);

drop table kabupaten

SELECT * FROM pengguna
SELECT * FROM pesanan
SELECT * FROM katalog
SELECT * FROM transaksi
SELECT * FROM metode_transaksi
SELECT * FROM detail_pesanan
SELECT * FROM alamat_pengiriman
SELECT * FROM jalan
SELECT * FROM kecamatan
SELECT * FROM kabupaten

SELECT COunt(*) from pengguna

--pengguna
INSERT INTO pengguna VALUES (1, '1', 'm hakimi', 'hakimipsg', 'hkmin', '085647121345', 'hakimi@gmail.com', '0');
INSERT INTO pengguna VALUES (2, '1', 'm salah', 'salahegypt', 'emngyah', '085649101240', 'msalah@gmail.com', '0');
INSERT INTO pengguna VALUES (3, '0', 'paul pogba', 'pogbang', 'pogball', '082237221395', 'pugba@gmail.com', '0');
INSERT INTO pengguna VALUES (4, '0', 'lancelot', 'mlbb', 'pancegg', '082240131285', 'pance@gmail.com', '0');
INSERT INTO pengguna VALUES (5, '0', 'kante', 'white', 'pace', '085640132393', 'elpace@gmail.com', '0');

--pesanan
INSERT INTO pesanan VALUES (1, '2024-01-05', 'dikirim', '2024-01-07', '0', 1, 1, 1);
INSERT INTO pesanan VALUES (2, '2024-02-10', 'diproses', '2024-02-14', '0', 1, 2, 1);
INSERT INTO pesanan VALUES (3, '2024-03-15', 'diproses', '2024-03-19', '0', 2, 3, 2);
INSERT INTO pesanan (id_pesanan, tanggal_pesanan, status_pesanan, is_delete, id_pengguna, id_transaksi, id_alamat_pengiriman)
VALUES (4, '2024-05-13', 'dibatalkan', '1', 4, 4, 3);
INSERT INTO pesanan VALUES (5, '2024-09-12', 'selesai', '2024-09-16', '0', 5, 5, 4);

--katalog
INSERT INTO katalog(id_katalog, nama_menu, stok_menu, harga_menu, jenis_menu, is_delete)
VALUES(1, 'arbica aceh gayo', 15, 17000, 'robusta', '0');
INSERT INTO katalog(id_katalog, nama_menu, stok_menu, harga_menu, jenis_menu, is_delete)
VALUES(2, 'robusta toraja', 13, 19000, 'robusta', '0');
INSERT INTO katalog(id_katalog, nama_menu, stok_menu, harga_menu, jenis_menu, is_delete)
VALUES(3, 'premium famasa', 11, 25000, 'arabica', '0');
INSERT INTO katalog VALUES (4, 'axcelsa', 10, 29000, 'robusta', 'cinnamond, fruity, spicy', '0');
INSERT INTO katalog (id_katalog, nama_menu, stok_menu, harga_menu, jenis_menu, is_delete)
VALUES (5, 'robusta telagawangi', 16, 20000, 'robusta', '0');

-- detail_pesanan
INSERT INTO detail_pesanan values (1, 2, 17000, 1, 1);
INSERT INTO detail_pesanan values (2, 3, 19000, 1, 2);
INSERT INTO detail_pesanan values (3, 1, 22000, 2, 3);
INSERT INTO detail_pesanan values (4, 2, 29000, 3, 4);
INSERT INTO detail_pesanan values (5, 3, 20000, 4, 5);
INSERT INTO detail_pesanan values (6, 2, 25000, 5, 3);

--transaksi
INSERT INTO transaksi values (1, 91000, 2);
INSERT INTO transaksi values (2, 22000, 1);
INSERT INTO transaksi values (3, 58000, 1);
INSERT INTO transaksi values (4, 60000, 2);
INSERT INTO transaksi values (5, 50000, 1);

--metode_transaksi
INSERT INTO metode_transaksi values (1, 'tunai');
INSERT INTO metode_transaksi values (2, 'non tunai');

--alamat_pengiriman
INSERT INTO alamat_pengiriman values (1, '12', 1);
INSERT INTO alamat_pengiriman values (2, '5B', 2);
INSERT INTO alamat_pengiriman values (3, '3A', 2);
INSERT INTO alamat_pengiriman values (4, '2', 3);

--jalan
INSERT INTO jalan values (1, 'jl. jawa', 1);
INSERT INTO jalan values (2, 'jl. riau', 1);
INSERT INTO jalan values (3, 'jl. mastrip', 2);

--kecamatan
INSERT INTO kecamatan values (1, 'sumbersari', 1);
INSERT INTO kecamatan values (2, 'tegal besar', 1);

--kabupaten
INSERT INTO kabupaten values (1, 'jember');