import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import datetime
import time

# web情報取得関数
def get_web_info(url):
    ret = None
    retry_num = 3   # リトライ回数
    retry_time = 5  # リトライ時間

    for i in range(retry_num):
        try:
            # User-Agent
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            
            res = requests.get(url, headers=headers, timeout=10)

            if res.status_code == 200:
                ret = res   # 取得成功
                break
            else:
                print(f"エラー発生。{retry_time}秒後にリトライします。")
                #print("エラー : ", e)
                time.sleep(retry_time)

        except requests.exceptions.RequestException as e:
            print(f"エラー発生。{retry_time}秒後にリトライします。")
            #print("エラー : ", e)
            time.sleep(retry_time)
    
    return ret

# web情報を取得
url = 'https://apps.apple.com/jp/iphone/charts/36?chart=top-free'
res = get_web_info(url)

# web情報の抽出
if res is not None:
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find_all("li")

    app_name = []
    for item in items:
        a = item.find("a", href=re.compile("/jp/app/"))
        if not a:
            continue

        label = a.get("aria-label")
        if not label:
            continue
        
        app_name.append(label)

    # csvファイル出力
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y%m%d')

    folder_path = os.path.join(os.getcwd(), "output")
    file_path = os.path.join(folder_path, date) + ".csv"
    
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)   # outputフォルダ新規作成

    df = pd.DataFrame(app_name, columns=["アプリ名"])
    df.insert(0, "順位", range(1, len(df) + 1)) # 一番左の列に順位を追加

    df.to_csv(file_path, index=False)

    if len(app_name) >= 10: # 10件以上取得できた場合は正常に取得できた判定
        print("web情報取得を成功しました。")
    else:
        print("取得件数が異常です。HTML構造変更の可能性あり。")

else:
    print("web情報取得を失敗しました。")
