# mistyPy

Official Python library to work with your Misty robot. Currently in BETA

## Requirements

python >= 3.4

requests

websocket

## Installing

### Step 1: Easy start

If you are already comfortable using Python, skip to step 2

Install anaconda for python >= 3.4 version
```
https://www.anaconda.com/download/
```
Enter the following in your terminal 
```
conda create -n <your_custom_environment_name> python=3.4 requests mistyPy
```
Now your environment is setup. To activate your environment enter the below command in your terminal:

Say you used the name 'misty_developer' in the conda create step
```
source activate misty_developer
pip install websocket
```

### Step 2: Self Setup 

use the command after setting up python >= 3.4
```
pip install mistyPy
pip install requests
pip install websocket
```

## Current support

#### API

Chanaging LED, Changing image on screen, Playing audio, Moving Head, Driving Misty

#### WebSockets

Backpack string stream, Time of Flights

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
