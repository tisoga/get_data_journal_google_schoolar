import urllib.parse
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests

file_name = input('Silahkan Masukan Nama File untuk data journal yang akan disimpan: ')
if not file_name:
    file_name = 'initial_name'

with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as csvfiles:
    writer = csv.writer(csvfiles)
    # writer.writerow(['sep=,'])
    writer.writerow(['Judul Jurnal', 'Tahun Jurnal', 'Penulis', 'lokasi'])


def writer_new(judul, tahun, penulis, loc):
    with open(f'{file_name}.csv', 'a', newline='', encoding='utf-8') as csvfiles:
        writer = csv.writer(csvfiles)
        writer.writerow([judul, tahun, penulis, loc])


def add_urls():
    url = input('Masukan Profile URL google scholar yang ingin diambil datanya : ')
    urls.append(url)
    ask = input('Apakah ingin Memasukan URL lain ? (Y/N)')
    if ask.upper() == 'Y':
        add_urls()
    elif ask.upper() == 'N':
        print('Harap Tunggu ......')


def encode_url(url):
    result = urllib.parse.quote(url)
    return result


urls = []

add_urls()
count = 1

for url in urls:
    url_encoded = url + '#d=gs_md_cita-d&u={}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        tabel = soup.find('tbody', id='gsc_a_b')
        row = tabel.find_all('tr', class_='gsc_a_tr')
    except:
        print('Harap Masukan Profile URL Google Scholar yang valid')
        break

    for data in row:
        judul = data.find('a', class_='gsc_a_at')
        penulis = data.find('div', class_='gs_gray')
        tahun = data.find('td', class_='gsc_a_y')
        lokasi = url_encoded.format(encode_url(judul['data-href']))
        writer_new(judul.text, tahun.text, penulis.text, lokasi)
    print(f'Url ke-{count} selesai')
    count += 1
