import pandas as pd
import numpy as np
import csv
import math

ITaddress = "C:\File Ikhsan\Development\Testing Automation\Interlocking Table THB REV02 - TESTINGBOT.xlsx"
VDUctrlAddress = 'C:\File Ikhsan\Development\Testing Automation\\13. REGISTER - FROM VDU.csv'
startCtrlVDU = 28
startInputField = 37
startOutputField = 500

simp = lambda a: a.replace('J', '').replace('JL', '').replace('L', '')

def readVDUCTRL(addres):
    rows = []
    with open(addres, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    dataVDUctrl = []
    count = 0
    for x, d in enumerate(rows):
        if len(d) != 0 and d[0] == '' and d[1] != '-':
            dataVDUctrl.append(['0_MODBUS_FROM_VDUX_' + str((count) // 16), d[1], d[2], 0, 0.0])
            count += 1
    return dataVDUctrl

# function to extract data for generating data testing dan register hima
def ITdata(address):
    # Read Excel File to data frame
    IT1df = pd.read_excel(address, sheet_name='IT 1')
    IT2df = pd.read_excel(address, sheet_name='IT 2')
    RUTEdf = pd.read_excel(address, sheet_name='RUTE')
    SIGNALdf = pd.read_excel(address, sheet_name='SIGNAL')
    PMdf = pd.read_excel(address, sheet_name='POINT MACHINE')
    TRACKdf = pd.read_excel(address, sheet_name='TRACK')
    BLOKdf = pd.read_excel(address, sheet_name='BLOK')
    JPLdf = pd.read_excel(address, sheet_name='JPL')

    # Convert data frame to excel and change the nan value
    IT1 = [[(str(str(x).strip().upper()) if str(x) != 'nan' else '') for x in d] for d in IT1df.values.tolist()]
    IT2 = [[(str(str(x).strip().upper()) if str(x) != 'nan' else '') for x in d] for d in IT2df.values.tolist()]
    RUTE = [[(str(str(x).strip().upper()) if str(x) != 'nan' else '') for x in d] for d in RUTEdf.values.tolist()]
    SIGNAL = [[d[0]] + [(int(x) if str(x) != 'nan' else 0) for x in d[1:]] for d in SIGNALdf.values.tolist()]
    PM = [[(str(str(x).strip().upper()) if str(x) != 'nan' else '') for x in d] for d in PMdf.values.tolist()]
    TRACK = [[(str(str(x).strip().upper()) if str(x) != 'nan' else '') for x in d] for d in TRACKdf.values.tolist()]
    BLOK = [[(str(str(x).strip().upper()) if str(x) != 'nan' else '') for x in d] for d in BLOKdf.values.tolist()]
    JPL = [[(str(str(x).strip().upper()) if str(x) != 'nan' else '') for x in d] for d in JPLdf.values.tolist()]

    return IT1, IT2, RUTE, SIGNAL, PM, TRACK, BLOK, JPL

# function for generating variable register from and to FIELD simulator
def genVar(RUTE, SIGNAL, PM, TRACK, BLOK, JPL):
    # variables for output of this class
    dataInput = ['VDR-DI', 'FAN-STATE-DI', 'PSU1-STATE-DI', 'PSU2-STATE-DI', 'PLN-IN', 'UPS-IN', 'GENSET-IN',
                 'GENSET-START-FAIL', 'GENSET-LOW-FUEL', 'UPS-INVERTER-FAIL', 'UPS-LOWBATT']
    dataOutput = ['FLASH', 'FLASH-500MS', 'RR-CTRL', 'RR', 'RR-OK', 'EAST-AS', 'WEST-AS', 'RRLS', 'SWRLS','AA-CTRL',
                  'AA-BZ-F', 'AA-BZ-DO', 'THB-PBE-F', 'THB-PBE-DO', 'TPR-BANTU-PBE', 'TPR-BANTU-PBE-F',
                  'TPR-BANTU-PBE-DO', 'VDR-DO', 'SYSTEM-FE', 'SYSTEM-FE-F', 'SYSTEM-FE-DO',
                  'CPR-PSU1-OK', 'CPR-PSU2-OK', 'WARNING-OK', 'WARNING-FE', 'WARNING-FE-F', 'WARNING-FE-DO', 'NV-V-OK',
                  'COMM-PLC', 'COMM-OK', 'COMM-FE', 'COMM-FE-F', 'COMM-FE-DO', 'LOGGER-V-CHK', 'V-LOGGER-CHK',
                  'LOGGER-V-OK', 'LOGGER-FE', 'LOGGER-FE-F', 'LOGGER-FE-DO', 'SWITCH-FE', 'SWITCH-FE-F', 'SWITCH-FE-DO',
                  'SIGNAL-FE', 'SIGNAL-FE1', 'SIGNAL-FE2', 'SIGNAL-FE3', 'SIGNAL-FE4',
                  'SIGNAL-FE5', 'SIGNAL-FE6', 'SIGNAL-FE-F', 'SIGNAL-FE-F1', 'SIGNAL-FE-F2', 'SIGNAL-FE-F3',
                  'SIGNAL-FE-F4', 'SIGNAL-FE-F5', 'SIGNAL-FE-F6', 'SIGNAL-FE-DO', 'DIR-FE', 'DIR-FE1', 'DIR-FE2',
                  'DIR-FE3', 'DIR-FE4', 'DIR-FE5', 'DIR-FE6', 'DIR-FE-F', 'DIR-FE-F1', 'DIR-FE-F2', 'DIR-FE-F3',
                  'DIR-FE-F4', 'DIR-FE-F5', 'DIR-FE-F6', 'DIR-FE-DO', 'PB-FAIL', 'PB-FE', 'PB-FE-F', 'PB-FE-DO',
                  'SUPPLY-PLN-DO', 'SUPPLY-UPS-DO', 'SUPPLY-GENSET-DO', 'PS-NORM-DO', 'PS-FE', 'PS-FE-F', 'PS-FE-DO',
                  'GEN-FAIL', 'GEN-F-A', 'GENSET-START-DO', 'GENSET-EMPTY-DO', 'UPS-FAIL', 'UPS-F-A', 'UPS-INVERTER-DO',
                  'UPS-LOWBATT-DO', 'CTC-NV-OK', 'TERPUSAT', 'TERPUSAT-F', 'TERPUSAT-DO', 'SETEMPAT', 'SETEMPAT-F',
                  'SETEMPAT-DO', 'LAMPTEST', 'LAMPTEST-PB-OK', 'LAMP-G', 'LAMP-Y', 'LAMP-R', 'LAMP-W', 'LAMP-PB',
                  'TESTBUZZER', 'TPR-COUNT-DO', 'TSD-COUNT-DO', 'TBMS-COUNT-DO', 'TWT-COUNT-DO', 'TBW-COUNT-DO']
    dataInternal = []
    # 'TBKM-COUNT-DO', 'TPB-COUNT-DO'

    ################################################## RUTE ##########################################################
    # base generator variable
    addROutputEoCF = ['-CTRL', '-RS', '-E-REQ', '-E-COUNT', '-E-RST-TE', '-B', '-E-L', '-E', '-E-AS-SR']
    # list signal with 3 aspect and green signal
    signal3Aspek = ' '.join([s[0] for s in SIGNAL if s[1] and s[2] and s[3]])
    signalGreen = ' '.join([s[0] for s in SIGNAL if s[3]])
    signalYellow = ' '.join([s[0] for s in SIGNAL if s[2]])
    blokWhr = ' '.join([b[0] for b in BLOK if b[6]])
    """
    '-CTRL', '-CF-CTRL', '-RS', '-CF-RS', '-E-REQ', '-E-COUNT', '-E-RST-TE', '-CF-E-REQ', '-CF-E-COUNT',
    '-CF-E-RST-TE', '-T-REQ', ", '-S-REQ', '-B', '-CF-B', '-P', '-E-L', '-CF-E-L', '-T-L', '-S-L', '-E',
    '-CF-E', '-H', #'-D', '-S', '-E-AS-SR', '-CF-E-AS-SR', '-S-AS-SR'
    Langsir antara
    '$rute$-2-RS', '$rute$-S-2-REQ', '$rute$-S-2-L', '$rute$-2-S', '$rute$-INT-PAR', '``-INT-AS',
    """
    # generator variable rute
    # | 0:SINYAL ASAL | 1:SINYAL TUJUAN | 2:JENIS RUTE | 3:LANGSIR ANTARA | 4:LANGSUNGAN |
    dataOutput += [r[0] + '-' + simp(r[1]) + '-H' for r in RUTE if (r[0] in signalYellow) and ('T' in r[2])]
    dataOutput += [r[0] + '-' + simp(r[1]) + add for add in ['-D', '-D-REQ'] for r in RUTE if ((r[0] in signal3Aspek) and r[4]) and ('A' != r[1][0])]
    dataOutput += [r[0] + '-' + r[1] + add for add in ['-D', '-D-REQ'] for r in RUTE if ((r[1] in blokWhr) and ('A' == r[1][0])) and (r[0] in signal3Aspek)]
    dataOutput += [r[0] + '-' + simp(r[1]) + out for out in ['-T-REQ', '-P', '-T-L'] for r in RUTE if 'T' in r[2]]
    dataOutput += [r[0] + '-' + simp(r[1]) + out for out in addROutputEoCF for r in RUTE if 'T' in r[2] or 'E' in r[2]]
    dataOutput += [r[0] + '-' + simp(r[1]) + '-CF' + out for out in addROutputEoCF for r in RUTE if 'CF' in r[2]]
    dataOutput += [r[0] + '-' + simp(r[1]) + out for out in ['-S-REQ', '-S-L', '-S', '-S-AS-SR', '-CTRL', '-B', '-RS'] for r in RUTE if 'S' in r[2]]
    # list of signal langsir antara
    LASignal = list(set(' '.join([r[3] for r in RUTE if r[3]]).split()))
    for la in LASignal:
        dataOutput += [la + '-' + simp(r[1]) + out for out in ['-2-RS', '-S-2-REQ', '-S-2-L', '-2-S', '-INT-PAR'] for r in RUTE if la in r[3]]
    dataOutput += [r + '-INT-AS' for r in LASignal]

    ################################################## SIGNAL ##########################################################
    # signal  generator
    # list signal with 3 aspect
    signal3Aspek = ' '.join([s[0] for s in SIGNAL if s[1] and s[2] and s[3]])
    siggnalTUR = ' '.join([r[0] for r in RUTE if 'TUR' in r[4]])
    signalDestination = ' '.join([r[1] for r in RUTE])
    signalStart = ' '.join([r[0] for r in RUTE])
    addSInput = ['-ER-DI', '-SR-DI', '-GR-DI', '-CFR-DI', '-RDR-DI', '-LDR-DI']
    addSOutputAspect = ['-ER-DO', '-SR-DO', '-GR-DO', '-CFR-DO', '-RDR-DO', '-LDR-DO']
    addSOutputINDR = ['-RGE', '-RGE-F', '-RGE-DO']
    addSOutputINDG = ['-CGE', '-CGE-F', '-CGE-DO']
    addSOutputINDCF = ['-CFGE', '-CFGE-F', '-CFGE-DO']
    addSOutputLangsungan = ['-EC-R-RD', '-EC-G-Y-TE', '-EC-Y-RD', '-EC-G-RD']
    addSOutputTUR = ['-F-CTRL', '-F-RS']
    """
    '-ECR-DI', '-ECR', '-ECRF', '-FAIL-A', '-FF-TE', '-HR-RST', '-DR-RST', '-EKR-DI', '-EKR', '-EKR-A', '-EK-TE',
    '-SECR-DI', '-SECR', '-SECRF', '-S-FAIL-A', '-I3-FF-TE', '-CFEK-DI', '-CFEK', '-CFRF', '-CF-FAIL-A', '-CF-TE',
    '-DKR-DI', '-DKR', '-RKRF', '-LKRF', '-RKR-A', '-LKR-A', '-RK-TE', '-LK-TE', '-E-AS', '-T-AS', '-S-AS',
    '-RST-CTRL', '-RST-CT', 
    TPR RRLS 
    '-RRLSPB-CTRL', '-RRLS', '-RRLS-TE', '-RRLS-CT', 
    PB 
    '-PB-DI', '-PBE', '-PBE-F', '-PBE-DO', 'TSD', '-E-CTRL',
    IND
    '-RGE', '-RGE-F', '-RGE-DO', '-CGE', '-CGE-F', '-CGE-DO', #'-EGE-DO', '-CFGE', '-CFGE-F', '-CFGE-DO', '-WGE-DO',
    '-HR-RD', '-DR-RD', '-ER-RD', '-GR-RD', 
    LANGSUNGAN
    '-EC-R-RD', '-EC-G-Y-TE', '-EC-Y-RD', '-EC-G-RD', '-F-CTRL', '-F-RS',
    """

    # | 0:NAMA SINYAL |	1:R | 2:Y |	3:G | 4:E | 5:Speed | 6:Langsir | 7:CF | 8.Dir-R | 8:Dir-L |
    dataInput += [s[0] + '-ECR-DI' for s in SIGNAL if (s[1] or s[2] or s[3]) and s[0][0] != 'L']
    dataInput += [s[0] + '-EKR-DI' for s in SIGNAL if (s[1] or s[2] or s[3]) and s[0][0] != 'L']
    dataInput += [s[0] + '-SECR-DI' for s in SIGNAL if s[5]]
    dataInput += [s[0] + '-CFEK-DI' for s in SIGNAL if s[7]]
    dataInput += [s[0] + '-HR-DI' for s in SIGNAL if s[1] and s[2]]
    dataInput += [s[0] + '-DR-DI' for s in SIGNAL if s[1] and s[3]]

    dataInternal += [s[0] + '-ECR-R' for s in SIGNAL if s[1]]
    dataInternal += [s[0] + '-ECR-Y' for s in SIGNAL if s[2]]
    dataInternal += [s[0] + '-ECR-G' for s in SIGNAL if s[3]]
    dataInternal += [s[0] + '-EKR' for s in SIGNAL if s[1] or s[2] or s[3]]
    dataInternal += [s[0] + '-SECR' for s in SIGNAL if s[5]]
    dataInternal += [s[0] + '-CFEK' for s in SIGNAL if s[7]]
    dataInternal += [s[0] + '-DKR' for s in SIGNAL if s[8] or s[9]]

    for s in SIGNAL:
        dataInput += [s[0] + adds for index, adds in enumerate(addSInput) if s[index+4]]
        dataOutput += [s[0] + adds for index, adds in enumerate(addSOutputAspect) if s[index + 4]]

    dataOutput += [s[0] + '-GR-RD' for s in SIGNAL if s[6]]
    dataOutput += [s[0] + '-HR-DO' for s in SIGNAL if s[1] and s[2]]
    dataOutput += [s[0] + '-DR-DO' for s in SIGNAL if s[1] and s[3]]
    dataOutput += [s[0] + '-HR-RD' for s in SIGNAL if s[1] and s[2] and 'IB' not in s[0]]
    dataOutput += [s[0] + '-DR-RD' for s in SIGNAL if s[1] and s[3] and 'IB' not in s[0]]
    dataOutput += [s[0] + '-ER-RD' for s in SIGNAL if s[1] and (s[2] or s[3]) and s[0][0] != 'L' and 'IB' not in s[0]]

    dataOutput += [s[0] + ind for ind in addSOutputINDR for s in SIGNAL if s[1] and s[0][0] != 'L']
    dataOutput += [s[0] + ind for ind in addSOutputINDG for s in SIGNAL if s[2] or s[3]]
    dataOutput += [s[0] + ind for ind in addSOutputINDCF for s in SIGNAL if s[7]]
    dataOutput += [s[0] + '-EGE-DO' for s in SIGNAL if s[4]]
    dataOutput += [s[0] + '-WGE-DO' for s in SIGNAL if s[6]]
    dataOutput += [s[0] + ind for ind in addSOutputLangsungan for s in SIGNAL if (s[0] in signal3Aspek) and 'IB' not in s[0]]
    dataOutput += [s[0] + ind for ind in addSOutputTUR for s in SIGNAL if s[0] in siggnalTUR]

    dataOutput += [s[0] + '-B' for s in SIGNAL if not s[6] and s[0][0] != 'X' and s[1] and (s[2] or s[3]) and 'IB' not in s[0]]
    dataOutput += [s[0] + '-S-B' for s in SIGNAL if s[6]]
    dataOutput += [s[0] + '-D-B' for s in SIGNAL if s[1] and s[2] and s[3] and 'IB' not in s[0]]
    dataOutput += [s[0] + out for out in ['-ECR', '-FAIL-A', '-FF-TE', '-EKR', '-EKR-A', '-EK-TE']
                   for s in SIGNAL if (s[1] or s[2] or s[3]) and s[0][0] != 'L']
    dataOutput += [s[0] + '-ECRF' for s in SIGNAL if (s[1] or s[2] or s[3]) and s[0][0] != 'L' and 'MJ' not in s[0]]
    dataOutput += [s[0] + out for out in ['-SECR', '-SECRF', '-S-FAIL-A', '-I3-FF-TE'] for s in SIGNAL if s[5]]
    dataOutput += [s[0] + out for out in ['-CFEK', '-CF-FAIL-A', '-CF-TE'] for s in SIGNAL if s[7]]
    dataOutput += [s[0] + out for out in ['-DKR'] for s in SIGNAL if s[8] or s[9]]
    dataOutput += [s[0] + out for out in ['-RKR-A', '-RK-TE'] for s in SIGNAL if s[8]]
    dataOutput += [s[0] + out for out in ['-LKR-A', '-LK-TE'] for s in SIGNAL if s[9]]
    dataOutput += [s[0] + '-E-AS' for s in SIGNAL if s[4] and s[0] in signalStart]
    dataOutput += [s[0] + '-T-AS' for s in SIGNAL if (s[1] and (s[2] or s[3])) and s[0][0] != 'L' and s[0] in signalStart]
    dataOutput += [s[0] + '-S-AS' for s in SIGNAL if s[6] and s[0] in signalStart]
    dataOutput += [s[0] + add for add in ['-PBE', '-PBE-F', '-PBE-DO', '-RST-CTRL', '-RST-CT'] for s in SIGNAL if s[0] in signalStart]
    dataOutput += [s[0] + add for add in ['-RRLSPB-CTRL', '-RRLS', '-RRLS-TE', '-RRLS-CT'] for s in SIGNAL if s[0] in signalDestination]
    dataOutput += [s[0] + out for out in ['-E-CTRL'] for s in SIGNAL if s[4]]
    dataOutput += [s[0] + '-HR-RST' for s in SIGNAL if 'IB' in s[0] and s[2]]
    dataOutput += [s[0] + '-DR-RST' for s in SIGNAL if 'IB' in s[0] and s[3]]

    ################################################## WESEL ########################################################## OK
    # Wesel
    # base generator variable
    addWOutput = ['-B-N', '-B-R', '-P-N', '-P-R', '-RS-N', '-RS-R', '-OL-N', '-OL-R', '-N-REQ', '-R-REQ',
               '-SWINIT', '-START', '-L', '-LS', '-N', '-R', '-N-BLOCK', '-R-BLOCK',
               '-N-FAIL', '-R-FAIL', '-BACK-TO-N', '-BACK-TO-R', '-NWC', '-RWC', '-NWP', '-RWP', '-NWZ', '-RWZ',
               '-NWZ-CALL', '-RWZ-CALL', '-NW-TE', '-RW-TE', '-PB-DI', '-TRAIL-CTRL', '-TRAIL-CTRL-Z',
               '-CAL-CTRL', '-SWRLSPB-CTRL', '-SWRLS', '-TPZ', '-B-CTRL', '-BLOCK', '-RST-CTRL', '-OOC', '-OOC-CALL',
               '-OOC-RD', '-SW-FAIL', '-SW-F-ACK', '-NWR-DO', '-RWR-DO', '-WLPR-DO']
    addWOutputInd = ['-BE', '-BE-F', '-BE-DO', '-LE', '-LE-F', '-LE-DO', '-NWE', '-NWE-F',
               '-NWE-DO', '-NWTE', '-NWTE-F', '-NWTE-DO', '-NRE-DO', '-NTE-DO', '-RWE', '-RWE-F', '-RWE-DO', '-RWTE',
               '-RWTE-F', '-RWTE-DO', '-RTE-DO', '-RRE-DO']
    addDOutput = ['-NPR-DO', '-NP', '-RP', '-REL-REQ', '-R-N', '-R-OK', '-FAIL', '-FAIL-A', '-FAIL-ACK',
                  '-B-CTRL', '-BE', '-BE-DO', '-BE-F', '-RST-CTRL']
    # Split Wesel and Deraileur
    WESEL = [p for p in PM if p[0][0] == 'W']
    DERAILEUR = [p for p in PM if p[0][0] == 'D']

    # generator variable PM
    # | 0:WESEL | 1:TRACK |
    dataInput += [d[0] + inp for inp in ['-NKR-DI', '-RKR-DI'] for d in DERAILEUR]
    dataInput += [w[0] + inp for inp in ['-NWP-DI', '-RWP-DI'] for w in WESEL]

    dataOutput += [d[0] + out for out in addDOutput for d in DERAILEUR]
    dataOutput += [w[0] + out for out in addWOutput for w in WESEL]
    for w in WESEL:
        if '/' in w[0]:
            for d in list(w[0].replace('W', '').split("/")):
                dataOutput += ['W' + d + add for add in addWOutputInd]
        else:
            dataOutput += [w[0] + add for add in addWOutputInd]

    dataInternal += [w[0] + add for add in ['-SNP', '-SRP', '-NOB', '-ROB', '-TRL'] for w in WESEL]

    ################################################## Track ##########################################################
    # base generator variable
    addTOutput = ['-TP', '-TE-DO', '-RE-DO']
    """
    OS TRACK
    '-TPBP', '-E-WS-RL', '-T-WS-RL', '-S-WS-RL', '-E-ES-RL', '-T-ES-RL', '-S-ES-RL',
    SUBROUTE
    '-RLS', '-E-WS', '-T-WS', '-S-WS', '-E-ES', '-T-ES', '-S-ES',
    LUNCURAN
    '-T-WLAS', '-T-ELAS',
    """
    # generator variable track
    # | 0:NAMA | 1:OS TRACK WEST | 2:OS TRACK EAST | 3:SUBROUTE WEST | 4:SUBROUTE EAST | 5:LUNCURAN |
    dataInput += [t[0] + '-TPR-DI' for t in TRACK]

    dataOutput += [t[0] + out for out in addTOutput for t in TRACK]
    dataOutput += [t[0] + '-TPBP' for t in TRACK if t[1] or t[2]]
    dataOutput += [t[0] + '-E-WS-RL' for t in TRACK if 'E' in t[1]] + [t[0] + '-T-WS-RL' for t in TRACK if
                                                                       'T' in t[1]] + [t[0] + '-S-WS-RL' for t in TRACK
                                                                                       if 'S' in t[1]]
    dataOutput += [t[0] + '-E-ES-RL' for t in TRACK if 'E' in t[2]] + [t[0] + '-T-ES-RL' for t in TRACK if
                                                                       'T' in t[2]] + [t[0] + '-S-ES-RL' for t in TRACK
                                                                                       if 'S' in t[2]]
    dataOutput += [t[0] + '-RLS' for t in TRACK if t[3] or t[4]]
    dataOutput += [t[0] + '-E-WS' for t in TRACK if 'E' in t[3]] + [t[0] + '-T-WS' for t in TRACK if 'T' in t[3]] + [
        t[0] + '-S-WS' for t in TRACK if 'S' in t[3]]
    dataOutput += [t[0] + '-E-ES' for t in TRACK if 'E' in t[4]] + [t[0] + '-T-ES' for t in TRACK if 'T' in t[4]] + [
        t[0] + '-S-ES' for t in TRACK if 'S' in t[4]]
    dataOutput += [t[0] + '-T-ELAS' for t in TRACK if 'E' in t[5]] + [t[0] + '-T-WLAS' for t in TRACK if 'W' in t[5]]

    ################################################## BLOK ##########################################################
    # base generator variable
    signalAspek = ' '.join([s[0] for s in SIGNAL if s[1] or s[2] or s[3]])
    addBOutput = ['-PBE', '-PBE-F', '-PBE-DO', '-RRLSPB-CTRL', '-RRLS', '-RRLS-TE', '-RRLS-CT', '-AA', '-ATE',
                  '-ATE-F', '-ATE-DO', '-BZ-TE', '-BLOK-FAIL']
    addBOutputCommon = ['FE', 'FE-F', 'FE-DO', 'FLE', 'FLE-F', 'FLE-DO']
    """
    COMMON
    '-WTP', '-ETP', '-WS', '-ES', '-WFE', '-WFE-F', '-WFE-DO', '-WFLE', '-WFLE-F', '-WFLE-DO', '-EFE', '-EFE-F',
    '-EFE-DO', '-EFLE', '-EFLE-F', '-EFLE-DO', '-CF-WFE', '-CF-WFE-F', '-CF-WFE-DO', '-CF-WFLE', '-CF-WFLE-F',
    '-CF-WFLE-DO', '-CF-EFE', '-CF-EFE-F', '-CF-EFE-DO', '-CF-EFLE', '-CF-EFLE-F', '-CF-EFLE-DO', '-WTE-DO',
    '-WRE-DO', '-ETE-DO', '-ERE-DO',
    SIL
    '-HR-DI', '-DR-DI', '-APP-TPR-DI', '-APP-TPR-DO', '-WFLZR-DI', '-EFLZR-DI', '-WFLR-DO', '-EFLR-DO', '-WFL-CFR',
    '-EFL-CFR', '-ECR-DI', '-ECR', '-ECR-DO', '-TBMS', '-TBMS-CTRL', '-CF-TBMS', '-CF-TBMS-CTRL',
    """
    # rute data for BLOK Info
    blokCF = ' '.join(set([r[1] for r in RUTE if r[1][0] == 'A' and r[2] == 'CF']))
    blokT = ' '.join(set([r[1] for r in RUTE if r[1][0] == 'A' and r[2] == 'T']))
    # generator variable blok
    # | 0:NAMA | 1:JENIS | 2:ARAH | 3:SINYAL MASUK | 4:APPROACH | 5:TRACK | 6:INPUT HR/DR |
    dataInput += [b[0] + '-APP-TPR-DI' for b in BLOK]
    dataInput += [b[0] + '-WFLZR-DI' for b in BLOK if 'E' in b[2]]
    dataInput += [b[0] + '-EFLZR-DI' for b in BLOK if 'W' in b[2]]

    dataInput += [b[0] + '-HR-DI' for b in BLOK if 'HR' in b[6]]
    dataInput += [b[0] + '-DR-DI' for b in BLOK if 'DR' in b[6]]
    dataInput += [b[0] + '-ECR-DI' for b in BLOK if b[0] in blokT]

    dataOutput += [b[0] + '-ECR' for b in BLOK if b[0] in blokT]
    dataOutput += [b[0] + bout for bout in addBOutput for b in BLOK]
    dataOutput += [b[0] + "-" + b[2] + boutC for boutC in addBOutputCommon for b in BLOK if b[0] not in blokCF]
    dataOutput += [b[0] + "-CF-" + b[2] + boutC for boutC in addBOutputCommon for b in BLOK if b[0] in blokCF]
    dataOutput += [b[0] + '-APP-TPR-DO' for b in BLOK if b[1] == 'SIL']
    dataOutput += [b[0] + '-ECR-DO' for b in BLOK if b[3] in signalAspek]
    dataOutput += [b[0] + '-ES' for b in BLOK if 'W' in b[2]]
    dataOutput += [b[0] + '-WS' for b in BLOK if 'E' in b[2]]
    dataOutput += [b[0] + boutSCF for boutSCF in ['-TBMS', '-TBMS-CTRL'] for b in BLOK if b[0] not in blokCF and b[1] == 'SIL']
    dataOutput += [b[0] + "-CF" + boutSCF for boutSCF in ['-TBMS', '-TBMS-CTRL'] for b in BLOK if b[0] in blokCF and b[1] == 'SIL']
    dataOutput += [b[0] + '-' + b[2] + add for add in ['FLR-DO', 'FL-CFR', 'TE-DO', 'RE-DO', 'TP'] for b in BLOK if b[1] == 'SIL']

    ##################################################### JPL ##########################################################
    addjpl = ['-AA-F', '-BUZZ-DO', '-PBE', '-PBE-DO', '-PBE-F', '-PB-ERR']
    dataOutput += ['JPL' + j[0] + jp for jp in addjpl for j in JPL]
    for lx in JPL:
        if lx[1]:
            for dir in lx[1].split(','):
                dataOutput += ['JPL' + lx[0] + '-W' + dir + dat for dat in ['-ACCNV', '-ACK', '-L', '-ON', '-START', '-ACCNV']]
        if lx[2]:
            for dir in lx[2].split(','):
                dataOutput += ['JPL' + lx[0] + '-E' + dir + dat for dat in ['-ACCNV', '-ACK', '-L', '-ON', '-START', '-ACCNV']]
        if lx[3]:
            for dir in lx[3].split(','):
                dataOutput += ['JPL' + lx[0] + '-WOL' + dir + dat for dat in ['-ACCNV', '-ACK', '-L', '-ON', '-START', '-ACCNV']]
        if lx[4]:
            for dir in lx[4].split(','):
                dataOutput += ['JPL' + lx[0] + '-EOL' + dir + dat for dat in ['-ACCNV', '-ACK', '-L', '-ON', '-START', '-ACCNV']]
        if lx[1] or lx[3]:
            dataOutput += ['JPL' + lx[0] + '-WAR' + dir + '-DO']
        if lx[2] or lx[4]:
            dataOutput += ['JPL' + lx[0] + '-EAR' + dir + '-DO']

    return dataInput, dataOutput, dataInternal

# function for creating csv file for hima modbus register
def genCSVData(startAddress, varData, nameStr):
    # input field data
    totalInData = math.ceil(len(varData) / 16)

    name = []
    dataName = [[nameStr + str(x) + '_BIT' + str(z) for z in range(16)] for x in range(totalInData)]
    for x in range(totalInData):
        name = name + dataName[x]

    dataType = ['BOOL' for x in range(totalInData * 16)]

    globalV = varData + ['' for x in range(totalInData * 16 - len(varData))]

    sizeBit = [1 for x in range(totalInData * 16)]

    datab2b = [[x + startAddress * 2 + z / 100 for z in range(8)] for x in range(totalInData * 2)]
    byteBit = []
    for x in range(0, totalInData * 2, 2):
        byteBit += datab2b[x + 1] + datab2b[x]

    registerBit = []
    dataReg = [[x + startAddress + z / 100 for z in range(16)] for x in range(totalInData)]
    for x in range(totalInData):
        registerBit += dataReg[x]

    bit = []
    dataBit = [x + startAddress * 16 for x in range(totalInData * 16)]
    for x in range(0, totalInData * 16, 16):
        bit += dataBit[x+8:x+16] + dataBit[x:x+8]

    registerData = [['Name', 'Data type', 'Global Variable', 'Size [Bit]', 'Byte.Bit', 'Register.Bit', 'Bit']] \
        + (np.transpose([name] + [dataType] + [globalV] + [sizeBit] + [byteBit] + [registerBit] + [bit])).tolist()

    return registerData

def genModbusData(simCtrlData, simINDData, internalData):
    simCtrlSt = int(float(simCtrlData[1][5]))
    simINDSt = int(float(simINDData[1][5]))
    simCtrlData = [[x[2]] + [1 if 'NWP' in x[2] or 'TPR' in x[2] or 'VDR' in x[2] or 'NKR' in x[2] or 'ECR' in x[2] or 'FLZR' in x[2] else 0]
                   for x in simCtrlData[1:]]
    simINDData = [[x[2]] + [0] for x in simINDData[1:]]
    intData = [[x, 0 if 'W' in x or 'D' in x else 1] for x in internalData]
    return [simCtrlData, simCtrlSt, simINDData, simINDSt, intData]

def forTest(IT1, IT2, RUTE, SIGNAL, PM, TRACK, BLOK, JPL, inputData, outputData, internalData):
    ruteCTRL = [r[0] + '-' + simp(r[1]) + '-CTRL' for r in RUTE if 'T' in r[2] or 'E' in r[2]]
    ruteCTRL += [r[0] + '-' + simp(r[1]) + '-CF-CTRL' for r in RUTE if 'CF' in r[2]]

    ruteE = [r[0] + '-' + simp(r[1]) + '-E' for r in RUTE if 'T' in r[2] or 'E' in r[2]]
    ruteE += [r[0] + '-' + simp(r[1]) + '-CF-E' for r in RUTE if 'CF' in r[2]]

    # print(ruteCTRL)
    return [PM, TRACK, ruteCTRL, ruteE, inputData, outputData, internalData]

# IT1, IT2, RUTE, SIGNAL, PM, TRACK, BLOK, JPL = ITdata(ITaddress)
# dataInput, dataOutput, dataInternal = genVar(RUTE, SIGNAL, PM, TRACK, BLOK, JPL)

"""""
########### cheat note ########

1. add 2 list
data1 = [1, 2]
data2 = [3,4]
data = data1 + data2
result:
data = [1,2,3,4]

or can use append
data = data1.append(3)
data = data1.append(4)
result:
data = [1,2,3,4]

other use of append
data = data1.append(data2)
result:
data = [1,2,[3,4]]

2. convert string to list
data = "ABCD"
data = map(str, data)
resutl:
data = ['A', 'B', 'C', 'D']

data = TES SATU DUA
data = data.split(" ")
result:
data = ['TES', 'SATU', 'DUA']

3. filter unique value of list
data = [1,1,2,3,1]
data = list(set(data))
result:
data = [1,2,3]

4. join all value on list and convert to text
data = [1,2,3]
data = ' '.join(data)

"""""


