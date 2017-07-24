# -*- coding: utf-8 -*-
import vk_api
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import datetime

root = Tk()
root.resizable(width=False, height=False)
root.title("VKChat by Kamidorik & Feelatkeen")
root.geometry("320x120")
root.iconbitmap('vk_icon.ico')


global lastmessage, attachment
vk_photo_url = None
chatid = 0
userid = 0
groupid = 0
lastmessage = [ ]
attachment = ""


def twostepaut():
	messagebox.showinfo(u"Сообщение", u"Посмотрите в консоль")
	key = input("Введите код для доступа к аккаунту: ")
	remember_device = True
	return key, remember_device

def OnCheck(event):
	global chatid, userid, groupid
	widget = event.widget
	selection=widget.curselection()
	value = widget.get(selection[0])
	namelabel['text'] = value
	for item in dialogs:
		if item['title'] == value:
			if 'chat_id' in item:
				chatid = item['chat_id']
				userid = 0
				groupid = 0
			if 'user_id' in item:
				userid = item['user_id']
				chatid = 0
				groupid = 0
			if 'group_id' in item:
				groupid = item['group_id']
				chatid = 0
				userid = 0
	chatbox.delete(0, END)
	

def sendmessage(event):
	global attachment
	me = vk.users.get()
	msg = enterbox.get("1.0", END)[:-1]
	if 'вложение:' in msg:
		if attachment == "":
			attachment = msg.split('вложение:',1)[1]
			msg = msg.split('вложение:',1)[0]
		else:
			attachment = attachment+','+msg.split('вложение:',1)[1] 
			msg = msg.split('вложение:',1)[0]
	time = datetime.datetime.now().strftime('[%H:%M:%S]')
	if chatid != 0:
		response = vk.messages.send(chat_id = chatid, message =  str(msg), attachment = str(attachment))
		if msg != "":
			chatbox.insert(END, time+' '+me[0]['first_name']+' '+me[0]['last_name']+': '+msg)
	elif userid != 0:
		response = vk.messages.send(user_id = userid, message =  str(msg), attachment = str(attachment))
		if msg != "":
			chatbox.insert(END, time+' '+me[0]['first_name']+': '+msg)
	elif groupid != 0:
		response = vk.messages.send(peer_id = groupid, message =  str(msg), attachment = str(attachment))
		if msg != "":
			chatbox.insert(END, time+' '+me[0]['first_name']+': '+msg)
	if len(msg) == 2:
		time = datetime.datetime.fromtimestamp(int(answer['items'][0]['date'])).strftime('[%H:%M:%S]')
		chatbox.insert(END, time+' '+me[0]['first_name']+' '+me[0]['last_name']+' отправил вложения:')
		chatbox.insert(END, attachment)
		lastmessage.append(attachment)
	enterbox.delete('1.0', END)
	attachment = ""

