# _*_ coding: utf-8 _*_
import os
import time
#import machine
#import esp32
#from machine import Pin

"""
print(os.listdir())
start = time.time()
time.sleep(2)
print("it took", time.time() - start, "seconds.")
"""

"""
wake1 = Pin(14, mode = Pin.IN)

#level parameter can be: esp32.WAKEUP_ANY_HIGH or esp32.WAKEUP_ALL_LOW
esp32.wake_on_ext0(pin = wake1, level = esp32.WAKEUP_ANY_HIGH)

#your main code goes here to perform a task

print('Im awake. Going to sleep in 10 seconds')
sleep(10)
print('Going to sleep now')
machine.deepsleep()
"""

# 計算與起始時間 start 的時間差 (經過的 ms)
def timeElapsed(start):
    return time.ticks_diff(time.ticks_ms(), start)


def testGC():
    import gc
    gc.collect()
    print(gc.mem_free())


def testTimeElapsed():
    start = time.ticks_ms()
    time.sleep(2)
    print('Time elapsed in milliseconds: ', timeElapsed(start))


# There are ten capacitive touch-enabled pins that can be used on the ESP32: 0, 2, 4, 12, 13 14, 15, 27, 32, 33.
# Trying to assign to any other pins will result in a ValueError.
def testTouchPad():
    from machine import TouchPad, Pin
    t = TouchPad(Pin(14))
    print(t.read())            # Returns a smaller number when touched


"""
import ubinascii
print('1: ', ubinascii.hexlify(b'ABC'))
print('2: ', ubinascii.unhexlify(b'414243'))

MAC = b'5ef8r3'
print('3: ', ubinascii.hexlify(MAC))
print('4: ', ubinascii.hexlify(MAC, ':'))
"""

"""
from machine import WDT
wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
wdt.feed()
"""

"""
# Callback Function 1
def double(x):
    return x * 2

# Callback Function 1
def quadruple(x):
    return x * 4

# Middle Function called and return value
def getOddNumber(k, getEvenNumber):
    return 1 + getEvenNumber(k)

def main():
    k = 1
    i = getOddNumber(k, double)
    print(i)
    i = getOddNumber(k, quadruple)
    print(i)
    i = getOddNumber(k, lambda x: x * 8)
    print(i)
"""

"""
def foo(func, args, callback):
    # 计算第一个函数结果
    result = func(*args)
    # 调用回调函数
    callback(result)

def bar(x, y):
    return x + y

def show_data(data):
    print(data)

def main():
    # 两个数相加，并显示出来
    print('----------demo01:simple------------')
    foo(bar, (1, 2), callback=show_data)
    foo(bar, (10, 2), callback=show_data)
"""

"""
class myCallback():
    def __init__(self, callback_func, *args, **kwargs):
        self.callback_func = callback_func
        self._callback_args = args

    def callback(self):
        return self.callback_func(*self._callback_args)

def timer_test(x, y):
    for i in range(x):
        time.sleep(1)
        print('目前已經過的秒數：', i+1)
    if y == 'ms':
        return x * 1000
    else:
        return x

def main():
    cb = myCallback(timer_test, 3, 'ms')
    result = cb.callback()
    print('已經過的毫秒數：', result)
"""

"""
import uasyncio

async def sleep_5sec():
    while True:
        print('sleep 5 seconds')
        await uasyncio.sleep(5)

async def sleep_7sec():
    while True:
        print('sleep 7 seconds')
        await uasyncio.sleep(7)

def main():
    loop = uasyncio.get_event_loop()
    loop.create_task(sleep_5sec())  # schedule asap
    loop.create_task(sleep_7sec())
    loop.run_forever()

"""


# 二進位 bits 字串 to 十六進位制
def bits2hex(bits_str, num_of_bits=8):
    return hex(int(bits_str[:num_of_bits], 2))


# 十六進位制 to 二進位 bits 字串
def hex2bits(v_hex, num_of_bits=8):
    scale = 16  # equals to hexadecimal
    return bin(int(v_hex, scale))[2:].zfill(num_of_bits)


def strFill(v_str, v_len, c, side='before'):
    side = side.upper()
    v_len -= len(v_str)
    for _ in range(v_len):
        if 'A' in side:
            v_str += c
        else:
            v_str = c + v_str
    return v_str


def rotate(bits_array=[], times=1, direction=True):
    if len(bits_array) < 1:
        bits_array = [
            "01100110",
            "11111111",
            "10011001",
            "10000001",
            "10000001",
            "01000010",
            "00100100",
            "00011000",
        ]

    for _ in range(times):
        new_list = []
        for bits_str in bits_array:
            new_list.append(list(bits_str))
        # list_of_tuples = zip(*new_list[::-1])
        # new_list_r90 = [list(elem) for elem in list_of_tuples]

        list_of_tuples = zip(*reversed(new_list))
        if direction:
            new_list_90 = [list(elem)[::-1] for elem in list_of_tuples][::-1]
        else:
            new_list_90 = [list(elem) for elem in list_of_tuples]
        # print(new_list_r90)
        bits_array = []
        for bits_list in new_list_90:
            bits_str = "".join(bits_list)
            bits_array.append(bits_str)
    return bits_array


def scroll(bits_array=[], direction=True):
    if len(bits_array) < 1:
        bits_array = [
            "01100110",
            "11111111",
            "10011001",
            "10000001",
            "10000001",
            "01000010",
            "00100100",
            "00011000",
        ]

    print("Original List:", bits_array)
    if direction:
        new_list = bits_array[1:]
        new_list.append(bits_array[0])
    else:
        new_list = bits_array[:-1]
        new_list.insert(0, bits_array[-1])
    print("New List:", new_list)
    return new_list


