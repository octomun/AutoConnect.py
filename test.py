import sys
from PyQt5.QtWidgets import *
import win32com.client
import pandas as pd
import os
import datetime
import time
def RequestMT(code, dwm, st, et):
    for j in code:
        # 연결 여부 체크
        g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
        objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        file = 'F:/stock/output_{}.csv'.format(j)
        if os.path.isfile(file):
            os.remove(file)

        st_year = str(st)[:4]
        st_month = str(st)[4:6]
        st_day = str(st)[6:]
        st = datetime.date(int(st_year),int(st_month),int(st_day))

        et_year = str(et)[:4]
        et_month = str(et)[4:6]
        et_day = str(et)[6:]
        et = datetime.date(int(et_year),int(et_month),int(et_day))

        if st > et:
            t = st
            st = et
            et = t

        while st != et:
            objStockChart.SetInputValue(0, j)
            # objStockChart.SetInputValue(0, code)  # 종목코드
            objStockChart.SetInputValue(1, ord('2'))  # 1기간 2개수로 받기
            objStockChart.SetInputValue(2, to_integer(et)) #종료일
            objStockChart.SetInputValue(3, to_integer(st)) #시작일
            # objStockChart.SetInputValue(2, 20210101)
            # objStockChart.SetInputValue(3, 20210125)
            objStockChart.SetInputValue(4, 380)  # 조회 개수 1일 380
            objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
            objStockChart.SetInputValue(6, dwm)  # '차트 주기 - 분/틱
            objStockChart.SetInputValue(7, 1)  # 분틱차트 주기
            objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용

            objStockChart.BlockRequest2(1)

            rqStatus = objStockChart.GetDibStatus()
            rqRet = objStockChart.GetDibMsg1()
            print("통신상태", rqStatus, rqRet)
            if rqStatus != 0:
                print('rqstatus != 0')
                exit()

            len = objStockChart.GetHeaderValue(3) # 수신개수
            print('len = ', len)
            dates = []
            opens = []
            highs = []
            lows = []
            closes = []
            vols = []
            times = []
            for i in range(len):
                dates.append(objStockChart.GetDataValue(0, i))
                times.append(objStockChart.GetDataValue(1, i))
                opens.append(objStockChart.GetDataValue(2, i))
                highs.append(objStockChart.GetDataValue(3, i))
                lows.append(objStockChart.GetDataValue(4, i))
                closes.append(objStockChart.GetDataValue(5, i))
                vols.append(objStockChart.GetDataValue(6, i))
            chart = pd.DataFrame({'dates':dates,'times':times,'opens':opens,'highs':highs,'lows':lows,'closes':closes,'vols':vols})
            if not os.path.isfile(file):
                chart.to_csv(file, index=False, mode='w', encoding='utf-8')
                chart = pd.DataFrame()
            else:
                chart.to_csv(file, index=False, mode='a', encoding='utf-8', header=False)
                chart = pd.DataFrame()
            et = et-datetime.timedelta(days=1)
            print(to_integer(et))
            time.sleep(0.5)
    return print(len)

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day


# def _wait(self):
#     time_remained = self.obj_CpCybos.LimitRequestRemainTime
#     cnt_remained = self.obj_CpCybos.GetLimitRemainCount(1)  # 0: 주문 관련, 1: 시세 요청 관련, 2: 실시간 요청 관련
#     if cnt_remained <= 0:
#         timeStart = time.time()
#         while cnt_remained <= 0:
#             time.sleep(time_remained / 1000)
#             time_remained = self.obj_CpCybos.LimitRequestRemainTime
#             cnt_remained = self.obj_CpCybos.GetLimitRemainCount(1)


# def codeEditChanged(self):
#     code = self.text()
#     self.setCode(code)
#
# def setCode(code):
#     if len(code) < 6:
#         return
# code.codeEditChanged
# # code.textChanged.connect(code.codeEditChanged)
# # code.setText('00660')
code = ['A005930']
RequestMT(code, ord('m'), 20190603,20210601)