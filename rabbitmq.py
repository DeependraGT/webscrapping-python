import pika
import time
import json

credentials = pika.PlainCredentials('deependra', 'deependra')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.6.51',5672,'/',credentials))
channel = connection.channel()

if connection.is_open:
    method, header, body = channel.basic_get(queue="HBNaukriQueue")
    print body
    p = json.loads(body)
    print "Session Id : " + p["sessionid"]
    print "Email Id : " + p["email"]
    print "Password : " + p["password"]
    #channel.basic_ack(delivery_tag=method.delivery_tag)
    time.sleep(1)

'''
channel.basic_publish(exchange='',
                        routing_key='HBNaukriQueue',
                        body = "{'otp':''}") '''

print "Message Get"
connection.close()

