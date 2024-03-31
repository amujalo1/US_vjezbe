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


sm = rp2.StateMachine(0, sevseg, freq=2000, out_base=Pin(2), sideset_base=Pin(10))
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

button1 = Pin(18, Pin.IN, Pin.PULL_UP)
button2 = Pin(19, Pin.IN, Pin.PULL_UP)
button3 = Pin(20, Pin.IN, Pin.PULL_UP)
button4 = Pin(21, Pin.IN, Pin.PULL_UP)


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


# sm.put(segmentize(counter));
counter = 0
auto_counting = False

# Glavna petlja
while True:
    if not button1.value():  # Provera tastera 1 (uvećavanje)
        counter += 1
        sm.put(segmentize(counter, len(str(counter))))
        time.sleep_ms(200)  # Dilej nakon što se pritisne taster
        while not button1.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    elif not button2.value():  # Provera tastera 2 (smanjivanje)
        counter -= 1
        sm.put(segmentize(counter, len(str(counter))))
        time.sleep_ms(200)  # Dilej nakon što se pritisne taster
        while not button2.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    elif not button3.value():  # Provera tastera 3 (resetovanje)
        counter = 0
        sm.put(segmentize(counter, len(str(counter))));
        time.sleep_ms(200)  # Dilej nakon što se pritisne taster
        while not button3.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    elif not button4.value():  # Provera tastera 4 (pokretanje/zaustavljanje automatskog brojanja)
        auto_counting = not auto_counting
        while not button4.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    if auto_counting:
        counter += 1  # Automatsko inkrementiranje
        sm.put(segmentize(counter, len(str(counter))))
        time.sleep_ms(1000)  # Dilej za automatsko brojanje
    else:
        print(counter)
        sm.put(segmentize(counter, len(str(counter))))

