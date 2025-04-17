import pika
import json
import threading
import requests
import logging
from train import train_main

# 日志配置
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

# RabbitMQ 配置
RABBITMQ_CONFIG = {
    'username': 'guest',
    'password': 'guest',
    'host': '127.0.0.1',
    'port': 5672,
    'queue': 'TestDirectQueue'
}

JAVA_SERVICE_URL = "http://127.0.0.1:8989/sys-task/state"


def ask_java(uuid, state):
    try:
        response = requests.get(JAVA_SERVICE_URL, params={'uuid': uuid, 'state': state})
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Error contacting Java service: {e}")
        return None


def thread_func(ch, method, body):
    try:
        data = json.loads(body)
        uuid = data.get('uuid')
        prams_str = data.get('prams')

        if not uuid or not prams_str:
            raise ValueError("Invalid message: missing uuid or prams")

        logging.info(f"Received task UUID: {uuid}")
        prams = json.loads(prams_str)
        file_name = prams.get('fileName')

        if not file_name:
            raise ValueError("Missing fileName in prams")

        logging.info(f"Starting training for file: {file_name}")
        ask_java(uuid, "开始训练")

        train_main(uuid, file_name, "LogisticRegression", {"solver": "liblinear"}, 1.0)

    except Exception as e:
        logging.error(f"Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    threading.Thread(target=thread_func, args=(ch, method, body)).start()


def main():
    credentials = pika.PlainCredentials(RABBITMQ_CONFIG['username'], RABBITMQ_CONFIG['password'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_CONFIG['host'],
            port=RABBITMQ_CONFIG['port'],
            virtual_host='/',
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_CONFIG['queue'], on_message_callback=callback)

    logging.info("Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
