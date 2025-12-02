import os 
if os.name == 'nt':
    from msvcrt import getch

def getch_(ascii = 0): # getch tapi ditambah jika os selain windows
    if os.name == 'nt': #Jika os nya windows
        if ascii == 0:
            return getch()
        elif ascii == 1:
            return ord(getch())
    elif os.name() == 'posix': #Jika osnya linux atau macOs
        if ascii == 0:
            return input()
        elif ascii == 1:
            string = input()
            return ord(string[0])


def passbintang(text=""):
    string= ""
    print(text)
    if os.name == 'nt':
        while True:
            c = getch()
            if c[0] > 31 and c[0] < 127:
                string = string + c.decode('utf-8')
                print ("*" ,end='',flush=True)

            elif c[0] == 8: # backspace , buat hapus
                clear()
                print (text)
                string = string[:len(string)-1]
                print ("*"*len(string),end='',flush=True)
            elif c[0] == 13: # enter , buat keluar
                break
    elif os.name == 'posix':
        return input()

    clear()
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
    if os.name == 'nt':
        os.system('cls')
    
    elif os.name == 'posix':
        os.system('clear')
        
    return

def select(text):
    textt = text.splitlines()
    # print(textt)
    target = 0

    i = 0
    for x in textt:
        if i == target:
            print ("O ",end = "")
        else:
            print("  ",end="")
        i += 1
        print (x)

    while True: #Ngecek input
        i= 0
        listt = []
        c = ""
        while len(listt) < 2:
            c = getch_()
            listt.append(ord(c))
            if ord(c) != 224:
                listt.append(ord(c))
                break
            # print (ord(c))
        clear()
        # print (listt)
    # temp = []
    # c = getch()
    # temp.append(c)
    # print (temp)
    # if 


        if listt[1] == 80:
            target += 1
            # print("kebawah")
        elif listt[1] == 72:
            target -= 1
            # print("keatas")
        elif listt[1] == 13 or listt[1] == 27:
            break

        if target == len(textt):
            target = 0
        elif target == -1:
            target = len(textt)-1

        for x in textt:
            if i == target:
                print (" O ",end = "")
            else:
                print("   ",end="")
            i += 1
            print (x)
        # print (target)
        # print (type(c))
    return target+1