def checkmessages():
	answer = vk.messages.get(count = 1, filters = 0, time_offest = 0, last_message_id = 0)
	getmessuser = vk.users.get(user_ids = answer['items'][0]['user_id'])
	if answer is not None and answer['items']:
		lastmessid = answer['items'][0]['id']
		for item in answer['items']:
			global lastmessage
			if 'chat_id' in answer['items'][0]:
				if (answer['items'][0]['body'] not in lastmessage) and (chatid == answer['items'][0]['chat_id']) and (answer['items'][0]['body'] != ""):
					time = datetime.datetime.fromtimestamp(int(answer['items'][0]['date'])).strftime('[%H:%M:%S]')
					chatbox.insert(END, time+' '+getmessuser[0]['first_name']+' '+getmessuser[0]['last_name']+': '+answer['items'][0]['body'])
					lastmessage.append(answer['items'][0]['body'])
			elif 'user_id' in answer['items'][0]:
				if (answer['items'][0]['body'] not in lastmessage) and (userid == answer['items'][0]['user_id']) and (answer['items'][0]['user_id'] > 0) and (answer['items'][0]['body'] != ""):
					time = datetime.datetime.fromtimestamp(int(answer['items'][0]['date'])).strftime('[%H:%M:%S]')
					chatbox.insert(END, time+' '+getmessuser[0]['first_name']+': '+answer['items'][0]['body'])
					lastmessage.append(answer['items'][0]['body'])
				elif (answer['items'][0]['body'] not in lastmessage) and (groupid == answer['items'][0]['user_id']) and (answer['items'][0]['user_id'] < 0) and (answer['items'][0]['body'] != ""):
					grid0 = str(answer['items'][0]['user_id'])
					grid1 = grid0.replace("-", "")
					getmessgroup = vk.groups.getById(group_id = int(grid1))
					time = datetime.datetime.fromtimestamp(int(answer['items'][0]['date'])).strftime('[%H:%M:%S]')
					chatbox.insert(END, time+' '+getmessgroup[0]['name']+': '+answer['items'][0]['body'])
					lastmessage.append(answer['items'][0]['body'])
			if 'attachments' in answer['items'][0]:
				for item in answer['items'][0]['attachments']:
					if item['type'] == 'photo':
						vk_attachment = 'photo'+str(item['photo']['owner_id'])+'_'+str(item['photo']['id'])+'_'+str(item['photo']['access_key'])
						typo = "фотографию"
					elif item['type'] == 'video':
						vk_attachment =  'video'+str(item['video']['owner_id'])+'_'+str(item['video']['id'])+'_'+str(item['video']['access_key'])
						typo = "видеозапись"
					elif item['type'] == 'audio':
						vk_attachment =  'audio'+str(item['audio']['owner_id'])+'_'+str(item['audio']['id'])
						typo = "аудиозапись"
					elif item['type'] == 'doc':
						vk_attachment =  'doc'+str(item['doc']['owner_id'])+'_'+str(item['doc']['id'])+'_'+str(item['doc']['access_key'])
						typo = "документ"
					elif item['type'] == 'wall':
						vk_attachment =  'wall'+str(item['wall']['from_id'])+'_'+str(item['wall']['id'])
						typo = "запись на стене"
					elif item['type'] == 'market':
						vk_attachment =  'market'+str(item['market']['owner_id'])+'_'+str(item['market']['id'])
						typo = "документ"
					time = datetime.datetime.fromtimestamp(int(answer['items'][0]['date'])).strftime('[%H:%M:%S]')
					if (vk_attachment not in lastmessage) and ((('chat_id' in answer['items'][0]) and (chatid == answer['items'][0]['chat_id'])) or (userid == answer['items'][0]['user_id'])) and (answer['items'][0]['user_id'] > 0):
						chatbox.insert(END, time+' '+getmessuser[0]['first_name']+' '+getmessuser[0]['last_name']+' отправил '+typo+':')
						chatbox.insert(END, vk_attachment)
						lastmessage.append(vk_attachment)
					elif (vk_attachment not in lastmessage) and (groupid == answer['items'][0]['user_id']) and (answer['items'][0]['user_id'] < 0):
						grid0 = str(answer['items'][0]['user_id'])
						grid1 = grid0.replace("-", "")
						getmessgroup = vk.groups.getById(group_id = int(grid1))
						chatbox.insert(END, time+' '+getmessgroup[0]['name']+' отправил '+typo+':')
						chatbox.insert(END, vk_attachment)
						lastmessage.append(vk_attachment)
	root.after(500, checkmessages)

def sendimage():
	global attachment
	fname = askopenfilename()
	if fname:
		try:
			upload = vk_api.VkUpload(vk_session)
			photo = upload.photo_messages(
				fname
			)
			vk_photo_url = 'photo{}_{}'.format(
				photo[0]['owner_id'], photo[0]['id']
			)
			if attachment == "":
				attachment = vk_photo_url
			else:
				attachment = attachment+','+vk_photo_url  
			messagebox.showinfo(u"Сообщение", u"Фотография успешно загружена")
		except Exception as e:
			messagebox.showerror(u"Ошибка", u"Не удалось загрузить фотографию")
			return

