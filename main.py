from tkinter import *
from PIL import ImageTk
from PIL import Image
import PIL.Image
import sys
from tkinter import font
import csv
import pandas as pd
import smtplib
from tkinter import messagebox
import tempfile
import os
import pandas as pd
import cv2
import numpy as np
from datetime import datetime
global win
import time
import datetime


# In[19]:


ts = time.time()      
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')


# # WINDOW 3

# In[20]:


def window3():
    
    def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass
         
            try:
                import unicodedata
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass
         
            return False
    
    def marking():
        recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainingImageLabel\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("CSV_files\\attendance.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['ID','NAME','DATE','TIME']
        attendance = pd.DataFrame(columns = col_names)    
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['ID'] == Id]['NAME'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['ID'],keep='first')    
            cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\\Attendance_"+date+".csv"
        attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        #print(attendance)
        res=attendance


    
    def enter_new_student():
        def training():
            def assure_path_exists(path):
                dir = os.path.dirname(path)
                if not os.path.exists(dir):
                    os.makedirs(dir)

            # Create Local Binary Patterns Histograms for face recognization
            recognizer = cv2.face.LBPHFaceRecognizer_create()

            # Using prebuilt frontal face training model, for face detection
            detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

            # Create method to get the images and label data
            def getImagesAndLabels(path):

                #get the path of all the files in the folder
                imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
                #print(imagePaths)
                
                #create empth face list
                faces=[]
                #create empty ID list
                Ids=[]
                #now looping through all the image paths and loading the Ids and the images
                for imagePath in imagePaths:
                    #loading the image and converting it to gray scale
                    pilImage=Image.open(imagePath).convert('L')
                    #Now we are converting the PIL image into numpy array
                    imageNp=np.array(pilImage,'uint8')
                    #getting the Id from the image
                    Id=int(os.path.split(imagePath)[-1].split(".")[1])
                    # extract the face from the training image sample
                    faces.append(imageNp)
                    Ids.append(Id)        
                return faces,Ids

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector =cv2.CascadeClassifier(harcascadePath)
            faces,Id = getImagesAndLabels("TrainingImage")
            recognizer.train(faces, np.array(Id))
            recognizer.save("TrainingImageLabel\Trainner.yml")
            res = "Image Trained"#+",".join(str(f) for f in Id)
            #message.configure(text= res)
            
            img = Image.open('Images_Used//7.jpeg')
            img = img.resize((1050,700), PIL.Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            label_ = Label(image = img)
            label_.place(x=300,y=1)
            w = Tk()
            w.overrideredirect(1)
            w.withdraw()
            w.mainloop()
            w.destroy()
        
        def insert_student(a,b,c):
            
            with open('CSV_files//attendance.csv', 'r') as f:
                reader = csv.reader(f)
                list2 = list(reader)
            f.close()
            flag1 = 1
            flag2 = 1
            flag3 = 1
            flag4 = 1
            flag5 = 1
            flag6 = 1
            inflag = 0
            if a=="" or b=="" or c=="":
                messagebox.showinfo("message",'Fill Complete form')
                flag1 = 0
            else:
                for i in list2:
                    if(a!=i[0]):
                        pass
                    else:
                        messagebox.showinfo("message",'Id is already in use!')
                        flag4=0

                #for j in list2:
                #    if(b!=j[1]):
                #        pass
                #    else:
                #        messagebox.showinfo("message",'Student name is already in use!')
                #        flag5=0
                        
                for k in list2:
                    if(c!=k[2]):
                        pass
                    else:
                        messagebox.showinfo("message",'Email address already in use!')
                        flag6=0
                        
                if(a.isdigit() and ((b>='A' and b<="Z") or (b>="a" and b<="z"))):
                    pass

                else:
                    messagebox.showinfo("message",'Type undefined!')
                    flag2 = 0


                #regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

                #if(re.search(regex,c)):    
                #    pass

                #else:  
                #    messagebox.showinfo("Error",'Incorrect email format, Enter again')
                #    flag3 = 0

            if (flag1==1 and flag2==1 and flag3==1 and flag4==1 and flag5==1 and flag6==1):
                with open('CSV_files//attendance.csv','a', newline = '') as f:
                    data_handler1 = csv.writer(f,delimiter = ',') 
                    data_handler1.writerow([a,b,c])
                    messagebox.showinfo("message","Record Entered. Please wait..!")
                        
        
            if a=="" and b=="" and c=="":
                messagebox.showinfo("message","Fill Above Form")
            else:
                
                def assure_path_exists(path):
                    dir = os.path.dirname(path) 
                    if not os.path.exists(dir): 
                        os.makedirs(dir)
                cam = cv2.VideoCapture(0)
                harcascadePath = "haarcascade_frontalface_default.xml"
                detector=cv2.CascadeClassifier(harcascadePath)
                sampleNum=0
                while(True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x,y,w,h) in faces:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                        #incrementing sample number 
                        sampleNum=sampleNum+1
                        #saving the captured face in the dataset folder TrainingImage
                        cv2.imwrite("TrainingImage\ "+b +"."+a +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                        #display the frame
                        cv2.imshow('frame',img)
                    #wait for 100 miliseconds 
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 100
                    elif sampleNum>100:
                        break
                cam.release()
                cv2.destroyAllWindows() 
                #res = "Images Saved for ID : " + a +" Name : "+ b
                #row = [a , b , c]
                #with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
                #    writer = csv.writer(csvFile)
                #    writer.writerow(row)
                #csvFile.close()
                #message.configure(text= res)
           
                cv2.destroyAllWindows()
                messagebox.showinfo("Message","Dataset Collected!")



        frame0=Frame(win2,width=1050,height=700)
        frame0.place(x=300,y=1)
        frame0.tkraise()
        label0.destroy()
        font_1 = font.Font(family = 'helvetica',size = 12,weight = "bold")
        label_1 = Label(frame0,text='Enter Student ID',bg = "RoyalBlue4",fg = "white",width = 20,height = 2)
        label_1['font']= font_1
        label_2 = Label(frame0,text="Enter Student Name",bg = "RoyalBlue4",fg = "white",width = 20,height = 2)
        label_2['font'] = font_1
        label_3 = Label(frame0,text="Enter Student Email ",bg = "RoyalBlue4",fg = "white",width = 20,height = 2)
        label_3['font'] = font_1
        
        button_2 = Button(frame0,text = " ENTER DATA AND SCAN", bg = 'white', fg = 'RoyalBlue4' , width = 25, height = 1,cursor = 'hand2',command=lambda:insert_student(entry_a.get(),entry_b.get(),entry_c.get()))
        #button_3 = Button(frame0,text = " TAKE STUDENT DATA ", bg = 'white', fg = 'RoyalBlue4' , width = 25, height = 1,cursor = 'hand2',command=lambda:open_cam(entry_a.get(),entry_b.get(),entry_c.get()))
        button_4 = Button(frame0,text = " TRAIN STUDENT DATA  ", bg = 'white', fg = 'RoyalBlue4' , width = 25, height = 1,cursor = 'hand2',command=training)
        
        font_2 = font.Font(family = "helvetica",size = 14,weight = "bold")
        font_2.configure(underline = True)
        button_2['font'] = font_2
        #button_3['font'] = font_2
        button_4['font'] = font_2
        
        entry_a = Entry(frame0)
        entry_b = Entry(frame0)
        entry_c = Entry(frame0)
        
        
        label_head = Label(frame0,text="STUDENT FORM",fg = "RoyalBlue4",width = 25,height = 2)
        label_head['font'] = font_2
        label_head.place(x=350,y=30)

        label_1.place(x=300,y=100)
        entry_a.place(x=550,y=110)

        label_2.place(x=300,y=200)
        entry_b.place(x=550,y=210)

        label_3.place(x=300,y=300)
        entry_c.place(x=550,y=310)

        button_2.place(x=350,y=450)
        #button_3.place(x=350,y=500)
        button_4.place(x=350,y=550)


    def view_attendance():
        w4 =Tk()
        w4.title("Attendance Sheet")
        w4.geometry('865x650')
        df1=pd.read_csv("CSV_files\\attendance.csv")
        df2=pd.read_csv("Attendance\\attendance_"+date+".csv")
        x=pd.merge(df1,df2,on='ID',how='outer')
        del(x['NAME_y'])
        x.to_csv("Final.csv",index=False)
        with open("Final.csv", newline = "") as file:
            reader = csv.reader(file)
            # r and c tell us where to grid the labels
            r = 20
            for col in reader:
                c = 20
                for row in col:
                    # i've added some styling
                    label = Label(w4, width = 30, height = 2,                                        text = row, relief = RIDGE)
                    label.grid(row = r, column = c)

                    c += 1
                r += 1
        w4.mainloop()
        w4.mainloop()
        w4.mainloop()
    def exit():
        win2.destroy()
    
    global label0,frame2
    win2=Tk()
    win2.title('Smart_Attendance')
    win2.geometry('1350x700+0+0')
    dashboard_frame=Frame(win2,width=300,height=800,bg='#1C2739')
    dashboard_frame.place(x=0,y=0)
    dashboard_frame.tkraise()

    image00 = PIL.Image.open('Images_Used//7.jpeg')
    image00 = image00.resize((1050,700), PIL.Image.ANTIALIAS) # (height, width)
    back_image00 = ImageTk.PhotoImage(image00)

    frame2=Frame(win2,width=1050,height=700)
    frame2.place(x=300,y=1)
    frame2.tkraise()

    label0=Label(image=back_image00)
    label0.place(x=300,y=1)


    img1=PhotoImage(file='Images_Used//divider-logo.png')
    img0=PhotoImage(file='Images_Used//dashboard-logo.png')



    dashboard_label = Label(image=img0, bg='#1C2739')
    dashboard_label.place(x=5, y=3)
    divider_logo = Label(image=img1, bg='#1C2739')
    divider_logo.place(x=5, y=50)

    font_1 = font.Font(family = 'helvetica',size = 12,weight = "bold")


    image = PIL.Image.open('Images_Used//T1.png')
    image = image.resize((290, 80), PIL.Image.ANTIALIAS) 
    back_image = ImageTk.PhotoImage(image)

    b1 = Button(image=back_image,command=view_attendance)
    b1.place(x=5,y=150)

    image1 = PIL.Image.open('Images_Used//T2.png')
    image1 = image1.resize((290, 80), PIL.Image.ANTIALIAS)
    back_image1 = ImageTk.PhotoImage(image1)

    b2 = Button(image=back_image1,command=enter_new_student)
    b2.place(x=5,y=250)

    image0 = PIL.Image.open('Images_Used//c3.png')
    image0 = image0.resize((290, 80), PIL.Image.ANTIALIAS)
    back_image0 = ImageTk.PhotoImage(image0)

    b4 = Button(image=back_image0,command=marking)
    b4.place(x=5,y=350)
    
    image3 = PIL.Image.open('Images_Used//5.png')
    image3 = image3.resize((290, 80), PIL.Image.ANTIALIAS) 
    back_image3 = ImageTk.PhotoImage(image3)

    b4 = Button(image=back_image3,command=email_sent)
    b4.place(x=5,y=450)

    image2 = PIL.Image.open('Images_Used//exit.png')
    image2 = image2.resize((290, 80), PIL.Image.ANTIALIAS) 
    back_image2 = ImageTk.PhotoImage(image2)

    b3 = Button(image=back_image2,command=exit)
    b3.place(x=5,y=550)
    win2.mainloop()

    


# In[21]:


def email_sent():
    df1=pd.read_csv("CSV_files\\attendance.csv")
    df2=pd.read_csv("Attendance\\attendance_"+date+".csv")
    x=pd.merge(df1,df2,on='ID',how='outer')
    del(x['NAME_y'])
    x.to_csv("Final.csv",index=False)
    with open("Final.csv",newline="") as f:
        reader=csv.DictReader(f)
        for row in reader:
            if row['DATE']=="":
                content = "Dear Student,You are absent today"
                mail = smtplib.SMTP('smtp.gmail.com',587) #server,port->465 or 587
                mail.ehlo() #identify yourself to the server ehlo for extended smtp
                mail.starttls() #encrypted
                #first make your email less secure from this link https://myaccount.google.com/u/2/lesssecureapps
                mail.login('cloudstorezcl@gmail.com','chilwyqfijpkvoic')  #enter your email address and password here
                mail.sendmail('cloudstorezcl@gmail.com',row['EMAIL'],content) #send mail #from,to,content
                mail.close() #closing the connection
                print("Email Sent successfully")
        messagebox.showinfo("Email Info","Email Sent Successfully!")


# # WINDOW 2

# In[22]:


def window2():
    def destroy():
        win1.destroy()
    def printing():
        #reading from csv writing in txt
        with open("CSV_files//newfile.txt", "w") as my_output_file:
            cs = pd.read_csv("CSV_files\\attendance.csv",header=None,index_col=None)
            with open("CSV_files//attendance.csv", "r") as my_input_file:
                [ my_output_file.write(" | ".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()

        #reading from file and storing into reader and converting into string as .write() takes string
        strnew = ""
        with open('CSV_files//newfile.txt',"r") as f:
            reader = f.read()
            strnew = reader
            
#         for checking
        with open('CSV_files//print.txt',"w") as f:
            f.write(strnew)
        
        #printing
        filename = tempfile.mktemp("attendance.txt")#creating a temp file

        open (filename , "w").write(strnew)

        os.startfile(filename, "print")
        messagebox.showinfo("Print","Printing Request sent successfully!")

    def view_passwords():
        # open file
        w3 = Tk()
        w3.title("Teachers Record")
        w3.geometry('430x290')
        with open("CSV_files//users_passwords.csv", newline = "") as file:
            reader = csv.reader(file)
            # r and c tell us where to grid the labels
            r = 20
            for col in reader:
                c = 20
                for row in col:
                    label = Label(w3, width = 30, height = 2,                                        text = row, relief = RIDGE)
                    label.grid(row = r, column = c)

                    c += 1
                r += 1
        w3.mainloop() 
        
    def view_attendance():
        w4 =Tk()
        w4.title("Attendance Sheet")
        w4.geometry('900x700')
        df1=pd.read_csv("CSV_files\\attendance.csv")
        df2=pd.read_csv("Attendance\\attendance_"+date+".csv")
        x=pd.merge(df1,df2,on='ID',how='outer')
        del(x['NAME_y'])
        x.to_csv("Final.csv",index='False')
        with open("Final.csv", newline = "") as file:
            reader = csv.reader(file)
            # r and c tell us where to grid the labels
            r = 20
            for col in reader:
                c = 20
                for row in col:
                    # i've added some styling
                    label = Label(w4, width = 30, height = 2,                                        text = row, relief = RIDGE)
                    label.grid(row = r, column = c)

                    c += 1
                r += 1
        w4.mainloop()
                    
    def enter_new_record(a,b):
        with open('CSV_files//users_passwords.csv', 'r') as f:
            reader = csv.reader(f)
            list1 = list(reader)
            
        flag1 = 1
        flag2 = 1
        flag3 = 1
        flag4 = 1

        if a=="" or b=="":
                messagebox.showinfo("message",' Fill Complete form')
                flag1 = 0
        else:
            for i in list1:
                if(a!=i[0]):
                    pass
                else:
                    messagebox.showinfo("message",'Username is already in use!')
                    flag3=0

            for j in list1:
                if(b!=j[1]):
                    pass
                else:
                    messagebox.showinfo("message",'Use another password!')
                    flag4=0
            
            if ((a>='A' and a<="Z") or (a>="a" and a<="z")):
                pass
            else:
                messagebox.showinfo("message",'Type undefined!')
                flag2 = 0
                

        if (flag1==1 and flag2==1 and flag3 == 1 and flag4 ==1):
            with open('CSV_files//users_passwords.csv','a', newline = '') as f:
                data_handler1 = csv.writer(f,delimiter = ',') 
                data_handler1.writerow([a,b])
                messagebox.showinfo("message",'New record entered')

                # framea.destroy()
            for widget in framea.winfo_children():
                  widget.destroy()
        
        img = Image.open('Images_Used//7.jpeg')
        img = img.resize((1050,700), PIL.Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label_ = Label(image = img)
        label_.place(x=300,y=1)
        w = Tk()
        w.overrideredirect(1)
        w.withdraw()
        w.mainloop()
        w.destroy()
           
    def new_record():
        global framea
        framea=Frame(win1,width=1050,height=700)
        framea.place(x=300,y=1)
        framea.tkraise()
        label0.destroy()
        global entry_1,entry_2
        font_1 = font.Font(family = 'helvetica',size = 12,weight = "bold")
        label_1 = Label(framea,text='Enter Teacher Name',bg = "RoyalBlue4",fg = "white",width = 20,height = 2)
        label_1['font']= font_1
        label_2 = Label(framea,text="Enter Password",bg = "RoyalBlue4",fg = "white",width = 20,height = 2)
        label_2['font'] = font_1
        button_2 = Button(framea,text = " CLICK HERE TO ENTER", bg = 'RoyalBlue4', fg = 'white' , width = 25, height = 1,cursor = 'hand2',command=lambda:enter_new_record(entry_1.get(),entry_2.get()))
        font_2 = font.Font(family = "helvetica",size = 14,weight = "bold")
        font_2.configure(underline = True)
        button_2['font'] = font_2
        entry_1 = Entry(framea)
        entry_2 = Entry(framea,show="*")
    
        label_head = Label(framea,text="TEACHER'S ENTRY",fg = "RoyalBlue4",width = 50,height = 5)
        label_head['font'] = font_2

        label_head.place(x=190,y=100)

        label_1.place(x=300,y=250)
        entry_1.place(x=550,y=260)

        label_2.place(x=300,y=350)
        entry_2.place(x=550,y=360)

        button_2.place(x=350,y=460)
        
    global win1    
    win1=Tk()
    win1.title('Smart_Attendance')
    win1.geometry('1350x700+0+0')
    dashboard_frame=Frame(win1,width=300,height=800,bg='#1C2739')
    dashboard_frame.place(x=0,y=0)
    dashboard_frame.tkraise()

    image00 = PIL.Image.open('Images_Used//7.jpeg')
    image00 = image00.resize((1050,700), PIL.Image.ANTIALIAS) # (height, width)
    back_image00 = ImageTk.PhotoImage(image00)

    frame2=Frame(win1,width=1050,height=700)
    frame2.place(x=300,y=1)
    frame2.tkraise()

    label0=Label(image=back_image00)
    label0.place(x=300,y=1)


    img1=PhotoImage(file='Images_Used//divider-logo.png')
    img0=PhotoImage(file='Images_Used//dashboard-logo.png')


    dashboard_label = Label(image=img0, bg='#1C2739')
    dashboard_label.place(x=5, y=3)
    divider_logo = Label(image=img1, bg='#1C2739')
    divider_logo.place(x=5, y=50)

    font_1 = font.Font(family = 'helvetica',size = 12,weight = "bold")


    image = PIL.Image.open('Images_Used//2.jpeg')
    image = image.resize((290, 80), PIL.Image.ANTIALIAS) 
    back_image = ImageTk.PhotoImage(image)

    b1 = Button(image=back_image,command = view_attendance)
    b1.place(x=5,y=100)    

    b2 = Button(image=back_image1,command=view_passwords)
    b2.place(x=5,y=200)

    image2 = PIL.Image.open('Images_Used//4.jpeg')
    image2 = image2.resize((290, 80), PIL.Image.ANTIALIAS)
    back_image2 = ImageTk.PhotoImage(image2)

    b3 = Button(image=back_image2,command=new_record)
    b3.place(x=5,y=300)

    image5 = PIL.Image.open('Images_Used//exit.png')
    image5 = image5.resize((290, 80), PIL.Image.ANTIALIAS) 
    back_image5 = ImageTk.PhotoImage(image5)

    b6 = Button(image=back_image5,command=destroy)
    b6.place(x=5,y=600)
    win1.mainloop()


# # WINDOW 1

# In[23]:


def checker():
    global e1,e2
    username = e1.get()
    password = e2.get()
    check_password(username,password)


# In[24]:


def check_password(u,p):
    import csv
    from tkinter import messagebox
    with open("CSV_files//users_passwords.csv",'r') as f:
        x = csv.reader(f)
        temp = 1
        for i in x:
            for j in range(1):
                if(u== 'Admin' and p == '12345'  ):
                    win.destroy()# current page destroy
                    window2()
                    temp=0
                    break
                else:
                    if(i[j]== u and i[j+1] == p):
                        win.destroy()
                        window3()
                        temp=0
                        break
                    elif(u== '' and p == ''):
                        temp=2
        if(temp != 0 and temp!=2) :
             msg = messagebox.showinfo("message",'Sorry incorrect Username or password') 
        if(temp==2):
             msg = messagebox.showinfo("message",'Please Enter username and password') 
def x():
    win.destroy()


# In[25]:


#WINDOW 1
win = Tk()
win.title('Login')
win.geometry('1350x700+0+0')

#FRAMES
topframe = Frame(win)
topframe.pack()

#For background Image
image = PIL.Image.open('Images_Used//1.jpg')
back_image = ImageTk.PhotoImage(image)
label_ = Label(image = back_image)
label_.pack()

#For button
b1_image = PhotoImage(file="Images_Used//login.png")
b1 = Button(image=b1_image,cursor="hand2",command=checker)
b1.place(x=140,y=500)
b2_image = PhotoImage(file="Images_Used//cancel.png")
b2 = Button(image=b2_image,cursor="hand2",command=x)
b2.place(x=320,y=500)

#For Entry box
e1 = Entry(win,bd=5,fg="magenta4",relief=GROOVE,width=30)
e1.place(x=300,y=300)
e2 = Entry(win,bd=5,fg="magenta4",show="*",relief=GROOVE,width=30)
e2.place(x=300,y=400)

#For text box
font_1 = font.Font(family = 'helvetica',size = 12,weight = "bold")
label_1 = Label(win,text='USERNAME :',fg="blue violet")
label_1['font']= font_1
label_2 = Label(win,text="PASSWORD :",fg="blue violet")
label_2['font'] = font_1
label_1.place(x=130,y=300)
label_2.place(x=130,y=400)

#For icon
win.iconbitmap("Images_Used//icon.ico")
win.mainloop()

