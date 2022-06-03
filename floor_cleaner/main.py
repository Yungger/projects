# _*_ coding: utf-8 _*_
# floor_cleaner 的主程式, IoT 專案 (須連網)
USE_OTA = False         # True: 使用 Over-The-Air  方式自動更新
USE_CONNECTOR = False   # True: 使用 WifiConnector 方式自動連網
if USE_OTA:
    YOUR_PROJECT_PATH = 'https://filedn.com/lHUQcwGvamDSp5jubYW5QTF/maker/projects/floor_cleaner'   # 或加密的專案連網字串
if USE_CONNECTOR:
    YOUR_WIFI_SSID = "VJKJ_211_plus"
    YOUR_WIFI_PSWD = "jane0404"

# 專案的客製程式碼
def runProject():
    print('\n開始: vvvvvvvv 專案的程式碼 vvvvvvvvv')
    print('...')
    print('\n結束: ^^^^^^^^ 專案的程式碼 ^^^^^^^^^')

# ----------- 基本上, 下面程式碼均無須異動 ----------
import utime as time
import gc
gc.collect()
gc.mem_alloc()

# time_span 與上次間隔時間, 若未超過則表示連續的異常重啟 (ex. 10 秒內被重啟)
def checkBoot(file='my_boot.txt', time_span=10000):
    last_boot_time = 0  # 上一次啟動的時間
    try:
        f = open(file, 'r')
        last_boot_time = int(f.readline())  # 讀取 MCU 上次的啟動時間
        f.close()
        time.sleep_ms(100)
        with open(file, 'w') as f:
            f.write(str(time.ticks_ms()))   # 寫入 MCU 此次的啟動時間
        f.close()
        time.sleep_ms(100)
    except:
        pass
    return time.ticks_diff(time.ticks_ms(), last_boot_time) > time_span


if __name__ == '__main__':
    if checkBoot():     # 程式的第一個函式, 用來檢查是否此次開機為異常重啟
        from My_OTA import myOTA
        if USE_CONNECTOR:
            from My_WifiConnector import myConnector
            wifi = myConnector()  # 載入自動連網設定, 不需指名 Wifi SSID 與 密碼
        else:
            from My_Wifi import myWifi
            wifi = myWifi(YOUR_WIFI_SSID, YOUR_WIFI_PSWD)
        try:
            if wifi.connect():
                if USE_OTA:
                    ota = myOTA(YOUR_PROJECT_PATH)  # floor_cleaner 為專案的根目錄
                    #print(ota.version())
                    ota.update()
                gc.collect()
                runProject()    # 此專案的客製程式碼所在
                wifi.disconnect(3)
        except:
            print('\n !!! STOP  !!! Forced exist !!!')
        gc.collect()
        gc.mem_free()
        gc.mem_alloc()
