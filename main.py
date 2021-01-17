import cv2
import numpy as np
import pyautogui
from phue import Bridge
import rgbxy 
from configparser import ConfigParser

config = ConfigParser()

config.read("config.ini")
print("Philups hue connecting...")

ip = ""
light = ""

print("Philups hue connecting...")
print("Get ready to enter the ip address of your hue, before you press enter press the connect button on your hue device")
ip = input("Please enter the IP ADDRESS of your hue: ")
light = input("Enter the NAME of the light, caps sensitive: ")


bridge = Bridge(ip)

bridge.connect()

bridge.get_api()
print("Connected to " + ip + "'s api")


light_real = bridge.get_light(light)

light_obj = bridge.get_light_objects(light_real["name"])


print(light_obj)
SCREEN_SIZE = (600,400)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
print("Starting")




converter = rgbxy.Converter(rgbxy.GamutB)

while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    avg_color_per_row = np.average(frame, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    r = avg_color[0]
    g =  avg_color[1]
    b = avg_color[2]
    xy = converter.rgb_to_xy(r, g, b)
    print(xy)
    bridge.set_light(light, 'xy', converter.get_random_xy_color())

    #bridge.set_light(light, "saturation", hsv[1])

    # "{'r': '"+ str(avg_color[0]) +"', 'g': '"+ str(avg_color[1]) +"', 'b': '"+ str(avg_color[2]) + "'}"

    cv2.imshow("screenshot", frame)
    if cv2.waitKey(1) == ord("q"):
        break

# make sure everything is closed when exited
cv2.destroyAllWindows()
out.release()




