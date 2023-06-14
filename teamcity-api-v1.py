#Дергаем по api события из teamcity и складываем в файл

import requests
import re
import time

event_id_pattern = re.compile('(?<=<auditEvent id=")[0-9]{5,8}')
daily_log = set()
event_id = list()
last_day_event_id = list()
first_day_event_id = list()
new_id = list()
flag = 0 # Ноль возможен только при первом запуске. Если скрипт выполнялся ранее, значение будет 1

while(True): #просто бесконечный цикл
    date = time.strftime("%Y%m%d-%H") #текущая дата
    daily_log.clear() #чистим множество для лога нового дня
    file_name = "/home/ubuntu/teamcity-logs/" + time.strftime("%Y%m%d-%H") + ".txt" #задаем имя файла согласно текущему дню
    # Определяем стартовый 
    if flag == 0:
        response_new_day = requests.get(
            "https://***********/app/rest/audit?locator=count:1",
            headers={"Authorization": "Bearer *************************"}
            )
        sep1 = re.split("(\<auditEvent id=.+?\<\/auditEvent\>)", str(response_new_day.text))
        for word in sep1:
            if "<auditEvent id=" in word:
                first_day_event_id = re.findall(event_id_pattern, word)
                print(first_day_event_id)
                print("start")
    print(flag)            
    with open(file_name, 'w') as log:            
        while date == time.strftime("%Y%m%d-%H"):
            response = requests.get(
                    "https://******************/app/rest/audit?locator=count:100",
                    headers={"Authorization": "Bearer **********************************"}
                    )
            sep = re.split("(\<auditEvent id=.+?\<\/auditEvent\>)", str(response.text))           
            for word in sep:
                if "<auditEvent id=" in word:
                    new_day_event_id = re.findall(event_id_pattern, word)
                    if first_day_event_id < new_day_event_id:
                        daily_log.add(f"{word}"+"\n")   
                        new_id = re.findall(event_id_pattern, word)
                    if event_id < new_id:
                        event_id = new_id
            time.sleep(60)                 
        log.writelines(sorted(daily_log))
        first_day_event_id = event_id
        flag = 1
        print(first_day_event_id)
        print("first_day_event_id")