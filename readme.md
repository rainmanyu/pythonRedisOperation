redis ip
10.2.16.113
port 6379

deploy server
10.2.47.17
/rainman

install python3
yum update -y;
yum install python3 -y
pip3 install flask
pip3 install flask_cors
pip3 install redis
pip3 install Timeloop
git clone -b main https://github.com/rainmanyu/pythonRedisOperation.git

nohup python3 server.py &
ps aux|grep python3

http://10.2.47.17:9888/sites