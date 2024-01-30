import socket
import os
import shutil
from select import select

import cv2
import cvzone


class VideoCamera(object):
    nbOfInter = 0

    def __init__(self, cam_id=0):
        self.video = cv2.VideoCapture(cam_id)
        VideoCamera.nbOfInter += 1

    def __del__(self):
        # when we release the frame, delete also all photo related
        self.video.release()
        path = os.path.join(os.getcwd(), 'static', 'road_image')
        if os.path.exists(path):
            shutil.rmtree(path)  # the shutil.rmtree() function recursively removes the directory and all of its content

    def get_state_feu(self, id):

        # Send to every road it's state properly
        if id == 0:
            data = ['Y', 'Y', 'Y', 'Y']
            # Recptions des Donnees (SERVEUR UDP)
            # cree une socket UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # lie la socket au port 8001 port d'ecoute
            s.bind(("localhost", 8001))
            s.setblocking(False)

            # Reception de l'etat de feu de circulation depuis Arduino
            ready_to_read, _, _ = select([s], [], [],
                                         0.1)  # verifi si un message est dispo dans le socket avant de recevoir le smg

            if ready_to_read:
                data, address = s.recvfrom(1024)  # format des donnees data = b'R,R,R,R'
                data = data.decode()  # data = 'R,R,R,R'
                data = data.split(",")  # data = ['R', 'R', 'R', 'R']

            return data[id]
        if id == 1:
            data = ['Y', 'Y', 'Y', 'Y']
            # Recptions des Donnees (SERVEUR UDP)
            # cree une socket UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # lie la socket au port 8002 port d'ecoute
            s.bind(("localhost", 8002))
            s.setblocking(False)

            # Reception de l'etat de feu de circulation depuis Arduino
            ready_to_read, _, _ = select([s], [], [],
                                         0.1)  # verifi si un message est dispo dans le socket avant de recevoir le smg

            if ready_to_read:
                data, address = s.recvfrom(1024)  # format des donnees data = b'R,R,R,R'
                data = data.decode()  # data = 'R,R,R,R'
                data = data.split(",")  # data = ['R', 'R', 'R', 'R']

            return data[id]
        if id == 2:
            data = ['Y', 'Y', 'Y', 'Y']
            # Recptions des Donnees (SERVEUR UDP)
            # cree une socket UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # lie la socket au port 8003 port d'ecoute
            s.bind(("localhost", 8003))
            s.setblocking(False)

            # Reception de l'etat de feu de circulation depuis Arduino
            ready_to_read, _, _ = select([s], [], [],
                                         0.1)  # verifi si un message est dispo dans le socket avant de recevoir le smg

            if ready_to_read:
                data, address = s.recvfrom(1024)  # format des donnees data = b'R,R,R,R'
                data = data.decode()  # data = 'R,R,R,R'
                data = data.split(",")  # data = ['R', 'R', 'R', 'R']

            return data[id]
        if id == 3:
            data = ['Y', 'Y', 'Y', 'Y']
            # Recptions des Donnees (SERVEUR UDP)
            # cree une socket UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # lie la socket au port 8004 port d'ecoute
            s.bind(("localhost", 8004))
            s.setblocking(False)

            # Reception de l'etat de feu de circulation depuis Arduino
            ready_to_read, _, _ = select([s], [], [],
                                         0.1)  # verifi si un message est dispo dans le socket avant de recevoir le smg

            if ready_to_read:
                data, address = s.recvfrom(1024)  # format des donnees data = b'R,R,R,R'
                data = data.decode()  # data = 'R,R,R,R'
                data = data.split(",")  # data = ['R', 'R', 'R', 'R']

            return data[id]

    def get_frame(self):

        success, frame = self.video.read()

        return frame
