import os
import json
import cv2
import base64
import numpy
import zmq
import zmq.auth

from zmq.auth.thread import ThreadAuthenticator

class NoDefault:
    pass

class Request:
    def __init__(self, data=str()):
        self.data = json.loads(data)

    def getValue(self, name, default=NoDefault()):
        if name in self.data:
            return self.data[name]

        if isinstance(default, NoDefault):
            raise Exception('Missing value for field: ' + name)

        return default

    def getValues(self):
        return self.data

    def getImage(self, name, default=NoDefault()):
        encoded = self.getValue(name, default)
        buf = base64.decodestring(encoded.encode())

        return cv2.imdecode(numpy.frombuffer(buf, dtype=numpy.uint8),
                            cv2.IMREAD_COLOR)

class Response:
    def __init__(self):
        self.data = {}

    def addValue(self, name, value):
        self.data[name] = value

    def addValues(self, values):
        self.data.update(values)

    def addImage(self, name, image, extension=".jpg"):
        encoded = base64.b64encode(cv2.imencode(extension, image)[1])
        self.addValue(name, encoded.decode('utf-8'))

    def toJSON(self):
        return json.dumps(self.data)

class CloudVis:
    def __init__(self, port, host='cloudvis.qcr.ai', secure=False, server_key_file=None, public_key_file=None):
        context = zmq.Context()

        self.socket = context.socket(zmq.REP)

        if secure:
            if public_key_file is None:
                public_key_dir = os.path.join(os.environ['HOME'], '.cloudvis', str(port))
                public_key_file =  os.path.join(public_key_dir, 'client.key_secret')

                if not os.path.exists(public_key_dir):
                    os.makedirs(public_key_dir)

                if not os.path.exists(public_key_file):
                    zmq.auth.create_certificates(public_key_dir, 'client')
            
            client_public, client_secret = zmq.auth.load_certificate(public_key_file)
            server_key, _ = zmq.auth.load_certificate(server_key_file)

            self.socket.setsockopt(zmq.CURVE_SECRETKEY, client_secret)
            self.socket.setsockopt(zmq.CURVE_PUBLICKEY, client_public)

            self.socket.setsockopt(zmq.CURVE_SERVERKEY, server_key)
            
            self.socket.setsockopt(zmq.TCP_KEEPALIVE, 1)

        self.socket.connect("tcp://{0}:{1}".format(host, port))

    def __del__(self):
        self.socket.close()

    def run(self, process, data={}):
        print ('Waiting')

        while True:
            try:
                req = Request(self.socket.recv().decode('utf-8'))
                resp = Response()

                print('Request received')

                try:
                    process(req, resp, data)
                except Exception as e:
                    resp.addValues({'error': 1, 'message': str(e)})
                
                self.socket.send(resp.toJSON().encode())
                print('Replied')

            except KeyboardInterrupt:
                print('Shutting down...')
                break
