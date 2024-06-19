from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from time import sleep, time
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QFileDialog, QDialog
import pandas as pd
import openpyxl


class testingBot(QObject):
    def __init__(self,  modbus):
        super(testingBot, self).__init__()
        self.start = 0
        self.modbus = modbus
        self.testMode = [0, 0, 0, 0, 0]
        self.FTTest = 0
        self.ITTest = 0
        self.CRTest = 0
        self.VTTest = 0
        self.DTTest = 0
        self.IT1 = []
        self.IT2 = []

        self.PM = []
        self.TRACK = []
        self.ruteCTRL = []
        self.ruteE = []
        self.inputData = []
        self.outputData = []
        self.internalData = []

        self.stopTest = 0
        self.startRoute = 0
        self.finishRoute = 0
        self.startRoute2 = 0
        self.finishRoute2 = 0

    def run(self):
        while True:
            if self.start:
                # TPR bantu dan TWT all Wesel
                if self.modbus.readVariable("TPR-BANTU-PBE-F") or self.modbus.readVariable("TPR-BANTU-PBE-DO"):
                    self.modbus.writePBVDU('TPR-BANTU-PB-DI')
                    while self.modbus.readVariable("TPR-BANTU-PBE-F") or self.modbus.readVariable("TPR-BANTU-PBE-DO"):
                        sleep(1)

                for w in self.PM:
                    if w[0][0] != 'D' and self.modbus.readVariable(w[0] + '-OOC'):
                        self.modbus.writeInternal(w[0] + '-SNP', 1)
                        sleep(0.2)
                        self.modbus.writePBVDU('TWT-PB-DI', w[0] + '-PB-DI')
                        while self.modbus.readVariable(w[0] + '-OOC'):
                            sleep(0.5)
                        self.modbus.writeInternal(w[0] + '-SNP', 0)
                sleep(1)

                # clearkan semua track sebelum pengetesan
                for track in self.TRACK:
                    if not self.modbus.readVariable(track[0] + '-TP'):
                        self.modbus.writeField(track[0] + '-TPR-DI', 1)
                        sleep(1)

                if self.FTTest:
                    pass

                ##################################### Interlocking Table Test ##########################################
                if self.ITTest:
                    # clearkan semua track sebelum pengetesan
                    for track in self.TRACK:
                        if not self.modbus.readVariable(track[0] + '-TP'):
                            self.modbus.writeField(track[0] + '-TPR-DI', 1)
                            sleep(0.2)

                    count = 0
                    errorLog = []
                    simp = lambda a: a.replace('J', '').replace('JL', '').replace('L', '')
                    for data in self.IT1[self.startRoute:self.finishRoute]:
                        print('Testing Interlocking table rute :' + data[0] + ' => ' + data[1].upper())
                        error = ''
                        sleep(2)
                        # jika ada deraileur yang harus rebah -> turunkan deraileur
                        if '-R' in data[19]:
                            for deraileur in data[19].split():
                                if '-R' in deraileur and 'D' in deraileur[0]:
                                    self.modbus.writePBVDU('TBKWM-PB-DI', deraileur.replace('-R', '') + '-PB-DI')
                                    sleep(3)
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 0)
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 1)
                                    sleep(1)

                        ###################################cek syarat wesel############################################
                        dataLuncuran = []
                        if '(T)' in data[1].upper():
                            for x in self.IT2:
                                if x[1].replace(' ', '') == data[1].upper().replace(' ', ''):
                                    dataLuncuran = x

                        # if '(T)' not in data[1].upper():
                        #     syaratWesel = list(filter(None, (data[18].split(" "))))
                        #     for w in syaratWesel:
                        #         sleep(0.2)
                        #         # arahkan wesel sesuai syarat wesel
                        #         if not self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKW-PB-DI")
                        #             while not self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(0.2)
                        #         # kancing wesel yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKGW-PB-DI")
                        #         while not self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(0.2)
                        #         # cek apakah -B jatuh
                        #         if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                        #             if '-N' in w:
                        #                 error += ', ' + w.replace('N', 'R') + ' seharusnya tidak menjadi syarat -B'
                        #             else:
                        #                 error += ', ' + w.replace('R', 'N') + ' seharusnya tidak menjadi syarat -B'
                        #         # buka kancing wesel yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TBKW-PB-DI")
                        #         sleep(1)
                        #         while self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(1)
                        #     sleep(2)
                        #     if 'S' not in data[1].upper():
                        #         if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-L'):
                        #             error += ', ada wesel yang seharusnya tidak jadi syarat di -E-L'
                        #     else:
                        #         if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-L'):
                        #             error += ', ada wesel yang seharusnya tidak jadi syarat di -S-L'
                        #
                        #     for w in syaratWesel:
                        #         sleep(0.2)
                        #         # arahkan wesel sesuai syarat wesel
                        #         if self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKW-PB-DI")
                        #             while not self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(1)
                        #         # kancing wesel yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKGW-PB-DI")
                        #         while not self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(0.2)
                        #         # cek apakah -B jatuh
                        #         if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                        #             error += ', ' + w + ' seharusnya menjadi syarat -B'
                        #         # buka kancing wesel yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TBKW-PB-DI")
                        #         sleep(1)
                        #         while self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(0.5)
                        #         if 'S' not in data[1].upper():
                        #             if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-L'):
                        #                 error += ', wesel ' + w + ' belum menjadi syarat di -E-L'
                        #         else:
                        #             if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-L'):
                        #                 error += ', wesel ' + w + ' belum menjadi syarat di -S-L'
                        #         sleep(1)
                        #         if not self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKW-PB-DI")
                        #             while not self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(1)
                        #     sleep(2)
                        #     # Kancing semua wesel kecuali yang menjadi syarat
                        #     allWesel = []
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWesel):
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TKGW-PB-DI")
                        #             while not self.modbus.readVariable(w[0] + '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.1)
                        #     # cek apakah -B jatuh
                        #     if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                        #         error += ', ada wesel yang seharusnya tidak di jadikan syarat -B'
                        #     sleep(1)
                        #     # normalkan kancing
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWesel):
                        #             sleep(1)
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TBKW-PB-DI")
                        #             sleep(1)
                        #             while self.modbus.readVariable(w[0] + '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.2)
                        #     sleep(1)
                        #     # TKW wesel kearah sebaliknya
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWesel):
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TKW-PB-DI")
                        #             while self.modbus.readVariable(w[0] + '-WLPR-DO'):
                        #                 sleep(0.2)
                        #             sleep(0.2)
                        #     sleep(1)
                        #
                        #     if 'S' not in data[1].upper():
                        #         if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-L'):
                        #             error += ', ada wesel yang seharusnya tidak jadi syarat di -E-L'
                        #     else:
                        #         if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-L'):
                        #             error += ', ada wesel yang seharusnya tidak jadi syarat di -S-L'
                        #
                        #     # Kancing semua wesel kecuali yang menjadi syarat
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWesel):
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TKGW-PB-DI")
                        #             while not self.modbus.readVariable(w[0] + '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.1)
                        #     sleep(1)
                        #
                        #     # normalkan Kancing
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWesel):
                        #             sleep(1)
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TBKW-PB-DI")
                        #             sleep(1)
                        #             while self.modbus.readVariable(w[0]+ '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.2)
                        # elif '(T)' in data[1].upper() and dataLuncuran:
                        #     syaratWesel = list(filter(None, (data[18].split(" "))))
                        #     syaratWeselLuncuran = list(filter(None, (dataLuncuran[7].split(" "))))
                        #     # sesuaikan syarat wesel
                        #     sleep(2)
                        #     for w in syaratWesel:
                        #         if not self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKW-PB-DI")
                        #             sleep(0.2)
                        #             while not self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(0.5)
                        #     sleep(2)
                        #
                        #     for w in syaratWeselLuncuran:
                        #         # arahkan wesel sesuai syarat wesel luncuran
                        #         sleep(0.2)
                        #         if not self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKW-PB-DI")
                        #             sleep(0.5)
                        #             while not self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(0.5)
                        #
                        #         # kancing wesel luncuran yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKGW-PB-DI")
                        #         sleep(0.5)
                        #         while not self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(0.2)
                        #
                        #         # cek apakah -B jatuh
                        #         if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                        #             if '-N' in w:
                        #                 error += ', ' + w.replace('N', 'R') + ' seharusnya tidak menjadi syarat -P'
                        #             else:
                        #                 error += ', ' + w.replace('R', 'N') + ' seharusnya tidak menjadi syarat -P'
                        #
                        #         # buka kancing wesel luncuran yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI',
                        #                                "TBKW-PB-DI")
                        #         sleep(1)
                        #         while self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(1)
                        #
                        #     sleep(2)
                        #     if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-L'):
                        #         error += ', ada wesel yang seharusnya tidak jadi syarat di -T-L'
                        #     sleep(1)
                        #
                        #     for w in syaratWeselLuncuran:
                        #         sleep(0.2)
                        #         # arahkan wesel luncuran berlawanan syarat wesel
                        #         if self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI',
                        #                                    "TKW-PB-DI")
                        #             sleep(0.2)
                        #             while self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(1)
                        #
                        #         # kancing wesel yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI',
                        #                                "TKGW-PB-DI")
                        #         sleep(0.5)
                        #         while not self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(0.2)
                        #
                        #         # cek apakah -B jatuh
                        #         if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                        #             error += ', ' + w + ' seharusnya menjadi syarat -P'
                        #
                        #         # buka kancing wesel yang jadi syarat
                        #         self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TBKW-PB-DI")
                        #         sleep(1)
                        #         while self.modbus.readVariable('W' + w.replace("N", "").replace("R", "") + 'BLOCK'):
                        #             sleep(0.2)
                        #         sleep(0.5)
                        #
                        #         if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-L'):
                        #             error += ', wesel ' + w + ' belum menjadi syarat di -T-L'
                        #         sleep(1)
                        #
                        #         if not self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI',
                        #                                    "TKW-PB-DI")
                        #             while not self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(1)
                        #     sleep(2)
                        #
                        #     # Kancing semua wesel kecuali yang menjadi syarat
                        #     allWesel = []
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWeselLuncuran):
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TKGW-PB-DI")
                        #             while not self.modbus.readVariable(w[0] + '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.1)
                        #
                        #     # cek apakah -P jatuh
                        #     if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                        #         error += ', ada wesel yang seharusnya tidak di jadikan syarat -P'
                        #     sleep(1)
                        #     # normalkan kancing
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWeselLuncuran):
                        #             sleep(1)
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TBKW-PB-DI")
                        #             sleep(1)
                        #             while self.modbus.readVariable(w[0] + '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.2)
                        #     sleep(1)
                        #     # TKW wesel kearah sebaliknya
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWeselLuncuran):
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TKW-PB-DI")
                        #             sleep(0.2)
                        #             while self.modbus.readVariable(w[0] + '-WLPR-DO'):
                        #                 sleep(0.2)
                        #             sleep(0.2)
                        #     sleep(1)
                        #     # Kancing semua wesel kecuali yang menjadi syarat
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWeselLuncuran):
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TKGW-PB-DI")
                        #             while not self.modbus.readVariable(w[0] + '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.1)
                        #     sleep(1)
                        #
                        #     # normalkan Kancing
                        #     for w in self.PM:
                        #         if 'D' not in w[0] and w[0].replace('W', '') not in ' '.join(syaratWeselLuncuran):
                        #             sleep(1)
                        #             self.modbus.writePBVDU(w[0] + '-PB-DI', "TBKW-PB-DI")
                        #             sleep(1)
                        #             while self.modbus.readVariable(w[0] + '-BLOCK'):
                        #                 sleep(0.2)
                        #             sleep(0.2)
                        #
                        #     # normalkan syarat wesel
                        #     sleep(2)
                        #     for w in syaratWesel:
                        #         if not self.modbus.readVariable('W' + w + 'WC'):
                        #             self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI',
                        #                                    "TKW-PB-DI")
                        #             sleep(0.2)
                        #             while not self.modbus.readVariable('W' + w + 'WC'):
                        #                 sleep(0.2)
                        #         sleep(0.2)
                        #     if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-L'):
                        #         error += ', ada wesel yang seharusnya tidak jadi syarat di -T-L'
                        ###############################################################################################
                        sleep(2)
                        # jika rute emergency -> merahkan track tujuan
                        if '(E)' in data[1].upper():
                            self.modbus.writeField(data[20].split()[-1].replace('T', '') + '-TPR-DI', 0)
                            sleep(1)

                        # bentuk rute
                        self.modbus.writePBVDU(data[2].upper() + '-PB-DI', data[15].upper() + '-PB-DI')

                        #######################################TEST Berdasar jenis Rute#################################
                        # Test Rute Normal
                        if '(T)' in data[1].upper():
                            # ambil data luncuran terkait rute yang di cek
                            dataLuncuran = []
                            for x in self.IT2:
                                if x[1].replace(' ', '') == data[1].upper().replace(' ', ''):
                                    dataLuncuran = x
                            syaratWesel = list(filter(None, (data[18].split(" ") + dataLuncuran[7].split(" "))))
                            # cek CTRL
                            timer = time()
                            while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL') and (time() - timer < 2):
                                # cek ctrl lain
                                for d in self.ruteCTRL:
                                    ruteOnly = d.split("-")
                                    if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (ruteOnly[1] != data[16]):
                                        error += ', ' + d + ' seharusnya tidak menyala'
                                sleep(0.15)
                            if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL'):
                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL tidak menyala'
                            else:
                                # cek ctrl lain
                                for d in self.ruteCTRL:
                                    ruteOnly = d.split("-")
                                    if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                            ruteOnly[1] != data[16]):
                                        error += ', ' + d + ' seharusnya tidak menyala'
                                sleep(2)
                                # jika -CTRL menyala
                                # cek -RS
                                timer = time()
                                while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-RS') and (time() - timer < 3):
                                    sleep(0.25)
                                if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-RS'):
                                    error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RS tidak menyala'
                                    # cek -B
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-B tidak menyala'
                                else:
                                    # jika RS menyala
                                    # cek syarat wesel
                                    for w in list(filter(None, data[18].split())):
                                        if '-N' in w and not self.modbus.readVariable('W' + w.replace('-N', '') + '-RS-N'):
                                            error += ', W ' + w + ' -RS-N harusnya menyala'
                                        if '-R' in w and not self.modbus.readVariable('W' + w.replace('-R', '') + '-RS-R'):
                                            error += ', W ' + w + ' -RS-R harusnya menyala'
                                    for w in list(filter(None, dataLuncuran[7].split())):
                                        if '-N' in w and not self.modbus.readVariable('W' + w.replace('-N', '') + '-OL-N'):
                                            error += ', W ' + w + ' -OL-N harusnya menyala'
                                        if '-R' in w and not self.modbus.readVariable('W' + w.replace('-R', '') + '-OL-R'):
                                            error += ', W ' + w + ' -OL-R harusnya menyala'
                                    # cek wesel bocor
                                    for w in self.PM:
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-N'):
                                            if w[0].replace('W', '') not in data[18] and w[0].replace('W', '') not in dataLuncuran[7]:
                                                error += ', ' + w[0] + ' -RS-N harusnya tidak menyala'
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-R'):
                                            if w[0].replace('W', '') not in data[18] and w[0].replace('W', '') not in dataLuncuran[7]:
                                                error += ', ' + w[0] + ' -RS-R harusnya tidak menyala'
                                    # cek -T-REQ
                                    timer = time()
                                    while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-REQ') and (
                                            time() - timer < 5):
                                        sleep(0.25)
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-REQ'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-T-REQ tidak menyala'
                                        # cek -P
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-P tidak menyala'
                                    else:
                                        # T-REQ menyala:
                                        # cek -H / -D
                                        pass

                                        # cek syarat subroute
                                        for track in data[20].replace('T', ' ').split() + dataLuncuran[9].replace('T', ' ').split():
                                            if 'APP' not in track:
                                                if not self.modbus.readVariable(track + '-RE-DO'):
                                                    error += ', Subroute ' + track + ' seharusnya menyala'
                                        # cek track bocor
                                        for track in self.TRACK:
                                            if self.modbus.readVariable(track[0] + '-RE-DO'):
                                                if track[0] not in data[20] + dataLuncuran[9]:
                                                    error += ', Subroute ' + track[0] + ' seharusnya tidak menyala'

                                        # cek perpanjangan wesel
                                        syaratTrack = data[20].replace('T', '') + ' ' + dataLuncuran[5].replace('T','') + ' ' + \
                                                      dataLuncuran[9].replace('T', '') + ' ' + dataLuncuran[13].replace('T', '')
                                        syaratWeselREDO = []

                                        for d in syaratWesel:
                                            if "/" in d:
                                                for cek in self.PM:
                                                    if (d[0:d.find('/')] in cek[0]) and ((cek[1].split(" "))[0] in syaratTrack):
                                                        syaratWeselREDO += ['W' + d[0:d.find('/')] + '-' + d[-1] + 'RE-DO']
                                                    if (d[d.find('/')+1:d.find('-')] in cek[0]) and ((cek[1].split(" "))[1] in syaratTrack):
                                                        syaratWeselREDO += ['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[-1] + 'RE-DO']
                                            else:
                                                syaratWeselREDO += ['W' + d + 'RE-DO']

                                        syaratWeselREDO = list(filter(None, syaratWeselREDO))
                                        for w in syaratWeselREDO:
                                            if not self.modbus.readVariable(w):
                                                error += ', Subroute wesel ' + w + ' seharusnya menyala'

                                        allWesel = self.filter(self.inputData, 'NRE-DO') + self.filter(self.inputData, 'RRE-DO')
                                        for w in allWesel:
                                            if self.modbus.readVariable(w) and w not in syaratWeselREDO:
                                                error += ', Subroute wesel ' + w + 'seharusnya tidak menyala'

                                        # cek sekat wesel
                                        for d in syaratWesel:
                                            if self.modbus.readVariable('W' + d.replace('-N', '').replace('-R','') + '-L'):
                                                error += ', wesel W' + d + ' seharusnya tersekat'
                                            if "/" in d:
                                                if not self.modbus.readVariable('W' + d[0:d.find('/')] + '-LE-DO'):
                                                    error += ', indikasi sekat wesel W' + d[0:d.find('/')] + ' seharusnya menyala'
                                                if not self.modbus.readVariable('W' + d[d.find('/') + 1:d.find('-')] + '-LE-DO'):
                                                    error += ', indikasi sekat wesel W' + d[d.find('/') + 1:d.find('-')] + ' seharusnya menyala'

                                        if data[24]:
                                            if (data[4] or data[5]) and self.modbus.readVariable(data[2].upper() + '-CGE-DO'):
                                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CGE-DO seharusnya tidak menyala saat approach belum jatuh'
                                            if data[8] and self.modbus.readVariable(data[2].upper() + '-SR-DO'):
                                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-SR-DO seharusnya tidak menyala saat approach belum jatuh'
                                            if data[10] and self.modbus.readVariable(data[2].upper() + '-LDR-DO'):
                                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-LDR-DO seharusnya tidak menyala saat approach belum jatuh'
                                            if data[11] and self.modbus.readVariable(data[2].upper() + '-RDR-DO'):
                                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RDR-DO seharusnya tidak menyala saat approach belum jatuh'
                                        sleep(1)

                                        # jika approach harus jatuh -> merahkan track approach
                                        if data[24]:
                                            sleep(1)
                                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)
                                            sleep(1)

                                        if data[25]:
                                            if (data[4] or data[5]) and self.modbus.readVariable(data[2].upper() + '-CGE-DO'):
                                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CGE-DO seharusnya tidak menyala saat belum ack jpl'

                                        sleep(1)
                                        # cek ack jpl
                                        for ackJpl in data[25].replace('\n', ' ').split(" "):
                                            if 'JPL' in ackJpl:
                                                 if not self.modbus.readVariable(ackJpl + '-PBE-F'):
                                                    error += ', ' + ackJpl + ' seharusnya terpanggil'
                                                 else:
                                                    self.modbus.writePBVDU(ackJpl + '-PB-DI')
                                            sleep(1)
                                        sleep(1)

                                        # cek sinyal
                                        if (data[4] or data[5]) and not self.modbus.readVariable(data[2].upper() + '-CGE-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CGE-DO seharusnya menyala'
                                        if data[8] and not self.modbus.readVariable(data[2].upper() + '-SR-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-SR-DO seharusnya menyala'
                                        if data[10] and not self.modbus.readVariable(data[2].upper() + '-LDR-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-LDR-DO seharusnya menyala'
                                        if data[11] and not self.modbus.readVariable(data[2].upper() + '-RDR-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RDR-DO seharusnya menyala'

                            # cek syarat track
                            syaratTrack = data[20].replace('T', '') + ' ' + dataLuncuran[5].replace('T', '') + ' ' + \
                                          dataLuncuran[9].replace('T', '') + ' ' + dataLuncuran[13].replace('T', '')
                            syaratWeselTEDO = []

                            for d in syaratWesel:
                                if "/" in d:
                                    for cek in self.PM:
                                        if (d[0:d.find('/')] in cek[0]) and ((cek[1].split(" "))[0] in syaratTrack):
                                            syaratWeselTEDO.append(['W' + d[0:d.find('/')] + '-' + d[-1] + 'TE-DO', (cek[1].split(" "))[0]])
                                        if (d[d.find('/') + 1:d.find('-')] in cek[0]) and ((cek[1].split(" "))[1] in syaratTrack):
                                            syaratWeselTEDO.append(['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[-1] + 'TE-DO', (cek[1].split(" "))[1]])

                                else:
                                    for cek in self.PM:
                                        if d.replace("-N", "").replace("-R", "") in cek[0]:
                                            syaratWeselTEDO.append(['W' + d + 'TE-DO', cek[1]])

                            syaratWeselTEDO = list(filter(None, syaratWeselTEDO))

                            for track in self.TRACK:
                                if track[0] not in syaratTrack:
                                    self.modbus.writeField(track[0] + '-TPR-DI', 0)
                            sleep(2)
                            if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                                error += ', syarat track di -P tidak sesuai'
                            if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-L'):
                                error += ', syarat track di -T-L tidak sesuai'

                            for track in self.TRACK:
                                if (track[0] not in syaratTrack) and (track[0] not in data[23]):
                                    self.modbus.writeField(track[0] + '-TPR-DI', 1)
                                    sleep(0.2)

                            transtepTrack = list(filter(None, syaratTrack.split(" ")))
                            for index, track in enumerate(transtepTrack):
                                sleep(0.5)
                                if index == 0:
                                    self.modbus.writeField(track + '-TPR-DI', 0)
                                    sleep(0.5)
                                    self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                                    sleep(0.5)
                                    if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                                        error += ', track ' + track + ' seharusnya jadi syarat -P'
                                    if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-L'):
                                        error += ', track ' + track + ' seharusnya jadi syarat -T-L'
                                    if  'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                        error += ', track ' + track + ' seharusnya merah'
                                    for wesel in syaratWeselTEDO:
                                        if wesel[1] in track:
                                            if not self.modbus.readVariable(wesel[0]):
                                                error += ', Subroute wesel ' + wesel[0] + ' seharusnya Merah saat' + track + ' jatuh'
                                elif index != len(transtepTrack) - 1:
                                    self.modbus.writeField(track + '-TPR-DI', 0)
                                    sleep(0.5)
                                    self.modbus.writeField(transtepTrack[index-1] + '-TPR-DI', 1)
                                    sleep(0.5)
                                    if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                                        error += ', track ' + track + ' seharusnya jadi syarat -P'
                                    if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-L'):
                                        error += ', track ' + track + ' seharusnya jadi syarat -T-L'
                                    if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                        error += ', track ' + track + ' seharusnya merah'
                                    for wesel in syaratWeselTEDO:
                                        if wesel[1] in track:
                                            if not self.modbus.readVariable(wesel[0]):
                                                error += ', Subroute wesel ' + wesel[0] + ' seharusnya Merah saat' + track + ' jatuh'
                                else:
                                    self.modbus.writeField(track + '-TPR-DI', 0)
                                    sleep(0.5)
                                    self.modbus.writeField(transtepTrack[index - 1] + '-TPR-DI', 1)
                                    sleep(0.5)
                                    if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-P'):
                                        error += ', track ' + track + ' seharusnya jadi syarat -P'
                                    if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-T-L'):
                                        error += ', track ' + track + ' seharusnya jadi syarat -T-L'
                                    if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                        error += ', track ' + track + ' seharusnya merah saat ' + track + ' jatuh'
                                    for wesel in syaratWeselTEDO:
                                        if wesel[1] in track:
                                            if not self.modbus.readVariable(wesel[0]):
                                                error += ', Subroute wesel ' + wesel[0] + ' seharusnya Merah saat' + track + ' jatuh'
                                    sleep(0.5)
                                    self.modbus.writeField(track + '-TPR-DI', 1)

                        if '(E)' in data[1].upper():
                            syaratWesel = list(filter(None, (data[18].split(" "))))
                           # jika rute emergency -> clearkan track tujuan
                            self.modbus.writeField(data[20].split()[-1].replace('T', '') + '-TPR-DI', 1)

                            timer = time()
                            while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL') and (
                                    time() - timer < 3):
                                # cek ctrl lain
                                for d in self.ruteCTRL:
                                    ruteOnly = d.split("-")
                                    if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                            ruteOnly[1] != data[16]):
                                        error += ', ' + d + ' seharusnya tidak menyala'
                                sleep(0.15)
                            if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL'):
                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL tidak menyala'
                            else:
                                # cek ctrl lain
                                for d in self.ruteCTRL:
                                    ruteOnly = d.split("-")
                                    if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                            ruteOnly[1] != data[16]):
                                        error += ', ' + d + ' seharusnya tidak menyala'

                                sleep(2)
                                # jika -CTRL menyala
                                # cek -RS
                                timer = time()
                                while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-RS') and (
                                        time() - timer < 5):
                                    sleep(0.25)
                                if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-RS'):
                                    error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RS tidak menyala'
                                    # cek -B
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-B tidak menyala'
                                else:
                                    # jika RS menyala
                                    # cek syarat wesel
                                    for w in data[18].split():
                                        if 'N' in w and not self.modbus.readVariable(
                                                'W' + w.replace('-N', '') + '-RS-N'):
                                            error += ', W ' + w + ' -RS-N harusnya menyala'
                                        if 'R' in w and not self.modbus.readVariable(
                                                'W' + w.replace('-R', '') + '-RS-R'):
                                            error += ', W ' + w + ' -RS-R harusnya menyala'

                                    # cek wesel bocor
                                    for w in self.PM:
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-N'):
                                            if w[0].replace('W', '') not in data[18]:
                                                error += ', ' + w[0] + ' -RS-N harusnya tidak menyala'
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-R'):
                                            if w[0].replace('W', '') not in data[18]:
                                                error += ', ' + w[0] + ' -RS-R harusnya tidak menyala'

                                    # cek syarat subroute
                                    for track in data[20].replace('T', ' ').split():
                                        if 'APP' not in track:
                                            if not self.modbus.readVariable(track + '-RE-DO'):
                                                error += ', Subroute ' + track + ' seharusnya menyala'

                                    # cek track bocor
                                    for track in self.TRACK:
                                        if self.modbus.readVariable(track[0] + '-RE-DO'):
                                            if track[0] not in data[20]:
                                                error += ', Subroute ' + track[0] + ' seharusnya tidak menyala'

                                    # cek perpanjangan wesel
                                    syaratWeselREDO = []
                                    for d in list(filter(None, data[18].split(" "))):
                                        if "/" in d:
                                            for cek in self.PM:
                                                if d[0:d.find('/')] in cek[0] and (cek[1].split(" "))[0] in data[20]:
                                                    syaratWeselREDO += ['W' + d[0:d.find('/')] + '-' + d[-1] + 'RE-DO']
                                                if d[d.find('/')+1:d.find('-')] in cek[0] and (cek[1].split(" "))[1] in data[20]:
                                                    syaratWeselREDO += ['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[-1] + 'RE-DO']
                                        else:
                                            syaratWeselREDO += ['W' + d + 'RE-DO']

                                    for w in syaratWeselREDO:
                                        if not self.modbus.readVariable(w):
                                            error += ', Subroute wesel ' + w + ' seharusnya menyala'

                                    allWesel = self.filter(self.inputData, 'NRE-DO') + self.filter(self.inputData, 'RRE-DO')
                                    for w in allWesel:
                                        if self.modbus.readVariable(w) and w not in syaratWeselREDO:
                                            error += ', Subroute wesel ' + w + 'seharusnya tidak menyala'

                                    # cek sekat wesel
                                    for d in syaratWesel:
                                        if self.modbus.readVariable('W' + d.replace('-N', '').replace('-R', '') + '-L'):
                                            error += ', wesel W' + d + ' seharusnya tersekat'
                                        if "/" in d:
                                            if not self.modbus.readVariable('W' + d[0:d.find('/')] + '-LE-DO'):
                                                error += ', indikasi sekat wesel W' + d[0:d.find('/')] + ' seharusnya menyala'
                                            if not self.modbus.readVariable('W' + d[d.find('/') + 1:d.find('-')] + '-LE-DO'):
                                                error += ', indikasi sekat wesel W' + d[d.find('/') + 1:d.find('-')] + ' seharusnya menyala'

                                    # cek sinyal
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-E seharusnya menyala'
                                    for d in self.ruteE:
                                        ruteOnly = d.split("-")
                                        if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                                ruteOnly[1] != data[16]):
                                            error += ', ' + d + ' seharusnya tidak menyala'

                                    if data[24]:
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-ER-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-ER-DO seharusnya tidak menyala sebelum approach jatuh'
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-EGE-DO seharusnya tidak menyala sebelum approach jatuh'
                                        if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RGE-DO seharusnya tidak menyala sebelum approach jatuh'

                                    # jika approach harus jatuh -> merahkan track approach
                                    if data[24]:
                                        sleep(1)
                                        self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)
                                        sleep(1)

                                    # jika emergency atau contraflow -> tekan TSD
                                    self.modbus.writePBVDU('TSD-PB-DI', data[2].upper() + '-PB-DI')
                                    sleep(0.25)

                                    if data[6] and not self.modbus.readVariable(data[2].upper() + '-ER-DO'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-ER-DO seharusnya menyala'
                                    if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-EGE-DO seharusnya menyala'
                                    if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RGE-DO seharusnya menyala'

                                    # cek syarat track
                                    syaratTrack = data[20].replace('T', '')
                                    syaratWeselTEDO = []
                                    syaratWesel = data[18].split(" ")
                                    syaratWesel = list(filter(None, syaratWesel))
                                    for d in syaratWesel:
                                        if "/" in d:
                                            for cek in self.PM:
                                                if (d[0:d.find('/')] in cek[0]) and ((cek[1].split(" "))[0] in syaratTrack):
                                                    syaratWeselTEDO.append(['W' + d[0:d.find('/')] + '-' + d[-1] + 'TE-DO', (cek[1].split(" "))[0]])
                                                if (d[d.find('/') + 1:d.find('-')] in cek[0]) and ((cek[1].split(" "))[1] in syaratTrack):
                                                    syaratWeselTEDO.append(['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[-1] + 'TE-DO', (cek[1].split(" "))[1]])
                                        else:
                                            for cek in self.PM:
                                                if d.replace("-N", "").replace("-R", "") in cek[0]:
                                                    syaratWeselTEDO.append(['W' + d + 'TE-DO', cek[1]])

                                    syaratWeselTEDO = list(filter(None, syaratWeselTEDO))

                                    if data[24]:
                                        self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)

                                    transtepTrack = list(filter(None, syaratTrack.split(" ")))
                                    for index, track in enumerate(transtepTrack):
                                        sleep(0.5)
                                        if index == 0:
                                            self.modbus.writeField(track + '-TPR-DI', 0)
                                            sleep(0.5)
                                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                                            sleep(0.5)
                                            if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                error += ', track ' + track + ' seharusnya merah'
                                            for wesel in syaratWeselTEDO:
                                                if wesel[1] in track:
                                                    if not self.modbus.readVariable(wesel[0]):
                                                        error += ', Subroute wesel ' + wesel[0] + ' seharusnya Merah saat' + track + ' jatuh'
                                        elif index != len(transtepTrack) - 1:
                                            self.modbus.writeField(track + '-TPR-DI', 0)
                                            sleep(0.5)
                                            self.modbus.writeField(transtepTrack[index-1] + '-TPR-DI', 1)
                                            sleep(0.5)
                                            if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                error += ', track ' + track + ' seharusnya merah'
                                            for wesel in syaratWeselTEDO:
                                                if wesel[1] in track:
                                                    if not self.modbus.readVariable(wesel[0]):
                                                        error += ', Subroute wesel ' + wesel[0] + ' seharusnya Merah saat' + track + ' jatuh'
                                        else:
                                            self.modbus.writeField(track + '-TPR-DI', 0)
                                            sleep(0.5)
                                            self.modbus.writeField(transtepTrack[index - 1] + '-TPR-DI', 1)
                                            sleep(0.5)
                                            if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                error += ', track ' + track + ' seharusnya merah saat ' + track + ' jatuh'
                                            for wesel in syaratWeselTEDO:
                                                if wesel[1] in track:
                                                    if not self.modbus.readVariable(wesel[0]):
                                                        error += ', Subroute wesel ' + wesel[0] + ' seharusnya Merah saat' + track + ' jatuh'
                                            sleep(0.5)
                                            self.modbus.writeField(track + '-TPR-DI', 1)

                        if '(CF)' in data[1].upper():
                            syaratWesel = list(filter(None, (data[18].split(" "))))

                            # cek -CTRL
                            timer = time()
                            while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-CTRL') and (time() - timer < 5):
                                # cek ctrl lain
                                for d in self.ruteCTRL:
                                    ruteOnly = d.split("-")
                                    if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                            ruteOnly[1] != data[16]):
                                        error += ', ' + d + ' seharusnya tidak menyala'
                                sleep(0.15)
                            if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-CTRL'):
                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CF-CTRL tidak menyala'
                            else:
                                # cek ctrl lain
                                for d in self.ruteCTRL:
                                    ruteOnly = d.split("-")
                                    if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                            ruteOnly[1] != data[16]):
                                        error += ', ' + d + ' seharusnya tidak menyala'

                                sleep(2)
                                # jika -CTRL menyala
                                # cek -RS
                                timer = time()
                                while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-RS') and (
                                        time() - timer < 5):
                                    sleep(0.25)
                                if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-RS'):
                                    error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CF-RS tidak menyala'
                                    # cek -B
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-B'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CF-B tidak menyala'
                                else:
                                    # jika RS menyala
                                    # cek syarat wesel
                                    for w in data[18].split():
                                        if 'N' in w and not self.modbus.readVariable('W' + w.replace('-N', '') + '-RS-N'):
                                            error += ', W ' + w + ' -RS-N harusnya menyala'
                                        if 'R' in w and not self.modbus.readVariable('W' + w.replace('-R', '') + '-RS-R'):
                                            error += ', W ' + w + ' -RS-R harusnya menyala'
                                    # cek wesel bocor
                                    for w in self.PM:
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-N'):
                                            if w[0].replace('W', '') not in data[18]:
                                                error += ', ' + w[0] + ' -RS-N harusnya tidak menyala'
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-R'):
                                            if w[0].replace('W', '') not in data[18]:
                                                error += ', ' + w[0] + ' -RS-R harusnya tidak menyala'

                                    # cek syarat subroute
                                    for track in data[20].replace('T', ' ').split():
                                        if 'APP' not in track:
                                            if not self.modbus.readVariable(track + '-RE-DO'):
                                                error += ', Subroute ' + track + ' seharusnya menyala'
                                    # cek track bocor
                                    for track in self.TRACK:
                                        if self.modbus.readVariable(track[0] + '-RE-DO'):
                                            if track[0] not in data[20]:
                                                error += ', Subroute ' + track[0] + ' seharusnya tidak menyala'

                                    # cek perpanjangan wesel
                                    syaratWeselREDO = []
                                    for d in list(filter(None, data[18].split(" "))):
                                        if "/" in d:
                                            for cek in self.PM:
                                                if d[0:d.find('/')] in cek[0] and (cek[1].split(" "))[0] in data[20]:
                                                    syaratWeselREDO += ['W' + d[0:d.find('/')] + '-' + d[-1] + 'RE-DO']
                                                if d[d.find('/')+1:d.find('-')] in cek[0] and (cek[1].split(" "))[1] in data[20]:
                                                    syaratWeselREDO += ['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[-1] + 'RE-DO']
                                        else:
                                            syaratWeselREDO += ['W' + d + 'RE-DO']

                                    for w in syaratWeselREDO:
                                        if not self.modbus.readVariable(w):
                                            error += ', Subroute wesel ' + w + ' seharusnya menyala'

                                    allWesel = self.filter(self.inputData, 'NRE-DO') + self.filter(self.inputData, 'RRE-DO')
                                    for w in allWesel:
                                        if self.modbus.readVariable(w) and w not in syaratWeselREDO:
                                            error += ', Subroute wesel ' + w + 'seharusnya tidak menyala'

                                    # cek sekat wesel
                                    for d in syaratWesel:
                                        if self.modbus.readVariable('W' + d.replace('-N', '').replace('-R', '') + '-L'):
                                            error += ', wesel W' + d + ' seharusnya tersekat'
                                        if "/" in d:
                                            if not self.modbus.readVariable('W' + d[0:d.find('/')] + '-LE-DO'):
                                                error += ', indikasi sekat wesel W' + d[0:d.find('/')] + ' seharusnya menyala'
                                            if not self.modbus.readVariable('W' + d[d.find('/') + 1:d.find('-')] + '-LE-DO'):
                                                error += ', indikasi sekat wesel W' + d[d.find('/') + 1:d.find('-')] + ' seharusnya menyala'

                                    # cek sinyal
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-E'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CF-E seharusnya menyala'
                                    for d in self.ruteE:
                                        ruteOnly = d.split("-")
                                        if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                                ruteOnly[1] != data[16]):
                                            error += ', ' + d + ' seharusnya tidak menyala'

                                    if data[24]:
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-ER-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-ER-DO seharusnya tidak menyala sebelum approach jatuh'
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-EGE-DO seharusnya tidak menyala sebelum approach jatuh'
                                        if data[9] and not self.modbus.readVariable(data[2].upper() + '-CFR-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CFR-DO seharusnya tidak menyala sebelum approach jatuh'
                                        if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RGE-DO seharusnya tidak menyala sebelum approach jatuh'

                                    # jika approach harus jatuh -> merahkan track approach
                                    if data[24]:
                                        sleep(1)
                                        self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)
                                        sleep(1)

                                    # jika emergency atau contraflow -> tekan TSD
                                    self.modbus.writePBVDU('TSD-PB-DI', data[2].upper() + '-PB-DI')
                                    sleep(0.25)

                                    if data[6] and not self.modbus.readVariable(data[2].upper() + '-ER-DO'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-ER-DO seharusnya menyala'
                                    if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-EGE-DO seharusnya menyala'
                                    if data[9] and not self.modbus.readVariable(data[2].upper() + '-CFR-DO'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CFR-DO seharusnya menyala'
                                    if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RGE-DO seharusnya menyala'

                                    # cek syarat track
                                    syaratTrack = data[20].replace('T', '')
                                    syaratWeselTEDO = []
                                    syaratWesel = data[18].split(" ")
                                    syaratWesel = list(filter(None, syaratWesel))
                                    for d in syaratWesel:
                                        if "/" in d:
                                            for cek in self.PM:
                                                if (d[0:d.find('/')] in cek[0]) and (
                                                        (cek[1].split(" "))[0] in syaratTrack):
                                                    syaratWeselTEDO.append(
                                                        ['W' + d[0:d.find('/')] + '-' + d[-1] + 'TE-DO',
                                                         (cek[1].split(" "))[0]])
                                                if (d[d.find('/') + 1:d.find('-')] in cek[0]) and (
                                                        (cek[1].split(" "))[1] in syaratTrack):
                                                    syaratWeselTEDO.append(
                                                        ['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[-1] + 'TE-DO',
                                                         (cek[1].split(" "))[1]])

                                        else:
                                            for cek in self.PM:
                                                if d.replace("-N", "").replace("-R", "") in cek[0]:
                                                    syaratWeselTEDO.append(['W' + d + 'TE-DO', cek[1]])

                                    syaratWeselTEDO = list(filter(None, syaratWeselTEDO))

                                    if data[24]:
                                        self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)

                                    transtepTrack = list(filter(None, syaratTrack.split(" ")))
                                    for index, track in enumerate(transtepTrack):
                                        sleep(0.5)
                                        if index == 0:
                                            self.modbus.writeField(track + '-TPR-DI', 0)
                                            sleep(0.5)
                                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                                            sleep(0.5)
                                            if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                error += ', track ' + track + ' seharusnya merah'
                                            for wesel in syaratWeselTEDO:
                                                if wesel[1] in track:
                                                    if not self.modbus.readVariable(wesel[0]):
                                                        error += ', Subroute wesel ' + wesel[
                                                            0] + ' seharusnya Merah saat' + track + ' jatuh'
                                        elif index != len(transtepTrack) - 1:
                                            self.modbus.writeField(track + '-TPR-DI', 0)
                                            sleep(0.5)
                                            self.modbus.writeField(transtepTrack[index - 1] + '-TPR-DI', 1)
                                            sleep(0.5)
                                            if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                error += ', track ' + track + ' seharusnya merah'
                                            for wesel in syaratWeselTEDO:
                                                if wesel[1] in track:
                                                    if not self.modbus.readVariable(wesel[0]):
                                                        error += ', Subroute wesel ' + wesel[
                                                            0] + ' seharusnya Merah saat' + track + ' jatuh'
                                        else:
                                            self.modbus.writeField(track + '-TPR-DI', 0)
                                            sleep(0.5)
                                            self.modbus.writeField(transtepTrack[index - 1] + '-TPR-DI', 1)
                                            sleep(0.5)
                                            if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                error += ', track ' + track + ' seharusnya merah saat ' + track + ' jatuh'
                                            for wesel in syaratWeselTEDO:
                                                if wesel[1] in track:
                                                    if not self.modbus.readVariable(wesel[0]):
                                                        error += ', Subroute wesel ' + wesel[
                                                            0] + ' seharusnya Merah saat' + track + ' jatuh'
                                            sleep(0.5)
                                            self.modbus.writeField(track + '-TPR-DI', 1)

                        if '(S)' in data[1].upper():
                            syaratWesel = list(filter(None, (data[18].split(" "))))
                            # cek CTRL
                            timer = time()
                            while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL') and (time() - timer < 2):
                                # cek ctrl lain
                                for d in self.ruteCTRL:
                                    ruteOnly = d.split("-")
                                    if self.modbus.readVariable(d) and (ruteOnly[0] != data[2].upper()) and (
                                            ruteOnly[1] != data[16]):
                                        error += ', ' + d + ' seharusnya tidak menyala'
                                sleep(0.15)
                            if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL'):
                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-CTRL tidak menyala'
                            else:
                                sleep(2)
                                # jika -CTRL menyala
                                # cek -RS
                                timer = time()
                                while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-RS') and ( time() - timer < 3):
                                    sleep(0.25)
                                if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-RS'):
                                    error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-RS tidak menyala'
                                    # cek -B
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                                        error += ', ' + d + ' seharusnya tidak menyala'
                                else:
                                    # jika RS menyala
                                    # cek syarat wesel
                                    for w in data[18].split():
                                        if '-N' in w and not self.modbus.readVariable('W' + w.replace('-N', '') + '-RS-N'):
                                            error += ', W ' + w + ' -RS-N harusnya menyala'
                                        if '-R' in w and not self.modbus.readVariable('W' + w.replace('-R', '') + '-RS-R'):
                                            error += ', W ' + w + ' -RS-R harusnya menyala'
                                    # cek wesel bocor
                                    for w in self.PM:
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-N'):
                                            if w[0].replace('W', '') not in data[18]:
                                                error += ', ' + w[0] + ' -RS-N harusnya tidak menyala'
                                        if 'W' in w and self.modbus.readVariable(w[0] + '-RS-R'):
                                            if w[0].replace('W', '') not in data[18]:
                                                error += ', ' + w[0] + ' -RS-R harusnya tidak menyala'
                                    # cek -S-REQ
                                    timer = time()
                                    while not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-REQ') and (
                                            time() - timer < 5):
                                        sleep(0.25)
                                    if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-REQ'):
                                        error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-S-REQ tidak menyala'
                                        # cek -B
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-B tidak menyala'
                                    else:
                                        # S-REQ menyala:
                                        # cek -H / -D
                                        pass

                                        # cek syarat subroute
                                        for track in data[20].replace('T', ' ').split():
                                            if 'APP' not in track:
                                                if not self.modbus.readVariable(track + '-RE-DO'):
                                                    error += ', Subroute ' + track + ' seharusnya menyala'
                                        # cek track bocor
                                        for track in self.TRACK:
                                            if self.modbus.readVariable(track[0] + '-RE-DO'):
                                                if track[0] not in data[20]:
                                                    error += ', Subroute ' + track[0] + ' seharusnya tidak menyala'

                                        # cek perpanjangan wesel
                                        syaratWeselREDO = []
                                        for d in list(filter(None, data[18].split(" "))):
                                            if "/" in d:
                                                for cek in self.PM:
                                                    if d[0:d.find('/')] in cek[0] and (cek[1].split(" "))[0] in data[
                                                        20]:
                                                        syaratWeselREDO += ['W' + d[0:d.find('/')] + '-' + d[-1] + 'RE-DO']
                                                    if d[d.find('/') + 1:d.find('-')] in cek[0] and (cek[1].split(" "))[
                                                        1] in data[20]:
                                                        syaratWeselREDO += ['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[
                                                            -1] + 'RE-DO']
                                            else:
                                                syaratWeselREDO += ['W' + d + 'RE-DO']

                                        for w in syaratWeselREDO:
                                            if not self.modbus.readVariable(w):
                                                error += ', Subroute wesel ' + w + ' seharusnya menyala'

                                        allWesel = self.filter(self.inputData, 'NRE-DO') + self.filter(self.inputData,
                                                                                                       'RRE-DO')
                                        for w in allWesel:
                                            if self.modbus.readVariable(w) and w not in syaratWeselREDO:
                                                error += ', Subroute wesel ' + w + 'seharusnya tidak menyala'

                                        # cek sekat wesel
                                        for d in syaratWesel:
                                            if self.modbus.readVariable('W' + d.replace('-N', '').replace('-R', '') + '-L'):
                                                error += ', wesel W' + d + 'seharusnya tersekat'
                                            if "/" in d:
                                                if not self.modbus.readVariable('W' + d[0:d.find('/')] + '-LE-DO'):
                                                    error += ', indikasi sekat wesel W' + d[0:d.find('/')] + ' seharusnya menyala'
                                                if not self.modbus.readVariable('W' + d[d.find('/') + 1:d.find('-')] + '-LE-DO'):
                                                    error += ', indikasi sekat wesel W' + d[d.find('/') + 1:d.find('-')] + ' seharusnya menyala'

                                        # cek sinyal
                                        if data[24]:
                                            if data[7] and not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S'):
                                                error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-S seharusnya tidak menyala sebelum approach jatuh'
                                            if data[7] and not self.modbus.readVariable(data[2].upper() + '-GR-DO'):
                                                error += ', ' + data[2].upper() + '-GR-DO seharusnya tidak menyala sebelum approach jatuh'
                                            if data[7] and not self.modbus.readVariable(data[2].upper() + '-WGE-DO'):
                                                error += ', ' + data[2].upper() + '-WGE-DO seharusnya tidak menyala sebelum approach jatuh'

                                        # jika approach harus jatuh -> merahkan track approach
                                        if data[24]:
                                            sleep(1)
                                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)
                                            sleep(1)

                                        if data[25]:
                                            if data[7] and not self.modbus.readVariable(data[2].upper() + '-WGE-DO'):
                                                error += ', ' + data[2].upper() + '-WGE-DO seharusnya tidak menyala sebelum ack jpl'

                                        # cek syarat JPL
                                        for ackJpl in data[25].replace('\n', ' ').split(" "):
                                            if 'JPL' in ackJpl:
                                                if not self.modbus.readVariable(ackJpl + '-PBE-F'):
                                                    error += ', ' + ackJpl + ' seharusnya terpanggil'
                                                else:
                                                    self.modbus.writePBVDU(ackJpl + '-PB-DI')
                                            sleep(1)
                                        sleep(1)

                                        # cek sinyal
                                        if data[7] and not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S'):
                                            error += ', ' + data[2].upper() + '-' + simp(data[15].upper()) + '-S seharusnya menyala'
                                        if data[7] and not self.modbus.readVariable(data[2].upper() + '-GR-DO'):
                                            error += ', ' + data[2].upper() + '-GR-DO seharusnya menyala'
                                        if data[7] and not self.modbus.readVariable(data[2].upper() + '-WGE-DO'):
                                            error += ', ' + data[2].upper() + '-WGE-DO seharusnya menyala'

                                        # cek syarat track
                                        syaratTrack = data[20].replace('T', '')
                                        syaratWeselTEDO = []
                                        syaratWesel = data[18].split(" ")
                                        syaratWesel = list(filter(None, syaratWesel))
                                        for d in syaratWesel:
                                            if "/" in d:
                                                for cek in self.PM:
                                                    if (d[0:d.find('/')] in cek[0]) and (
                                                            (cek[1].split(" "))[0] in syaratTrack):
                                                        syaratWeselTEDO.append(
                                                            ['W' + d[0:d.find('/')] + '-' + d[-1] + 'TE-DO',
                                                             (cek[1].split(" "))[0]])
                                                    if (d[d.find('/') + 1:d.find('-')] in cek[0]) and (
                                                            (cek[1].split(" "))[1] in syaratTrack):
                                                        syaratWeselTEDO.append(
                                                            ['W' + d[d.find('/') + 1:d.find('-')] + '-' + d[-1] + 'TE-DO',
                                                             (cek[1].split(" "))[1]])

                                            else:
                                                for cek in self.PM:
                                                    if d.replace("-N", "").replace("-R", "") in cek[0]:
                                                        syaratWeselTEDO.append(['W' + d + 'TE-DO', cek[1]])

                                        syaratWeselTEDO = list(filter(None, syaratWeselTEDO))

                                        if data[24]:
                                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)

                                        transtepTrack = list(filter(None, syaratTrack.split(" ")))
                                        for index, track in enumerate(transtepTrack):
                                            sleep(0.5)
                                            if index == 0:
                                                self.modbus.writeField(track + '-TPR-DI', 0)
                                                sleep(0.5)
                                                self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                                                sleep(0.5)
                                                if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                                                    error += ', track ' + track + ' belum menjadi syarat ' + data[2].upper() + '-' + simp(data[15].upper()) + '-B'
                                                if self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-L'):
                                                    error += ', track ' + track + ' belum menjadi syarat ' + data[2].upper() + '-' + simp(data[15].upper()) + '-S-L'

                                                if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                    error += ', track ' + track + ' seharusnya merah'
                                                for wesel in syaratWeselTEDO:
                                                    if wesel[1] in track:
                                                        if not self.modbus.readVariable(wesel[0]):
                                                            error += ', Subroute wesel ' + wesel[
                                                                0] + ' seharusnya Merah saat' + track + ' jatuh'
                                                # jika tidak ada track approach langsir / jalur simpan -> tunggu aproach stik mati 30s
                                                    if not data[23]:
                                                        sleep(30)
                                            elif index != len(transtepTrack) - 1:
                                                self.modbus.writeField(track + '-TPR-DI', 0)
                                                sleep(0.5)
                                                self.modbus.writeField(transtepTrack[index - 1] + '-TPR-DI', 1)
                                                sleep(0.5)
                                                if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                    error += ', track ' + track + ' seharusnya merah'
                                                for wesel in syaratWeselTEDO:
                                                    if wesel[1] in track:
                                                        if not self.modbus.readVariable(wesel[0]):
                                                            error += ', Subroute wesel ' + wesel[
                                                                0] + ' seharusnya Merah saat' + track + ' jatuh'
                                            else:
                                                self.modbus.writeField(track + '-TPR-DI', 0)
                                                sleep(0.5)
                                                self.modbus.writeField(transtepTrack[index - 1] + '-TPR-DI', 1)
                                                sleep(0.5)
                                                if 'APP' not in track and not self.modbus.readVariable(track + '-TE-DO'):
                                                    error += ', track ' + track + ' seharusnya merah saat ' + track + ' jatuh'
                                                for wesel in syaratWeselTEDO:
                                                    if wesel[1] in track:
                                                        if not self.modbus.readVariable(wesel[0]):
                                                            error += ', Subroute wesel ' + wesel[
                                                                0] + ' seharusnya Merah saat' + track + ' jatuh'
                                                sleep(0.5)
                                                self.modbus.writeField(track + '-TPR-DI', 1)

                        sleep(3)

                        # hapus rute
                        self.modbus.writePBVDU('TPR-PB-DI', data[2].upper() + '-PB-DI')
                        sleep(1)

                        # jika approach harus jatuh -> clearkan track approach
                        if data[24]:
                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                            sleep(1)
                        # jika ada deraileur yang harus rebah -> naikan deraileur
                        if '-R' in data[19]:
                            for deraileur in data[19].split():
                                if '-R' in deraileur and 'D' in deraileur[0]:
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 1)
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 0)
                                    # jika track emergency -> clearkan track tujuan
                        if '(E)' in data[1].upper():
                            self.modbus.writeField(data[20].split()[-1].replace('T', '') + '-TPR-DI', 1)
                            sleep(1)

                        # tunggu sampai rute terhapus
                        while not self.modbus.readVariable(data[2].upper() + ('-T' if '(T)' in data[1].upper() else
                                                                        ('-S' if '(S)' in data[1].upper() else '-E')) + '-AS'):
                            sleep(1)

                        print(error)
                        if error:
                            count += 1
                            errorLog += [[count, 'Rute ' + data[1].upper() + ' ' + error, '']]

                        if self.stopTest:
                            self.stopTest = 0
                            break

                    file, check = QFileDialog.getSaveFileName(None, "QFileDialog getSaveFileName() Demo",
                                                              "Error Log Interlocking Table.xlsx",
                                                              "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
                    if check:
                        dfFI = pd.DataFrame(errorLog, columns=['NO', 'Temuan', 'Perbaikan'])
                        dfFI.to_excel(file, index=False)

                if self.CRTest:
                    # counter untuk penomoran error log
                    count = 0
                    # array yang menyimpan informasi error sebelum di write ke csv
                    errorLog = []
                    # function untuk menyesuaikan variable untuk rute contoh : J10 ke JL12B jadi J10-12B-XXXX
                    simp = lambda a: a.replace('J', '').replace('JL', '').replace('L', '')
                    # iterate data IT1 berdasarkan nomor rute yang akan di tes untuk kolom vertikal rute pada CR
                    for ruteUtama in self.IT[self.startRoute:self.finishRoute]:
                        # iterate data IT1 berdasarkan nomor rute yang akan di tes untuk kolom horizontal rute pada CR
                        for ruteConflict in self.IT[self.startRoute2:self.finishRoute2]:
                            # cek rute yang tidak perlu di cek
                            cek = True
                            # jika rute utamanya dengan rute conflictnya sama tidak perlu di cek
                            if ruteUtama == ruteConflict:
                                cek = False
                            # jika rute utama normal dan rute conflictnya rute emergency dia sendiri tidak perlu di cek
                            if (ruteUtama["Jenis Rute"] == "Normal" and ruteConflict["Jenis Rute"] == "Emergency"):
                                if ruteUtama[1].upper().replace('(T)', '') == ruteConflict[1].upper().replace('(E)', ''):
                                    cek = False
                            # jika rute conflictnya rute normal tidak perlu di cek, karna yang di cek adalah -B dan -E/CF/S-L
                            if ruteConflict["Jenis Rute"] == "Normal":
                                cek = False
                            # jika rute utamanya rute normal dan tujuannya stasiun sebelah tidak perlu di cek, karna track konflictnya sama dengan track di rute emergency-nya
                            if (ruteUtama["Jenis Rute"] == "Normal") and ('A' == ruteUtama["Sinyal Tujuan"].upper().strip()[0]):
                                cek = False

                            # start conflict route
                            if cek:
                                # print informasi progress di console IDE
                                print('Testing Conflict Rute => ' + ruteUtama["No Rute"] + ': ' + ruteUtama["Nama Rute"] +
                                      ' VS ' + ruteConflict["No Rute"] + ': ' + ruteConflict["Nama Rute"])
                                # variable untuk simpan informasi error sebelum di pindahkan ke array errorlog
                                error = ''
                                # cek syarat -B
                                bConflict = False
                                # mencari tau apakah kedua rute saling conflict berdasarkan irisan track
                                syaratTrack1 = []
                                if '(T)' in data[1].upper():
                                    # ambil data luncuran terkait rute yang di cek
                                    dataLuncuran1 = []
                                    for x in self.IT2:
                                        if x[1].replace(' ', '') == data[1].upper().replace(' ', ''):
                                            dataLuncuran1 = x
                                    syaratTrack1 = list(filter(None, (data[20].split(" ") + dataLuncuran1[9].split(" "))))
                                else:
                                    syaratTrack1 = list(filter(None, (data[20].split(" "))))
                                syaratTrack2 = []
                                if '(T)' in dataVS[1].upper():
                                    # ambil data luncuran terkait rute yang di cek
                                    dataLuncuran2 = []
                                    for x in self.IT2:
                                        if x[1].replace(' ', '') == dataVS[1].upper().replace(' ', ''):
                                            dataLuncuran2 = x
                                    syaratTrack2 = list(filter(None, (dataVS[20].split(" ") + dataLuncuran2[9].split(" "))))
                                else:
                                    syaratTrack2 = list(filter(None, (dataVS[20].split(" "))))

                                # cek apakah ada track yang beririsan atau conflict
                                ruteConflict = False
                                for track1 in syaratTrack1:
                                    for track2 in syaratTrack2:
                                        if track1 == track2:
                                            ruteConflict = True

                                ruteLangsungConflict = False
                                if (data[15].upper().strip() == dataVS[2].upper().strip()) and ('(S)' not in data[1]) and ('(S)' not in dataVS[1]):
                                    ruteConflict = True
                                    ruteLangsungConflict = True

                                ################################ bentuk rute 1 #########################################
                                if ('(S)' in data[1].upper() and not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-AS-SR')) or \
                                    ('(S)' not in data[1].upper() and not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR')):

                                    # jika ada deraileur yang harus rebah -> turunkan deraileur
                                    if '-R' in data[19]:
                                        for deraileur in data[19].split():
                                            if '-R' in deraileur and 'D' in deraileur[0]:
                                                self.modbus.writePBVDU('TBKWM-PB-DI', deraileur.replace('-R', '') + '-PB-DI')
                                                sleep(1)
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 0)
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 1)
                                                sleep(1)

                                    # jika rute emergency -> merahkan track pancingan emergency
                                    if '(E)' in data[1].upper():
                                        self.modbus.writeField(
                                            data[20].split()[-1].replace('T', '') + '-TPR-DI', 0)
                                        # jika approach harus jatuh -> merahkan track approach
                                        if data[24]:
                                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)

                                    # bentuk rute
                                    self.modbus.writePBVDU(data[2].upper() + '-PB-DI', data[15].upper() + '-PB-DI')
                                    sleep(1)

                                ################################ bentuk rute 2 #########################################
                                # jika ada deraileur yang harus rebah -> turunkan deraileur
                                if '-R' in dataVS[19]:
                                    for deraileur in dataVS[19].split():
                                        if '-R' in deraileur and 'D' in deraileur[0]:
                                            self.modbus.writePBVDU('TBKWM-PB-DI', deraileur.replace('-R', '') + '-PB-DI')
                                            sleep(3)
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 0)
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 1)
                                            sleep(1)
                                    sleep(1)

                                syaratWesel = list(filter(None, (dataVS[18].split(" "))))
                                for w in syaratWesel:
                                    # arahkan wesel sesuai syarat wesel
                                    if not self.modbus.readVariable('W' + w + 'WC'):
                                        self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI', "TKW-PB-DI")
                                    sleep(1)

                                dataLuncuran = []
                                if '(T)' in dataVS[1]:
                                    dataLuncuran = ["" for x in range(14)]
                                    for d in self.IT2:
                                        if (d[1].strip().replace(" ", "") == dataVS[1]) or (d[0].strip().replace(" ", "") == dataVS[0]):
                                            dataLuncuran = d
                                    syaratWeselLuncuran = list(filter(None, (dataLuncuran[7].split(" "))))
                                    for w in syaratWeselLuncuran:
                                        # arahkan wesel sesuai syarat wesel
                                        if not self.modbus.readVariable('W' + w + 'WC'):
                                            self.modbus.writePBVDU('W' + w.replace("N", "").replace("R", "") + 'PB-DI',
                                                                   "TKW-PB-DI")
                                        sleep(1)

                                ####################################### Cek Conflict ###################################
                                sleep(1)
                                ruteStr = dataVS[2].upper() + '-' + simp(dataVS[15].upper())
                                reset = False
                                Bjatuh = False

                                if '(CF)' in dataVS[1].upper():
                                    if not self.modbus.readVariable(ruteStr + '-CF-B'):
                                        Bjatuh = True
                                else:
                                    if not self.modbus.readVariable(ruteStr + '-B'):
                                        Bjatuh = True

                                Ljatuh = False
                                if '(S)' in dataVS[1].upper():
                                    if not self.modbus.readVariable(ruteStr + '-S-L'):
                                        Ljatuh = True
                                elif '(CF)' in dataVS[1].upper():
                                    if not self.modbus.readVariable(ruteStr + '-CF-E-L'):
                                        Ljatuh = True
                                else:
                                    if not self.modbus.readVariable(ruteStr + '-E-L'):
                                        Ljatuh = True

                                if ruteConflict:
                                    if not Bjatuh:
                                        error += ruteStr + '-B tidak jatuh -> seharusnya jatuh, '
                                        reset = True
                                    if (not Ljatuh) and (not ruteLangsungConflict):
                                        error += ruteStr + '-L tidak jatuh -> seharusnya jatuh, '
                                        reset = True
                                else:
                                    if Bjatuh:
                                        error += ruteStr + '-B jatuh -> seharusnya tidak jatuh, '
                                    if Ljatuh:
                                        error += ruteStr + '-L jatuh -> seharusnya tidak jatuh, '

                                ###################################### Clearence R2 ####################################
                                # jika ada deraileur yang harus rebah -> naikan deraileur
                                if '-R' in dataVS[19]:
                                    for deraileur in dataVS[19].split():
                                        if '-R' in deraileur and 'D' in deraileur[0] and 'D' in deraileur[0]:
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 1)
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 0)
                                            # jika track emergency -> clearkan track tujuan

                                ###################################### Clearence R1 ####################################
                                if reset:
                                    if '(E)' in data[1].upper() or '(CF)' in data[1].upper():
                                        # clearkan track pancingan emergency
                                        self.modbus.writeField(data[20].split()[-1].replace('T', '') + '-TPR-DI', 1)
                                        sleep(1)
                                    # jika approach harus jatuh -> clearkan track approach
                                    if data[24]:
                                        self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                                        sleep(1)

                                    # jika ada deraileur yang harus rebah -> naikan deraileur
                                    if '-R' in data[19]:
                                        for deraileur in data[19].split():
                                            if '-R' in deraileur and 'D' in deraileur[0]:
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 1)
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 0)
                                                # jika track emergency -> clearkan track tujuan

                                    # hapus rute
                                    self.modbus.writePBVDU('TPR-PB-DI', data[2].upper() + '-PB-DI')
                                    sleep(1)

                                    # tunggu sampai rute terhapus
                                    while not self.modbus.readVariable(
                                            data[2].upper() + ('-T' if '(T)' in data[1].upper() else
                                            ('-S' if '(S)' in data[1].upper() else '-E')) + '-AS'):
                                        sleep(1)

                                    if self.stopTest:
                                        self.stopTest = 0
                                        break

                                print(error)
                                if error:
                                    count += 1
                                    errorLog += [[count, data[1].upper() + ' VS ' + dataVS[1].upper(), error, '']]

                                if self.stopTest:
                                    break

                        ###################################### Clearence R1 ####################################
                        if '(E)' in data[1].upper() or '(CF)' in data[1].upper():
                            # clearkan track pancingan emergency
                            self.modbus.writeField(
                                data[20].split()[-1].replace('T', '') + '-TPR-DI', 1)
                            sleep(1)

                            # jika approach harus jatuh -> CLEARKAN track approach
                            if data[24]:
                                self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)

                        # jika ada deraileur yang harus rebah -> naikan deraileur
                        if '-R' in data[19]:
                            for deraileur in data[19].split():
                                if '-R' in deraileur and 'D' in deraileur[0]:
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 1)
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 0)
                                    # jika track emergency -> clearkan track tujuan

                        # hapus rute
                        self.modbus.writePBVDU('TPR-PB-DI', data[2].upper() + '-PB-DI')
                        sleep(1)

                        # tunggu sampai rute terhapus
                        while not self.modbus.readVariable(
                                data[2].upper() + ('-T' if '(T)' in data[1].upper() else
                                ('-S' if '(S)' in data[1].upper() else '-E')) + '-AS'):
                            sleep(1)

                        if self.stopTest:
                            self.stopTest = 0
                            break

                    # Simpan Error log ke file
                    file, check = QFileDialog.getSaveFileName(None, "QFileDialog getSaveFileName() Demo",
                                                                  "Error Log Conflict Route.xlsx",
                                                                  "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
                    if check:
                        dfFI = pd.DataFrame(errorLog, columns=['NO', 'Rute', 'Temuan','Perbaikan'])
                        dfFI.to_excel(file, index=False)

                if self.VTTest:
                    pass

                if self.DTTest:
                    pass

                if self.CRTest and self.DTTest:
                    count = 0
                    errorLog = []
                    simp = lambda a: a.replace('J', '').replace('JL', '').replace('L', '')

                    for data in self.IT1[self.startRoute:self.finishRoute]:
                        for dataVS in self.IT1[self.startRoute2:self.finishRoute2]:
                            error = ''
                            # cek rute yang sama atau rute Normal dan Emergency yang sama
                            cek = True
                            if data == dataVS:
                                cek = False
                            elif ('(T)' in data[1].upper() and '(E)' in dataVS[1].upper()) or ('(E)' in data[1].upper() and '(T)' in dataVS[1].upper()):
                                if data[1].upper().replace('(T)', '').replace('(E)', '') == dataVS[1].upper().replace('(T)', '').replace('(E)', ''):
                                    cek = False

                            # start conflict route
                            if cek:
                                # persiapan data
                                print('Testing Conflict Rute => ' + data[0] + ': ' + data[1].upper() + ' VS ' + dataVS[0] + ': ' + dataVS[1].upper())
                                error = ''

                                # mencari tau apakah kedua rute saling conflict berdasarkan irisan track
                                syaratTrack1 = []
                                if '(T)' in data[1].upper():
                                    # ambil data luncuran terkait rute yang di cek
                                    dataLuncuran1 = []
                                    for x in self.IT2:
                                        if x[1].replace(' ', '') == data[1].upper().replace(' ', ''):
                                            dataLuncuran1 = x
                                    syaratTrack1 = list(
                                        filter(None, (data[20].split(" ") + dataLuncuran1[9].split(" "))))
                                else:
                                    syaratTrack1 = list(filter(None, (data[20].split(" "))))
                                syaratTrack2 = []
                                if '(T)' in dataVS[1].upper():
                                    # ambil data luncuran terkait rute yang di cek
                                    dataLuncuran2 = []
                                    for x in self.IT2:
                                        if x[1].replace(' ', '') == dataVS[1].upper().replace(' ', ''):
                                            dataLuncuran2 = x
                                    syaratTrack2 = list(filter(None, (dataVS[20].split(" ") + dataLuncuran2[9].split(" "))))
                                else:
                                    syaratTrack2 = list(filter(None, (dataVS[20].split(" "))))
                                # cek apakah ada track yang beririsan atau conflict
                                ruteConflict = False
                                for track1 in syaratTrack1:
                                    for track2 in syaratTrack2:
                                        if track1 == track2:
                                            ruteConflict = True

                                ################################ bentuk rute 1 #########################################
                                if ('(S)' in data[1].upper() and not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-AS-SR')) or \
                                    ('(S)' not in data[1].upper() and not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR')):

                                    # jika ada deraileur yang harus rebah -> turunkan deraileur
                                    if '-R' in data[19]:
                                        for deraileur in data[19].split():
                                            if '-R' in deraileur and 'D' in deraileur[0]:
                                                self.modbus.writePBVDU('TBKWM-PB-DI',
                                                                       deraileur.replace('-R', '') + '-PB-DI')
                                                sleep(3)
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 0)
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 1)
                                                sleep(1)

                                    # jika rute emergency -> merahkan track pancingan emergency
                                    if '(E)' in data[1].upper():
                                        self.modbus.writeField(
                                            data[20].split()[-1].replace('T', '') + '-TPR-DI', 0)
                                        sleep(1)

                                    # bentuk rute
                                    self.modbus.writePBVDU(data[2].upper() + '-PB-DI', data[15].upper() + '-PB-DI')
                                    sleep(1)

                                    # jika approach harus jatuh -> merahkan track approach
                                    if data[24]:
                                        self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 0)
                                        sleep(1)

                                    if '(T)' in data[1].upper() or '(S)' in data[1].upper():
                                        # cek ack jpl
                                        for ackJpl in data[25].replace('\n', ' ').split(" "):
                                            if 'JPL' in ackJpl:
                                                sleep(1)
                                                if self.modbus.readVariable(ackJpl + '-PBE-F'):
                                                    self.modbus.writePBVDU(ackJpl + '-PB-DI')
                                                sleep(1)
                                        sleep(1)

                                    if '(E)' in data[1].upper() or '(CF)' in data[1].upper():
                                        # tekan TSD
                                        self.modbus.writePBVDU('TSD-PB-DI', data[2].upper() + '-PB-DI')
                                        sleep(1)

                                        # clearkan track pancingan emergency
                                        self.modbus.writeField(
                                            data[20].split()[-1].replace('T', '') + '-TPR-DI', 1)
                                        sleep(1)

                                ################################ bentuk rute 2 #########################################
                                # jika ada deraileur yang harus rebah -> turunkan deraileur
                                if '-R' in dataVS[19]:
                                    for deraileur in dataVS[19].split():
                                        if '-R' in deraileur and 'D' in deraileur[0]:
                                            self.modbus.writePBVDU('TBKWM-PB-DI', deraileur.replace('-R', '') + '-PB-DI')
                                            sleep(3)
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 0)
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 1)
                                            sleep(1)
                                sleep(1)

                                # bentuk rute
                                self.modbus.writePBVDU(dataVS[2].upper() + '-PB-DI', dataVS[15].upper() + '-PB-DI')
                                sleep(1)

                                if ('(S)' in dataVS[1].upper() and self.modbus.readVariable(dataVS[2].upper() + '-' + simp(dataVS[15].upper()) + '-S-AS-SR')) or \
                                        ('(S)' not in dataVS[1].upper() and self.modbus.readVariable(dataVS[2].upper() + '-' + simp(dataVS[15].upper()) + '-E-AS-SR')):
                                    # jika approach harus jatuh -> merahkan track approach
                                    if dataVS[24]:
                                        self.modbus.writeField(dataVS[23].replace('T', '') + '-TPR-DI', 0)
                                        sleep(1)
                                    if '(T)' in dataVS[1].upper() or '(S)' in dataVS[1].upper():
                                        # cek ack jpl
                                        for ackJpl in dataVS[25].replace('\n', ' ').split(" "):
                                            if 'JPL' in ackJpl:
                                                sleep(1)
                                                if self.modbus.readVariable(ackJpl + '-PBE-F'):
                                                    self.modbus.writePBVDU(ackJpl + '-PB-DI')
                                                sleep(1)
                                        sleep(1)
                                    if '(E)' in dataVS[1].upper() or '(CF)' in dataVS[1].upper():
                                        # tekan TSD
                                        self.modbus.writePBVDU('TSD-PB-DI', dataVS[2].upper() + '-PB-DI')
                                        sleep(1)

                                        # clearkan track pancingan emergency
                                        self.modbus.writeField(
                                            dataVS[20].split()[-1].replace('T', '') + '-TPR-DI', 1)
                                        sleep(1)

                                ####################################### Cek  R1 ########################################
                                R1jatuh = False
                                strRute = data[2].upper() + '-' + simp(data[15].upper())
                                if '(T)' in data[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRute + '-E-AS-SR'):
                                        R1jatuh = True
                                    # cek sinyal
                                    if (data[4] or data[5]) and not self.modbus.readVariable(data[2].upper() + '-CGE-DO'):
                                        R1jatuh = True

                                if '(E)' in data[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRute + '-E-AS-SR'):
                                        R1jatuh = True
                                    # cek sinyal
                                    if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                        R1jatuh = True
                                    if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                        R1jatuh = True

                                if '(CF)' in data[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRute + '-E-AS-SR'):
                                        R1jatuh = True
                                    # cek sinyal
                                    if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                        R1jatuh = True
                                    if data[9] and not self.modbus.readVariable(data[2].upper() + '-CFR-DO'):
                                        R1jatuh = True
                                    if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                        R1jatuh = True

                                if '(S)' in data[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRute + '-S-AS-SR'):
                                        R1jatuh = True
                                    # cek sinyal
                                    if data[7] and not self.modbus.readVariable(data[2].upper() + '-WGE-DO'):
                                        R1jatuh = True
                                sleep(1)

                                ####################################### Cek  R2 ########################################
                                R2jatuh = False
                                strRuteVS = dataVS[2].upper() + '-' + simp(dataVS[15].upper())
                                if '(T)' in dataVS[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRuteVS + '-E-AS-SR'):
                                        R2jatuh = True
                                    # cek sinyal
                                    if (dataVS[4] or dataVS[5]) and not self.modbus.readVariable(dataVS[2].upper() + '-CGE-DO'):
                                        R2jatuh = True

                                if '(E)' in dataVS[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRuteVS + '-E-AS-SR'):
                                        R2jatuh = True
                                    # cek sinyal
                                    if dataVS[6] and not self.modbus.readVariable(dataVS[2].upper() + '-EGE-DO'):
                                        R2jatuh = True
                                    if dataVS[3] and not self.modbus.readVariable(dataVS[2].upper() + '-RGE-DO'):
                                        R2jatuh = True

                                if '(CF)' in dataVS[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRuteVS + '-E-AS-SR'):
                                        R2jatuh = True
                                    # cek sinyal
                                    if dataVS[6] and not self.modbus.readVariable(dataVS[2].upper() + '-EGE-DO'):
                                        R2jatuh = True
                                    if dataVS[9] and not self.modbus.readVariable(dataVS[2].upper() + '-CFR-DO'):
                                        R2jatuh = True
                                    if dataVS[3] and not self.modbus.readVariable(dataVS[2].upper() + '-RGE-DO'):
                                        R2jatuh = True

                                if '(S)' in dataVS[1].upper():
                                    # cek syarat subroute
                                    if not self.modbus.readVariable(strRuteVS + '-S-AS-SR'):
                                        R2jatuh = True
                                    # cek sinyal
                                    if dataVS[7] and not self.modbus.readVariable(dataVS[2].upper() + '-WGE-DO'):
                                        R2jatuh = True
                                sleep(1)

                                ####################################### Cek Conflict ###################################
                                def cekRuteBlock(data):
                                    error = ""
                                    if '(CF)' in data[1].upper():
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-B'):
                                            error = data[2].upper() + '-' + simp(data[15].upper()) + '-CF-B jatuh, '
                                    else:
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-B'):
                                            error = data[2].upper() + '-' + simp(data[15].upper()) + '-B jatuh, '
                                    return error
                                def cekRuteLock(data):
                                    error = ""
                                    if '(S)' in data[1].upper():
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-L'):
                                            error = data[2].upper() + '-' + simp(data[15].upper()) + '-S-L jatuh, '
                                    elif '(CF)' in data[1].upper():
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-CF-E-L'):
                                            error = data[2].upper() + '-' + simp(
                                                data[15].upper()) + '-CF-E-L jatuh, '
                                    else:
                                        if not self.modbus.readVariable(
                                                data[2].upper() + '-' + simp(data[15].upper()) + '-E-L'):
                                            error = data[2].upper() + '-' + simp(data[15].upper()) + '-E-L jatuh, '
                                    return error

                                def cekSinyal(data):
                                    error = ""
                                    if '(T)' in data[1].upper():
                                        # cek syarat subroute
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR'):
                                            error += data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR jatuh, '
                                        # cek sinyal
                                        if (data[4] or data[5]) and not self.modbus.readVariable(
                                                data[2].upper() + '-CGE-DO'):
                                            R1jatuh = True
                                        if data[8] and not self.modbus.readVariable(data[2].upper() + '-SR-DO'):
                                            R1jatuh = True
                                        if data[10] and not self.modbus.readVariable(data[2].upper() + '-LDR-DO'):
                                            R1jatuh = True
                                        if data[11] and not self.modbus.readVariable(data[2].upper() + '-RDR-DO'):
                                            R1jatuh = True

                                    if '(E)' in data[1].upper():
                                        # cek syarat subroute
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR'):
                                            error += data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR jatuh, '
                                        # cek sinyal
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-ER-DO'):
                                            R1jatuh = True
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                            R1jatuh = True
                                        if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                            R1jatuh = True

                                    if '(CF)' in data[1].upper():
                                        # cek syarat subroute
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR'):
                                            error += data[2].upper() + '-' + simp(data[15].upper()) + '-E-AS-SR jatuh, '
                                        # cek sinyal
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-ER-DO'):
                                            R1jatuh = True
                                        if data[6] and not self.modbus.readVariable(data[2].upper() + '-EGE-DO'):
                                            R1jatuh = True
                                        if data[9] and not self.modbus.readVariable(data[2].upper() + '-CFR-DO'):
                                            R1jatuh = True
                                        if data[3] and not self.modbus.readVariable(data[2].upper() + '-RGE-DO'):
                                            R1jatuh = True

                                    if '(S)' in data[1].upper():
                                        # cek syarat subroute
                                        if not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S-AS-SR'):
                                            error += data[2].upper() + '-' + simp(data[15].upper()) + '-S-AS-SR jatuh, '
                                        # cek sinyal
                                        if data[7] and not self.modbus.readVariable(data[2].upper() + '-' + simp(data[15].upper()) + '-S'):
                                            R1jatuh = True
                                        if data[7] and not self.modbus.readVariable(data[2].upper() + '-GR-DO'):
                                            R1jatuh = True
                                        if data[7] and not self.modbus.readVariable(data[2].upper() + '-WGE-DO'):
                                            R1jatuh = True

                                if ruteConflict:
                                    if R1jatuh and not R2jatuh:
                                        error += 'Rute Versus menjatuhkan Rute Utama -> seharusnya tidak, '
                                        error += cekRuteBlock(data)
                                        error += cekRuteLock(data)
                                    elif not R1jatuh and not R2jatuh:
                                        error += 'Rute Versus seharusnya tidak terbentuk, '
                                    elif R1jatuh and R2jatuh:
                                        error += 'Rute Versus menjatuhkan Rute Utama -> seharusnya tidak, '
                                        error += cekRuteBlock(data)
                                        error += cekRuteLock(data)
                                else:
                                    if R1jatuh and not R2jatuh:
                                        error += 'Rute Versus menjatuhkan Rute Utama  -> seharusnya tidak, '
                                        error += cekRuteBlock(data)
                                        error += cekRuteLock(data)
                                    elif not R1jatuh and R2jatuh:
                                        error += 'Rute Versus tidak terbentuk  -> seharusnya keduanya terbentuk, '
                                        error += cekRuteBlock(dataVS)
                                        error += cekRuteLock(dataVS)
                                    elif R1jatuh and R2jatuh:
                                        error += 'Kedua rute terhapus -> seharusnya keduanya terbentuk, '
                                        error += cekRuteBlock(data)
                                        error += cekRuteBlock(dataVS)
                                        error += cekRuteLock(data)
                                        error += cekRuteLock(dataVS)

                                ###################################### Clearence R2 ####################################
                                # jika approach harus jatuh -> merahkan track approach
                                if dataVS[24]:
                                    self.modbus.writeField(dataVS[23].replace('T', '') + '-TPR-DI', 1)
                                    sleep(1)

                                # hapus rute
                                self.modbus.writePBVDU('TPR-PB-DI', dataVS[2].upper() + '-PB-DI')
                                sleep(1)

                                # jika ada deraileur yang harus rebah -> naikan deraileur
                                if '-R' in dataVS[19]:
                                    for deraileur in dataVS[19].split():
                                        if '-R' in deraileur and 'D' in deraileur[0] and 'D' in deraileur[0]:
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 1)
                                            self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 0)
                                            # jika track emergency -> clearkan track tujuan

                                # tunggu sampai rute terhapus
                                while not self.modbus.readVariable(dataVS[2].upper() + ('-T' if '(T)' in dataVS[1].upper() else
                                ('-S' if '(S)' in dataVS[1].upper() else '-E')) + '-AS'):
                                    sleep(1)

                                print(error)
                                if error:
                                    count += 1
                                    errorLog += [[count, data[1].upper() + ' VS ' + dataVS[1].upper(), error, '']]

                                if self.stopTest:
                                    break

                                ###################################### Clearence R1 ####################################
                                if R1jatuh or '(E)' in data[1] or '(CF)' in data[1]:
                                    # jika approach harus jatuh -> clearkan track approach
                                    if data[24]:
                                        self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                                        sleep(1)

                                    # hapus rute
                                    self.modbus.writePBVDU('TPR-PB-DI', data[2].upper() + '-PB-DI')
                                    sleep(1)

                                    # jika ada deraileur yang harus rebah -> naikan deraileur
                                    if '-R' in data[19]:
                                        for deraileur in data[19].split():
                                            if '-R' in deraileur and 'D' in deraileur[0]:
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 1)
                                                self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 0)
                                                # jika track emergency -> clearkan track tujuan

                                    # tunggu sampai rute terhapus
                                    while not self.modbus.readVariable(
                                            data[2].upper() + ('-T' if '(T)' in data[1].upper() else
                                            ('-S' if '(S)' in data[1].upper() else '-E')) + '-AS'):
                                        sleep(1)

                                    if self.stopTest:
                                        self.stopTest = 0
                                        break

                        ###################################### Clearence R1 ####################################
                        # jika approach harus jatuh -> clearkan track approach
                        if data[24]:
                            self.modbus.writeField(data[23].replace('T', '') + '-TPR-DI', 1)
                            sleep(1)

                        # hapus rute
                        self.modbus.writePBVDU('TPR-PB-DI', data[2].upper() + '-PB-DI')
                        sleep(1)

                        # jika ada deraileur yang harus rebah -> naikan deraileur
                        if '-R' in data[19]:
                            for deraileur in data[19].split():
                                if '-R' in deraileur and 'D' in deraileur[0]:
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-NKR-DI', 1)
                                    self.modbus.writeField(deraileur.replace('-R', '') + '-RKR-DI', 0)
                                    # jika track emergency -> clearkan track tujuan

                        # tunggu sampai rute terhapus
                        while not self.modbus.readVariable(data[2].upper() + ('-T' if '(T)' in data[1].upper() else
                        ('-S' if '(S)' in data[1].upper() else '-E')) + '-AS'):
                            sleep(1)

                        if self.stopTest:
                            self.stopTest = 0
                            break

                    # Simpan Error log ke file
                    file, check = QFileDialog.getSaveFileName(None, "QFileDialog getSaveFileName() Demo",
                                                                  "Error Log Conflict Route.xlsx",
                                                                  "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
                    if check:
                        dfFI = pd.DataFrame(errorLog, columns=['NO', 'Rute', 'Temuan','Perbaikan'])
                        dfFI.to_excel(file, index=False)

                self.start = 0

    # function untuk memulai pengetesan Rute dengan memberi informasi data pengetesan dan jenis pengetesan
    def startRun(self, IT1, IT2, testMode = [0, 0, 0, 0, 0], startRoute = "0", finishRoute = "0", startRoute2 = "0", finishRoute2 = "0"):

        # menyimpan data IT1 dan IT untuk keperluan di masa yang akan datang
        self.IT1 = IT1
        self.IT2 = IT2

        # function untuk memodifikasi nama sinyal tujual supaya sesuai dengan variable, contoj J10-JL12B => J10-12B
        mod = lambda a: a.replace('J', '').replace('JL', '').replace('L', '')

        # function menentukan jenis rute
        def ruteTipe(namaRute):
            if '(T)' in namaRute:
                jenisRute = 'Normal'
            elif '(E)' in namaRute:
                jenisRute = 'Emergency'
            elif '(CF)' in namaRute:
                jenisRute = 'Contra Flow'
            elif '(S)' in namaRute:
                jenisRute = 'Langsir'
            return jenisRute

        # function memfilter rute


        # variable untuk menyimpan data dictionary dari IT
        self.IT = []

        # function untuk konversi data IT menjadi list berisi dictionary data IT
        for data in IT1:
            # data dari IT1 di conversi kedalam dictionary
            dictData = {"No Rute": data[0], "Nama Rute": data[1], "Sinyal Asal": data[2], "Aspek Merah": data[3],
                        "Aspek Kuning": data[4], "Aspek Hijau": data[5], "Emergency": data[6], "Kecepatan": data[7],
                        "Contraflow": data[8], "Arah Kiri": data[9], "Arah Kanan": data[10], "Sinyal Muka": data[11],
                        "Sinyal Muka Aspek Kuning": data[12], "Sinyal Muka Aspek Hijau": data[13],
                        "Nama Stasiun Tujuan": data[14], "Sinyal Tujuan": data[15], "Sinyal Tujuan MOD": mod(data[15]), "Nama Stasiun": data[16],
                        "Prooving Aspek Sinyal Tujuan": data[17], "Syarat Wesel Rute": data[18], "Syarat Deraileur Rute": data[18],
                        "Syarat Track Rute": data[19], "Langsir Antara": data[20], "Opposing Signal Rute": data[21],
                        "Track Approach": data[22], "Butuh pproach": data[23], "Remark Rute": data[24], "Jenis Rute": ruteTipe(data[1]), "Rute": data[1]}
            # function untuk menambah data IT dengan tambahan informasi luncuran
            for dataIT2 in IT2:
                if dataIT2[1].upper() == dictData["Nama Rute"]:
                    dictData["Signal Flank Rute"] = dataIT2[4]
                    dictData["Track Flank Rute"] = dataIT2[5]
                    dictData["Syarat Wesel Luncuran"] = dataIT2[7]
                    dictData["Syarat Deraileur Luncuran"] = dataIT2[8]
                    dictData["Syarat Track Luncuran"] = dataIT2[9]
                    dictData["Opposing Signal Luncuran"] = data[10]
                    dictData["Signal Flank Luncuran"] = dataIT2[12]
                    dictData["Track Flank Luncuran"] = dataIT2[13]
                    dictData["Remark Luncuran"] = dataIT2[14]
            # data dari dictionary tadi di simpan di variable dalam bentuk list
            self.IT.append(dictData)

        # mode pegetesan => 0:FT | 1:IT | 2:CR | 3:VT | 4:DT
        # khusus function test nilainya di konversi berdasarkan jenis pengetesan detailnya
        self.FTTest = testMode[0]
        self.ITTest = testMode[1]
        self.CRTest = testMode[2]
        self.VTTest = testMode[3]
        self.DTTest = testMode[4]

        # jika ada perintah pengetesan maka mulai pengetesan
        if sum(testMode):
            self.start = 1
            self.stopTest = 0

        # variable untuk memaksa menyudahi pengetesan
        self.startRoute = int(startRoute) - 1
        if finishRoute.upper().replace(' ', '') == "MAX":
            self.finishRoute = len(self.IT1)
        else:
            self.finishRoute = int(finishRoute)

        self.startRoute2 = int(startRoute2) - 1
        if finishRoute2.upper().replace(' ', '') == "MAX":
            self.finishRoute2 = len(self.IT1)
        else:
            self.finishRoute2 = int(finishRoute2)

    def addonData(self, dataTambahan):
        self.PM = dataTambahan[0]
        self.TRACK = dataTambahan[1]
        self.ruteCTRL = dataTambahan[2]
        self.ruteE = dataTambahan[3]
        self.inputData = dataTambahan[4]
        self.outputData = dataTambahan[5]
        self.internalData = dataTambahan[6]

    def filter(self, listData, textFilter1):
        dataOutput = []
        for data in listData:
            if textFilter1 in data:
                dataOutput += data
        return dataOutput

    # function untuk mengubah varible perintah stop pengetesan
    def stopTesting(self):
        self.stopTest = 1