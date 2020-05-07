# Wrapper: Python

Python library to work with your Misty robot. Currently in BETA. Supported by the community and not Misty Robotics.

## Requirements

python >= 3.4

requests

websocket 0.52.0

## Installing

### Step 1: Easy start

If you are already comfortable using Python, skip to step 2

Install anaconda for python >= 3.4 version
```
https://www.anaconda.com/download/
```
Enter the following in your terminal 
```
conda create -n <your_custom_environment_name> python=3.4 requests
```
Now your environment is setup. To activate your environment enter the below command in your terminal:

Say you used the name 'misty_developer' in the conda create step
```
source activate misty_developer
pip install mistyPy
pip install websocket-client==0.52.0
```
skip step 2
```
Note:
Everytime you open a new termial, enter 
source activate <your_custom_environment_name>
```

### Step 2: Self Setup 

use the command after setting up python >= 3.4
```
pip install mistyPy
pip install requests
pip install websocket-client==0.52.0
```

## Current support

#### API

Chanaging LED, Changing image on screen, Playing audio, Moving Head, Driving Misty

#### WebSockets

Backpack string stream, Time of Flights, Face Recognition, Face Training, Face Detection

## Writing your own python program for Misty

```
import mistyPy
```
#### Connecting to the robot
Syntax: robot_name = mistyPy.Robot("Enter the robot IP here")
Name your misty- > let me call mine 'mia'  
```
mia = mistyPy.Robot("10.0.1.206")
```
Now you can refer to your robot as mia

#### Change LED color
Synatx: robot_name.changeLED(red,green,blue)
```
mia.changeLED(0,200,255) # Purple
```

#### Change image on the screen

Syntax: robot_name.changeImage("image_name.format")
```
mia.changeImage("Happy.jpg")
```
to get a list of all the images saved on your misty
```
mia.printImageList()        # prints ["Happy.jpg","Confused.jpg","Angry.jpg" ....]
images = mia.getImageList() # Return list of saved image files
```

#### Play saved audio file

Synatx: robot_name.playAudio("file_name.format")
```
mia.playAudio("008-Ah.wav")
```
to get a list of all the audio files saved on your misty
```
mia.printAudioList()        # prints ["eeee.wav","Aaah.wav","nah.wav"....]
audios = mia.getAudioList() # returns list of saved audio files 

```

#### Battery check

Synatx: output = robot_name.battery()
```
charge_percentage = mia.battery()
print(charge_percentage)
```

#### Move the head

Roll, pitch and yaw values can range from -5 to 5

One Command to control roll, pitch, and yaw

Syntax: robot_name.moveHead(roll_value, pitch_value, yaw_value, optional velocity_value)
```
mia.moveHead(-1,-5,3)
mia.moveHead(-1,-5,3, velocity = 5)
```

Individial command per axis (also can take an optional velocity argument)
```
mia.headRoll(-1)
mia.headPitch(-5, velocity = 5)
mia.headYaw(3)
```

#### Drive Misty

There are three modes to drive Misty
1. drive      : you tell the linear and angular speed and Misty keeps on driving 
2. driveTime  : you tell misty the speeds and also how long misty has to execute it
3. driveTrack : instead of telling misty linear and angular speed, you tell the speed of left and right wheels individually

Syntax: robot_name.drive(linear_velocity, angular_velocity)

Syntax: robot_name.driveTime(linear_velocity, angular_velocity,time_in_milli_second)

Syntax: robot_name.driveTrack(left_track_speed,right_track_speed)
```
mia.drive(50,20)         # goes forward and turns
mia.driveTime(70,0,3000) # goes forward for three seconds
mia.driveTrack(50,-50)   # spins in the same place
```

Note: 
velocity range -100 to 100

#### Stop Driving

You could either send a command with velocities 0 or use this

Syntax: robot_name.stop()
```
mia.stop()
```

#### Train a Face for Misty to recognise

Syntax: robot_name.learnFace(<name_of_person>)
```
mia.learnFace("Ian")
```

Misty takes 15 seconds to capture your face and another 15 seconds to process it!

You would see a countdown printing in the terminal

#### Get a list of the Learned Faces

Syntax: robot_name.getLearnedFaces()
```
mia.printLearnedFaces()       # prints [Ian, CP, John, Allison, Woo,....]
names = mia.getLearnedFaces() # returns the names of trained faces as a list
```

#### Delete all Learned Faces

Syntax: robot_name.clearLearnedFaces()
```
mia.clearLearnedFaces()
```

### WebSockets - a brief into 

Consider all the above commands as a short handshakes while websockets work like you keep holding hands for a long time. You could continuosly stream data with websockets. Comes in handy when working with sensors on Misty, Arduino/Raspberry backpacks.

