from machine import Pin
import time

segments = [9,2,3,4,5,6,7,8] #DP A B C D E F G
dig = [10,11,12,13] #4, 3, 2, 1: 4 odgovara za hiljdatidi broj, 3 za stotice 2 za desetice i 1 za jedinice

digits = [
    [0,1,1,1,1,1,1,0], # 0
    [0,0,1,1,0,0,0,0], # 1
    [0,1,1,0,1,1,0,1], # 2
    [0,1,1,1,1,0,0,1], # 3
    [0,0,1,1,0,0,1,1], # 4
    [0,1,0,1,1,0,1,1], # 5
    [0,1,0,1,1,1,1,1], # 6
    [0,1,1,1,0,0,0,0], # 7
    [0,1,1,1,1,1,1,1], # 8
    [0,1,1,1,1,0,1,1], # 9
    [0,0,0,0,0,0,0,0], # prazno
    [1,0,0,0,0,0,0,0], # zarez
]
digits = [[not bit for bit in digit] for digit in digits]

def print7segment(digits_array):
  for c, cifra in enumerate(digits_array):
    for i, pin in enumerate(segments):
      Pin(pin,Pin.OUT).value(cifra[i])
    Pin(dig[c], Pin.OUT).value(1)
    time.sleep_ms(20)
    Pin(dig[c], Pin.OUT).value(0)

button1 = Pin(18, Pin.IN, Pin.PULL_UP)
button2 = Pin(19, Pin.IN, Pin.PULL_UP)
button3 = Pin(20, Pin.IN, Pin.PULL_UP)
button4 = Pin(21, Pin.IN, Pin.PULL_UP)


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


counter = 0
print7segment([digits[10]]*4);
auto_counting = False

# Glavna petlja
while True:
    print7segment(segmentize(counter,len(str(counter))));
    if not button1.value():  # Provera tastera 1 (uvećavanje)
        counter += 1
        print7segment(segmentize(counter, len(str(counter))))
        time.sleep_ms(100)  # Dilej nakon što se pritisne taster
        while not button1.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    elif not button2.value():  # Provera tastera 2 (smanjivanje)
        counter -= 1
        print7segment(segmentize(counter, len(str(counter))))
        time.sleep_ms(100)  # Dilej nakon što se pritisne taster
        while not button2.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    elif not button3.value():  # Provera tastera 3 (resetovanje)
        counter = 0
        print7segment(segmentize(counter, len(str(counter))));
        time.sleep_ms(100)  # Dilej nakon što se pritisne taster
        while not button3.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    elif not button4.value():  # Provera tastera 4 (pokretanje/zaustavljanje automatskog brojanja)
        auto_counting = not auto_counting
        while not button4.value():  # Čekanje dok se taster ne otpusti
            time.sleep_ms(20)
    if auto_counting:
        counter += 1  # Automatsko inkrementiranje
        for _ in range(10):
            print7segment(segmentize(counter, len(str(counter))))
            time.sleep_ms(10)  # Dilej za automatsko brojanje

    else:
        print(counter)
        print7segment(segmentize(counter, len(str(counter))))