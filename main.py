#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import face_recognition
import numpy
import os
from datetime import datetime
import pandas as pd
from csv import writer
from tkinter import *  
import tkinter.messagebox
from tkinter import font as tkFont
import tkinter as tk
from tkinter import ttk,messagebox
import pickle
from PIL import ImageTk, Image  
import csv
from tkinter import simpledialog
from pandastable import Table, TableModel
from tkinter import Frame
from easygui import *
from tkcalendar import Calendar, DateEntry
import time
import smtplib
from email.message import EmailMessage
from tkinter import filedialog


# In[2]:


root = Tk()
root.title("Attendence App")
root.geometry("945x628")
root.resizable(False,False)
bg = PhotoImage(file = "bg_image.png")

def new_member():
    fscreen = Tk()
    fscreen.title("Security")
    fscreen.geometry("600x200")
    
    
    def change_password_request():
        pscreen = Tk()
        pscreen.title("Change Password")
        pscreen.geometry("600x200")
        
        def change_password():
            password_dataset = open("password", "rb")
            existing_password = pickle.load(password_dataset)
            entered_old_password = tf1.get()
            entered_new_password = tf2.get()
            entered_new_password_confirm = tf3.get()
            if(existing_password == entered_old_password):
                if(entered_new_password == entered_new_password_confirm):
                    password_dataset = open("password", "rb")
                    existing_password = pickle.load(password_dataset)
                    empty_file = []
                    file = open("password", "wb")
                    file.write(pickle.dumps(empty_file))
                    file.close()
                    file1 = open("password", "wb")
                    file1.write(pickle.dumps(entered_new_password))
                    file1.close()
                else:
                    tkinter.messagebox.showinfo("Message","Password do not match !!!!")
            else:
                tkinter.messagebox.showinfo("Message","Entered Incorrect Password !!!!")
        
        label1 = Label(pscreen,text = "Enter the Old Password : ",font =("Helvetica",15,"bold"))
        label1.place(x = 40,y = 25)
        tf1 = tk.Entry(pscreen, borderwidth = 2,width =29,show = "*")
        tf1.place(x = 300,y = 30)
        label2 = Label(pscreen,text = "Enter the New Password : ",font =("Helvetica",15,"bold"))
        label2.place(x = 35,y = 65)
        tf2 = tk.Entry(pscreen, borderwidth = 2,width =29,show = "*")
        tf2.place(x = 300,y = 70)
        label3 = Label(pscreen,text = "Confirm Password : ",font =("Helvetica",15,"bold"))
        label3.place(x = 90,y = 105)
        tf3 = tk.Entry(pscreen, borderwidth = 2,width =29,show = "*")
        tf3.place(x = 300,y = 110)
        button1 = Button(pscreen,text = "Submit",font =("Helvetica",15,"bold"),command = change_password)
        button1.place(x = 180,y = 145)
        button2 = Button(pscreen,text = "Quit",font =("Helvetica",15,"bold"),command = pscreen.destroy)
        button2.place(x = 300,y = 145)
        
        
        pscreen.mainloop()
    

    def p_check():
        password_dataset = open("password", "rb")
        existing_password = pickle.load(password_dataset)
        password = t_1.get()
        if (password == existing_password):
            fscreen.destroy()
            screen = Tk()
            screen.title("Add New Member")
            screen.geometry("600x300")    

            def adding_new_member():
                existing_fileobj = open("face_enc", "rb")
                existing_mydata = pickle.load(existing_fileobj)
                images = []
                global my_image
                screen.filename = filedialog.askopenfilename(initialdir="/desktop",title = "Select a File",
                                                       filetypes =(("png files","*.png"),("all files","*.*")))
                #my_label = Label(screen,text = root.filename).pack()
                person_name_with_extension = os.path.basename(screen.filename)
                person_name = person_name_with_extension.split(".")[0]
                current_img = cv2.imread(screen.filename)
                images.append(current_img)
                def faceEncodings(images):                        # Encoding -- HOG Algorithm
                    encode_List = []
                    for img in images:
                        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                        encode = face_recognition.face_encodings(img)[0]
                        encode_List.append(encode)
                    return encode_List
                encode_List_Known = faceEncodings(images)
                #my_image_label = Label(root,text = person_name).pack()
                existing_mydata["names"].append(person_name)
                existing_mydata["encodings"].append(encode_List_Known[0])
                f = open("face_enc", "wb")
                f.write(pickle.dumps(existing_mydata))
                f.close()
                tkinter.messagebox.showinfo("Message","Finished")
                #my_image = ImageTk.PhotoImage(Image.open(root.filename))
                #my_image_label = Label(image = my_image).pack()

            def get_mail():
                emails_dataset = open("emails", "rb")
                emails = pickle.load(emails_dataset)
                name = t1.get(1.0, "end-1c")
                mail = t2.get(1.0, "end-1c")
                emails[name] = mail
                f = open("emails", "wb")
                f.write(pickle.dumps(emails))
                f.close()
                #my_email_label = Label(screen,text = Student_emails).pack()

            l1 = Label(screen,text = "Enter your name : ",font =("Helvetica",15,"bold"))
            l1.place(x = 30,y = 25)
            t1 = Text(screen, borderwidth = 2,wrap = "word",width =29,height = 1)
            t1.place(x = 250,y = 33)
            l2 = Label(screen,text = "Enter your email : ",font =("Helvetica",15,"bold"))
            l2.place(x = 30,y = 65)
            t2 = Text(screen, borderwidth = 2,wrap = "word",width =29,height = 1)
            t2.place(x = 250,y = 73)
            b1 = Button(screen,text = "Submit Details",font =("Helvetica",15,"bold"),command = get_mail)
            b1.place(x = 180,y = 110)
            l3 = Label(screen,text = "Select Image : ",font =("Helvetica",20,"bold"))
            l3.place(x = 30,y = 170)
            b2 = Button(screen,text = "Import Image",font =("Helvetica",20,"bold"),command = adding_new_member)
            b2.place(x = 250,y=170)
            b2 = Button(screen, text="Quit", font =("Helvetica",15,"bold"),command=screen.destroy)
            b2.place(x = 220,y = 240)

            screen.mainloop()
        else:
            tkinter.messagebox.showinfo("Alert","Wrong Password")
            fscreen.destroy()
        
        
    l_1 = Label(fscreen,text = "Enter the Password : ",font =("Helvetica",15,"bold"))
    l_1.place(x = 80,y = 25)
    t_1 = tk.Entry(fscreen, borderwidth = 2,width =29,show = "*")
    t_1.place(x = 300,y = 30)
    b_1 = Button(fscreen,text = "Submit",font =("Helvetica",15,"bold"),command = p_check)
    b_1.place(x = 80,y = 80)
    b_2 = Button(fscreen,text = "Quit",font =("Helvetica",15,"bold"),command = fscreen.destroy)
    b_2.place(x = 430,y = 80)
    b_3 = Button(fscreen, text="Change Password", font =("Helvetica",15,"bold"),command=change_password_request)
    b_3.place(x = 200,y = 80)
    
    fscreen.mainloop()

