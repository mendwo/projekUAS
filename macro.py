from msvcrt import *
import os


def passbintang(text=""):
    string= ""
    print(text)
    while True:
        c = getch()
        if c[0] > 31 and c[0] < 127:
            string = string + c.decode('utf-8')
            print ("*" ,end='',flush=True)

        elif c[0] == 8: # backspace , buat hapus
            os.system('cls')
            print (text)
            string = string[:len(string)-1]
            print ("*"*len(string),end='',flush=True)
        elif c[0] == 13: # enter , buat keluar
            break


    os.system('cls')
    # print(string)
    return string

def inputint(comment):
    while True:
        try:
            a = int(input(comment))
            break
        except ValueError:
            print ("Masukkan angka yang benar")

    return a

def clear():
    os.system('cls')