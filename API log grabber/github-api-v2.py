#Дергаем по api логи из github
import requests
import re
import time  

hourly_log = set()
current_timestamp = list()   
timestamp_pattern = re.compile("(?<=stamp\":)[0-9]{13,14}")
eldest_timestamp = list()

while(True):
    date = time.strftime("%Y%m%d-%H") #текущая дата
    hourly_log.clear() #чистим множество для лога нового дня
    file_name = "/home/ubuntu/github-logs/" + time.strftime("%Y%m%d-%H") + ".txt"
    with open(file_name, 'w') as log:
        while date == time.strftime("%Y%m%d-%H"):
            response = requests.get(
                "https://api.github.com/enterprises/*******/audit-log?per_page=100",
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": "Bearer ***********************",
                    "X-GitHub-Api-Version": "2022-11-28"
                    }
                )

            sep = re.split(",(?={\"@timestamp\")", str(response.text))        
            for word in sep:
                if "timestamp" in word:
                    word = re.sub(r"]$", "", word) #избавляемся от [ и ] в начале/конце строки
                    word = re.sub(r"^\[", "", word)
                    current_timestamp = re.findall(timestamp_pattern, word)
                    if current_timestamp > eldest_timestamp: #Если current_timestamp меньше самого большого таймстампа прошлого часа - это лог из прошлого часа и он есть в предыдущем файле
                        hourly_log.add(f"{word}"+"\n") 
                        new_timestamp = current_timestamp
                        if new_timestamp > eldest_timestamp:
                            candidate_timestamp = new_timestamp
            time.sleep(20)
#            print(word)
#            print(eldest_timestamp)
        log.writelines(sorted(hourly_log))    
        eldest_timestamp = candidate_timestamp