def recording_attendence():
    p = "P"
    def attendence(name):
        time_now = datetime.now()
        t_str = time_now.strftime("%H:%M:%S")
        d_str = time_now.strftime("%Y-%m-%d")
        
        df = pd.read_csv("Attendence_file.csv")
        df_curdate = df.loc[df["Date"] == time_now.strftime("%Y-%m-%d")]
        already_entered_name = list(df_curdate["Name"])
        already_entered_date = list(df_curdate["Date"])
        
        if(name in already_entered_name):
            if(time_now.strftime("%Y-%m-%d") in already_entered_date):
                print("Already Entered")
            else:
                l_presents = []
                l_presents.append([name,p,time_now.strftime("%H:%M:%S"),time_now.strftime("%Y-%m-%d")])
                with open("Attendence_file.csv","a") as f:
                    writer = csv.writer(f)
                    for i in l_presents:
                        writer.writerow(i)

        else:
            l_presents = []
            l_presents.append([name,p,time_now.strftime("%H:%M:%S"),time_now.strftime("%Y-%m-%d")])
            with open("Attendence_file.csv","a") as f:
                writer = csv.writer(f)
                for i in l_presents:
                    writer.writerow(i)

    
    #file = open("face_enc", "rb")
    #data = pickle.load(file)
    data = pickle.loads(open('face_enc', "rb").read())
    cam = cv2.VideoCapture(0)
    person_Name = data["names"]
    while True:
        ret,frame = cam.read()
        faces = cv2.resize(frame,(0,0),None,0.25,0.25)
        faces = cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
        faces_current_frame = face_recognition.face_locations(faces)
        encodes_current_frame = face_recognition.face_encodings(faces,faces_current_frame)
        for encodeFace,faceLoc in zip(encodes_current_frame, faces_current_frame):
            matches = face_recognition.compare_faces(data["encodings"],encodeFace)
            faceDis = face_recognition.face_distance(data["encodings"],encodeFace)
            match_index = numpy.argmin(faceDis)
            if matches[match_index]:
                name = person_Name[match_index]
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                                
                attendence(name)   # Calling the function to mark the attendence of the person
                #cv2.putText(frame,"Attendence Marked",(x1+10,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
        key = cv2.waitKey(1) & 0xFF
    
        if key==ord("q"):
            break
        cv2.imshow("Camera",frame)
    
    
    cam.release()
    cv2.destroyAllWindows()
    

