from tkinter import *
from tkinter import ttk
#from server3 import *
import threading
import socket
import sys
import satvik
import algorithm
import threading
from queue import Queue
from functools import partial
import pyautogui
import time
import cv2
import pickle
import struct
import pygame
list_of_connection_object=[]
list_of_ip=[]
line=Queue()
def socket_create():
	try:
		global host
		global port
		global s
		global words
		global dic
		host=''
		port=9999
		s=socket.socket()
		
		l,words=satvik.words()
		dic=algorithm.dictionary_builder('comm.xlsx')
		
	except socket.error as msg:
		print('Error my friend:'+ str(msg))


#--------------------------------------------------------------------------------------------------------------------------------#

def socket_bind():
	try:
		global host
		global port
		global s
		print('binding take place......')
		s.bind((host,port))
		s.listen(5)
	except socket.error as msg:
		print("I am Fail")
		socket_bind()
#-------------------------------------------------------------------------------------------------------------------------------#
def socket_accept():
	
	global s
	global list_of_connection_object
	while True:
		conn,adress=s.accept()
		list_of_connection_object.append(conn)
		list_of_ip.append(str(adress[0]))
		make(list_of_ip)
		#option_menu.children['menu'].delete(0,'end')
		#for ll in list_of_ip:
			#option_menu.children['menu'].add_command(label=ll,command=partial(print_it2,ll))
		#print('address:'+adress[0]+'ip:'+str(adress[1]))
		#send_commands(conn) 
#--------------------------------------------------------------------------------------------------------------------------------#
def inner_command(exc,cmd,exc2):
	global list_of_ip
	#print(cmd.get())
	conn=get_connection_object(cmd.get())
	send_commands(exc,conn,exc2)
#---------------------------------------------------------------------------------------------------------------------------------#
def send_commands(entry,conn,entry2):
	global s
	global words
	global dic
	
	
	
	
	cmd=entry.get()
	if cmd=='quit':
		pass
	else:
		cmd=algorithm.probability(cmd,words,dic,'')
		print(cmd)
		if cmd=='cd':
			sub_part=entry2.get()
			cmd=cmd+' '+sub_part
		elif cmd=='mkdir':
			sub_part=entry2.get()
			cmd=cmd+' '+sub_part
		elif cmd=='open':
			sub_part=entry2.get()
			cmd='explorer'+' '+sub_part
		elif cmd=='type nul>':
			sub_part=entry2.get()
			cmd='type nul>'+' '+sub_part
		conn.send(str.encode(cmd))
		#data=conn.recv(1024)
		#try:
			#array=pickle.loads(data)
			#cv2.imshow('Window',array)
		#except:
			#pass
		#sender_response=str(data,'utf-8')
		#texing_result(sender_response)
		#print(sender_response,end='')
		#var.set('')

#---------------------------------------------------------------------------------------------------------------------------------#

def get_connection_object(selected_ip):
	global list_of_ip
	global list_of_connection_object
	
	index=list_of_ip.index(selected_ip)
	conn=list_of_connection_object[index]
	return conn


#----------------------------------------------------------------------------------------------------------------------------------#
def thread_creater():
	for i in range(0,2):
		t=threading.Thread(target=work)
		t.deamon=True
		t.start()

#------------------------------------------------------------------------------------------------------------------------------------#
def job_maker():
	global line
	for i in range(1,3):
		line.put(i)
	line.join()

#-------------------------------------------------------------------------------------------------------------------------------------#
def work():
	global line
	while True:
			x=line.get()
			if x==1:
				socket_create()
				socket_bind()
				socket_accept()
			if x==2:
				inner_command()
	line.task_done()
#--------------------------------------------------------------------------------------------------------------------------------------#
def main():

	thread_creater()
	job_maker()
#---------------------------------------------------------------------------------------------------------------------------------------#
def work_1():
	while True:
		socket_create()
		socket_bind()
		socket_accept()
#-----------------------------------------------------------------------------------------------------------------------------------------#
def make(list):
			option_menu=OptionMenu(root,var,*list,command=print_it)
			option_menu.place(x=100,y=290)
#-------------------------------------------------------------------------------------------------------------------------------------------#
def work_2(exc,string,exc2):
		print('\n'+string.get())
		inner_command(exc,string,exc2)
		
#------------------------------------------------------------------------------------------------------------------------------------------#
#main()
#--------------------------------------------------------------------------------------------------------------------------------------------#
def print_it(event):
	global var
	print(var.get())
#----------------------------------------------------------------------------------------------------------------------------------------------#

def print_it2(text):
	global entry
	global var
	var.set(text)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def texing_result(text):
	global text_box
	window_maker()	
	text_box.config(state='normal')
	text_box.insert('end','\n'+text)
	text_box.config(state='disabled')
#--------------------------------------------------------------------------------------------------------------------------------------------------#
def job_1():
	#global option_menu
	tam=threading.Thread(target=work_1)
	tam.daemon=True
	tam.start()