def senddocument():
	global attachment
	fname = askopenfilename()
	if fname:
		try:
			upload = vk_api.VkUpload(vk_session)
			doc = upload.document(
				fname,
			)
			vk_doc_url = 'doc{}_{}'.format(
				doc[0]['owner_id'], doc[0]['id']
			)
			if attachment == "":
				attachment = vk_doc_url
			else:
				attachment = attachment+','+vk_doc_url 
			messagebox.showinfo(u"Сообщение", u"Документ успешно загружен")
		except Exception as e:
			messagebox.showerror(u"Ошибка", u"Не удалось загрузить документ")
			return

def popup(event):
    menu.post(event.x_root, event.y_root)

def entervk(event):
	global vk_session, vk, dialogs
	login = str(logininput.get("1.0", END)[:-1])
	password = str(pswdinput.get())

	vk_session = vk_api.VkApi(
        login, password,
        auth_handler=twostepaut
    )

	try:
		vk_session.auth()
	except Exception as error_msg:
		messagebox.showerror(u"Ошибка", u"Неправильный логин или пароль")
		print(error_msg)
		return

	vk = vk_session.get_api()
	dialogs = []
	root.destroy()
	root2 = Tk()
	root2.iconbitmap('vk_icon.ico')
	root2.resizable(width=False, height=False)
	root2.title("VKChat by Kamidorik & Feelatkeen")
	global namelabel
	namelabel = Label(root2, text=u"Название Чата/Конфы", font="Arial 10")
	namelabel.grid(row=0, column=1)
	global chatbox
	chatbox = Listbox(root2, height=10, width=50)
	chatbox.grid(row=1, column=1)
	userlist = Listbox(root2)
	mydialog = vk.messages.getDialogs(count = 10)
	for item in mydialog['items']:
		if 'chat_id' in item['message']:
			dialogs.append({ "title": item['message']['title'], 'chat_id': item['message']['chat_id']} )
			userlist.insert(END, item['message']['title'])
		else:
			if item['message']['user_id'] > 0:
				getmessuser = vk.users.get(user_ids = item['message']['user_id'])
				dialogs.append({ "title": getmessuser[0]['first_name']+' '+getmessuser[0]['last_name'], "user_id": item['message']['user_id']})
				userlist.insert(END, getmessuser[0]['first_name']+' '+getmessuser[0]['last_name'])
			elif item['message']['user_id'] < 0:
				grid0 = str(item['message']['user_id'])
				grid1 = grid0.replace("-", "")
				getmessgroup = vk.groups.getById(group_id = int(grid1))
				dialogs.append({ "title": getmessgroup[0]['name'], "group_id": item['message']['user_id']})
				userlist.insert(END, getmessgroup[0]['name'])
	userlist.bind("<Double-Button-1>", OnCheck)
	userlist.grid(row=1, column=2)
	global enterbox, menu
	enterbox = Text(root2, height=1, width=50)
	enterbox.grid(row=2, column=1)
	menu = Menu(root2, tearoff=0)
	menu.add_command(label="Добавить фото", command=sendimage)
	menu.add_command(label="Добавить документ", command=senddocument)
	enterbutton = Button(root2, text="Отправить", width=10, height=1, bg="white", fg="black")
	enterbox.bind("<Return>", sendmessage)
	enterbutton.bind("<Button-1>", sendmessage)
	enterbutton.bind("<Button-3>", popup)
	enterbutton.grid(row=2, column=2)
	root.after(500, checkmessages)
	root2.mainloop()

loginlabel = Label(root, text=u"Логин", font="Arial 10")
loginlabel.pack()
logininput = Text(root, width=15, height=1)
logininput.pack()
pswdlabel = Label(root, text=u"Пароль", font="Arial 10")
pswdlabel.pack()
pswdinput = Text(root, width=15, height=1)
pswdinput = Entry(root, show="*", width=15)
pswdinput.pack()
btn = Button(root, text="Войти", width=10, height=1,bg="white", fg="black")
btn.bind("<Button-1>", entervk)
btn.pack()
root.mainloop()
