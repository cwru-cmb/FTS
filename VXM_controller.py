# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 14:09:08 2014

@author: Samuel Musilli, szm5@case.edu
This module is used to operate a Velmex brand linear slide
 via Python. It has motion control and position determining capabilities. 
 Before using the module for the first time you may need to use the PySerial
 installation applications included in the folder. One is for 64-bit Python,
 the other is for 32. They are labelled accordingly. It will likely be unnecessary with Linux."""

def steps_to_mm(steps):
    """converts units of bislide motor steps to millimeters"""
    return steps * .00635
    
def mm_to_steps(mm):
    """converts millimeters to units of steps of the bislide motor"""
    return int((mm / .00635) + .5)


def VXM_online(port=None):
    """initiates communication with the VXM and puts it in on-line mode. This function also takes
    the stage to the home position, at the center of the linear stage, and defines this point as zero. To find 
    the COM port in Windows, go to control panel. Open System and Security. Choose System. Then,
    on the left panel, choose Device Manager. Use the Ports (COM & LPT) drop down
    button. The USB interface labeled Serial will have something like COMx next to it. In Linux, simply go to the command terminal and type "dmesg | grep tty". It will be necessary to change the code for the proper serial port. However, unless there are other devices attached, you likely will not need to change this."""
    import serial, os #with Python, you have to import each group of functions, called "modules", that you will use. 
    global serport, ser, serial #This makes it so that you don't have to import the module for every function you use. 
    ser = serial.Serial() #there are lots of functions within serial. Setting ser as the name of serial.Serial() is just shorthand.
    if port is None:
        port = '/dev/ttyUSB0'
    ser.port = port #setting ser.port equal to this string variable 
    sudo_string = 'sudo chmod o+rw ' + port
    os.system(sudo_string) #writes directly to OS... like typing into command prompt
    serport = ser.port    
    ser.baudrate = 9600 #These next several lines are specific to working with serial ports. It just sets up communication.
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    ser.writeTimeout = 2
    ser.open()
    if ser.isOpen():
        ser.flushInput()
        ser.flushOutput()
        ser.write('F'.encode())
        print('opened successfully') #your standard Python print syntax
        ser.close()
        VXM_home_position()
    else: print('not opened successfully')

def VXM_home_position():
    """returns the slide to it's home position at x = 0, at the center of the slide."""
    import time   
    scan('-', 11, 160)
    time.sleep(15)
    scan('+', 10, 78.61935)
    time.sleep(10)
    ser.open() 
    ser.write('N'.encode())
    ser.close()
    
def VXM_to_position(destination):
    """receives a destination in units of millimeters, then commands the slide there."""
    ser.open()    
    ser.write('C,X'.encode())
    curr_pos = int(ser.readline()) #here I have used the "int" function. Python has 3 primary data types - 
    # strings, integers, and floats. Certain functions require a certain data type. To convert between data types,
    # you can use the functions str(x), int(x), and float(x). Floats are decimals. Strings are text. Integers are...
    # well, they're integers.
    if mm_to_steps(destination) != curr_pos: #here I have used '!=' which returns true/false, and means "does not equal"
    #if it is true, it will run the script in the if statement. If it is false, it goes to the else statement.
        move = str(mm_to_steps(destination) - curr_pos)
        string_4 ='C,I1M'+move+',R,C' 
        ser.write(string_4.encode())
    else:
        print( "that is the current position.")
    ser.close()

def VXM_get_position(command):
    """Gives the current position of the linear slide in units of millimeters.
    It receives a string, either 'print' or 'return' and performs the operation
    commanded. Both print and return give the value in units of millimeters."""
    ser.open()    
    ser.write('C,X'.encode())
    if command == 'print':
        print(str(steps_to_mm(int(ser.readline()))) + 'mm')
    elif command == 'return':   
        return steps_to_mm(int(ser.readline()))
    ser.close()

def scan(direction, speed, distance):
    """receives a direction as either '+' or '-', a speed in units mm/s,
    and a distance in mm. It then commands the stage to move the distance specified
    at the speed specified. Maximum motor speed is 38 mm/s."""
    ser.open()    
    if speed <= 38.1:
        speed = str(mm_to_steps(speed))
        if direction == '+':
            sign = 1
        else:
            sign = -1
        string1 = 'C,SA1M'+speed + ',R'
        ser.write(string1.encode())
        string2 = 'I1M'+ str(sign*mm_to_steps(distance))+',R'
        ser.write(string2.encode())
    else: 
        print('error: maximum speed is 38.1 mm/s')
    ser.close()
    
def scanset(direction, speed, distance, n):
    """receives a direction as either '+' or '-', a speed in units mm/s,
    a distance in mm, and an integer n that determines the number of times it will 
    make one cycle (to destination, then back). It then commands the stage to 
    move the distance specified at the speed specified. Maximum motor speed is 38 mm/s."""
    import time    
    ser.open()
    t = distance/speed
    if speed <= 38.1:  
        speed = str(mm_to_steps(speed))
        command = str(mm_to_steps(distance))
        code = 'C,'
        string_3 ='C,SA1M'+speed+',R' 
        ser.write(string_3.encode())
        if direction == '+':
            for i in range(n):
                code = code+'I1M'+command+',I1M-'+command+','       
        else:
            for i in range(n):
                code = code+'I1M-'+command+',I1M'+command+','
        code = code+'R'
        print("Running Scan " + str(n))
        ser.write(code.encode())
    else: 
        print('error: maximum speed is 38.1 mm/s')
    ser.close()

def tell(str):
    ser.open()
    ser.write(str.encode())
    ser.close()

def show_pos():
    import time
    while True:
        VXM_get_position('print')
        time.sleep(.5)