#--------------------------------------------------------------------------------------------------------------------------------------------------#
def job_2():
	global entry
	global var
	print('\n'+var.get())
	td=threading.Thread(target=work_2,args=(entry,var))
	td.daemon=True
	td.start()
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def fun():
	global THREAD_ALLOWED
	THREAD_ALLOWED=True
	conn=get_connection_object(var.get())
	screen=pygame.display.set_mode((1360,750))
	while THREAD_ALLOWED:
		
		for e in pygame.event.get():
			clicking_indicator=' '
			mainx,mainy=pygame.mouse.get_pos()
			sending_string='string '+str(mainx)+' '+str(mainy)
			if e.type==pygame.MOUSEBUTTONDOWN:
				clicking_indicator=' clicked'
		
			print(clicking_indicator)
			conn.send(str.encode(sending_string+clicking_indicator))
			time.sleep(1)
		time.sleep(0.03)
		pygame.display.update()
			
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def fun1():
	global THREAD_ALLOWED1
	THREAD_ALLOWED1=True
	conn=get_connection_object(var.get())
	conn.send(str.encode('see'))
	data = b""
	payload_size = struct.calcsize(">L")
	print("payload_size: {}".format(payload_size))
	while True:
		if THREAD_ALLOWED1:
			while len(data) < payload_size:
				print("Recv: {}".format(len(data)))
				data += conn.recv(4096)

			print("Done Recv: {}".format(len(data)))
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack(">L", packed_msg_size)[0]
			print("msg_size: {}".format(msg_size))
			while len(data) < msg_size:
				data += conn.recv(4096)
			frame_data = data[:msg_size]
			data = data[msg_size:]

			frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
			frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
			cv2.imshow('ImageWindow',frame)
			cv2.waitKey(1)
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def stop():
	global THREAD_ALLOWED
	global thres
	THREAD_ALLOWED=False
	thres.join()
	conn=get_connection_object(var.get())
	conn.send(str.encode('set'))
#----------------------------------------------------------------------------------------------------------------------------------------------------#
def stop4():
	global THREAD_ALLOWED1
	global thread
	conn=get_connection_object(var.get())
	conn.send(str.encode('set'))
	THREAD_ALLOWED=False
	thread.join()
#-----------------------------------------------------------------------------------------------------------------------------------------------------#
def rock(asd):
	conn=get_connection_object(var.get())
	conn.send(str.encode('text'+' '+asd.get('1.0',END)))

#------------------------------------------------------------------------------------------------------------------------------------------------------#
def work_4():
	global thread
	thread=threading.Thread(target=fun1)
	thread.daemon=True
	thread.start()

#----------------------------------------------------------------------------------------------------------------------------------------------------#
def work_3():
	global thres
	thres=threading.Thread(target=fun)
	thres.daemon=True
	thres.start()
#-----------------------------------------------------------------------------------------------------------------------------------------------------#
def window_maker():
	global root
	global text_box
	global scroll_bar
	global var
	global option_menu
	global ip_list
	global entry
	ip_list=[1,'127.0.0.1']
	
	root=Tk()
	
	var=StringVar()
	option_menu=OptionMenu(root,var,*ip_list,command=print_it)
	#option_menu.children['menu'].add_command(label='8',command=print_it2)
	text_box=Text(root,height=2,width=85)
	entry=Entry(root)
	entry2=Entry(root)
	butt=Button(root,text='start server',bg='red',fg='white',command=job_1,height=5,width=10)
	butt.place(x=100,y=390)
	butt2=Button(root,text='coversation',bg='blue',fg='white',command=partial(work_2,entry,var,entry2),height=5,width=10)
	butt2.place(x=200,y=390)
	butt3=Button(root,text='start mouse controll',bg='green',fg='white',command=work_3,height=5,width=17)
	butt3.place(x=100,y=590)
	butt4=Button(root,text='stop mouse controll',bg='green',fg='white',command=stop,height=5,width=15)
	butt4.place(x=200,y=590)
	butt5=Button(root,text='show monitor screen',command=work_4)
	butt5.place(x=100,y=490)
	butt6=Button(root,text='stop_kr',command=partial(rock,text_box))
	butt6.place(x=100,y=150)
	scroll_bar=Scrollbar(root)
	scroll_bar.pack(side=RIGHT,fill=Y)
	entry.place(x=100,y=190)
	entry2.place(x=100,y=240)
	option_menu.place(x=100,y=290)
	text_box.pack(side=RIGHT,fill=Y)
	scroll_bar.config(command=text_box.yview)
	text_box.config(yscrollcommand=scroll_bar.set)
	'''while a!=None:
		a=''
		a=input()
		root.config(bg=a)'''
#--------------------------------------------------------------------------------------------------------------------------------------------------#	


window_maker()
	

ter=threading.Thread(target=root.mainloop())
ter.daemon=True
ter.start()