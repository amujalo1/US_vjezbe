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
def read_keys():
    pressed_keys = []
    for col_index, col_pin in enumerate(COLS):
        col_pin.value(1)
        for row_index, row_pin in enumerate(ROWS):
            if row_pin.value() == 1:
                pressed_keys.append(key_map[row_index][col_index])
                utime.sleep_ms(200)  # Dodajemo kratki delay kako bismo spriječili višestruka čitanja
        col_pin.value(0)
    return pressed_keys


# Funkcija za čitanje pritisnutih tastera, uzima samo brojeve
def read_numbers():
    pressed_keys = []
    for col_index, col_pin in enumerate(COLS):
        col_pin.value(1)
        for row_index, row_pin in enumerate(ROWS):
            if row_pin.value() == 1:
                key_pressed = key_map[row_index][col_index]
                # Provjeravamo da li je pritisnuti taster broj
                if key_pressed.isdigit():
                    pressed_keys.append(key_pressed)
                utime.sleep_ms(200)  # Dodajemo kratki delay kako bismo spriječili višestruka čitanja
        col_pin.value(0)
    return pressed_keys


# Funkcija koja čeka otpuštanje tastera
def wait_for_release():
    while any(row.value() == 1 for row in ROWS):
        pass


import rp2
from rp2 import PIO
from machine import Pin
import time


# ------ #
# sevseg #
# ------ #

@rp2.asm_pio(out_init=[PIO.OUT_LOW] * 8, sideset_init=[PIO.OUT_LOW] * 4)
def sevseg():
    wrap_target()
    label("0")
    pull(noblock).side(0)  # 0
    mov(x, osr).side(0)  # 1
    out(pins, 8).side(1)  # 2
    out(pins, 8).side(2)  # 3
    out(pins, 8).side(4)  # 4
    out(pins, 8).side(8)  # 5
    jmp("0").side(0)  # 6
    wrap()


sm = rp2.StateMachine(0, sevseg, freq=2000, out_base=Pin(10), sideset_base=Pin(17))
sm.active(1)

digits = [
    0b11000000,  # 0
    0b11111001,  # 1
    0b10100100,  # 2
    0b10110000,  # 3
    0b10011001,  # 4
    0b10010010,  # 5
    0b10000010,  # 6
    0b11111000,  # 7
    0b10000000,  # 8
    0b10011000,  # 9
    0b11111111,  # prazno
]
DP = Pin(21, Pin.OUT)


def segmentize(num, vel):
    segs = [
        digits[num % 10],  # Posljednja cifra
        digits[num // 10 % 10] << 8,  # Pretposljednja cifra
        digits[num // 100 % 10] << 16,  # Treća cifra s desna
        digits[num // 1000 % 10] << 24  # Prva cifra
    ]
    if num % 10 == 0 and vel == 0:
        segs[0] = digits[10]
    if (num // 10) % 10 == 0 and vel < 2:
        segs[1] = digits[10] << 8
    if (num // 100) % 10 == 0 and vel < 3:
        segs[2] = digits[10] << 16
    if (num // 1000) % 10 == 0 and vel < 4:
        segs[3] = digits[10] << 24

    return segs[0] | segs[1] | segs[2] | segs[3]


def CekanjeZaUnosHesha():
    while True:
        pressed = read_keys()
        if pressed and pressed[0] == '#':
            # Ovdje dodajte kod koji se izvršava nakon unosa #
            break
        else:
            wait_for_release()
        utime.sleep_ms(100)  # Pauza između očitavanja


# Glavna petlja
DP.on()
waiting_for_pound = False
num4 = ""
wrong_attempts = 0  # Brojač pogrešnih pokušaja
sm.put(segmentize(0, 0))

while True:
    pressed = read_numbers()
    if pressed:
        num4 += ''.join(pressed)

        sm.put(segmentize(int(num4), len(num4)))
        if len(num4) == 4:
            waiting_for_pound = True
    else:
        if waiting_for_pound:
            CekanjeZaUnosHesha()
            if num4 == '1234':  # Promijeniti sa stvarnim PIN-om
                sm.put((digits[10] | digits[10] << 8 | digits[10] << 16 | digits[10] << 24))  # tacan pin
                for _ in range(5):
                    DP.off()
                    utime.sleep_ms(500)
                    DP.on()
                    utime.sleep_ms(500)
                sm.put(segmentize(0, 0))
            else:
                wrong_attempts += 1
                if wrong_attempts == 3:
                    for i in range(9, -1, -1):  # Odbrojavanje od 9 do 0
                        sm.put(segmentize(i, 1))
                        utime.sleep(1)
                    sm.put(segmentize(0, 0))
                    wrong_attempts = 0  # Resetujemo brojač pogrešnih pokušaja
                    num4 = ""  # Resetujemo num4 nakon odbrojavanja
                    waiting_for_pound = False
                    continue  # Nastavljamo sa čekanjem unosa PIN-a
                for _ in range(5):
                    sm.put((0b10111111 | 0b10111111 << 8 | 0b10111111 << 16 | 0b10111111 << 24))
                    utime.sleep_ms(500)  # Pogrešan PIN
                    sm.put((0b11111111 | 0b11111111 << 8 | 0b11111111 << 16 | 0b11111111 << 24))
                    utime.sleep_ms(500)
                sm.put(segmentize(0, 0))
            num4 = ""  # Resetujemo num4 nakon provjere PIN-a
            waiting_for_pound = False
            wait_for_release()
        else:
            wait_for_release()
            prev_pressed = []
    utime.sleep_ms(100)  # Pauza između očitavanja

