import os
import time
import signal
import subprocess
from datetime import datetime
from select import select

camera = dict()
command = dict()
currentVideo = dict()
commandTimeout = 5

def startVideo(camera, resolution="width=1280,height=720"):	
    directory = "camera/" + str(camera) + "/" + datetime.now().strftime("%Y-%m-%d") + "/" + datetime.now().strftime("%H") + "/"
    filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.mp4'
    audio = camera + 1;

    currentVideo['filename'] = filename;
    currentVideo['time'] = datetime.now()

    if not os.path.exists(directory):
            os.makedirs(directory)
            
    return subprocess.Popen(['gst-launch',
                                '-e', 'v4l2src', 'device=/dev/video' + str(camera), '!', 'image/jpeg,' + resolution, '!', 'jpegdec', '!',
                                'tee', 'name=t', '!', 'queue', '!', 'ffenc_mpeg4', 'bitrate=3200000', '!',
                                'mp4mux', 'name=mux', '!', 'filesink', 'location=' + directory + filename,
                                'autoaudiosrc', '!', 'lamemp3enc', '!', 'mux.', 't.', '!', 'queue', '!', 'colorspace', '!', 'autovideosink'])

#gst-launch -e v4l2src ! 'image/jpeg,width=1280,height=720' ! jpegdec !  tee name=t ! queue ! ffenc_mpeg4 bitrate=3200000 ! mp4mux name=mux ! filesink location=example.mp4   autoaudiosrc ! lamemp3enc ! mux.   t. ! queue ! colorspace ! autovideosink

def startCam(camera, cameraNumber, resolution = "big"):
    if(resolution == 'big'):
        resolution = "width=1280,height=720"
    elif(resolution == 'medium' or resolution == 'med'):
        resolution = "width=640,height=480"
    
    cameraNumber = cameraNumber - 1
    camera[cameraNumber] = startVideo(cameraNumber, resolution)
    return camera

def stopCam(camera, cameraNumber):
    cameraNumber = cameraNumber - 1
    camera[cameraNumber] = startVideo(cameraNumber, resolution)
    return camera
    

def startCams(camera):
    camera[0] = startVideo(0)
    camera[1] = startVideo(1)
    camera[2] = startVideo(2)
    camera[3] = startVideo(3)
#	camera[4] = startVideo(4)
#	camera[5] = startVideo(5)

    return camera
    
def stopCams(camera):
#	camera[0].send_signal(signal.SIGINT);
#	camera[1].send_signal(signal.SIGINT);
#	camera[2].send_signal(signal.SIGINT);
    subprocess.Popen(['killall', '-INT', 'gst-launch-0.10'])
    time.sleep(1)
    
    return camera

def restartCams(camera):
    camera = stopCams(camera)
    camera = startCams(camera)

    return camera

camera = startCams(camera)

#camera1 = startVideo(0)
#camera2 = startVideo(1)
#camera3 = startVideo(2)

while 1:
    command['input']= raw_input("> ")
    
    if(command['input']):
        command['list'] = command['input'].lower()
        command['list'] = command['list'].split()
                
        if len(command['list']) <= 2:
            if len(command['list']) <= 1:
                command['list'].append(0)
                
            command['list'].append(0)
                
        if command['list'][0] == 'quit':
            print "Closing cameras..."
            camera = stopCams(camera)
            print "Goodbye!"
            break

        elif command['list'][0] == 'restart':
            print "Restarting cameras..."
            camera = restartCams(camera)
            
        elif command['list'][0] == 'start':
            print type(command['list'][1])
            
            if(command['list'][1]):
                if(command['list'][1] == 'all'):
                    camera = startCams(camera, command['list'][2])
                
                else:
                    cameraNumber = int(command['list'][1])

                    if len(command['list']) > 2 and command['list'][2]:
                        camera = startCam(camera, cameraNumber, command['list'][2])
                    else:
                        camera = startCam(camera, cameraNumber)

            else:
                cameraNumber = raw_input("What number? \n> ")
                cameraNumber = int(cameraNumber)
                camera = startCam(camera, cameraNumber)
            
        elif command['list'][0] == 'stop':
            if(command['list'][1]):
                if(command['list'][1] == 'all'):
                    camera = stopCams(camera)	
                else:
                    cameraNumber = int(command['list'][1])

                    if len(command['list']) > 2 and command['list'][2]:
                        camera = stopCam(camera, cameraNumber, command['list'][2])
                    else:
                        camera = stopCam(camera, cameraNumber)
            else:
                cameraNumber = raw_input("What number? \n> ")
                
                if(cameraNumber == 'all'):
                    camera = stopCams(camera)
                
                else:
                    cameraNumber = int(cameraNumber)
                    camera = stopCam(camera, cameraNumber)


#			camera = stopCams(camera)
            
        elif command['list'][0] == 'kill':
            subprocess.Popen(['killall', 'gst-launch-0.10'])
            
        elif command['list'][0] == 'time':
            print "The time is... " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print "The video started at... " + currentVideo['time'].strftime("%Y-%m-%d %H:%M:%S")
            print "Time elapsed... " + str(timeElapsed.seconds)
            
        elif command['input']:
    #		print "Saving annotation: " + command + " at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open("annotations.txt", "a") as myfile:
                myfile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + command['input'] + "\n")

