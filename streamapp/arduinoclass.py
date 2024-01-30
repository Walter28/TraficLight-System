import pyfirmata
import time


class Arduino(object):
    def __new__(cls, port='COM10'):
        obj = super().__new__(cls)
        obj.port = port
        obj.board = pyfirmata.Arduino(port)
        obj.v1Pin = 2
        obj.o1Pin = 3
        obj.r1Pin = 4
        obj.v2Pin = 5
        obj.o2Pin = 6
        obj.r2Pin = 7
        obj.v3Pin = 8
        obj.o3Pin = 9
        obj.r3Pin = 10
        obj.v4Pin = 11
        obj.o4Pin = 12
        obj.r4Pin = 13
        obj.startTime1 = 0
        obj.startTime2 = 0
        obj.startTime3 = 0
        obj.startTime4 = 0
        obj.greenTime = 5000
        obj.orangeTime = 2000
        obj.redTime = obj.greenTime + obj.orangeTime
        obj.stateFeu = [""] * 4

        obj.setup()
        obj.loop()
        return obj

    # def __init__(self, port='COM10'):


    def setLow(self, *args):
        # *args : tuple qui contient la liste de tout les params a metre a LOW
        for arg in args:
            # boucle pour parcourir les parametres inconnu
            self.board.digital[arg].write(0)

    def setPinsModeOUT(self, *args):
        # *args : tuple qui contient la liste de tout les params a metre a le pin mode
        for arg in args:
            # boucle pour parcourir les parametres inconnu
            self.board.digital[arg].mode = pyfirmata.OUTPUT

    def setPinsModeIN(self, *args):
        # *args : tuple qui contient la liste de tout les params a metre a le pin mode
        for arg in args:
            # boucle pour parcourir les parametres inconnu
            self.board.digital[arg].mode = pyfirmata.INPUT

    def getStateFeux(self):
        # read the actual state of all pins with digitalRead()
        stateR1 = self.board.digital[self.r1Pin].read()
        stateO1 = self.board.digital[self.o1Pin].read()
        stateV1 = self.board.digital[self.v1Pin].read()

        stateR2 = self.board.digital[self.r2Pin].read()
        stateO2 = self.board.digital[self.o2Pin].read()
        stateV2 = self.board.digital[self.v2Pin].read()

        stateR3 = self.board.digital[self.r3Pin].read()
        stateO3 = self.board.digital[self.o3Pin].read()
        stateV3 = self.board.digital[self.v3Pin].read()

        stateR4 = self.board.digital[self.r4Pin].read()
        stateO4 = self.board.digital[self.o4Pin].read()
        stateV4 = self.board.digital[self.v4Pin].read()

        feu1State = [stateR1, stateO1, stateV1]
        feu2State = [stateR2, stateO2, stateV2]
        feu3State = [stateR3, stateO3, stateV3]
        feu4State = [stateR4, stateO4, stateV4]
        color = ['R', 'O', 'V']

        for i in range(0, 3, 1):

            if feu1State[i] == 1:
                self.stateFeu[0] = color[i]

            if feu2State[i] == 1:
                self.stateFeu[1] = color[i]

            if feu3State[i] == 1:
                self.stateFeu[2] = color[i]

            if feu4State[i] == 1:
                self.stateFeu[3] = color[i]


    def setup(self):
        # put your setup code here, to run once:
        # Serial.begin(9600) important seulement dans arduino

        # Settings Pins Mode as OUTPUT
        self.setPinsModeOUT(self.v1Pin, self.o1Pin, self.r1Pin, self.v2Pin, self.o2Pin,
                            self.r2Pin, self.v3Pin, self.o3Pin, self.r3Pin, self.v4Pin, self.o4Pin, self.r4Pin)

        # initialise all pin as LOW => Eteint Only Red Light => HIGH
        self.setLow(self.v1Pin, self.o1Pin, self.r1Pin, self.v2Pin, self.o2Pin, self.r2Pin,
                    self.v3Pin, self.o3Pin, self.r3Pin, self.v4Pin, self.o4Pin, self.r4Pin)
        self.board.digital[self.r1Pin].write(1)
        self.board.digital[self.r2Pin].write(1)
        self.board.digital[self.r3Pin].write(1)
        self.board.digital[self.r4Pin].write(1)


    def loop(self):
        # put your main code here, to run repeatedly:

        since = int(time.time() * 1000)

        while True:

            currentTime = int(time.time() * 1000) - since

            # get Fire state at any sec
            self.getStateFeux()
            # print(stateFeu)

            # voie 1
            if currentTime - self.startTime1 < self.greenTime:
                self.board.digital[self.v1Pin].write(1)
                self.setLow(self.o1Pin, self.r1Pin)

            elif currentTime - self.startTime1 < self.greenTime + self.orangeTime:
                self.board.digital[self.o1Pin].write(1)
                self.setLow(self.v1Pin, self.r1Pin)

            elif currentTime - self.startTime1 < self.greenTime + self.orangeTime + self.redTime:
                self.board.digital[self.r1Pin].write(1)
                self.setLow(self.v1Pin, self.o1Pin)
            else:
                self.startTime1 = currentTime

            # voie 3
            if currentTime - self.startTime3 < self.greenTime:
                self.board.digital[self.v3Pin].write(1)
                self.setLow(self.o3Pin, self.r3Pin)

            elif currentTime - self.startTime3 < self.greenTime + self.orangeTime:
                self.board.digital[self.o3Pin].write(1)
                self.setLow(self.v3Pin, self.r3Pin)
            elif currentTime - self.startTime3 < self.greenTime + self.orangeTime + self.redTime:
                self.board.digital[self.r3Pin].write(1)
                self.setLow(self.v3Pin, self.o3Pin)
            else:
                self.startTime3 = currentTime

            # voie 2
            # apres seulement 4 secondes on commence ce cycle
            if currentTime > self.greenTime + self.orangeTime:

                if currentTime - self.startTime2 < self.greenTime + (self.greenTime + self.orangeTime):
                    self.board.digital[self.v2Pin].write(1)
                    self.setLow(self.o2Pin, self.r2Pin)

                elif currentTime - self.startTime2 < self.greenTime + self.orangeTime + (self.greenTime + self.orangeTime):
                    self.board.digital[self.o2Pin].write(1)
                    self.setLow(self.v2Pin, self.r2Pin)

                elif currentTime - self.startTime2 < self.greenTime + self.orangeTime + self.redTime + (self.greenTime + self.orangeTime):
                    self.board.digital[self.r2Pin].write(1)
                    self.setLow(self.v2Pin, self.o2Pin)

                else:
                    self.board.sp.write(b'2 Reset Time')
                    self.startTime2 = currentTime - (self.greenTime + self.orangeTime)

            # voie 4
            # apres seulement 4 seconde on commence ce cycle
            if currentTime > self.greenTime + self.orangeTime:

                if currentTime - self.startTime4 < self.greenTime + (self.greenTime + self.orangeTime):
                    self.board.digital[self.v4Pin].write(1)
                    self.setLow(self.o4Pin, self.r4Pin)

                elif currentTime - self.startTime4 < self.greenTime + self.orangeTime + (self.greenTime + self.orangeTime):
                    self.board.digital[self.o4Pin].write(1)
                    self.setLow(self.v4Pin, self.r4Pin)

                elif currentTime - self.startTime4 < self.greenTime + self.orangeTime + self.redTime + (self.greenTime + self.orangeTime):
                    self.board.digital[self.r4Pin].write(1)
                    self.setLow(self.v4Pin, self.o4Pin)

                else:
                    self.board.sp.write(b'4 Reset Time')
                    self.startTime4 = currentTime - (self.greenTime + self.orangeTime)


# ardu = Arduino()