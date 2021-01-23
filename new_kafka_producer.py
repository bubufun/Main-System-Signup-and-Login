from confluent_kafka import Producer
import sys


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


def kafka_connect(ip):
    props = {
        'bootstrap.servers': '%s:9092'%ip,
        'error_cb': error_cb
    }
    producer = Producer(props)
    return producer

def kafka_producer(topicName,msg,key=None):
    # producer =kafka_connect('10.1.0.87')
    producer = kafka_connect('10.1.1.133')
    msgCounter = 0
    try:
        # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
        producer.produce(topicName, '%s' % msg,key)
        producer.flush()
        msgCounter += 1
        print('Send ' + str(msgCounter) + ' messages to Kafka')
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)
    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()

# 主程式進入點
if __name__ == '__main__':
    kafka_producer('test69', 'test','test')
