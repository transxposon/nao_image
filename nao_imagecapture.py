import os
import numpy as np
from PIL import Image
import sys
sys.path.append('/Users/princess/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231/lib/python2.7/site-packages')
from naoqi import ALProxy


def image_capture_nao(NAO_IP, PORT, output_dir=None, resolution=(320, 240)):

    """
    Capture images from Nao's TOP CAM and save them to a specified directory.

    Args:
        NAO_IP (str): IP address of the Nao robot.
        PORT (int): Port number for the connection.
        output_dir (str): Directory where images will be saved. Defaults to the current working directory.
        resolution (tuple, opt): Resolution of the captured image as (width, height). Defaults 320,240

    Returns:
        None
    """

    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "nao_photos")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    SubID = "NAO"

    try:
        videoDevice_nao = ALProxy('ALVideoDevice', NAO_IP, PORT)
    except Exception as e:
        print "Error connecting to Nao robot:", e
        return

    AL_kTopCamera, Frame_Rates = 0, 5  # Top camera, 5 FPS
    AL_kBGRColorSpace = 13
    resolution_map = {(160, 120): 0, (320, 240): 1, (640, 480): 2}

    if resolution not in resolution_map:
        print "Unsupported resolution {}. Supported resolutions: {}".format(
            resolution, list(resolution_map.keys())
        )
        return

    captureDevice_nao = videoDevice_nao.subscribeCamera(
        SubID, AL_kTopCamera, resolution_map[resolution], AL_kBGRColorSpace, Frame_Rates
    )

    width, height = resolution
    image = np.zeros((height, width, 3), np.uint8)

    try:
        result = videoDevice_nao.getImageRemote(captureDevice_nao)

        if result is None:
            print "Camera problem."
            return
        elif result[6] is None:
            print "No image captured."
            return

        # img to array
        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3

        # sequential image naming
        existing_files = [
            f for f in os.listdir(output_dir) if f.startswith("image") and f.endswith(".png")
        ]
        if existing_files:
            existing_files.sort()
            last_number = int(existing_files[-1][5:10])
            next_number = last_number + 1
        else:
            next_number = 1
        image_name = "image{:05d}.png".format(next_number)

        # save
        image_path = os.path.join(output_dir, image_name)
        img = Image.fromarray(image)
        img.save(image_path)
        print "Image saved at:", image_path

    finally:
        # unsubscribe from the camera
        videoDevice_nao.unsubscribe(captureDevice_nao)


if __name__ == "__main__":


    NAO_IP = "192.168.0.131"
    PORT = 9559

    image_capture_nao(NAO_IP, PORT)
