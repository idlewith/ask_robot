local_package='/Users/zhouxinzheng/code/ask_robot/dist/ask_robot-0.0.1-py3-none-any.whl'
server_package='/root/ask_robot-0.0.1-py3-none-any.whl'
local_requirements='/Users/zhouxinzheng/code/ask_robot/linux-requirements.txt'
server_requirements='/root/linux-requirements.txt'
log='/opt/idlewith/logs/output.log'
python_env='/usr/bin/python3'

scp $local_package root@120.25.224.28:~/
scp $local_requirements root@120.25.224.28:~/

ssh root@120.25.224.28 "$python_env -m pip uninstall ask-robot -y"
ssh root@120.25.224.28 "$python_env -m pip install $server_package"
ssh root@120.25.224.28 "$python_env -m pip install -r $server_requirements"
ssh root@120.25.224.28 "nohup $python_env -m ask_robot.main >> $log &"