def joinBitmap(str_list_1, str_list_2, direction='Up'):
    tmp_list1 = str_list_1.copy()
    tmp_list2 = str_list_2.copy()
    #print(len(tmp_list1), len(tmp_list2), direction)
    if len(tmp_list2) < 1:
        new_list = tmp_list1
    else:
        direction = direction.upper()
        if 'D' in direction:
            tmp_list2.extend(tmp_list1)
            new_list = tmp_list2
        elif 'L' in direction:
            new_list = []
            for i in range(len(tmp_list1)):
                if len(tmp_list2) > i:
                    print(tmp_list1[i] + tmp_list2[i])
                    new_list.append( tmp_list1[i] + tmp_list2[i])
        elif 'R' in direction:
            new_list = []
            for i in range(len(tmp_list1)):
                if len(tmp_list2) > i:
                    new_list.append(tmp_list2[i] + tmp_list1[i])
        else:
            tmp_list1.extend(tmp_list2)
            new_list = tmp_list1
    return new_list

# 字串補字元 (0)
def leadingZero(v_str, v_len):
    v_pre = v_str[:2].lower() if len(v_str) > 1 else ""
    if v_pre == '0x' or v_pre == '0b' or v_pre == '0o':
        v_str = v_str[2:]
    else:
        v_pre = ""
    if v_len > len(v_str):
        v_len = v_len - len(v_str)
        for _ in range(v_len):
            v_str = '0' + v_str
    return v_pre + v_str

def convHex2Bin(bits_array=[]):
    new_list = []
    #bits_array = [0x27, 0x75, 0x27, 0x0, 0x41, 0x22, 0x1c, 0x0]
    for bits in bits_array:
        if isinstance(bits, str):
            if bits[:2].lower() != '0x':
                bits += '0x'
        bits = bin(int(bits))  # 回傳 2 進位字串
        bits_str = leadingZero(bits, 8)
        new_list.append(bits_str)
    return new_list

"""
def joinBitmap(str_list_1, str_list_2, direction='Up'):
    tmp_list1 = str_list_1.copy()
    tmp_list2 = str_list_2.copy()
    # print(len(tmp_list1), len(tmp_list2), direction)
    if len(tmp_list2) < 1:
        new_list = tmp_list1
    else:
        direction = direction.upper()
        if 'D' in direction:
            tmp_list2.extend(tmp_list1)
            new_list = tmp_list2
        elif 'L' in direction:
            new_list = []
            for i in range(len(tmp_list1)):
                if len(tmp_list2) > i:
                    print(tmp_list1[i] + tmp_list2[i])
                    new_list.append(tmp_list1[i] + tmp_list2[i])
        elif 'R' in direction:
            new_list = []
            for i in range(len(tmp_list1)):
                if len(tmp_list2) > i:
                    new_list.append(tmp_list2[i] + tmp_list1[i])
        else:
            tmp_list1.extend(tmp_list2)
            new_list = tmp_list1
    return new_list
"""

if __name__ == "__main__":
    from machine import Pin, PWM

    PIN_TX = 13  # ESP8266:D7
    pin = PWM(Pin(PIN_TX))  # Define pin according to platform
    pin.freq(38000)  # NEC/38KHz, RC-5 RC-6/36KHz, Sony/40KHz, MCE/38KHz, Samsung/38KHz, Panasonic/36.3KHz
    pin.duty(0)

    #testGC()
    #testTimeElapsed()
    #testTouchPad()

    """
    bits_str = "1000000000000001"
    hex_value = bits2hex(bits_str, 16)
    print("{} {} -> {} {}".format(type(bits_str), bits_str, type(hex_value), hex_value))

    bits_str = hex2bits(hex_value, 16)
    print("{} {} -> {} {}".format(type(hex_value), hex_value, type(bits_str), bits_str))
    """

    #print(rotate([], 1))
    #print(rotate([], 1, False))

    """
    bits_array = scroll()
    scroll(bits_array, False)
    """

    #v_str = "11100"
    #print(strFill(v_str, 8, '0', 'before'))
    #print(strFill(v_str, 8, '0', 'after'))
    """
    bits_array1 = [
        "01100110",
        "11111111",
        "10011001",
        "10000001",
        "10000001",
        "01000010",
        "00100100",
        "00011000",
    ]

    bits_array2 = [
        "00000000",
        "11000011",
        "10011001",
        "10000001",
        "10000001",
        "01000010",
        "00100100",
        "11111111",
    ]

    joinBitmap(bits_array1, bits_array2, 'Up')
    joinBitmap(bits_array1, bits_array2, 'Down')
    joinBitmap(bits_array1, bits_array2, 'Left')
    joinBitmap(bits_array1, bits_array2, 'Right')
    """

    """
    # 繪自定義的 8x8 點陣圖
    bits_array = [
        0b00100111,
        0b01110101,
        0b00100111,
        0b00000000,
        0b01000001,
        0b00100010,
        0b00011100,
        0b00000000]

    # 2 進位 => 16 進位
    for bits in bits_array:
        if isinstance(bits, str):
            bits = str.encode(bits)         # String => Bytes
        print(hex(int(bits)))  # 回傳 16 進位字串
    print('\n')
    """

    # 轉換 Hex2Bin
    bits_array = [0x27, 0x75, 0x27, 0x0, 0x41, 0x22, 0x1c, 0x0]
    print(convHex2Bin(bits_array))

    """
    
    v_type = 'hex'
    for bits in bits_array:
        if isinstance(bits, str):
            if bits[:2].lower() != '0x':
                bits += '0x'
        bits_str = bin(int(bits))  # 回傳 2 進位字串
        print(bits_str)


        #print(hex(int(bits)))  # 回傳 16 進位字串
    """


