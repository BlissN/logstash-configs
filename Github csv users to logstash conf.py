
#just use this script to create part of logstash config
#input example:
#csv file, [real name];[login];[department]
#output example:
#if [actor] == "LOGIN" {
#   mutate {
#       update => { "real_name" => "REAL_NAME" }
#       update => { "department" => "DEPARTMENT_NAME" }
#   }
# }
import re
login_pattern=re.compile('(?<=;).+(?=;)')
real_name_pattern=re.compile('.+(?=;.+;)')
department_pattern=re.compile('\w+$')
w1 = 'if [actor] == "'
w2 = '" { mutate { update => { "real_name" => "'
w3 = '" }'
#dont forget \n in output
w4 = 'update => { "department" => "'
w5 = '" } } }'
with open('empl.csv', 'r') as log:
    with open('user_list.txt', 'w') as user_list:
        for line in log:
            login=re.findall(login_pattern, line)
            real_name=re.findall(real_name_pattern, line)
            department=re.findall(department_pattern, line)
            login_str = ''.join(map(str, login))
            name_str = ''.join(map(str, real_name))
            department_str = ''.join(map(str, department))
            print(w1 + login_str + w2 + name_str + w3 + '\n' + w4 + department_str + w5 + '\n')
            user_list.writelines(w1 + login_str + w2 + name_str + w3 + '\n' + w4 + department_str + w5 + '\n')