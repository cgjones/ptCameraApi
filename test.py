# Pan/Tilt Camera API Test
# Chris Jones

from ptCameraApi import ptCameraApi as pt
import time

pt.clear_onboard_pictures()

pt.move_camera(-90,0)
time.sleep(3)

for i in range (-90, 90, 10):
        pt.move_camera(i,0)
        print(pt.get_last_commanded_pos())
        pt.set_light(255)
        time.sleep(1)
        filename = pt.take_picture()
        pt.transfer_picture(filename, "./scratch/")
        pt.set_light(0)
        time.sleep(1)
