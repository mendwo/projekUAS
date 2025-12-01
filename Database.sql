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

SELECT COUNT(*) from pengguna

SELECT * FROM pengguna

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

create table riwayat_stok(
id_riwayat_stok serial PRIMARY KEY,
tanggal_riwayat DATE NOT NULL,
is_tambah BOOLEAN NOT NULL,
jumlah_pemasukan NUMERIC (10,2) NOT NULL,
is_delete BOOLEAN NOT NULL,
id_pengguna INTEGER REFERENCES pengguna (id_pengguna),
id_katalog INTEGER REFERENCES katalog (id_katalog)
);

drop table riwayat_stok

create table katalog(
id_katalog serial primary key,
nama_menu VARCHAR (30) NOT NULL,
stok_menu NUMERIC (10,2) NOT NULL,
harga_menu INTEGER NOT NULL,
jenis_menu VARCHAR (30) NOT NULL,
deskripsi_menu VARCHAR (30),
soft_delete BOOLEAN NOT null,
id_pengguna INTEGER REFERENCES pengguna (id_pengguna)
);

drop table katalog

create table transaksi(
id_transaksi SERIAL PRIMARY KEY,
tanggal_transaksi DATE NOT NULL,
status_transaksi VARCHAR (30) NOT NULL,
is_delete BOOLEAN NOT NULL,
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
SELECT * FROM riwayat_stok
SELECT * FROM katalog
SELECT * FROM transaksi
SELECT * FROM metode_transaksi
SELECT * FROM detail_pesanan
SELECT * FROM alamat_pengiriman
SELECT * FROM jalan
SELECT * FROM kecamatan
SELECT * FROM kabupaten


--pengguna
INSERT INTO pengguna VALUES (1, '1', 'rahman hakimi', 'hakimiman', 'hakimipsg', '085647109817', 'hakimipsg@gmail.com', '0');
INSERT INTO pengguna VALUES (2, '1', 'kevin levrone', 'levrone', 'levronegacor', '085410293813', 'kevlevrone@gmail.com', '0');
INSERT INTO pengguna VALUES (3, '0', 'paul pogba', 'pogbaall', 'kingfrance', '085223198980', 'paulpogba@gmail.com', '0');
INSERT INTO pengguna VALUES (4, '0', 'kylian mbbappe', 'mbappey', 'kingmadrid', '082231923410', 'kmbappe@gmail.com', '0');

delete from pengguna
where id_pengguna = '1'

--riwayat stok
INSERT INTO riwayat_stok VALUES (1, '2024-01-03', '1', 13, '0', 1, 1);
INSERT INTO riwayat_stok VALUES (2, '2024-03-18', '1', 12, '0', 1, 2);
INSERT INTO riwayat_stok VALUES (3, '2024-02-05', '1', 10, '0', 2, 3);
INSERT INTO riwayat_stok VALUES (4, '2024-05-15', '1', 9, '0', 2, 4);

delete from riwayat_stok 
where id_riwayat_stok = '2'

--katalog 
INSERT INTO katalog(id_katalog, nama_menu, stok_menu, harga_menu, jenis_menu, soft_delete, id_pengguna)
VALUES(1, 'arbica aceh gayo', 13, 17000, 'robusta', '0', 1);
INSERT INTO katalog(id_katalog, nama_menu, stok_menu, harga_menu, jenis_menu, soft_delete, id_pengguna)
VALUES(2, 'robusta toraja', 12, 19000, 'robusta', '0', 1);
INSERT INTO katalog(id_katalog, nama_menu, stok_menu, harga_menu, jenis_menu, soft_delete, id_pengguna)
VALUES(3, 'premium famasa', 10, 24000, 'arabbica', '0', 2);
INSERT INTO katalog VALUES (4, 'axcelsa', 9, 26000, 'robusta', 'cinnamond, fruity, spicy', '0', 2);

delete from katalog
where id_katalog = '1'

--pesanan 
INSERT INTO pesanan VALUES (1, '2024-01-05', 'diproses', '2024-01-09', '0', 3, 1, 1);
INSERT INTO pesanan VALUES (2, '2024-03-19', 'dikirim', '2024-03-22', '0', 3, 1, 1);
INSERT INTO pesanan(id_pesanan, tanggal_pesanan, status_pesanan, is_delete, id_pengguna, id_transaksi) 
VALUES (3, '2024-02-10', 'dibatalkan', '1', 4, 3);
INSERT INTO pesanan VALUES (4, '2024-05-17', 'selesai', '2024-05-19', '0', 4, 4, 3);

delete from pesanan
where id_pesanan = '1'

--detail pesanan
INSERT INTO detail_pesanan VALUES (1, '2', '17000', 1, 1);
INSERT INTO detail_pesanan VALUES (2, '3', '19000', 1, 2);
INSERT INTO detail_pesanan VALUES (3, '2', '24000', 2, 3);
INSERT INTO detail_pesanan VALUES (4, '2', '26000', 4, 4);

delete from detail_pesanan
where id_detail_pesanan = '1'

--transaksi
INSERT INTO transaksi VALUES (1, '2024-01-05', 'sudah bayar', '0', 2);
INSERT INTO transaksi VALUES (2, '2024-03-22', 'belum bayar', '0', 1);
INSERT INTO transaksi VALUES (3, '2024-02-10', 'dibatalkan', '1', 2);
INSERT INTO transaksi VALUES (4, '2024-05-19', 'sudah bayar', '0', 1);

delete from transaksi
where id_transaksi = '1'

--metode_transaksi
INSERT INTO metode_transaksi VALUES (1, 'tunai');
INSERT INTO metode_transaksi VALUES (2, 'non tunai');

delete from metode_transaksi
where id_metode_transaksi = '1'

--alamat_pengiriman
INSERT INTO alamat_pengiriman VALUES (1, '3', 1);
INSERT INTO alamat_pengiriman VALUES (2, '5B', 1);
INSERT INTO alamat_pengiriman VALUES (3, '1', 2);
INSERT INTO alamat_pengiriman VALUES (4, '7', 3);

delete from alamat_pengiriman
where id_alamat_pengiriman = '1'

--jalan
INSERT INTO jalan VALUES (1, 'jl. sumatra', 1);
INSERT INTO jalan VALUES (2, 'jl. riau', 1);
INSERT INTO jalan VALUES (3, 'jl. jaksa agung', 2);

delete from jalan
where id_jalan = '1'

--kecamatan
INSERT INTO kecamatan VALUES (1, 'sumbersari', 1);
INSERT INTO kecamatan VALUES (2, 'ajung', 1);

delete from kecamatan
where id_kecamatan= '1'

--kabupaten
INSERT INTO kabupaten VALUES (1, 'jember');

delete from kabupaten
where id_kabupaten = '1'