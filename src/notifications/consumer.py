from http import client
import logging
import json
import os
import threading

from flask import Flask, app, request, Response, render_template
from flask_restful import Api, Resource
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from gevent.pywsgi import WSGIServer

socketio = SocketIO()
mqtt = Mqtt()

bitrate_topic = os.getenv('MQTT_APP_BITRATE_INFO_TOPIC')        
mode_topic = os.getenv('MQTT_APP_MODE_INFO_TOPIC')
connectivity_topic = os.getenv('MQTT_CONNECTIVITY_TOPIC')
video_stream = os.getenv('VIDEO_STREAM')        

class Consumer(Resource):

    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = int(os.getenv('CONSUMER_PORT'))
        self.http_server = None
        self.server_thread = None
        

        # setup Flask
        self.app = Flask(__name__)        
        self.api = Api(self.app)
        socketio.init_app(self.app)

        self.app.config.from_mapping(
            MQTT_BROKER_URL=os.getenv('MQTT_BROKER_ADDRESS'),
            MQTT_BROKER_PORT=int(os.getenv('MQTT_BROKER_PORT')),
            MQTT_USERNAME=os.getenv('MQTT_USER'),
            MQTT_PASSWORD=os.getenv('MQTT_PASS'),
            MQTT_KEEPALIVE=5,
            MQTT_TLS_ENABLED=False
        )

        mqtt.init_app(self.app)
        
        # endpoints
        self.api.add_resource(Location,
                              "/callbacks/location/<loc_subs_type>")
        self.api.add_resource(RadioNetworkInformation,
                              "/callbacks/rni/<radio_type>")
        self.api.add_resource(WlanAccessInformation,
                              "/callbacks/wai/<wifi_type>")
        
        @self.app.route('/')
        @self.app.route('/hackathon.html')
        def home():
            return render_template("hackathon.html", video_stream=video_stream)

        @mqtt.on_message()
        def incoming_message(client, userdata, message):
            if (message.topic == mode_topic):
                data=message.payload.decode("utf-8")
                logging.info(data)
                data = json.loads(data)        
                socketio.emit('message', {'msg': data}, namespace='/appMode')                        

            if (message.topic == bitrate_topic):
                data=message.payload.decode("utf-8")
                logging.info(data)
                data = json.loads(data)        
                socketio.emit('message', {'msg': data}, namespace='/appBr')                        

        mqtt.subscribe(bitrate_topic)
        mqtt.subscribe(mode_topic)
        mqtt.subscribe(connectivity_topic)

        
    def start(self):

        self.server_thread = threading.Thread(target=self._start_flask, args=())
        self.server_thread.name = self.__class__.__name__
        self.server_thread.start()

    def stop(self):
        if self.http_server:
            logging.info('Stopping %s' % self.__class__.__name__)
            self.http_server.stop(timeout=1)

    def _start_flask(self):
        logging.info("Starting %s endpoint @ http://%s:%d" % (
            self.__class__.__name__, self.ip, self.port))
        
        self.http_server = WSGIServer(
            (self.ip, self.port),
            self.app  # don't show http logs
        )
        self.http_server.serve_forever(stop_timeout=1)
        logging.info('Stopped %s' % self.__class__.__name__)

class Location(Resource):
    
    def post(self, loc_subs_type):
        logging.info("API CALL: %s POST. Location subscription: %s", self.__class__.__name__, loc_subs_type)
        
        data = json.loads(request.data)
        #print(json.dumps(data, indent=4, sort_keys=True))
        if (data["zonalPresenceNotification"]["userEventType"] == "Leaving"):
            mqtt.publish(connectivity_topic, "{\"conectivity\": \"DISCONNECTED\"}")
        
        socketio.emit('message', {'msg': data}, namespace='/location')

        return Response(status=201)

class RadioNetworkInformation(Resource):

    def post(self, radio_type):
        logging.info("API CALL: %s POST. Radio type: %s", self.__class__.__name__, radio_type)
        
        data = json.loads(request.data)
        #print(json.dumps(data, indent=4, sort_keys=True))
        if (radio_type == "4g"):
            mqtt.publish(connectivity_topic, "{\"conectivity\": \"4G\"}")
        else:
            mqtt.publish(connectivity_topic, "{\"conectivity\": \"5G\"}")
        
        socketio.emit('message', {'msg': data, 'radio_type': radio_type}, namespace='/rni')

        return Response(status=201)

class WlanAccessInformation(Resource):
    
    def post(self, wifi_type):
        logging.info("API CALL: %s POST. %s", self.__class__.__name__, wifi_type)
        
        data = json.loads(request.data)
        #print(json.dumps(data, indent=4, sort_keys=True))

        if (wifi_type == "wifi"):
            mqtt.publish(connectivity_topic, "{\"conectivity\": \"WIFI\"}")
        
        socketio.emit('message', {'msg': data, 'wifi_type': wifi_type}, namespace='/wai')
        
        return Response(status=201)

