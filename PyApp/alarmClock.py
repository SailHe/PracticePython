import winsound  # 导入此模块实现声音播放功能
import time  # 导入此模块，获取当前时间

def currentTimeArray():
    t = time.localtime()  # 当前时间的纪元值
    fmt = "%H %M %S"
    now = time.strftime(fmt, t)  # 将纪元值转化为包含时、分的字符串
    now = now.split(' ') #以空格切割，将时、分放入名为now的列表中
    return now

def alarmClock(my_hour, my_minute, my_seconds):
    flag = 1
    inTimeStr = str(my_hour) + str(my_minute) + str(my_seconds)
    while flag:
        now = currentTimeArray()
        currentHour = now[0]
        currentMinute = now[1]
        currentSeconds = now[2]
        nowTimeStr = str(currentHour) + str(currentMinute) + str(currentSeconds)
        if currentHour == my_hour and currentMinute == my_minute and currentSeconds == my_seconds:
            print("time out!")
            music = 'Good Time.wav'
            winsound.PlaySound(music, winsound.SND_ALIAS)
            flag = 0
        elif nowTimeStr > inTimeStr:
            print("输入时间已经过去")
            flag = 0

if __name__ == '__main__':
    launchTimeArr = currentTimeArray()
    # 提示用户设置时间和分钟
    print("格式 HH MM SS 不足两位前置0")
    my_hour = input("请输入时" + launchTimeArr[0] + "：")
    my_minute = input("请输入分" + launchTimeArr[1] + "：")
    my_seconds = input("请输入秒" + launchTimeArr[2] + "：")
    alarmClock(my_hour, my_minute, my_seconds)
    