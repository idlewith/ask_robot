#path_root="/Users/zhouxinzheng/code/ask_robot"
path_root="C:\\PycharmProjects\\ask_robot"

server="120.25.224.28"

local_package=${path_root}'/dist/ask_robot-0.0.1-py3-none-any.whl'
local_requirements=${path_root}'/linux-requirements.txt'

server_package='/root/ask_robot-0.0.1-py3-none-any.whl'
server_requirements='/root/linux-requirements.txt'

#log='/opt/idlewith/logs/output.log'
python_env='/usr/bin/python3'

cd $path_root
python setup.py publish

scp ${local_package} root@$server:~/
scp $local_requirements root@$server:~/

ssh root@$server "$python_env -m pip uninstall ask-robot -y"
ssh root@$server "$python_env -m pip install $server_package"
ssh root@$server "$python_env -m pip install -r $server_requirements"


ssh root@$server "netstat -lnput|grep 8081|awk -F ' ' '{print \$7}'|awk -F '/' '{print \$1}'|xargs kill -9"
ssh root@$server "netstat -lnput|grep 8081|awk -F ' ' '{print \$7}'|awk -F '/' '{print \$1}'|xargs kill -9"
ssh root@$server "netstat -lnput|grep 8081|awk -F ' ' '{print \$7}'|awk -F '/' '{print \$1}'|xargs kill -9"
#ssh root@$server "nohup ${python_env} -m ask_robot.main >> $log &"
ssh root@$server "nohup ${python_env} -m ask_robot.main &"
ssh root@$server "nginx -s reload"

