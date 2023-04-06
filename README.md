
# Ask robot

**for WeChat platform, offer api to do an ask robot.**





# install python from source

```shell
wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz
tar -xzvf Python-3.9.7.tar.xz

cd Python-3.9.7
./configure --prefix=/opt/idlepig/apps/python397
make
make altinstall

cd ~/code/venv
/opt/idlepig/apps/python397/bin/python3.9 -m venv wx
source ~/code/venv/wx/bin/activate

cd ~/code/wx
pip install -r requirements.txt
```


# or install python directly


in centos

```shell
yum install python36u
```

# env

create virtual environment and source

```shell
mkdir -p ~/code/venv
cd ~/code/venv
python3 -m venv wx
source ~/code/venv/wx/bin/activate
```



# install ask_robot

```
pip install ask_robot
```



# start flask service

you need set actual info for token, aes_key, appid

if you are in plaintext mode, just set token is ok.

```shell
export token=''
export app_id=''
export aes_key=''
export secret=''
export email_from=''
export email_password=''
export email_to=''
export chatgpt=''
```

```
nohup ask &
```

then http://0.0.0.0:8081 will work


# install nginx


```shell
yum install nginx
```

vi /etc/nginx/nginx.conf

```shell
http {
...
upstream idlewith {
    server 127.0.0.1:8081;
  }
...
}
```

vi /etc/nginx/conf.d/default.conf

```shell
server {
    listen 80;
    server_name _;
    location / {
      proxy_pass http://idlewith;
    }
}
```

so, we map 80 port to 8081 port

start nginx

```shell
nginx
```
