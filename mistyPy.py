import requests
import json
import threading
import time
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
from random import*

class Robot:

    def __init__(self,ip):
        self.ip = ip

        self.images_saved = []
        self.audio_saved  = []
        self.faces_saved = []

        self.backpack_instance = None
        self.time_of_flight_instance = [None]*4
        self.face_recognition_instance = None

        self.available_subscriptions = ["StringMessage","TimeOfFlight","FaceDetection","FaceRecognition","LocomotionCommand","HaltCommand","SelfState","WorldState"]

        self.populateImages()
        self.populateAudio()
        self.populateLearnedFaces()

    def changeLED(self,red,green,blue):
        assert red in range(0,256) and blue in range(0,256) and green in range(0,256), " changeLED: The colors need to be in 0-255 range"
        requests.post('http://'+self.ip+'/api/led/change',json={"red": red,"green": green,"blue": blue})

    def changeImage(self,image_name,timeout=5):
        if image_name in self.images_saved:
            requests.post('http://'+self.ip+'/api/images/change',json={'FileName': image_name ,'TimeOutSeconds': 5,'Alpha': 1})
        else:
            print(image_name,"not found on the robot, use <robot_name>.printImageList() to see the list of saved images")

    def playAudio(self,file_name):
        if file_name in self.audio_saved:
            requests.post('http://'+self.ip+'/api/audio/play',json={"AssetId": file_name})
        else:
            print(file_name,"not found on the robot, use <robot_name>.printAudioList() to see the list of saved audio files")

    def battery(self):
        resp = requests.get('http://'+self.ip+'/api/info/battery')
        for reply in resp.json():
        	return (reply['result'])

    def moveHead(self,roll,pitch,yaw,velocity=1):
        assert roll in range(-5,6) and pitch in range(-5,6) and yaw in range(-5,6), " moveHead: Roll, Pitch and Yaw needs to be in range -5 to +5"
        assert velocity in range(0,11), " moveHead: Velocity needs to be in range 0 to 10"
        requests.post('http://'+self.ip+'/api/beta/head/move',json={"Pitch": pitch, "Roll": roll, "Yaw": yaw, "Velocity": velocity})
    
    def headRoll(self,roll,velocity=1):
        assert roll in range(-5,6), " headRoll: Roll needs to be in range -5 to 5"
        requests.post('http://'+self.ip+'/api/beta/head/position',json={"Axis": "roll", "position": roll, "Velocity": velocity})

    def headPitch(self,pitch,velocity=1):
        assert pitch in range(-5,6), " headPitch: Pitch needs to be in range -5 to 5"
        requests.post('http://'+self.ip+'/api/beta/head/position',json={"Axis": "pitch", "position": pitch, "Velocity": velocity})
    
    def headYaw(self,yaw,velocity=1):
        assert yaw in range(-5,6), " headYaw: Yaw needs to be in range -5 to 5"
        requests.post('http://'+self.ip+'/api/beta/head/position',json={"Axis": "yaw", "position": yaw, "Velocity": velocity})

    def drive(self,linear_velocity, angular_velocity):
        assert linear_velocity in range(-100,101) and angular_velocity in range(-100,101), " drive: The velocities needs to be in the range -100 to 100"
        requests.post('http://'+self.ip+'/api/drive',json={"LinearVelocity": linear_velocity,"AngularVelocity": angular_velocity})

    def driveTime(self,linear_velocity, angular_velocity,time_in_milli_second):
        assert linear_velocity in range(-100,101) and angular_velocity in range(-100,101), " driveTime: The velocities needs to be in the range -100 to 100"
        assert isinstance(time_in_milli_second, int) or isinstance(time_in_milli_second, float), " driveTime: Time should be an integer or float and the unit is milli seconds"
        requests.post('http://'+self.ip+'/api/drive/time',json={"LinearVelocity": linear_velocity,"AngularVelocity": angular_velocity, "TimeMS": time_in_milli_second})

    def driveTrack(self,left_track_speed,right_track_speed):
        assert left_track_speed in range(-100,101) and right_track_speed in range(-100,101), " driveTrack: The velocities needs to be in the range -100 to 100"
        requests.post('http://'+self.ip+'/api/drive/track',json={"LeftTrackSpeed": left_track_speed,"RightTrackSpeed": right_track_speed})
    
    def stop(self):
        requests.post('http://'+self.ip+'/api/drive/stop')
        
    def sendBackpack(self,message):
        assert isinstance(message, str), " sendBackpack: Message sent to the Backpack should be a string"
        requests.post('http://'+self.ip+'/api/alpha/serialport',json={"Message": message})

    def populateImages(self):
        self.images_saved = []
        resp = requests.get('http://'+self.ip+'/api/images')
        for reply in resp.json():
            for out in reply["result"]:
                self.images_saved.append(out["name"])

    def populateAudio(self):
        self.audio_saved = []
        resp = requests.get('http://'+self.ip+'/api/audio')
        for reply in resp.json():
            for out in reply["result"]:
                self.audio_saved.append(out["name"])

    def populateLearnedFaces(self):
        self.faces_saved = []
        resp = requests.get('http://'+self.ip+'/api/beta/faces')
        for reply in resp.json():
            self.faces_saved = reply["result"]

    def printImageList(self):
        print(self.images_saved)
    
    def getImageList(self):
        return self.images_saved

    def printAudioList(self):
        print(self.audio_saved)
    
    def getAudioList(self):
        return self.audio_saved
    
    def printSubscriptionList(self):
        print(self.available_subscriptions)

    def startFaceRecognition(self):
        requests.post('http://'+self.ip+'/api/beta/faces/recognition/start')
    
    def stopFaceRecognition(self):
        requests.post('http://'+self.ip+'/api/beta/faces/recognition/stop')

    def printLearnedFaces(self):
        print(self.faces_saved)

    def getLearnedFaces(self):
        return self.faces_saved

    def clearLearnedFaces(self):
        requests.post('http://'+self.ip+'/api/beta/faces/clearall')
        self.faces_saved = []
    
    def learnFace(self,name):
        assert isinstance(name, str), " trainFace: name must be a string"
        requests.post('http://'+self.ip+'/api/beta/faces/training/start',json={"FaceId": name})
        print("Please look at Misty's face for 15 seconds..")
        for i in range(15):
            print(15-i)
            time.sleep(1)
        print("Face Captured!!")
        print("Please allow 15 second processing time !")
        for i in range(15):
            print(15-i)
            time.sleep(1)
        print("Face Trained")
        self.populateLearnedFaces()

    ##### WEB SOCKETS #####

    def backpack(self):
        if self.backpack_instance is not None:
            data = self.backpack_instance.data
            try:
                return json.loads(data)["message"]["message"]
            except:
                return json.loads(data)

        else:
            return " Backpack data is not subscribed, use the command robot_name.subscribe(\"StringMessage\")"

    def time_of_flight(self):
        if self.time_of_flight_instance[0] is not None or self.time_of_flight_instance[1] is not None or self.time_of_flight_instance[2] is not None or self.time_of_flight_instance[3] is not None:

            out = "{"
            for i in range(4):
                try:
                    data_out = json.loads(self.time_of_flight_instance[i].data)
                    #print(data_out)
                    out+="\""+data_out["message"]["sensorPosition"]+"\""+":"
                    out+=str(data_out["message"]["distanceInMeters"])+","
                except:
                    return json.loads(self.time_of_flight_instance[i].data)
            out = out[:-1]
            out+="}"
            return json.loads(out)
        else:
            return " TimeOfFlight not subscribed, use the command robot_name.subscribe(\"TimeOfFlight\")"

    def faceRec(self):
        data = json.loads(self.face_recognition_instance.data)
        try:
            out = "{ \"personName\" : \"" + data["message"]["personName"] + "\", \"distance\" : \"" + str(data["message"]["distance"]) + "\", \"elevation\" :\"" + str(data["message"]["elevation"]) + "\"}"
            return(json.loads(out))
        except:
            return json.loads(self.face_recognition_instance.data)
        

    def subscribe(self,Type,value=None,debounce =0):
        assert isinstance(Type, str), " subscribe: type name need to be string"

        if Type in self.available_subscriptions:

            if Type == "StringMessage":
                if self.backpack_instance is  None:
                    self.backpack_instance = Socket(self.ip,Type,_value=value, _debounce = debounce)
                    time.sleep(1)

            elif Type ==  "TimeOfFlight":
                if self.time_of_flight_instance[0] is None:
                    self.time_of_flight_instance[0] = Socket(self.ip,Type,_value="Left", _debounce = debounce)
                    time.sleep(0.05)
                    self.time_of_flight_instance[1] = Socket(self.ip,Type,_value="Center", _debounce = debounce)
                    time.sleep(0.05)
                    self.time_of_flight_instance[2] = Socket(self.ip,Type,_value="Right", _debounce = debounce)
                    time.sleep(0.05)
                    self.time_of_flight_instance[3] = Socket(self.ip,Type,_value="Back", _debounce = debounce)
                    time.sleep(1)

            elif Type == "FaceRecognition":
                if self.face_recognition_instance is None:
                    self.startFaceRecognition()
                    print("FaceRecStarted")
                    self.face_recognition_instance = Socket(self.ip,Type,_value="ComputerVision", _debounce = debounce)
                
        else:
            print(" subscribe: Type name - ",Type,"is not recognised by the robot, use <robot_name>.printSubscriptionList() to see the list of possible Type names")
    
    def unsubscribe(self,Type):
        assert isinstance(Type, str), " unsubscribe: type name need to be string"

        if Type in self.available_subscriptions:

            if Type == "StringMessage":

                if self.backpack_instance is not None:
                    self.backpack_instance.unsubscribe()
                    self.backpack_instance = None
                else:
                    print("Unsubscribe:",Type, "is not subscribed")

            elif Type ==  "TimeOfFlight":
                
                if self.time_of_flight_instance[0] is not None:
                    for i in range(4):
                        self.time_of_flight_instance[i].unsubscribe()
                        time.sleep(0.05)
                    self.time_of_flight_instance = [None]*4
                else:
                    print("Unsubscribe:",Type,"is not subscribed")

            if Type == "FaceRecognition":

                if self.face_recognition_instance is not None:
                    self.face_recognition_instance.unsubscribe()
                    self.face_recognition_instance = None
                    self.stopFaceRecognition()
                else:
                    print("Unsubscribe:",Type, "is not subscribed")

        else:
            print(" unsubscribe: Type name - ",Type,"is not recognised by the robot, use <robot_name>.printSubscriptionList() to see the list of possible Type names")


