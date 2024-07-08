import serial
def main():
    s = serial.Serial(port="COM10", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)
    s.flush()
    while 1:
        data = input("data: ")
        s.write(f"{data}\r".encode())
        mes = s.read_until().strip()
        print(mes.decode())
if __name__ == "__main__":
    main()