def marking_attendence():
    emails_dataset = open("emails", "rb")
    emails = pickle.load(emails_dataset)
    time_now = datetime.now()
    df = pd.read_csv("Attendence_file.csv")
    df_curdate = df.loc[df["Date"] == time_now.strftime("%Y-%m-%d")]
    df_pr_curdate = df_curdate.loc[df_curdate["Status"] == "P"]
    l1 = list(df_pr_curdate["Name"])
    l2 = list(df_pr_curdate["Time"])
    for i,j in zip(l1,l2):
        d_str = time_now.strftime("%Y-%m-%d")
        def send_mail(name,time,d_str,email):
            msg = EmailMessage()
            msg.set_content(" Hi "+name+" !!\n Your present is marked \n Date - "+d_str+"\n Time - "+time)
            msg['Subject'] = 'Attendence'
            msg['From'] = "sanchitjain223223@gmail.com"
            msg['To'] = email
            # Send the message via our own SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("sanchitjain223223@gmail.com", "ziykuiglcgmzumzk")
            server.send_message(msg)
            server.quit()
        send_mail(i,j,d_str,emails[i])    
    
    total_students = list(emails.keys())
    present_students = list(df_pr_curdate["Name"])
    absent_names = list(set(total_students) - set(present_students))
    l_absentes = []
    for j in absent_names:
        l_absentes.append([j,"A","-",time_now.strftime("%Y-%m-%d")])
    with open("Attendence_file.csv","a") as f:
        writer = csv.writer(f)
        for i in l_absentes:
            writer.writerow(i)
    tkinter.messagebox.showinfo("Message","Attendence is Marked !!!!!")
        
            
            
def See_Attendence():
    emails_dataset = open("emails", "rb")
    emails = pickle.load(emails_dataset)
    total_students = list(emails.keys())
    time_now = datetime.now()
    df = pd.read_csv("Attendence_file.csv")
    df_curdate = df.loc[df["Date"] == time_now.strftime("%Y-%m-%d")]
    df_pr_curdate = df_curdate.loc[df_curdate["Status"] == "P"]    
    present_students = list(df_pr_curdate["Name"])
    absent_names = list(set(total_students) - set(present_students))
    def listToString(s): 
        str1 = "" 
        for i in s: 
            str1 += i + ","  
        return str1
    present_students_names = listToString(present_students)
    absent_students_names = listToString(absent_names)
    tkinter.messagebox.showinfo("See Atendence","Date: "+time_now.strftime("%Y-%m-%d")
                                +"\n\nPresent Students: \n" + present_students_names +
                                "\n\n"+ "Absent Students : \n"+ absent_students_names)
    
    
def report():
    win= Tk()
    #Set the Geometry
    win.geometry("550x150")
    win.title("Report")
    
    def show_output():
        dt1 = cal.get_date()
        str1 = dt1.strftime("%y-%m-%d")
        dt2 = cal1.get_date()
        str2 = dt2.strftime("%y-%m-%d")
        selected_name = namechoosen.get()
        df = pd.read_csv("Attendence_file.csv")
        df_specificdf = df.loc[df["Name"] == selected_name]
        final_df = df_specificdf[df_specificdf["Date"].between("20"+str(str1),"20"+str(str2))]
        specific_report = dict(final_df.value_counts(df_specificdf["Status"]))
        if("P" in specific_report):
            no_of_present = specific_report["P"]
        else:
            no_of_present = 0
        if("A" in specific_report):
            no_of_absent = specific_report["A"]
        else:
            no_of_absent = 0
        tkinter.messagebox.showinfo("REPORT","Dates: "+"20"+str(str1)+"  ---  "+"20"+str(str2)
                                    +"\n\nNo. of Presents (P): " +" - "+str(no_of_present)+
                                    "\n\n"+ "No. of Absents(A) : "+" - "+str(no_of_absent))
    
    label = Label(win,text = "Name",font=("Helvetica",15,"bold"),fg = "black")
    label.place(x = 105,y = 20)
    #name = Text(win, borderwidth = 2,wrap = "word",width =29,height = 2)
    #name.place(x = 100,y = 20)
    emails_dataset = open("emails", "rb")
    emails = pickle.load(emails_dataset)
    n = StringVar()
    namechoosen = ttk.Combobox(win, width = 27, textvariable = n,state = "readonly")

    # Adding combobox drop down list
    namechoosen['values'] = list(emails.keys())
    namechoosen.place(x = 200, y = 25)
    namechoosen.current()

    label1 = Label(win,text = "Start Date",font=("Helvetica",15,"bold"),fg = "black")
    label1.place(x = 80,y = 50)
    cal = DateEntry(win, width= 16, background= "magenta3", foreground= "white",bd=2)
    cal.place(x = 200,y = 55)
    #b1 = Button(win,text = "Read",command = lambda:date_upd(cal,l1))
    #b1.place(x = 340,y = 55)
    #l1 = Label(win,bg = "yellow")
    #l1.place(x= 400,y = 55)
    label2 = Label(win,text = "End Date",font=("Helvetica",15,"bold"),fg = "black")
    label2.place(x = 80,y = 80)
    cal1 = DateEntry(win, width= 16, background= "magenta3", foreground= "white",bd=2)
    cal1.place(x = 200,y = 80)
    #b2 = Button(win,text = "Read",command = lambda:date_upd(cal1,l2))
    #b2.place(x = 340,y = 80)
    #l2 = Label(win,bg = "yellow")
    #l2.place(x= 400,y = 80)
    b2 = Button(win,text = "SUBMIT",command = show_output)
    b2.place(x = 180,y = 110)
    b2 = Button(win, text="QUIT",command=win.destroy)
    b2.place(x = 250,y = 110)
    win.mainloop()
    
    
