import serial
import struct
import time

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.01)

try:
    while True:
        
         # Lee la entrada del usuario
        dato1 = int(input("Ingrese el valor para dato1: "))
        dato2 = int(input("Ingrese el valor para dato2: "))
        dato3 = int(input("Ingrese el valor para dato3: "))
        
        data = f"{dato1},{dato2}, {dato3} \n"
                
        ser.write(data.encode())
        print(data.encode())
        
        time.sleep(0.1)     
       
except KeyboardInterrupt:
    # Maneja la interrupción del teclado (Ctrl+C)
    print("Programa interrumpido")
    ser.close()



