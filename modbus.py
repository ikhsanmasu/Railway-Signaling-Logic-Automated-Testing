from pyModbusTCP.client import ModbusClient
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from time import time

ts = time()

ipDefault = "10.10.3.106"
c = ModbusClient(host=ipDefault, port=502, auto_open=True, debug=False)

class hima(QObject):
    def __init__(self):
        super(hima, self).__init__()
        self.start = 0
        # [Name, Data type, Global Variable, Size [Bit], Byte.Bit, Register.Bit, Bit, Value, Timer]
        self.dataVDUctrl = []
        self.startVDUctrl = 28
        self.dataFieldctrl = []
        self.startFieldctrl = 37
        self.dataFieldInd = []
        self.startFieldInd = 250
        self.dictDatafield = {}
        self.internalField = {}
        self.signalVar = []
        self.engkolAll = 0

        self.weselTstamp = time()

    def run(self):
        while True:
            # PB Simulation
            if self.start and self.dataVDUctrl:
                # Timer Off PB for 2 second and 0
                writeData = [int([''.join([str(self.dataVDUctrl[x + z][3]) for z in range(15, -1, -1)])][0], 2) for x in
                             range(0, len(self.dataVDUctrl), 16)]
                is_ok = c.write_multiple_registers(self.startVDUctrl, writeData)

                # Generate Flip Flop for VDU 2 Connection
                for x, d in enumerate(self.dataVDUctrl):
                    if d[3] == 1 and time() - d[4] > 2 and d[2] != 'VDU-ALIVE-IN':
                        self.dataVDUctrl[x][3] = 0
                        self.dataVDUctrl[x][4] = 0

                    if d[2] == 'VDU-ALIVE-IN' and time() - d[4] > 2:
                        if d[3]:
                            self.dataVDUctrl[x][3] = 0
                        else:
                            self.dataVDUctrl[x][3] = 1
                        self.dataVDUctrl[x][4] = time()

            # write field data
            if self.start and self.dataFieldctrl:
                writeData = [int([''.join([str(self.dataFieldctrl[x + z][1]) for z in range(15, -1, -1)])][0], 2) for x in
                             range(0, len(self.dataFieldctrl), 16)]
                is_ok = c.write_multiple_registers(self.startFieldctrl, writeData)

            # read field data
            if self.start and self.dataFieldInd:
                readData = []
                regNb = 0
                for index in range(0, int(len(self.dataFieldInd)/16), 125):
                    if int(len(self.dataFieldInd)/16) - index >= 125:
                        regNb = 125
                    else:
                        regNb = int(len(self.dataFieldInd)/16) - index
                    readData += c.read_holding_registers(self.startFieldInd + index, regNb)

                # convert read data to sorted list for var
                readData1 = [bin(x)[2:] for x in readData]
                readData2 = [list(reversed(['0' for z in range(16 - len(x))] + list(x))) for x in readData1]
                readData3 = sum(readData2, [])

                for i, x in enumerate(readData3):
                    self.dataFieldInd[i][1] = x

                for i, d in enumerate(self.dataFieldInd):
                    self.dictDatafield[d[0]] = int(d[1])

            # signal simulation
            if self.start == 1:
                for i, x in enumerate(self.dataFieldctrl):
                    if '-EKR-DI' in x[0]:
                        S = x[0].replace('-EKR-DI', '')
                        self.dataFieldctrl[i][1] = int(self.i(S + '-EKR'))

                    if '-ECR-DI' in x[0]:
                        S = x[0].replace('-ECR-DI', '')

                        if S + '-HR-DO' in self.signalVar and S + '-DR-DO' in self.signalVar and S + '-GR-DO' not in self.signalVar:
                            self.dataFieldctrl[i][1] = int((self.i(S + '-ECR-R') and not self.v(S + '-HR-DO')) or (
                                        self.i(S + '-ECR-Y') and self.v(S + '-HR-DO')) or (self.i(
                                S + '-ECR-G') and self.v(S + '-HR-DO') and self.v(S + '-DR-DO')))
                        if S + '-HR-DO' in self.signalVar and S + '-DR-DO' in self.signalVar and S + '-GR-DO' in self.signalVar:
                            self.dataFieldctrl[i][1] = int(((self.i(S + '-ECR-R') and not self.v(S + '-HR-DO')) or (
                                        self.i(S + '-ECR-Y') and self.v(S + '-HR-DO')) or (self.i(
                                S + '-ECR-G') and self.v(S + '-HR-DO') and self.v(S + '-DR-DO')) and not self.v(S + '-GR-DO')))

                        if S + '-HR-DO' in self.signalVar and S + '-DR-DO' not in self.signalVar and S + '-GR-DO' not in self.signalVar:
                            self.dataFieldctrl[i][1] = int((self.i(S + '-ECR-R') and not self.v(S + '-HR-DO')) or (
                                        self.i(S + '-ECR-Y') and self.v(S + '-HR-DO')))
                        if S + '-HR-DO' in self.signalVar and S + '-DR-DO' not in self.signalVar and S + '-GR-DO' in self.signalVar:
                            self.dataFieldctrl[i][1] = int(((self.i(S + '-ECR-R') and not self.v(S + '-HR-DO')) or (
                                        self.i(S + '-ECR-Y') and self.v(S + '-HR-DO'))) and not self.v(S + '-GR-DO'))

                        if S + '-HR-DO' not in self.signalVar and S + '-DR-DO' in self.signalVar and S + '-GR-DO' not in self.signalVar:
                            self.dataFieldctrl[i][1] = int((self.i(S + '-ECR-R') and not self.v(S + '-DR-DO')) or (
                                        self.i(S + '-ECR-G') and self.v(S + '-DR-DO')))
                        if S + '-HR-DO' not in self.signalVar and S + '-DR-DO' in self.signalVar and S + '-GR-DO' in self.signalVar:
                            self.dataFieldctrl[i][1] = int(((self.i(S + '-ECR-R') and not self.v(S + '-DR-DO')) or (
                                        self.i(S + '-ECR-G') and self.v(S + '-DR-DO'))) and not self.v(S + '-GR-DO'))

                        if S + '-HR-DO' not in self.signalVar and S + '-DR-DO' not in self.signalVar and not S + '-GR-DO' in self.signalVar and S[0] == 'J':
                            self.dataFieldctrl[i][1] = int(self.i(S + '-ECR-R'))

                    if '-HR-DI' in x[0]:
                        S = x[0].replace('-HR-DI', '')
                        self.dataFieldctrl[i][1] = int(self.v(S + '-HR-DO'))
                    if '-DR-DI' in x[0]:
                        S = x[0].replace('-DR-DI', '')
                        self.dataFieldctrl[i][1] = int(self.v(S + '-DR-DO'))
                    if '-ER-DI' in x[0]:
                        S = x[0].replace('-ER-DI', '')
                        self.dataFieldctrl[i][1] = int(self.v(S + '-ER-DO'))
                    if '-SECR-DI' in x[0]:
                        S = x[0].replace('-SECR-DI', '')
                        self.dataFieldctrl[i][1] = int(self.i(S + '-SECR'))
                    if '-GR-DI' in x[0]:
                        S = x[0].replace('-GR-DI', '')
                        self.dataFieldctrl[i][1] = int(self.v(S + '-GR-DO'))

            # wesel simulation
            if self.start == 1:
                # if self.start == 1 and (time() - self.weselTstamp > 3):
                for i, x in enumerate(self.dataFieldctrl):
                    if '-NWP-DI' in x[0]:
                        # print(self.dictDatafield)
                        W = x[0].replace('-NWP-DI', '')
                        W_NWR = self.v(W + '-NWR-DO') and not self.v(W + '-RWR-DO') and self.v(W + '-WLPR-DO')
                        self.dataFieldctrl[i][1] = int(((W_NWR and not self.i(W + '-NOB')) or self.i(W + '-SNP') or self.dataFieldctrl[i][1]) and
                                                       (not self.i(W + '-SRP') or (
                                                                   self.i(W + '-SNP') and self.i(W + '-SRP'))) and
                                                       not self.i(W + '-TRL') and not self.v(W + '-RWR-DO'))


                    elif '-RWP-DI' in x[0]:
                        W = x[0].replace('-RWP-DI', '')
                        W_RWR = self.v(W + '-RWR-DO') and not self.v(W + '-NWR-DO') and self.v(W + '-WLPR-DO')
                        self.dataFieldctrl[i][1] = int(((W_RWR and not self.i(W + '-ROB')) or self.i(W + '-SRP') or self.dataFieldctrl[i][1]) and
                                                       (not self.i(W + '-SNP') or (
                                                                   self.i(W + '-SNP') and self.i(W + '-SRP'))) and
                                                       not self.i(W + '-TRL') and not self.v(W + '-NWR-DO'))
                # self.weselTstamp = time()

    def startRun(self, ip, dataVDUctrl, startVDUctrl, dataS):
        c.host = ip

        self.dataVDUctrl = dataVDUctrl
        self.startVDUctrl = int(startVDUctrl)
        self.dataFieldctrl = dataS[0]
        self.startFieldctrl = dataS[1]
        self.dataFieldInd = dataS[2]
        self.startFieldInd = dataS[3]

        self.signalVar = ' '.join([x[0] for x in self.dataFieldInd])

        for i, d in enumerate(dataS[4]):
            self.internalField[d[0]] = int(d[1])

        for i, d in enumerate(self.dataFieldInd):
            self.dictDatafield[d[0]] = 0
        self.start = 1

    def stopRun(self):
        self.start = 0

    # write pushbutton for VDU like
    def writePBVDU(self, pb1, pb2=''):
        for x, d in enumerate(self.dataVDUctrl):
            if d[2] == pb1 or d[2] == pb2:
                self.dataVDUctrl[x][3] = 1
                self.dataVDUctrl[x][4] = time()

    # write field
    def writeField(self, variable, value):
        for index, data in enumerate(self.dataFieldctrl):
            if variable == data[0]:
                self.dataFieldctrl[index][1] = value

    # write internal
    def writeInternal(self, variable, value):
        self.internalField[variable] = value

    # read data modbus from SIM
    def readVariable(self, var):
        return self.dictDatafield[var]

    # get value from modbus from SIM
    def v(self, var):
        return self.dictDatafield[var]

    # get value internal variable
    def i(self, var):
        return self.internalField[var]

