from datetime import datetime, timedelta
import requests
import re
import time

daily_log = set()

while(True):
    date_hour = time.strftime("%Y%m%d-%H")
    file_name = "/home/infosec/CF/" + time.strftime("%Y%m%d-%H") + ".txt" #задаем имя файла согласно текущему дню          
    with open(file_name, 'a+') as log:          
        while date_hour == time.strftime("%Y%m%d-%H"):
            one_min_ago = (((datetime.now() - timedelta(minutes=1)).isoformat() + "Z")) # обратить внимание на смещение из-за часового пояса
            url = "https://api.cloudflare.com/client/v4/accounts/##################################/audit_logs"
            headers = {"Authorization": "Bearer ######################", "Content-Type": "application/json"}
            param_request = {"since": one_min_ago}
            response = requests.get(url, headers=headers, params=param_request)
            string = response.text
            string = re.sub(r"\{\"result\"\:\[", "", string)
            string = re.sub(r"\]\,\"success\"\:true\,\"errors\"\:\[\]\,\"messages\"\:\[\]\}", "", string)
            sep = re.split("(\{\"action\"\:\{\"result\"\:.+?Z\"\})", str(string))
            with open(file_name, 'a+') as log:  
                for word in sep:
                    if "action" in word:
                        log.write(word + "\n")
                        print(word)
                        print("new min")
            time.sleep(60)
