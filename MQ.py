import pika
import json
import threading
import requests
from train import train_main
def askJava(uuid,state):
    return requests.get(url="http://127.0.0.1:8989/sys-task/state?uuid="+uuid+"&state="+state)
# 远程rabbitmq服务的配置信息
username = 'guest'  # 指定远程rabbitmq的用户名密码
pwd = 'guest'
ip_addr = '127.0.0.1'
port_num = 5672
 
credentials = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(ip_addr, port_num, '/', credentials))
channel = connection.channel()
# 消费成功的回调函数
# 消费成功的回调函数
def thread_func(ch, method, body):
    data=json.loads(body)
    print(data)
    uuid=data['uuid']
    print(data['prams'])
    parms=json.loads(data['prams'])
    fileName=parms['fileName']
    res=askJava(uuid,"开始训练")
    print(res)
    train_main(uuid,fileName,"LogisticRegression",{"solver":"liblinear"},1.0)
    #time.sleep(10)
    ch.basic_ack(delivery_tag = method.delivery_tag)
def callback(ch, method, properties, body):
    threading.Thread(target=thread_func, args=(ch, method, body)).start()

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback,
                      queue='TestDirectQueue')
channel.start_consuming()