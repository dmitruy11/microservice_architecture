import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes

np.random.seed(42)
# Загружаем датасет о диабете
X, y = load_diabetes(return_X_y=True)
# Формируем случайный индекс строки
random_row = np.random.randint(0, X.shape[0]-1)

# Подключение к серверу на локальном хосте:
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создаём очередь y_true
channel.queue_declare(queue='y_true')
# Создаём очередь features
channel.queue_declare(queue='features')

# Публикуем сообщение в очередь y_true
channel.basic_publish(exchange='',
                      routing_key='y_true',
                      body=json.dumps(y[random_row]))
print('Сообщение с правильным ответом отправлено в очередь')

# Публикуем сообщение в очередь features
channel.basic_publish(exchange='',
                      routing_key='features',
                      body=json.dumps(list(X[random_row])))
print('Сообщение с вектором признаков отправлено в очередь')

# Закрываем подключение
connection.close()

# Публик
##  docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# Закрываем подключение


##Теперь давайте заглянем в RabbitMQ и посмотрим, пришло ли наше сообщение. Для этого в соседнем терминале выполните команду для запуска командной оболочки bash RabbitMQ:

# $ docker exec -it rabbitmq bash 
#В результате выполнения этой команды вы попадёте внутрь контейнера, где функционирует брокер. Давайте заглянем в очередь y_true и посмотрим, появилось ли в ней сообщение. Для этого внутри контейнера выполните команду:

#$ rabbitmqadmin get queue=y_true count=10


# СЕРВИС II. СЕРВИС ДЛЯ ПРЕДСКАЗАНИЯ
#   cd features/src    cd features/src
# python3 features.py

# 
#  docker-compose build
#  docker-compose up -d
#   docker-compose ps