def detailed_report():
    win1= Tk()
    win1.geometry("550x150")
    win1.title("Detailed Report")
    
    def name_detailed_report():
        selected_name1 = namechoosen1.get()
        df = pd.read_csv("Attendence_file.csv")
        df_specificdf = df.loc[df["Name"] == selected_name1]
        class TestApp(Frame):
            def __init__(self, parent=None):
                self.parent = parent
                Frame.__init__(self)
                self.main = self.master
                self.main.geometry('600x400+200+100')
                self.main.title('Detailed Report')
                f = Frame(self.main)
                f.pack(fill=tk.BOTH,expand=1)
                self.table = pt = Table(f, dataframe=df_specificdf,showtoolbar=True)
                pt.show()
                return
        TestApp()
    
        
    label = Label(win1,text = "Name -- ",font=("Helvetica",20,"bold"),fg = "black")
    label.place(x = 80,y = 25)
    emails_dataset = open("emails", "rb")
    emails = pickle.load(emails_dataset)
    n = StringVar()
    namechoosen1 = ttk.Combobox(win1,font = ("Helvetica",20),width = 20, textvariable = n,state = "readonly")
    namechoosen1['values'] = list(emails.keys())
    namechoosen1.place(x = 200, y = 25)
    namechoosen1.current()
    b1 = Button(win1,text = "SUBMIT",font =("Helvetica",20),command = name_detailed_report)
    b1.place(x = 150,y = 80)
    b2 = Button(win1, text="QUIT",font =("Helvetica",20),command=win1.destroy)
    b2.place(x = 300,y = 80)
    win1.mainloop()
     
    
label = Label( root, image = bg)
label.place(x = 0, y = 0)    
    
#label1 = Label(root,text = "Attendence Management Sysytem",font=("Helvetica",50,"bold","underline"),fg = "black")
#label1.place(x = 70,y = 30)

img_b1 = PhotoImage(file = "img_ra.png")
b1 = Button(root,height=110,width=198,image = img_b1,command = recording_attendence)
b1.place(x = 25,y = 80)

img_b2 = PhotoImage(file = "img_ma1.png")
b2 = Button(root,height=110,width=198, image = img_b2,command = marking_attendence)
b2.place(x = 25,y = 240)

img_b3 = PhotoImage(file = "img_sa.png")
b3 = Button(root,height=110,width=198,image = img_b3,command = See_Attendence)
b3.place(x = 25,y = 400)

img_b4 = PhotoImage(file = "img_r.png")
b4 = Button(root,height=110,width=198,image = img_b4,command = report)
b4.place(x = 720,y = 80)

img_b5 = PhotoImage(file = "img_dr.png")
b5 = Button(root,height=110,width=198,image = img_b5,command = detailed_report)
b5.place(x = 720,y = 240)

img_b6 = PhotoImage(file = "img_new_mem.png")
b6 = Button(root,height=110,width=198,image = img_b6,command = new_member)
b6.place(x = 380,y = 30)

img_b7 = PhotoImage(file = "img_quit.png")
b7 = Button(root,height=110,width=198,image = img_b7,command = root.destroy)
b7.place(x = 720,y = 400)

root.mainloop()


# In[ ]:




