from mistyPy import Robot

# TODO: Replace with your IP
misty = Robot("192.168.0.31") # This is the IP of my misty. Replace with your IP
misty.changeLED(0, 0, 255)
misty.moveHeadPosition(0, 0, 0, 100) # center the head
misty.moveArmsDegrees(0, 0, 100, 100)