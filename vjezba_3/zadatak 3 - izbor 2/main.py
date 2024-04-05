import machine
import utime

# Definiraj pinove za redove i kolone matrice tastature
ROWS = [machine.Pin(pin) for pin in [9, 8, 7, 6]]
COLS = [machine.Pin(pin) for pin in [5, 4, 3, 2]]

# Mapiranje tastera na karaktere
key_map = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Konfiguracija pinova
for col in COLS:
    col.init(mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)

for row in ROWS:
    row.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_DOWN)


# Funkcija za čitanje pritisnutih tastera
def read_keys(stanje):
    pressed_keys = []
    for col_index, col_pin in enumerate(COLS):
        col_pin.value(1)
        print7segment(stanje)
        for row_index, row_pin in enumerate(ROWS):
            if row_pin.value() == 1:
                print7segment(stanje)
                pressed_keys.append(key_map[row_index][col_index])
                utime.sleep_ms(100)  # Dodajemo kratki delay kako bismo spriječili višestruka čitanja
        col_pin.value(0)
    return pressed_keys


# Funkcija za čitanje pritisnutih tastera, uzima samo brojeve
def read_numbers(stanje):
    pressed_keys = []
    for col_index, col_pin in enumerate(COLS):
        col_pin.value(1)
        print7segment(stanje)
        for row_index, row_pin in enumerate(ROWS):
            if row_pin.value() == 1:
                print7segment(stanje)
                key_pressed = key_map[row_index][col_index]
                # Provjeravamo da li je pritisnuti taster broj
                if key_pressed.isdigit():
                    pressed_keys.append(key_pressed)
                utime.sleep_ms(10)  # Dodajemo kratki delay kako bismo spriječili višestruka čitanja
        col_pin.value(0)
    return pressed_keys


# Funkcija koja čeka otpuštanje tastera
def wait_for_release():
    while any(row.value() == 1 for row in ROWS):
        pass


from machine import Pin
import time

segments = [21, 10, 11, 12, 13, 14, 15, 16]  # DP A B C D E F G
dig = [17, 18, 19, 20]  # 4, 3, 2, 1: 4 odgovara za hiljdatidi broj, 3 za stotice 2 za desetice i 1 za jedinice

digits = [
    [0, 1, 1, 1, 1, 1, 1, 0],  # 0
    [0, 0, 1, 1, 0, 0, 0, 0],  # 1
    [0, 1, 1, 0, 1, 1, 0, 1],  # 2
    [0, 1, 1, 1, 1, 0, 0, 1],  # 3
    [0, 0, 1, 1, 0, 0, 1, 1],  # 4
    [0, 1, 0, 1, 1, 0, 1, 1],  # 5
    [0, 1, 0, 1, 1, 1, 1, 1],  # 6
    [0, 1, 1, 1, 0, 0, 0, 0],  # 7
    [0, 1, 1, 1, 1, 1, 1, 1],  # 8
    [0, 1, 1, 1, 1, 0, 1, 1],  # 9
    [0, 0, 0, 0, 0, 0, 0, 0],  # prazno
    [1, 0, 0, 0, 0, 0, 0, 0],  # zarez
    [0, 0, 0, 0, 0, 0, 0, 1],  # minus
]
digits = [[not bit for bit in digit] for digit in digits]


def print7segment(digits_array):
    for c, cifra in enumerate(digits_array):
        for i, pin in enumerate(segments):
            Pin(pin, Pin.OUT).value(cifra[i])
        Pin(dig[c], Pin.OUT).value(1)
        time.sleep_ms(20)
        Pin(dig[c], Pin.OUT).value(0)


def segmentize(num, vel):
    segs = [
        digits[num // 1000 % 10],  # Prva cifra
        digits[num // 100 % 10],  # Treća cifra s desna
        digits[num // 10 % 10],  # Pretposljednja cifra
        digits[num % 10]  # Posljednja cifra

    ]
    if num % 10 == 0 and vel == 0:
        segs[3] = digits[10]
    if (num // 10) % 10 == 0 and vel < 2:
        segs[2] = digits[10]
    if (num // 100) % 10 == 0 and vel < 3:
        segs[1] = digits[10]
    if (num // 1000) % 10 == 0 and vel < 4:
        segs[0] = digits[10]

    return segs


def CekanjeZaUnosHesha(stanje):
    while True:
        print7segment(stanje)
        pressed = read_keys(stanje)
        if pressed and pressed[0] == '#':
            # Ovdje dodajte kod koji se izvršava nakon unosa #
            break
        else:
            wait_for_release()
        utime.sleep_ms(10)  # Pauza između očitavanja


# Glavna petlja
waiting_for_pound = False
num4 = ""
wrong_attempts = 0  # Brojač pogrešnih pokušaja
print7segment([digits[10]] * 4)

while True:
    if num4 == "":
        pressed = read_numbers([digits[10]] * 4)
    else:
        pressed = read_numbers(segmentize(int(num4), len(num4)))
    if pressed:
        num4 += ''.join(pressed)

        print7segment(segmentize(int(num4), len(num4)))
        if len(num4) == 4:
            waiting_for_pound = True
    else:
        if waiting_for_pound:
            CekanjeZaUnosHesha(segmentize(int(num4), len(num4)))
            if num4 == '1234':  # Promijeniti sa stvarnim PIN-om
                # tacan pin
                for _ in range(5):
                    for _ in range(5):
                        print7segment([digits[11]] * 4)
                        utime.sleep_ms(10)
                    for _ in range(5):
                        print7segment([digits[10]] * 4)
                        utime.sleep_ms(10)
                print7segment([digits[10]] * 4)
            else:
                wrong_attempts += 1
                if wrong_attempts == 3:
                    for i in range(9, -1, -1):  # Odbrojavanje od 9 do 0
                        for _ in range(10):
                            print7segment(segmentize(i, 1))
                            utime.sleep_ms(10)

                    print7segment([digits[10]] * 4)
                    wrong_attempts = 0  # Resetujemo brojač pogrešnih pokušaja
                    num4 = ""  # Resetujemo num4 nakon odbrojavanja
                    waiting_for_pound = False
                    continue  # Nastavljamo sa čekanjem unosa PIN-a
                for _ in range(5):  # Pogrešan PIN
                    for _ in range(5):
                        print7segment([digits[12]] * 4)
                        utime.sleep_ms(10)
                    for _ in range(5):
                        print7segment([digits[10]] * 4)
                        utime.sleep_ms(10)
                print7segment([digits[10]] * 4)
            num4 = ""  # Resetujemo num4 nakon provjere PIN-a
            waiting_for_pound = False
            wait_for_release()
        else:
            wait_for_release()
            prev_pressed = []
    utime.sleep_ms(10)  # Pauza između očitavanja

