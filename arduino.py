# ********************************************************************************************************
#
# @Autor : Walter Christiann
# Date : 11 aout 2023 at 00:10
#
# ********************************************************************************************************

# import some libraries
import multiprocessing
import socket

import pyfirmata
import time
import subprocess


def run_django():
    path = "C:/Users/HP/PycharmProjects/ObjectDetection/venv/Scripts/python"
    subprocess.run([path, "manage.py", "runserver"])


if __name__ == '__main__':

    # queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_django)
    process.start()

    # arduino board initialisation
    board = pyfirmata.Arduino('COM10')

    # PINs setting

    # feux premier
    v1Pin = 2
    o1Pin = 3
    r1Pin = 4

    # feux deuxieme
    v2Pin = 5
    o2Pin = 6
    r2Pin = 7

    # feux troisieme
    v3Pin = 8
    o3Pin = 9
    r3Pin = 10

    # feux quatrieme
    v4Pin = 11
    o4Pin = 12
    r4Pin = 13

    # Timing Setup
    startTime1 = 0
    startTime2 = 0
    startTime3 = 0
    startTime4 = 0

    # light delay
    greenTime = 5000
    orangeTime = 2000
    redTime = greenTime + orangeTime
    # totalTime1 = greenTime + orangeTime + redTime
    # totalTime2 = totalTime1 * 2

    # feu fondamental de la lecture des bronches
    stateFeu = [""] * 4  # doit etre de longueur 4 pour le 4 feu de circu

    # ENVOIE DES DONNEE EN UTILISANT LES Socket.io (CLIENT UDP)
    # cree une socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Associer le socket au port 8005 : pour l'ecoute
    s.bind(("localhost", 8005))



    # ferme la socket
    # s.close()


    # SOME FUCNTIONS

    def setLow(*args):
        # *args : tuple qui contient la liste de tout les params a metre a LOW

        for arg in args:
            # boucle pour parcourir les parametres inconnu
            board.digital[arg].write(0)


    def setPinsModeOUT(*args):
        # *args : tuple qui contient la liste de tout les params a metre a le pin mode

        for arg in args:
            # boucle pour parcourir les parametres inconnu
            board.digital[arg].mode = pyfirmata.OUTPUT


    def setPinsModeIN(*args):
        # *args : tuple qui contient la liste de tout les params a metre a le pin mode

        for arg in args:
            # boucle pour parcourir les parametres inconnu
            board.digital[arg].mode = pyfirmata.INPUT


    # fonction qui get l'etat actuel du feu
    def getStateFeux():
        # read the actual state of all pins with digitalRead()
        stateR1 = board.digital[r1Pin].read()
        stateO1 = board.digital[o1Pin].read()
        stateV1 = board.digital[v1Pin].read()

        stateR2 = board.digital[r2Pin].read()
        stateO2 = board.digital[o2Pin].read()
        stateV2 = board.digital[v2Pin].read()

        stateR3 = board.digital[r3Pin].read()
        stateO3 = board.digital[o3Pin].read()
        stateV3 = board.digital[v3Pin].read()

        stateR4 = board.digital[r4Pin].read()
        stateO4 = board.digital[o4Pin].read()
        stateV4 = board.digital[v4Pin].read()

        feu1State = [stateR1, stateO1, stateV1]
        feu2State = [stateR2, stateO2, stateV2]
        feu3State = [stateR3, stateO3, stateV3]
        feu4State = [stateR4, stateO4, stateV4]
        color = ['R', 'Y', 'V']

        for i in range(0, 3, 1):

            if feu1State[i] == 1:
                stateFeu[0] = color[i]

            if feu2State[i] == 1:
                stateFeu[1] = color[i]

            if feu3State[i] == 1:
                stateFeu[2] = color[i]

            if feu4State[i] == 1:
                stateFeu[3] = color[i]


    def setup():
        # put your setup code here, to run once:
        # Serial.begin(9600) important seulement dans arduino

        # Settings Pins Mode as OUTPUT
        setPinsModeOUT(v1Pin, o1Pin, r1Pin, v2Pin, o2Pin, r2Pin, v3Pin, o3Pin, r3Pin, v4Pin, o4Pin, r4Pin)

        # initialise all pin as LOW => Eteint Only Red Light => HIGH
        setLow(v1Pin, o1Pin, r1Pin, v2Pin, o2Pin, r2Pin, v3Pin, o3Pin, r3Pin, v4Pin, o4Pin, r4Pin)
        board.digital[r1Pin].write(1)
        board.digital[r2Pin].write(1)
        board.digital[r3Pin].write(1)
        board.digital[r4Pin].write(1)


    setup()


    def loop():
        # put your main code here, to run repeatedly:
        global startTime1, startTime3, startTime2, startTime4

        since = int(time.time() * 1000)

        while True:

            currentTime = int(time.time() * 1000) - since

            # get Fire state at any sec
            getStateFeux()
            # print(stateFeu)

            # envoie des donnees au serveur
            # socket n'accepte que les donnees de type byte
            stateFeu_to_str = ",".join(stateFeu)  # on aura un truc du genre stateFeu_to_str = "X, X, X, X"
            stateFeu_to_byte = str(stateFeu_to_str).encode("utf-8")  # on aura stateFeu_to_byte = b"X, X, X, X"

            #on envoi la donnee au port 8001
            s.sendto(stateFeu_to_byte, ("localhost", 8001))
            # on envoi la donnee au port 8002
            s.sendto(stateFeu_to_byte, ("localhost", 8002))
            # on envoi la donnee au port 8003
            s.sendto(stateFeu_to_byte, ("localhost", 8003))
            # on envoi la donnee au port 8004
            s.sendto(stateFeu_to_byte, ("localhost", 8004))

            # voie 1
            if currentTime - startTime1 < greenTime:
                board.digital[v1Pin].write(1)
                setLow(o1Pin, r1Pin)

            elif currentTime - startTime1 < greenTime + orangeTime:
                board.digital[o1Pin].write(1)
                setLow(v1Pin, r1Pin)

            elif currentTime - startTime1 < greenTime + orangeTime + redTime:
                board.digital[r1Pin].write(1)
                setLow(v1Pin, o1Pin)
            else:
                startTime1 = currentTime

            # voie 3
            if currentTime - startTime3 < greenTime:
                board.digital[v3Pin].write(1)
                setLow(o3Pin, r3Pin)

            elif currentTime - startTime3 < greenTime + orangeTime:
                board.digital[o3Pin].write(1)
                setLow(v3Pin, r3Pin)
            elif currentTime - startTime3 < greenTime + orangeTime + redTime:
                board.digital[r3Pin].write(1)
                setLow(v3Pin, o3Pin)
            else:
                startTime3 = currentTime

            # voie 2
            # apres seulement 4 secondes on commence ce cycle
            if currentTime > greenTime + orangeTime:

                if currentTime - startTime2 < greenTime + (greenTime + orangeTime):
                    board.digital[v2Pin].write(1)
                    setLow(o2Pin, r2Pin)

                elif currentTime - startTime2 < greenTime + orangeTime + (greenTime + orangeTime):
                    board.digital[o2Pin].write(1)
                    setLow(v2Pin, r2Pin)

                elif currentTime - startTime2 < greenTime + orangeTime + redTime + (greenTime + orangeTime):
                    board.digital[r2Pin].write(1)
                    setLow(v2Pin, o2Pin)

                else:
                    board.sp.write(b'2 Reset Time')
                    startTime2 = currentTime - (greenTime + orangeTime)

            # voie 4
            # apres seulement 4 seconde on commence ce cycle
            if currentTime > greenTime + orangeTime:

                if currentTime - startTime4 < greenTime + (greenTime + orangeTime):
                    board.digital[v4Pin].write(1)
                    setLow(o4Pin, r4Pin)

                elif currentTime - startTime4 < greenTime + orangeTime + (greenTime + orangeTime):
                    board.digital[o4Pin].write(1)
                    setLow(v4Pin, r4Pin)

                elif currentTime - startTime4 < greenTime + orangeTime + redTime + (greenTime + orangeTime):
                    board.digital[r4Pin].write(1)
                    setLow(v4Pin, o4Pin)

                else:
                    board.sp.write(b'4 Reset Time')
                    startTime4 = currentTime - (greenTime + orangeTime)


    loop()