To start the handshake you got to subscribe to a topic

--- Continuos data stream ---

To end the handshake you got to unsubscribe from the same topic

--- No more data ---

#### Arduino/RaspberryPy backpack

To start the hanshake / to subscribe to the backpack (anything you send from arduino Serial.println("your_data") to Misty)

Syntax: robot_name.subscribe("StringMessage")
```
mia.subscribe("StringMessage")
```
This streams all data into the function call 'backpack()'

Syntax: robot_name.backpack()

You could call this any number of times at any time instant to get the data steram from you arduino

Lets say arduino is sending me temparature data in celcius and i want to turn my air cooler on at a threshold of 25˚C
```
while True:
    temp = mia.backpack()
    if int(temp) > 25:
        turn_on_air_cooler()
    else:
        pass
```
To end the handshake / to unsubscribe from the backpack data stream

Syntax: robot_name.unsubscribe("StringMessage")
```
mia.unsubscribe("StringMessage")
```
#### Time Of Flights

Misty has three time of flight sensors in the front and one on the back. They stream distance to obstacles in meters. 

To start handshake / subscribe to time of flight sensors data

Syntax: robot_name.subscribe("TimeOfFlight")
```
mia.subscribe("TimeOfFlight")
```
This streams all 4 time of flight sensor data into the function call 'time_of_flight()' 

Syntax: robot_name.time_of_flight()
```
incoming_data = mia.time_of_flight()
```
print(incoming_data) would print {'Left': 0.233, 'Center': 0.072, 'Right': 0.037, 'Back': 0.115}

To get just the Left time of flight sensor data
```
print(incoming_data["Left"])
```

Say misty is driving backwards and you want to stop if the wall is just or closer than 10 cm
```
mia.drive(-10,0)
while True:
    if mia.time_of_flight()["Back"] <= 0.010:
        mia.stop()
        break
```

#### Computer Vision

To start the Face Recognition / Face Detection you subscribe to the websocket first

Syntax: robot_name.subscribe("FaceRecognition")
```
mia.subscribe("FaceRecognition")
```
This streams all data into the function call 'faceRec()'

Syntax: robot_name.faceRec()

Once subscribed to Face Recognition you could call faceRec() anytime to pull the latest data from Misty

```
while True:
    data = mia.faceRec()
    print(data)                     # {'personName' : 'Samanta', 'distance' : '95', 'elevation' : '6'} 
    name      = data["personName"]  # You could extract specific values of your interest like this
    distance  = data["distance"]    # units in mm
    elevation = data["elevation"]

```

If a face is detected and the person is unknown the "personName" field would output "unknown_person"

To stop Face Recognition / Face Detection

Syntax: robot_name.unsubscribe("FaceRecognition")
```
mia.unsubscribe("FaceRecognition")
```

---

**WARRANTY DISCLAIMER.**

* General. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, MISTY ROBOTICS PROVIDES THIS SAMPLE SOFTWARE “AS-IS” AND DISCLAIMS ALL WARRANTIES AND CONDITIONS, WHETHER EXPRESS, IMPLIED, OR STATUTORY, INCLUDING THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, QUIET ENJOYMENT, ACCURACY, AND NON-INFRINGEMENT OF THIRD-PARTY RIGHTS. MISTY ROBOTICS DOES NOT GUARANTEE ANY SPECIFIC RESULTS FROM THE USE OF THIS SAMPLE SOFTWARE. MISTY ROBOTICS MAKES NO WARRANTY THAT THIS SAMPLE SOFTWARE WILL BE UNINTERRUPTED, FREE OF VIRUSES OR OTHER HARMFUL CODE, TIMELY, SECURE, OR ERROR-FREE.
* Use at Your Own Risk. YOU USE THIS SAMPLE SOFTWARE AND THE PRODUCT AT YOUR OWN DISCRETION AND RISK. YOU WILL BE SOLELY RESPONSIBLE FOR (AND MISTY ROBOTICS DISCLAIMS) ANY AND ALL LOSS, LIABILITY, OR DAMAGES, INCLUDING TO ANY HOME, PERSONAL ITEMS, PRODUCT, OTHER PERIPHERALS CONNECTED TO THE PRODUCT, COMPUTER, AND MOBILE DEVICE, RESULTING FROM YOUR USE OF THIS SAMPLE SOFTWARE OR PRODUCT.

Please refer to the Misty Robotics End User License Agreement for further information and full details: https://www.mistyrobotics.com/legal/end-user-license-agreement/

--- 

*Copyright 2020 Misty Robotics*<br>
*Licensed under the Apache License, Version 2.0*<br>
*http://www.apache.org/licenses/LICENSE-2.0*
