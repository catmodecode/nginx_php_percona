import os
import sys
import glob
import shutil
import subprocess
import os.path
import time
from os import path

dbIzeoFolder = 'data/mysql57dbizeo'

def restoreList(doPrint=False):
    files = []
    for file in glob.glob("*.tar.gz"):
        files.append(file)

    return files


def decompressDb(file):
    os.system("tar xvfz " + file)


def restoreDb(folder):
    print(folder)
    if path.exists(dbIzeoFolder + 'backdb') and path.isdir(dbIzeoFolder + 'backdb'):
        shutil.rmtree(dbIzeoFolder + 'backdb')
    shutil.move(dbIzeoFolder, dbIzeoFolder + 'backdb')
    shutil.move(folder, dbIzeoFolder)
    shutil.rmtree('replica')

def stopIzeo():
    if isIzeoRunning():
        print("Stopping izeo, wait a minute")
        try:
            result = subprocess.check_output(
                'docker stop dbizeo',
                shell=True,
                stderr=subprocess.STDOUT
            ).decode("UTF-8")
        except BaseException as err:
            bye(err)

        if result.find("ERROR") >= 0:
            bye("error" + result)

        if isIzeoRunning():
            bye("Izeo cant be stopped")
        print("Izeo stoped!")
    else:
        print("Izeo wasn't started!")


def startIzeo():

    if isIzeoRunning():
        bye("IZEO WAS RUNNING!!!")

    try:
        result = subprocess.check_output(
            'docker-compose up -d dbizeo',
            shell=True,
            stderr=subprocess.STDOUT
        ).decode("UTF-8")
    except BaseException as err:
        bye(err)

    if not isIzeoRunning():
        bye("Izeo DIDNT STARTED!!!")
    print("Izeo started!")


def isIzeoRunning():
    try:
        result = subprocess.check_output(
            'docker ps -f "name=dbizeo"',
            shell=True,
            stderr=subprocess.STDOUT
        ).decode("UTF-8")
    except subprocess.CalledProcessError as perror:
        bye(perror)
    except BaseException as err:
        bye(err.args[0])

    found = result.find("dbizeo") >= 0
    
    return found

fileList = restoreList()

print("Chose archive to restore:")

for i in range(len(fileList)):
    print(str(i + 1) + ") " + fileList[i][:-7])

select = int(input())

if select < 1 or select > len(fileList):
    print("incorrect")
    sys.exit(1)

chosenFile = fileList[select-1]

decompressDb(chosenFile)
decompressedFolder = 'replica/' + chosenFile[:-7] + '/'
stopIzeo()
restoreDb(decompressedFolder)
startIzeo()

print("Wait 60 seconds for dbIzeo up")
for i in range(60, 0, -1):
    print(i)
    time.sleep(1)

subprocess.check_output(
        'docker exec -i dbizeo mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON izeo.* TO \'root\'@\'%\' IDENTIFIED BY \'root\';"',
        shell=True,
        stderr=subprocess.STDOUT
    )
subprocess.check_output(
        'docker exec -i dbizeo mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON spmarket.* TO \'root\'@\'%\' IDENTIFIED BY \'root\';"',
        shell=True,
        stderr=subprocess.STDOUT
    )
subprocess.check_output(
        'docker exec -i dbizeo mysql -uroot -proot -e "flush privileges;"',
        shell=True,
        stderr=subprocess.STDOUT
    )

print("Done!")
