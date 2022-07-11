import os
import subprocess


def run_command(command_str):
    stdout, stderr = subprocess.Popen(command_str, stdout=subprocess.PIPE, shell=True).communicate()
    if isinstance(stdout, bytes):
        return stdout.decode('utf-8')
    else:
        return stdout


# path_root="/Users/zhouxinzheng/code/ask_robot"
root_path = "C:\\PycharmProjects\\ask_robot"

server = "120.25.224.28"

dist_path = os.path.join(root_path, 'dist')
local_package = os.path.join(dist_path, 'ask_robot-0.0.1-py3-none-any.whl')
local_requirements = os.path.join(root_path, 'linux-requirements.txt')
print(dist_path)
print(local_package)
print(local_requirements)

server_package = '/root/ask_robot-0.0.1-py3-none-any.whl'
server_requirements = '/root/linux-requirements.txt'

# log='/opt/idlewith/logs/output.log'
python_env = '/usr/bin/python3'

run_command(f'cd {root_path}')
run_command('python setup.py publish')

run_command(f'scp {local_package} root@{server}:~/')
run_command(f'scp {local_requirements} root@{server}:~/')

run_command(f'ssh root@{server} "{python_env} -m pip uninstall ask-robot -y"')
run_command(f'ssh root@{server} "{python_env} -m pip install {server_package} --user"')
run_command(f'ssh root@{server} "{python_env} -m pip install -r {server_requirements} --user"')

# ssh root@$server "netstat -lnput|grep 8081|awk -F ' ' '{print \$7}'|awk -F '/' '{print \$1}'|xargs kill -9"
run_command(f'ssh root@{server} "netstat -lnput|grep 8081|awk -F \' \' \'{{print $7}}\'|awk -F \'/\' \'{{print $1}}\'|xargs kill -9"')
run_command(f'ssh root@{server} "netstat -lnput|grep 8081|awk -F \' \' \'{{print $7}}\'|awk -F \'/\' \'{{print $1}}\'|xargs kill -9"')
run_command(f'ssh root@{server} "netstat -lnput|grep 8081|awk -F \' \' \'{{print $7}}\'|awk -F \'/\' \'{{print $1}}\'|xargs kill -9"')
# ssh root@$server "nohup ${python_env} -m ask_robot.main >> $log &"
run_command(f'ssh root@{server} "nohup {python_env} -m ask_robot.main &"')
run_command(f'ssh root@{server} "nginx -s reload"')
