pid=`netstat -lnput|grep 8081|awk -F ' ' '{print $7}'|awk -F '/' '{print $1}'`

export PASSWORD_EMAIL=''
export PASSWORD_IMAGE=''
export PASSWORD_IMAGE_ID=''

kill -9 $pid

source ~/code/venv/wx/bin/activate

nohup python ~/code/wx/main.py &

nginx -s reload