from os import system
#system calls a command from terminal
# system("python C:/Users/answl/Desktop/news_analy/news_an/stock_mysql_64/stock_setting.py")
# exec("  C:/Users/answl/Desktop/news_analy/news_an/stock/prediction/prediction.py")
import subprocess
from glob import glob
# 파일리스트 = glob("*.py")

# for 파일 in 파일리스트:
# subprocess.Popen(['python', 'C:/Users/answl/Desktop/news_analy/news_an/dist/stock_day_model/stock_day_model.exe'])
# subprocess.Popen(['C:/Users/answl/Desktop/news_analy/news_an/stock/model/dist/stock_day_model/stock_day_model.exe'])
subprocess.Popen(['C:/Users/answl/Desktop/news_analy/news_an/stock/model/dist/stock_day_model.exe'])



