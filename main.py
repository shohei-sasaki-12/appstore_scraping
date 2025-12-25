import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import datetime
import time

# web情報取得関数
def GetWebInfo(url):
    retry_num = 3   # リトライ回数
    retry_time = 5  # リトライ時間

    for i in range(retry_num):
        try:
            res = requests.get(url)
            return res   # 取得成功

        except requests.exceptions.RequestException as e:
            print(f"エラー発生。{retry_time}秒後にリトライします。")
            #print("エラー : ", e)
            time.sleep(retry_time)
    
    return None # 取得失敗

# web情報を取得
url = 'https://apps.apple.com/jp/iphone/charts/36?chart=top-free'
res = GetWebInfo(url)

# web情報の抽出
if res != None:
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    elems = soup.find_all(href=re.compile("apps.apple.com/jp/app"))

    app_name = []
    for elem in elems:
        app_name.append(elem.attrs["aria-label"])

    # csvファイル出力
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y%m%d')

    folder_path = os.path.join(os.getcwd(), "output")
    file_path = os.path.join(folder_path, date) + ".csv"
    
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)   # outputフォルダ新規作成

    df = pd.DataFrame(app_name, columns=["アプリ名"])
    df.index += 1   # インデックスを1からスタート
    
    df.to_csv(file_path)
    print("web情報取得を成功しました。")

else:
    print("web情報取得を失敗しました。")
