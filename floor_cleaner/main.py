# _*_ coding: utf-8 _*_
# floor_cleaner 的主程式, IoT 專案 (須連網)
USE_OTA = True         # True: 使用 Over-The-Air  方式自動更新
USE_CONNECTOR = True   # True: 使用 WifiConnector 方式自動連網
if USE_OTA:
    YOUR_PROJECT_PATH = 'https://filedn.com/lHUQcwGvamDSp5jubYW5QTF/maker/projects/floor_cleaner'   # 或加密的專案連網字串
if not USE_CONNECTOR:
    YOUR_WIFI_SSID = "YOUR_WIFI_SSIDs"
    YOUR_WIFI_PSWD = "YOUR_WIFI_PSWD"

# *********** 基本上, 下面程式碼均無須被修改 **********
import utime as time
import gc

# time_span 與上次間隔時間, 若未超過則表示連續的異常重啟 (ex. 10 秒內被重啟)
def checkBoot(file='my_boot.txt', time_span=10000):
    last_boot_time = 0  # 上一次啟動的時間
    try:
        f = open(file, 'r')
        last_boot_time = int(f.readline())  # 讀取 MCU 上次的啟動時間
        f.close()
        time.sleep_ms(100)
    except:
        pass
    try:
        with open(file, 'w') as f:
            f.write(str(time.ticks_ms()))   # 寫入 MCU 此次的啟動時間
        f.close()
        time.sleep_ms(100)
    except:
        pass
    #print(time.ticks_ms(), last_boot_time, (time.ticks_ms(), last_boot_time), time_span, time.ticks_diff(time.ticks_ms(), last_boot_time))
    return time.ticks_diff(time.ticks_ms(), last_boot_time) > time_span


if __name__ == '__main__':
    gc.collect()
    if checkBoot():     # 程式的第一個函式, 用來檢查是否此次開機為異常重啟
        try:
            from My_OTA import myOTA
            if USE_CONNECTOR:
                from My_WifiConnector import myConnector
                wifi = myConnector(debug=True)  # 載入自動連網設定, 不需指名 Wifi SSID 與 密碼
            else:
                from My_Wifi import myWifi
                wifi = myWifi(YOUR_WIFI_SSID, YOUR_WIFI_PSWD)
            if wifi.connect():
                if USE_OTA:
                    ota = myOTA(YOUR_PROJECT_PATH)  # floor_cleaner 為專案的根目錄
                    #ota.version(0.11)  # 測試用, 故意降版
                    if not ota.is_uptodate:
                        ota.update()
                runProject()    # 此專案的客製程式碼所在
                wifi.disconnect(3)
        except:
            print('\n !!! STOP  !!! Forced exist !!!')
