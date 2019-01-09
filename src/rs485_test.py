import serial
from time import sleep

ser = serial.Serial('COM28', 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

print(ser.is_open)

str_check_M = '$01M\r'
str_check_F = '$01F\r'
str_set_ON = '#010001\r'
str_set_OFF = '#010000\r'

ser.write(str_check_M.encode())
sleep(1)
while True:
    read_out = ser.readline().decode('ascii')
    if not read_out:
        sleep(1)
        continue
    else:
        break

print(read_out)


ser.write(str_check_F.encode())
sleep(1)
while True:
    read_out = ser.readline().decode('ascii')
    if not read_out:
        sleep(1)
        continue
    else:
        break

print(read_out)


ser.write(str_set_ON.encode())
sleep(1)
while True:
    read_out = ser.readline().decode('ascii')
    if not read_out:
        sleep(1)
        continue
    else:
        break

print(read_out)

sleep(10)

ser.write(str_set_OFF.encode())
sleep(1)
while True:
    read_out = ser.readline().decode('ascii')
    if not read_out:
        sleep(1)
        continue
    else:
        break

print(read_out)
