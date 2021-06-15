from multiprocessing import Process, Semaphore, shared_memory
from win32com.shell import shell
if shell.IsUserAnAdmin() :
    print("관리자입니다.")
else :
    print("관리자가 아닙니다.")

import win32com.client

from pywinauto import application
import time
import os
#프로세스 킬 /IM 이미지 이름으로 대상 선택
class connectCreon():
    os.system('taskkill /IM coStarter* /F /T')
    os.system('taskkill /IM CpStart* /F /T')
    os.system('taskkill /IM DibServer* /F /T')
    # wmic로 윈도우 실행
    os.system('wmic process where "name like \'%coStarter%\'" call terminate')
    os.system('wmic process where "name like \'%CpStart%\'" call terminate')
    os.system('wmic process where "name like \'%DibServer%\'" call terminate')
    time.sleep(5)

    app = application.Application()
    #모의투자 testmun qazsx852
    app.start('C:/CREON/STARTER/coStarter.exe /prj:cp /id:munocto /pwd:@@qazsx8 /pwdcert:@@qazsx852 /autostart')
    time.sleep(50)