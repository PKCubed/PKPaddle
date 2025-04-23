import pygame
import serial
from serial.tools import list_ports
from pynput.keyboard import Key, Controller
import time
import tkinter as tk
import threading

closed = False

serial_port = "COM14"
baud_rate = 115200

serial_ports = []
serial_port = "None"

keyboard_key = Key.space

def get_ports():
    global serial_ports
    serial_ports = []
    for port, desc, hwid in sorted(list_ports.comports()):
        serial_ports.append(port)
    print(serial_ports)

get_ports()


def gui_function():
    global closed, serial_ports, serial_port
    
    window = tk.Tk()
    window.title("PKPaddle")
    window.geometry("300x200")

    icon = tk.PhotoImage(file="icon.png")
    window.iconphoto(True, icon)

    lbl = tk.Label(window, text="Select serial port:")
    lbl.grid()

    def comport_dropdown_changed(value):
        print(f"Selected option: {value}")
        serial_port = value
        comSelected.set(serial_port)

    comSelected = tk.StringVar(window)
    if serial_ports:
        comSelected.set(serial_ports[0])
        serial_port = serial_ports[0]
    else:
        comSelected.set("None")
    
    if serial_ports:
        comSelect = tk.OptionMenu(window, comSelected, *serial_ports, command=comport_dropdown_changed)
    else:
        comSelect = tk.OptionMenu(window, comSelected, "None", command=comport_dropdown_changed)
    comSelect.grid()
    
    def refresh():
        global serial_port, serial_ports
        print("Refreshing")
        get_ports()
        comSelect['menu'].delete(0,'end')
        if serial_ports:
            for port in serial_ports:
                comSelect['menu'].add_command(label=port)
            if serial_port not in serial_ports:
                serial_port = serial_ports[0]
            comSelected.set(serial_port)
                
        else:
            comSelect['menu'].add_command(label="None")
            comSelected.set("None")

    tk.Button(window, text="Refresh", command=refresh).grid()
    
    window.mainloop()
    closed = True

gui_thread = threading.Thread(target=gui_function)

gui_thread.start()

keyboard = Controller()
volume = 0
volume_timer = 0

pygame.mixer.init()
sound = pygame.mixer.Sound("C.wav")
sound.set_volume(0)
sound.play(-1)

while not closed:
    try:
        ser = serial.Serial(serial_port, 115200, timeout=1)
        while True:
            data = ser.readline().decode('ascii').rstrip()
            if data:
                if data == "1":
                    volume = 1
                    if keyboard_key:
                        keyboard.press(Key.space)
                elif data == "0":
                    volume = 0
                    if keyboard_key:
                        keyboard.release(Key.space)
                sound.set_volume(volume)
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
    time.sleep(1)
if 'ser' in locals() and ser.is_open:
    ser.close()
