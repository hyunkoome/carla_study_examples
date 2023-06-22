# import glob
# import os
# import sys
import random
# from turtle import width
import carla
# from matplotlib import image
# import tensorflow as tf
import cv2
import numpy as np


# import time
# import argparse
# import imutils

def camera_callback(image, data, save_dir):
    data['image'] = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4))
    image.save_to_disk(f"{save_dir}/{image.frame}.png")


def camera_callback2(image, data, save_dir):
    capture = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4))
    data['image'] = capture
    cv2.imwrite(f"{save_dir}/{image.frame}.png", capture)


def main():
    save_dir = '/home/hyunkoo/DATA/Study_Carla/SaveCarla/images'
    print("")
    # Laden von Carla,Library,Map, erstellen des Spectators
    client = carla.Client('localhost', 2000)
    client.set_timeout(500.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spectator = world.get_spectator()
    bp_lib = world.get_blueprint_library()
    spawn_points = world.get_map().get_spawn_points()

    # Laden von Carla,Library,Map, erstellen des Spectators
    client = carla.Client('localhost', 2000)
    client.set_timeout(500.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawnpoints = world.get_map().get_spawn_points()
    spectator = world.get_spectator()

    # Nun Einstellungen zum Fahrzeug
    vehicle_blueprint = blueprint_library.find('vehicle.audi.etron')
    # Fahrzeug wird an einem zufälligen Spawnpunkt gespawnt
    vehicle = world.try_spawn_actor(vehicle_blueprint, random.choice(spawnpoints))
    transform = carla.Transform(vehicle.get_transform().transform(carla.Location(x=2, z=0.5)),
                                vehicle.get_transform().rotation)
    spectator.set_transform(transform)

    # Kamera
    camera_blueprint = blueprint_library.find('sensor.camera.rgb')
    camera_transform = carla.Transform(carla.Location(z=2, x=0.5))
    camera = world.spawn_actor(camera_blueprint, camera_transform, attach_to=vehicle)

    image_width = camera_blueprint.get_attribute("image_size_x").as_int()
    image_height = camera_blueprint.get_attribute("image_size_y").as_int()
    camera_data = {'image': np.zeros((image_height, image_width, 4))}

    camera.listen(lambda image: camera_callback(image, camera_data, save_dir))

    # Anzeigen des Bildes
    while True:
        cv2.namedWindow('Camera', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Camera', camera_data['image'])
        vehicle.set_autopilot(True)
        # cv2.waitKey(1)

        if cv2.waitKey(1) == ord('q'):
            client.reload_world()
            break
    # while True:
    #     img = cv2.imshow('Camera', camera_data['image'])
    #     vehicle.set_autopilot(True)
    #     camera.listen(lambda image: image.save_to_disk(r"/home/hyun/DATA/Codes/CARLA_0.9.14/PythonAPI/carla_hyunkoo_examples/images",
    #                                                    color_converter=None))
    #
    #     if cv2.waitKey(1) == ord('p'):
    #         client.reload_world()
    #         break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
