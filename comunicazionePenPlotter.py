import serial
import time
import serial.tools.list_ports

class Coordinata:
    def __init__(self, x, y):
        self.x=int(x)
        self.y=int(y)
    def inviami():
        a=len(str(self.x)+str(self.y))+2
        arduino.write(a)
        arduino.write(str.encode(","))
        arduino.write(self.x)
        arduino.write(str.encode(";"))
        arduino.write(self.y)
    def getX():
        return self.x
    def getY():
        return self.y

        
def inviaQuadrato(val):
    for i in range(4):
        #if i%3==0: x=val.getX()/4 else x=val.getX()*3/4
        x=val.getX()/4 if i%3==0 else val.getX()*3/4
        y=val.getY()/4 if i/2==0 else val.getY()*3/4
        coor=Coordinata(x,y)
        coor.inviami()
    
def cercaPorta():
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    for i in myports:
        if len(i[0].split("ACM"))>1:
            return "/dev/ttyACM"+i[0].split("ACM")[1]
    return None

def wait_readOne():
    while arduino.in_waiting<=0:
        time.sleep(0.0001)
    return arduino.read(1)

def leggiCoordinata():
    print("attendo numero cifre")
    
    strCifre=""
    strCifre+=wait_readOne()
    last_char = strCifre[-1]
    
    while last_char != ",":
        strCifre+=wait_readOne()
        last_char = strCifre[-1]
        
    strCifre=strCifre.split(",")
    cifre=strCifre[0]
    
    print(f"attendo {cifre} byte")
    #coordinateCalibrazione= Coordinate(x,y)
    while arduino.in_waiting<cifre:
        time.sleep(0.0001)
        
    strLetta=arduino.read(cifre);
    val=stringaLetta.split(";")
    
    return Coordinata(val[0],val[1])
 
def start_stop():
    print("attendo una 's'")
    while arduino.in_waiting<=0:
        time.sleep(0.0001)
    x=arduino.read(1)
    #print(x)
    if  x == b's':
        return 's'
    elif x == b'e':
        return 'e'
    return 'n'


#CERCO SERIALE        
print("Inserisci Arduino")
while cercaPorta() == None:
    time.sleep(0.1)
arduino=serial.Serial(port=cercaPorta(), baudrate=9600, timeout=.1)

#ATTENDO E INVIO S
while start_stop()!='s':
    time.sleep(0.0001)
arduino.reset_input_buffer()
print("invio s")
arduino.write(str.encode("s"))

#ATTENDO DATI CALIBRAZIONE
calibrazione=leggiCoordinata()
print(calibrazione)

#CALCOLIAMO PUNTI DA INVIARE
#so che il motore si trova nell'angolo in basso a sinistra
inviaQuadrato(calibrazione)