# Every web socket is considered an instance     
class Socket:

    def __init__(self, ip,Type, _value = None, _debounce = 0):

        self.ip = ip
        self.Type  = Type
        self.value = _value 
        self.debounce = _debounce
        self.data = "{\"status\":\"Not_Subscribed or just waiting for data\"}"
        self.event_name = None
        self.ws = None
        self.initial_flag = True
    
        dexter = threading.Thread(target=self.initiate)
        dexter.start()

    def initiate(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://"+self.ip+"/pubsub",on_message = self.on_message,on_error = self.on_error,on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(ping_timeout=10)

    def on_message(self,ws,message):
        if self.initial_flag:
            self.initial_flag = False
        else:
            self.data = message
        
    def on_error(self,ws, error):
        print(error)

    def on_close(self,ws):
        ws.send(str(self.get_unsubscribe_message(self.Type)))
        self.data = "{\"status\":\"Not_Subscribed or just waiting for data\"}"
        print("###",self.Type," socket is closed ###")

    def on_open(self,ws):
        def run(*args):
            self.ws.send(str(self.get_subscribe_message(self.Type)))
        thread.start_new_thread(run, ())

    def unsubscribe(self):
        self.on_close(self.ws)

    def get_subscribe_message(self,Type):

        self.event_name = str(randint(0,10000000000))

        if Type == "StringMessage":

            subscribeMsg = {
                "Operation": "subscribe",
                "Type": "StringMessage",
                "DebounceMs": self.debounce,
                "EventName": self.event_name,
                "Message": "",
                "ReturnProperty": "StringMessage"}

        elif Type == "TimeOfFlight":

            subscribeMsg = {
            "$id" : "1",
            "Operation": "subscribe",
            "Type": "TimeOfFlight",
            "DebounceMs": self.debounce,
            "EventName": self.event_name,
            "Message": "",
            "ReturnProperty": "",
            "EventConditions":
            [{
                "Property": "SensorPosition",
                "Inequality": "=",
                "Value": self.value
            }]}
        
        elif Type == "FaceRecognition":

            subscribeMsg = {
                "Operation": "subscribe",
                "Type": self.value,
                "DebounceMs": self.debounce,
                "EventName": self.event_name,
                "Message": "",
                "ReturnProperty": ""}

        return subscribeMsg

    def get_unsubscribe_message(self,Type):

        if Type == "StringMessage":

            unsubscribeMsg = {
                "Operation": "unsubscribe",
                "EventName": self.event_name,
                "Message": ""}

        elif Type == "TimeOfFlight":
            
            unsubscribeMsg = {
                "Operation": "unsubscribe",
                "EventName": self.event_name,
                "Message": ""}

        elif Type == "FaceRecognition":
            
            unsubscribeMsg = {
                "Operation": "unsubscribe",
                "EventName": self.event_name,
                "Message": ""}
        
        return unsubscribeMsg