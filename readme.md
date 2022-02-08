redis ip
10.2.16.113
port 6379

deploy server
10.3.238.72
/rainman

install python3
yum update -y
yum install python3 -y
pip3 install flask
pip3 install flask_cors
pip3 install redis
git clone -b main https://github.com/rainmanyu/pythonRedisOperation.git