# EmplopyeeManagement
## 环境
python3.8
## 怎样运行系统并通过rest api进行调用？
### 1 下载、安装、运行redis和kafka
#### redis
redis下载链接:  
https://download.redis.io/releases/redis-6.2.6.tar.gz  
下载后，运行以下命令解压:  
`tar -zxvf redis-6.2.6.tar.gz`  
解压后进入redis-6.2.6目录，执行以下命令编译:  
`make`  
编译完成后，执行以下命令验证编译是否成功:  
`make test`  
验证成功后，执行以下命令运行redis:  
`./src/redis-server ./redis.conf`  
#### kafka
kafka下载链接:  
https://www.apache.org/dyn/closer.cgi?path=/kafka/3.0.0/kafka_2.13-3.0.0.tgz  
下载后，运行以下命令解压:  
`tar -zxvf kafka_2.13-3.0.0.tgz`  
解压后进入kafka_2.13-3.0.0目录，先运行zookeeper:  
`./bin/zookeeper-server-start.sh`  
再启动kafka server:  
`./bin/kafka-server-start.sh`
### 2 运行员工管理系统
#### 创建kafka topic
员工管理系统会将注册的员工信息写入redis数据库，然后将这一事件发送到kafka，之后用户管理系统会从kafka中读取这一事件  
我们需要创建一个专门的topic(名为employee-user)用于员工管理系统和用户管理系统之间的消息传递  
进入kafka根目录，执行以下命令以创建该topic:  
`./bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic employee-user --partitions 1 --replication-factor 1`  
#### 运行员工管理系统
拉下员工管理系统的代码之后，执行以下命令以运行系统:  
`python employee.py`  
#### 通过rest api调用员工管理系统的注册功能，以注册员工
`curl -i -H "Content-Type: application/json" -X POST -d '{"number":"000000","name":"Bob","department":"Sale"}' http://127.0.0.1:5000/employee/api/register`  
该api调用会在员工管理系统中注册一个员工，姓名为Bob，工号为000000，部门为Sale  
在redis根目录下执行`./src/redis-cli`可进入redis交互式命令行，然后执行`hgetall 000000`可以看到刚刚注册的该员工信息
