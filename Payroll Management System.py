from tkinter import *
import mysql.connector as sql
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import datetime
import calendar
#============================SQL COMMANDS============================
mycon=sql.connect(host='localhost',user='root',passwd='root')
cur=mycon.cursor()
cur.execute('create database if not exists payroll')
mycon.commit()
cur.execute('use payroll')
mycon.commit()
cur.execute('create table if not exists login_info(username varchar(50) PRIMARY KEY,password varchar(50))')
mycon.commit()
cur.execute('create table if not exists employee_details(emp_id varchar(20),emp_name varchar(100),emp_fathers_name varchar(100),emp_mothers_name varchar(100),gender varchar(5),D_O_B varchar(15),designation varchar(50),emp_PF_NO varchar(50),emp_ESI varchar(50),department varchar(50),division varchar(50),branch varchar(50),bank_branch varchar(50),bank_no varchar(50),address varchar(100),contact_no varchar(11),email_address varchar(100))')
mycon.commit()
try:
    cur.execute('insert into login_info values("admin","admin")')
    mycon.commit()
except:
    pass
#==================================================================================
now = datetime.datetime.now()
days=calendar.monthrange(now.year, now.month)[1]
months = ["","January","Febuary","March","April","May","June","July","August","September","October","November","December"]
year = (now.year)
month = (months[now.month])
q='attendance_{}'.format(month)
q1='earnings_{}'.format(month)
q2='deductions_{}'.format(month)
#######################     ATTENDANCE TABLE CREATION ##################
try:
    sql1='create table if not exists {}(emp_id varchar(20) PRIMARY KEY,emp_name varchar(20),paydays int(11),present_days int(11),CL int,EL  int, ML int, LOP int)'.format(q)
    cur.execute(sql1)
    mycon.commit()
    cur.execute('select * from employee_details')
    r=cur.fetchall()
    x='Successfully created table{}'.format(q)
    for i in r:
        sql1='insert into {} values("{}","{}",{},{},{},{},{},{})'.format(q,i[0],i[1],days,days,0,0,0,0)
        cur.execute(sql1)
        mycon.commit()
    messagebox.showinfo('ALERT',x)
except:
    pass
###################### EARNINGS TABLE CREATION ###########################
try:
    sql1='create table if not exists {}(emp_id varchar(20) PRIMARY KEY,emp_name varchar(50),paydays int,present_days int,basic int,hr int,ta int,medical int,washing int,others int,incentive int,advance int,bonus int,total_earnings int)'.format(q1)
    cur.execute(sql1)
    mycon.commit()
    cur.execute('select * from employee_details')
    r=cur.fetchall()
    for i in r:
        sql1='insert into {}(emp_id,emp_name,basic,hr,ta,medical,washing,others,incentive,advance,bonus,total_earnings) values("{}","{}",{},{},{},{},{},{},{},{},{},{})'.format(q1,i[0],i[1],13200,5500,1600,1250,150,300,0,0,0,22000)
        cur.execute(sql1)
        mycon.commit()
    sql12='select emp_id,paydays,present_days from {}'.format(q)
    cur.execute(sql12)
    r=cur.fetchall()
    for i in r:
        sql1='update {} set paydays={},present_days={} where emp_id="{}"'.format(q1,i[1],i[2],i[0])
        cur.execute(sql1)
        mycon.commit() 
except:
    pass
############################################ DEDUCTION TABLE CREATION #############################################
try:
    sql1='create table if not exists {}(emp_id varchar(20) PRIMARY KEY,emp_name varchar(50),PF int,ESI int,TDS int,advance int,checque_bounce int, insurance int, total_deductions int)'.format(q2)
    cur.execute(sql1)
    mycon.commit()
    cur.execute('select * from employee_details')
    r=cur.fetchall()
    for i in r:
        sql1='insert into {} values("{}","{}",{},{},{},{},{},{},{})'.format(q2,i[0],i[1],1500,100,0,0,0,0,1600)
        cur.execute(sql1)
        mycon.commit()
except:
    pass
###################################################################################################################
def exitt(): 
    if messagebox.askquestion('ALERT','Do you want to exit?')=='yes':
        window.destroy()
############################################### VIEW EMPLOYEE TABLE ###############################################
def delete_info(*event):
    if tree.focus():
        c=tree.focus()
        f=tree.item(c)
        f=f['values']
        p1=str(f[0])
        s='delete from emp where emp_id = "{}"'.format(p1)
        print(s)
        cur.execute(s)
        mycon.commit()
        for i in tree.get_children():
            tree.delete(i)
        cur.execute('select * from emp')
        r=cur.fetchall()
        total=len(r)
        labl.configure(text=total)
        for i in r:
            tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]))
def delete1(*event):
    if tree.focus():
        c=tree.focus()
        f=tree.item(c)
        f=f['values']
        p1=str(f[0])
        s='delete from employee_details where emp_id ="{}" '.format(p1)
        cur.execute(s)
        mycon.commit()
        for i in tree.get_children():
            tree.delete(i)
        cur.execute('select * from employee_details')
        r=cur.fetchall()
        for i in r:
            tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]))
        mycon.close()
def search1():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    p=s1.get()
    if p!='':
        search2.delete(0,END)
        sql1='select * from employee_details where emp_name = "{}"'.format(p)
        cur.execute(sql1)
        r=cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for i in r:
            tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]))
        mycon.close()
def refresh1():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    cur.execute('select * from employee_details')
    r=cur.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]))
    mycon.close()
def back10():
    viewform.destroy()
    emp()
def editemp():
    try:
        wind13.destroy()
    except:
        pass
    global tree,viewform,s1,search2
    viewform=Tk()
    viewform.geometry('1200x650')
    s1=StringVar()
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    text = Label(TopViewForm, text="View Employee Details", font=('arial', 18), width=600)
    text.pack(fill=X)
    txtsearch = Label(LeftViewForm, text="SEARCH \n Enter Employee Name", font=('arial', 20)).place(x=30,y=25)
    search2 = Entry(LeftViewForm, font=(15),bd=3,textvariable=s1 ,width=20)
    search2.place(x=50,y=100)
    search = Button(LeftViewForm,bd=3,command=search1,text='SEARCH',font=('arial', 20)).place(x=70,y=150)
    reset = Button(LeftViewForm,bd=3,command=refresh1,text='REFRESH',font=('arial', 20)).place(x=70,y=230)
    delete = Button(LeftViewForm,bd=3,command=delete1,text='DELETE',font=('arial', 20)).place(x=70,y=310)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'), height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree['columns']=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17')
    tree['show']='headings'
    tree.heading('1', text="Employee Id")
    tree.heading('2', text="Employee Name")
    tree.heading('3', text="Father's Name")
    tree.heading('4', text="Mother's Name")
    tree.heading('5', text="Gender")
    tree.heading('6', text="D.O.B")
    tree.heading('7', text="Designation")
    tree.heading('8', text="Employee PF Number")
    tree.heading('9', text="Employee ESI")
    tree.heading('10', text="Department")
    tree.heading('11', text="Division")
    tree.heading('12', text="Branch")
    tree.heading('13', text="Bank branch")
    tree.heading('14', text="Bank No")
    tree.heading('15', text="Address")
    tree.heading('16', text="Phone number")
    tree.heading('17', text="Email Address")
    tree.column('4',width=170,anchor='center')
    tree.column('3',width=280,anchor='center')
    tree.column('2',width=280,anchor='center')
    tree.column('1',width=170,anchor='center')
    tree.column('5',width=280,anchor='center')
    tree.column('6',width=280,anchor='center')
    tree.column('7',width=280,anchor='center')
    tree.column('8',width=280,anchor='center')
    tree.column('9',width=280,anchor='center')
    tree.column('10',width=280,anchor='center')
    tree.column('11',width=280,anchor='center')
    tree.column('12',width=280,anchor='center')
    tree.column('13',width=280,anchor='center')
    tree.column('14',width=280,anchor='center')
    tree.column('15',width=280,anchor='center')
    tree.column('16',width=280,anchor='center')
    tree.column('17',width=280,anchor='center')
    tree.pack()
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    cur.execute('select * from employee_details')
    r=cur.fetchall()
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16]))
    search = Button(LeftViewForm,text='BACK',command=back10,font=('arial', 20),bd=3).place(x=80,y=460)
    viewform.mainloop()
####################################### COMPANY DETAILS ######################################
def back3():
    wind12.destroy()
    wind2()
def companyinfo():
    global wind12
    try:
        wind11.destroy()
    except:
        pass
    wind12=Tk()
    wind12.title("company")
    wind12.configure(background="black")
    wind12.geometry("1200x650")
    lABEL1=Label(wind12,text="COMPANY DETAILS",width=50,bg="black",fg="white",font=("arial",30))
    lABEL1.pack()
    l1=Label(wind12,text="COMPANY NAME: STARK INDUSTRIES",width=75,bg="black",fg="white",font=("arial",20))
    l1.pack()
    l2=Label(wind12,text="ADDRESS :1353 BLACKWELL STREET, AK, ALASKA- 99656",width=80,bg="black",fg="white",font=("arial",20))
    l2.pack()
    l3=Label(wind12,text="WEBSITE:www.starkindustries.com",width=50,bg="black",fg="white",font=("arial",20))
    l3.pack()
    l4=Label(wind12,text="EMAIL:info@staarkindustries.com",width=50,bg="black",fg="white",font=("arial",20))
    l4.pack()
    l5=Label(wind12,text="MANAGING DIRECTOR: STARK",width=50,bg="black",fg="white",font=("arial",20))
    l5.pack()
    b1=Button(wind12,text='BACK',bg="black",fg="white",font=("arial",20),command=back3)
    b1.pack()
    wind.mainloop()
###################################### EMPLOYEE REGISTRATION #########################################
def back5():
    r3.destroy()
    emp()
def empid():
        cur.execute('select * from employee_details')
        r=cur.fetchall()
        now = datetime.datetime.now()
        c=''
        c+=str(now.year)[2:]
        c+=str(200000+len(r))
        return c
def emp_sub(*event):
    t=str(empid())
    t1=q1.get()
    t2=q2.get()
    t3=q3.get()
    t4=q4.get()
    t5=q5.get()
    t6=q6.get()
    t7=q7.get()
    t8=q8.get()
    t9=q9.get()
    t10=q10.get()
    t11=q11.get()
    t12=q12.get()
    t13=q13.get()
    t14=q14.get()
    t15=q15.get()
    t16=q16.get()
    if '' not in [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16]:
        if '@' in t16:
            try:
                len(t15)==10
                int(t15)
                sql1 = "INSERT INTO employee_details values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(t,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16)
                cur.execute(sql1)
                mycon.commit()
                messagebox.showinfo('ALERT','successfully registered employee')
            except:
                messagebox.showinfo('ALERT','enter correct phone number')   
        else:
            messagebox.showinfo('ALERT','enter correct Email address')                  
    else:
        messagebox.showinfo('ALERT','No field should be empty')
def emp_registration():
    try:
        wind13.destroy()
    except:
        pass
    global fn,ln,dob,ph,em,qu,ge,exp,fa,mo,ad,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,r3
    global q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16
    r3=Tk()
    r3.title('Employee registration')
    r3.geometry('1200x650')
    r3.resizable(0,0)
    q1=StringVar()
    q2=StringVar()
    q3=StringVar()
    q4=StringVar()
    q5=StringVar()
    q6=StringVar()
    q7=StringVar()
    q8=StringVar()
    q9=StringVar()
    q10=StringVar()
    q11=StringVar()
    q12=StringVar()
    q13=StringVar()
    q14=StringVar()
    q15=StringVar()
    q16=StringVar()
    Label(r3,text='EMPLOYEE REGISTRATION',font=('TIMES',35)).place(x=170,y=50)
    Label(r3,text='Employee\n Name',font=('arial',13)).place(x=70,y=150)
    e1=Entry(r3,textvariable=q1,font=('arial',13),bd=3,width=30)
    e1.place(x=170,y=150)
    Label(r3,text='Email\n Address',font=('arial',13)).place(x=70,y=210)
    e2=Entry(r3,textvariable=q16,font=('arial',13),bd=3,width=30)
    e2.place(x=170,y=210)
    Label(r3,text="Father's\n Name",font=('arial',13)).place(x=70,y=270)
    e3=Entry(r3,textvariable=q2,font=('arial',13),bd=3,width=30)
    e3.place(x=170,y=270)
    Label(r3,text="Mother's\n Name",font=('arial',13)).place(x=70,y=330)
    e4=Entry(r3,textvariable=q3,font=('arial',13),bd=3,width=30)
    e4.place(x=170,y=330)
    Label(r3,text='Gender',font=('arial',13)).place(x=70,y=390)
    e5=Entry(r3,textvariable=q4,font=('arial',13),bd=3,width=30)
    e5.place(x=170,y=390)
    Label(r3,text='Date Of Birth',font=('arial',13)).place(x=460,y=150)
    e6=Entry(r3,textvariable=q5,font=('arial',13),bd=3,width=30)
    e6.place(x=580,y=150)
    Label(r3,text='Designation',font=('arial',13)).place(x=460,y=210)
    e7=Entry(r3,textvariable=q6,font=('arial',13),bd=3,width=30)
    e7.place(x=580,y=210)
    Label(r3,text='emp pfno',font=('arial',13)).place(x=460,y=270)
    e8=Entry(r3,textvariable=q7,font=('arial',13),bd=3,width=30)
    e8.place(x=580,y=270)
    Label(r3,text='emp esi',font=('arial',13)).place(x=460,y=330)
    e9=Entry(r3,textvariable=q8,font=('arial',13),bd=3,width=30)
    e9.place(x=580,y=330)
    Label(r3,text='department',font=('arial',13)).place(x=460,y=390)
    e10=Entry(r3,textvariable=q9,font=('arial',13),bd=3,width=30)
    e10.place(x=580,y=390)
    Label(r3,text='Division',font=('arial',13)).place(x=460,y=450)
    e12=Entry(r3,textvariable=q10,font=('arial',13),bd=3,width=30)
    e12.place(x=580,y=450)
    Label(r3,text='Address',font=('arial',13)).place(x=460,y=510)
    e11=Entry(r3,textvariable=q14,font=('arial',13),bd=3,width=30)
    e11.place(x=580,y=510)
    Label(r3,text='Phone No',font=('arial',13)).place(x=460,y=570)
    e11=Entry(r3,textvariable=q15,font=('arial',13),bd=3,width=30)
    e11.place(x=580,y=570)
    Label(r3,text='Bank No',font=('arial',13)).place(x=70,y=450)
    e15=Entry(r3,textvariable=q13,font=('arial',13),bd=3,width=30)
    e15.place(x=170,y=450)
    Label(r3,text='Bank Branch',font=('arial',13)).place(x=60,y=510)
    e13=Entry(r3,textvariable=q12 ,font=('arial',13),bd=3,width=30)
    e13.place(x=170,y=510)
    Label(r3,text='Branch',font=('arial',13)).place(x=70,y=570)
    e14=Entry(r3,textvariable=q11 ,font=('arial',13),bd=3,width=30)
    e14.place(x=170,y=570)
    b1=Button(r3,text='SUBMIT',command=emp_sub,font=('arial',25))
    b1.place(x=970,y=300)
    b1=Button(r3,text='BACK',command=back5,font=('arial',25))
    b1.place(x=990,y=390)
    r3.mainloop()
def back4():
    wind13.destroy()
    wind2()
def emp():
    global wind13
    try:
        wind11.destroy()
    except:
        pass
    wind13=Tk()
    wind13.title("employee")
    wind13.geometry('1200x650')
    wind13.configure(background="black")
    Label(wind13,text='EMPLOYEE DETAILS',bg="black",fg="white",font=('times',40,'underline')).pack()
    b1=Button(wind13,text="ADD EMPLOYEE",bd=4,width=30,command=emp_registration,bg="black",fg="white",font=("arial",30))
    b1.pack()
    b2=Button(wind13,text="EDIT EMPLOYEE",bd=4,width=30,command=editemp,bg="black",fg="white",font=("arial",30))
    b2.pack()
    b3=Button(wind13,text="BACK",bd=4,width=30,command=back4,bg="black",fg="white",font=("arial",30))
    b3.pack()
    wind.mainloop()
def back2():
    wind22.destroy()
    wind2()
###################################### ATT TABLE ######################################
def back19():
    viewform.destroy()
    attendance()
def search22():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    p=s1.get()
    if p!='':
        search2.delete(0,END)
        sql1='select * from {} where emp_name="{}"'.format(q,p)
        cur.execute(sql1)
        r=cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for i in r:
            tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
        mycon.close()
def re14():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    sql1='select * from {}'.format(q)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
    mycon.close()
def att_table():
    try:
        wind22.destroy()
    except:
        pass
    global tree,viewform,s1,search2
    viewform=Tk()
    viewform.geometry('1200x650')
    s1=StringVar()
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    text = Label(TopViewForm, text="ATTENDANCE REPORT", font=('arial', 18), width=600)
    text.pack(fill=X)
    txtsearch = Label(LeftViewForm, text="SEARCH \n Enter Employee Name", font=('times', 20,'underline')).place(x=5,y=25)
    search2 = Entry(LeftViewForm, font=(15),bd=3,textvariable=s1 ,width=20)
    search2.place(x=50,y=100)
    search = Button(LeftViewForm,bd=3,command=search22,text='SEARCH',font=('arial', 20)).place(x=70,y=150)
    reset = Button(LeftViewForm,bd=3,command=re14,text='REFRESH',font=('arial', 20)).place(x=70,y=230)
    search = Button(LeftViewForm,text='BACK',command=back19,font=('arial', 20),bd=3).place(x=80,y=460)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=('1','2','3','4','5','6','7','8'), height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree['columns']=('1','2','3','4','5','6','7','8')
    tree['show']='headings'
    tree.heading('1', text="Employee Id")
    tree.heading('2', text="Employee Name")
    tree.heading('3', text="Pay Days")
    tree.heading('4', text="Present Days")
    tree.heading('5', text="CL")
    tree.heading('6', text="EL")
    tree.heading('7', text="ML")
    tree.heading('8', text="LOP")
    tree.column('4',width=100,anchor='center')
    tree.column('3',width=100,anchor='center')
    tree.column('2',width=160,anchor='center')
    tree.column('1',width=100,anchor='center')
    tree.column('5',width=100,anchor='center')
    tree.column('6',width=100,anchor='center')
    tree.column('7',width=100,anchor='center')
    tree.column('8',width=100,anchor='center')
    tree.pack()
    sql1='select * from {}'.format(q)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
    viewform.mainloop()
#######################################################################################
def attendance():
    try:
        wind11.destroy()
    except:
        pass
    global wind22,t12
    wind22=Tk()
    def lop():
        mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
        cur=mycon.cursor()
        g12=t12.get()
        cur.execute('select emp_id from employee_details')
        r=cur.fetchall()
        for i in r:
            if i[0]==g12:
                sql1='update {} set LOP=LOP+1 where emp_id="{}"'.format(q,g12)
                sql2='update {} set present_days=present_days-1 where emp_id="{}"'.format(q,g12)
                sql3='update {} set paydays=paydays-1 where emp_id="{}"'.format(q,g12)
                sql4='update {} set present_days=present_days-1 where emp_id="{}"'.format(q1,g12)
                sql5='update {} set paydays=paydays-1 where emp_id="{}"'.format(q1,g12)
                sql6='update {} set total_deductions=total_deductions+400 where emp_id="{}"'.format(q2,g12)
                ex=[sql1,sql2,sql3,sql4,sql5,sql6]
                for i in ex:
                    cur.execute(i)
                    mycon.commit()
                x='Employee {} took LEAVE WITHOUT PAYMENT. Rs.400 deducted from salary'.format(g12)
                messagebox.showinfo('LOP',x)
                break
        else:
            messagebox.showinfo('ALERT','Employee not found')
    def att_sub(a):
        mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
        cur=mycon.cursor()
        g12=t12.get()
        cur.execute('select emp_id from employee_details')
        r=cur.fetchall()
        for i in r:
            if i[0]==g12:
                
                sql1='update {} set {}={}+1 where emp_id="{}"'.format(q,a,a,g12)
                sql2='update {} set present_days=present_days-1 where emp_id="{}"'.format(q,g12)
                sql3='update {} set present_days=present_days-1 where emp_id="{}"'.format(q1,g12)
                val=[sql1,sql2,sql3]
                for i in val:
                    cur.execute(i)
                    mycon.commit()
                x='Employee {} took {}'.format(g12,a)
                messagebox.showinfo(a,x)
                break
        else:
            messagebox.showinfo('ALERT','Employee not found')
    t12=StringVar()
    wind22.title("LEAVE REPORT")
    wind22.geometry('500x550')
    wind22.configure(background="black")
    l1=Label(wind22,text="LEAVE DETAILS",bg="black",fg="white",font=('times',40,'underline'))
    l1.grid(row=0,columnspan=2)
    l2=Label(wind22,text="Search Employee:",font=("arial",20),bg="black",fg="white")
    l2.grid(row=1,column=0)
    t1=Entry(wind22,width=30,bd=4,font=("arial",20),textvariable=t12,bg="white")
    t1.grid(row=2,column=0)
    l4=Label(wind22,text="Entry:",font=("arial",20),bg="black",fg="white")
    l4.grid(row=3,column=0)
    b1=Button(wind22,text="CASUAL LEAVE",bd=4,font=("arial",20),width=20,command= lambda: att_sub('CL'),bg="black",fg="white")
    b1.grid(row=4,column=0)
    b2=Button(wind22,text="MEDICAL LEAVE",bd=4,font=("arial",20),width=20,command=lambda: att_sub('ML'),bg="black",fg="white")
    b2.grid(row=5,column=0)
    b3=Button(wind22,text="EARNED LEAVE",bd=4,font=("arial",20),width=20,command=lambda: att_sub('EL'),bg="black",fg="white")
    b3.grid(row=6,column=0)
    b4=Button(wind22,text="LOSS OF PAY",bd=4,font=("arial",20),width=30,command=lop,bg="black",fg="white")
    b4.grid(row=7,column=0)
    b41=Button(wind22,text="VIEW ATTENDANCE TABLE",bd=4,font=("arial",20),width=30,command=att_table,bg="black",fg="white")
    b41.grid(row=8,column=0)
    b5=Button(wind22,text="BACK",bd=4,font=("arial",20),width=30,command=back2,bg="black",fg="white")
    b5.grid(row=9,column=0)
    wind22.mainloop()
def logout1():
    if messagebox.askquestion('ALERT','Do you want to logout?')=='yes':
        wind11.destroy()
        main_page()
######################################## EARNINGS ###############################################################
def back18():
    viewform.destroy()
    earn_page()
def search33():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    p=s1.get()
    if p!='':
        search2.delete(0,END)
        sql1='select * from {} where emp_name="{}"'.format(q1,p)
        cur.execute(sql1)
        r=cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for i in r:
            tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13]))
        mycon.close()
def re13():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    sql1='select * from {}'.format(q1)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13]))
    mycon.close()
def ern_table():
    try:
        r1.destroy()
    except:
        pass
    global tree,viewform,s1,search2
    viewform=Tk()
    viewform.geometry('1200x650')
    s1=StringVar()
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    text = Label(TopViewForm, text="EMPLOYEE EARNINGS REPORT", font=('arial', 18), width=600)
    text.pack(fill=X)
    txtsearch = Label(LeftViewForm, text="SEARCH \n Enter Employee Name", font=('times', 20,'underline')).place(x=5,y=25)
    search2 = Entry(LeftViewForm, font=(15),bd=3,textvariable=s1 ,width=20)
    search2.place(x=50,y=100)
    search = Button(LeftViewForm,bd=3,command=search33,text='SEARCH',font=('arial', 20)).place(x=70,y=150)
    reset = Button(LeftViewForm,bd=3,command=re13,text='REFRESH',font=('arial', 20)).place(x=70,y=230)
    search = Button(LeftViewForm,text='BACK',command=back18,font=('arial', 20),bd=3).place(x=80,y=460)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=('1','2','3','4','5','6','7','8','9','10','11','12','13','14'), height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree['columns']=('1','2','3','4','5','6','7','8','9','10','11','12','13','14')
    tree['show']='headings'
    tree.heading('1', text="Employee Id")
    tree.heading('2', text="Employee Name")
    tree.heading('3', text="PF")
    tree.heading('4', text="ESI")
    tree.heading('5', text="TDS")
    tree.heading('6', text="Advance")
    tree.heading('7', text="Checque Bounce")
    tree.heading('8', text="Insurance")
    tree.heading('9', text="Total Deduction")
    tree.heading('10', text="Total Deduction")
    tree.heading('11', text="Total Deduction")
    tree.heading('12', text="Total Deduction")
    tree.heading('13', text="Total Deduction")
    tree.heading('14', text="Total Deduction")
    tree.column('4',width=100,anchor='center')
    tree.column('3',width=100,anchor='center')
    tree.column('2',width=160,anchor='center')
    tree.column('1',width=100,anchor='center')
    tree.column('5',width=100,anchor='center')
    tree.column('6',width=100,anchor='center')
    tree.column('7',width=100,anchor='center')
    tree.column('8',width=100,anchor='center')
    tree.column('9',width=100,anchor='center')
    tree.column('10',width=100,anchor='center')
    tree.column('11',width=100,anchor='center')
    tree.column('12',width=100,anchor='center')
    tree.column('13',width=100,anchor='center')
    tree.column('14',width=100,anchor='center')
    tree.pack()
    sql1='select * from {}'.format(q1)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13]))
    viewform.mainloop()
def back11():
    r11.destroy()
    earn_page()
def bonus_page():
    global g1,r11
    try:
        r1.destroy()
    except:
        pass
    r11=Tk()
    def add():
        amt=g1.get()
        cur.execute('select emp_id from employee_details')
        r=cur.fetchall()
        try:
            int(amt)
            for i in r:
                sql2='update {} set bonus=bonus+{} where emp_id="{}"'.format(q1,amt,i[0])
                sql3='update {} set total_earnings=total_earnings+{} where emp_id="{}"'.format(q1,amt,i[0])
                val=[sql2,sql3]
                for j in val:
                    print(j)
                    cur.execute(j)
                    mycon.commit()
            messagebox.showinfo('ALERT','Bonus amount added to all employee\'s')
        except:
            messagebox.showinfo('ALERT','Enter valid bonus amount.')
    g1=StringVar()
    r11.title('Bonus page')
    r11.configure(background='black')
    r11.geometry('700x500')
    Label(r11,text='BONUS ADDITION',font=('times',40,'underline'),bg='black',fg='white').pack()
    Label(r11,text='ENTER BONUS AMOUNT',font=('arial',25,),bg='black',fg='white').place(x=150,y=110)
    Button(r11,text='SUBMIT',command=add,font=('arial',25),bd=4,bg='black',fg='white').place(x=250,y=270)
    Button(r11,text='BACK',command=back11,font=('arial',25),bd=4,bg='black',fg='white').place(x=270,y=390)
    en1=Entry(r11,textvariable=g1,bd=3,font=('arial',25,))
    en1.place(x=160,y=180)
    r11.mainloop()
def back12():
    r11.destroy()
    earn_page()
def spl_add():
    global g1,r11
    try:
        r1.destroy()
    except:
        pass
    r11=Tk()
    def add(a):
        emp=g1.get()
        amt=g2.get()
        cur.execute('select emp_id from employee_details')
        r=cur.fetchall()
        for i in r:
            if i[0]==emp:
                if emp:
                    try:
                        int(amt)
                        sql2='update {} set {}={}+{} where emp_id="{}"'.format(q1,a,a,amt,emp)
                        sql3='update {} set total_earnings=total_earnings+{} where emp_id="{}"'.format(q1,amt,emp)
                        val=[sql2,sql3]
                        for i in val:
                            cur.execute(i)
                            mycon.commit()
                        x='Amount {} added to employee {}'.format(amt,emp)
                        messagebox.showinfo(a,x)
                        break
                    except:
                        messagebox.showinfo('ALERT','Enter valid amount.')
                        break
                else:
                    messagebox.showinfo('ALERT','Enter employee ID')
        else:
            messagebox.showinfo('ALERT','Employee not found')
    g1=StringVar()
    g2=StringVar()
    r11.title('Special additions')
    r11.configure(background='black')
    r11.geometry('710x510')
    Label(r11,text='SPECIAL ADDITION',font=('times',40,'underline'),bg='black',fg='white').pack()
    Label(r11,text='ENTER\n EMPLOYEE ID',font=('arial',25,),bg='black',fg='white').place(x=30,y=110)
    en1=Entry(r11,textvariable=g1,bd=3,font=('arial',25,)).place(x=300,y=125)
    Label(r11,text='ENTER AMOUNT',font=('arial',25,),bg='black',fg='white').place(x=15,y=200)
    en1=Entry(r11,textvariable=g2,bd=3,font=('arial',25,)).place(x=300,y=200)
    Button(r11,text='INCENTIVE',command= lambda: add('incentive'),font=('arial',25),bd=4,bg='black',fg='white').place(x=250,y=270)
    Button(r11,text='ADVANCE',command= lambda: add('advance'),font=('arial',25),bd=4,bg='black',fg='white').place(x=256,y=350)
    Button(r11,text='BACK',command=back12,font=('arial',25),bd=4,bg='black',fg='white').place(x=285,y=430)
    r11.mainloop()
def back13():
    r1.destroy()
    wind2()
def earn_page():
    try:
        wind11.destroy()
    except:
        pass
    global r1
    r1=Tk()
    r1.title('earning')
    r1.configure(background='black')
    r1.geometry('700x600')
    Label(r1,text='EMPLOYEE EARNING',font=('times',40,'underline'),bg='black',fg='white').pack()
    Button(r1,text='BONUS',command=bonus_page,font=('arial',30),bd=4,bg='black',fg='white').place(x=250,y=150)
    Button(r1,text='SPECIAL ADDITIONS',command=spl_add,font=('arial',30),bd=4,bg='black',fg='white').place(x=130,y=270)
    Button(r1,text='VIEW TABLE',command=ern_table,font=('arial',30),bd=4,bg='black',fg='white').place(x=200,y=390)
    Button(r1,text='BACK',command=back13,font=('arial',30),bd=4,bg='black',fg='white').place(x=270,y=510)
    r1.mainloop()
##################################### DEDUCTIONS ##################################################
def back17():
    viewform.destroy()
    ded_page()
def search44():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    p=s1.get()
    if p!='':
        search2.delete(0,END)
        sql1='select * from {} where emp_name="{}"'.format(q2,p)
        cur.execute(sql1)
        r=cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for i in r:
            tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
        mycon.close()
def re12():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    sql1='select * from {}'.format(q2)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    mycon.close()
def ded_table():
    try:
        ded.destroy()
    except:
        pass
    global tree,viewform,s1,search2
    viewform=Tk()
    viewform.geometry('1200x650')
    s1=StringVar()
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    text = Label(TopViewForm, text="SALARY SHEET REPORT", font=('arial', 18), width=600)
    text.pack(fill=X)
    txtsearch = Label(LeftViewForm, text="SEARCH \n Enter Employee Name", font=('times', 20,'underline')).place(x=5,y=25)
    search2 = Entry(LeftViewForm, font=(15),bd=3,textvariable=s1 ,width=20)
    search2.place(x=50,y=100)
    search = Button(LeftViewForm,bd=3,command=search44,text='SEARCH',font=('arial', 20)).place(x=70,y=150)
    reset = Button(LeftViewForm,bd=3,command=re12,text='REFRESH',font=('arial', 20)).place(x=70,y=230)
    search = Button(LeftViewForm,text='BACK',command=back17,font=('arial', 20),bd=3).place(x=80,y=460)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=('1','2','3','4','5','6','7','8','9'), height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree['columns']=('1','2','3','4','5','6','7','8','9')
    tree['show']='headings'
    tree.heading('1', text="Employee Id")
    tree.heading('2', text="Employee Name")
    tree.heading('3', text="PF")
    tree.heading('4', text="ESI")
    tree.heading('5', text="TDS")
    tree.heading('6', text="Advance")
    tree.heading('7', text="Checque Bounce")
    tree.heading('8', text="Insurance")
    tree.heading('9', text="Total Deduction")
    tree.column('4',width=100,anchor='center')
    tree.column('3',width=100,anchor='center')
    tree.column('2',width=160,anchor='center')
    tree.column('1',width=100,anchor='center')
    tree.column('5',width=100,anchor='center')
    tree.column('6',width=100,anchor='center')
    tree.column('7',width=100,anchor='center')
    tree.column('8',width=100,anchor='center')
    tree.column('9',width=100,anchor='center')
    tree.pack()
    sql1='select * from {}'.format(q2)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    viewform.mainloop()
def back15():
    ded.destroy()
    wind2()
def ded_page():
    global ded
    try:
        wind11.destroy()
    except:
        pass
    ded=Tk()
    def sub(a,b=None):
        emp=g1.get()
        amt=g2.get()
        cur.execute('select * from employee_details')
        r=cur.fetchall()  
        if emp:
            for i in r:
                if i[0]==emp:
                    try:
                        
                        if b==500:
                            amt=b
                            sql2='update {} set {}={}+{} where emp_id="{}"'.format(q2,a,a,b,emp)
                            sql3='update {} set total_deductions=total_deductions+{} where emp_id="{}"'.format(q2,b,emp)
                            a='CHECK BOUNCE'   
                        else:
                            int(amt)
                            sql2='update {} set {}={}+{} where emp_id="{}"'.format(q2,a,a,amt,emp)
                            sql3='update {} set total_deductions=total_deductions+{} where emp_id="{}"'.format(q2,amt,emp)        
                        val=[sql2,sql3]
                        for i in val:
                            cur.execute(i)
                            mycon.commit()
                        x='Successfully added amount {} to employee {}'.format(amt,emp)
                        messagebox.showinfo(a,x)
                        break
                    except:
                        messagebox.showinfo('ALERT','Enter valid amount.')
                        break
            else:
                messagebox.showinfo('ALERT','Employee not found')
        else:
            messagebox.showinfo('ALERT','Enter employee ID')
    ded.geometry('710x770')
    g1=StringVar()
    g2=StringVar()
    ded.title('Deduction page')
    ded.configure(background='black')
    Label(ded,text='DEDUCTIONS',font=('times',40,'underline'),bg='black',fg='white').pack()
    Label(ded,text='ENTER\n EMPLOYEE ID',font=('arial',25,),bg='black',fg='white').place(x=30,y=110)
    en1=Entry(ded,textvariable=g1,bd=3,font=('arial',25,)).place(x=300,y=125)
    Label(ded,text='ENTER AMOUNT',font=('arial',25,),bg='black',fg='white').place(x=15,y=200)
    en1=Entry(ded,textvariable=g2,bd=3,font=('arial',25,)).place(x=300,y=200)
    Button(ded,text='INSURANCE',command= lambda: sub('insurance'),font=('arial',25),bd=4,bg='black',fg='white').place(x=250,y=270)
    Button(ded,text='ADVANCE',command= lambda: sub('advance'),font=('arial',25),bd=4,bg='black',fg='white').place(x=265,y=350)
    Button(ded,text='TDS',command= lambda: sub('TDS'),font=('arial',25),bd=4,bg='black',fg='white').place(x=300,y=430)
    Button(ded,text='CHECK BOUNCE',command= lambda: sub('checque_bounce',500),font=('arial',25),bd=4,bg='black',fg='white').place(x=205,y=515)
    Button(ded,text='SHOW TABLE',command=ded_table,font=('arial',25),bd=4,bg='black',fg='white').place(x=235,y=600)
    Button(ded,text='BACK',command=back15,font=('arial',25),bd=4,bg='black',fg='white').place(x=285,y=685)
    ded.mainloop()
################################SALARY SHEET REPORT ################################################
def back16():
    viewform.destroy()
    wind2()
def search3():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    p=s1.get()
    if p!='':
        search2.delete(0,END)
        sql1='select a.emp_id,a.emp_name,c.paydays,c.present_days,c.CL,c.EL,c.ML,c.LOP,b.PF,b.ESI,b.TDS,b.advance,b.checque_bounce,b.insurance,a.basic,a.hr,a.ta,a.medical,a.washing,a.others,a.incentive,a.advance,a.bonus,b.total_deductions,a.total_earnings from {} a, {} b,{} c where a.emp_id=b.emp_id and a.emp_id=c.emp_id and a.emp_name="{}"'.format(q1,q2,q,p)
        cur.execute(sql1)
        r=cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for i in r:
            tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],int(i[24])-int(i[23])))
        mycon.close()
def re1():
    mycon=sql.connect(host='localhost',user='root',passwd='root',database='payroll')
    cur=mycon.cursor()
    print(q,q1,q2)
    sql1='select a.emp_id,a.emp_name,c.paydays,c.present_days,c.CL,c.EL,c.ML,c.LOP,b.PF,b.ESI,b.TDS,b.advance,b.checque_bounce,b.insurance,a.basic,a.hr,a.ta,a.medical,a.washing,a.others,a.incentive,a.advance,a.bonus,b.total_deductions,a.total_earnings from {} a, {} b,{} c where a.emp_id=b.emp_id and a.emp_id=c.emp_id'.format(q1,q2,q)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],int(i[24])-int(i[23])))
    mycon.close()
def sal_sheet():
    try:
        wind11.destroy()
    except:
        pass
    global tree,viewform,s1,search2
    viewform=Tk()
    viewform.geometry('1200x650')
    s1=StringVar()
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    text = Label(TopViewForm, text="SALARY SHEET REPORT", font=('arial', 18), width=600)
    text.pack(fill=X)
    txtsearch = Label(LeftViewForm, text="SEARCH \n Enter Employee Name", font=('times', 20,'underline')).place(x=5,y=25)
    search2 = Entry(LeftViewForm, font=(15),bd=3,textvariable=s1 ,width=20)
    search2.place(x=50,y=100)
    search = Button(LeftViewForm,bd=3,command=search3,text='SEARCH',font=('arial', 20)).place(x=70,y=150)
    reset = Button(LeftViewForm,bd=3,command=re1,text='REFRESH',font=('arial', 20)).place(x=70,y=230)
    search = Button(LeftViewForm,text='BACK',command=back16,font=('arial', 20),bd=3).place(x=80,y=460)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26'), height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree['columns']=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26')
    tree['show']='headings'
    tree.heading('1', text="Employee Id")
    tree.heading('2', text="Employee Name")
    tree.heading('3', text="Pay days")
    tree.heading('4', text="Present days")
    tree.heading('5', text="CL")
    tree.heading('6', text="EL")
    tree.heading('7', text="ML")
    tree.heading('8', text="LOP")
    tree.heading('9', text="PF")
    tree.heading('10', text="ESI")
    tree.heading('11', text="TDS")
    tree.heading('12', text="Advance")
    tree.heading('13', text="Checque bounce")
    tree.heading('14', text="Insurance")
    tree.heading('15', text="Basic")
    tree.heading('16', text="HR")
    tree.heading('17', text="TA")
    tree.heading('18', text="Medical")
    tree.heading('19', text="Washing")
    tree.heading('20', text="Others")
    tree.heading('21', text="Incentive")
    tree.heading('22', text="Advance")
    tree.heading('23', text="Bonus")
    tree.heading('24', text="Total Deductions")
    tree.heading('25', text="Total Earnings")
    tree.heading('26', text="Total Salary")
    tree.column('4',width=100,anchor='center')
    tree.column('3',width=100,anchor='center')
    tree.column('2',width=160,anchor='center')
    tree.column('1',width=100,anchor='center')
    tree.column('5',width=100,anchor='center')
    tree.column('6',width=100,anchor='center')
    tree.column('7',width=100,anchor='center')
    tree.column('8',width=100,anchor='center')
    tree.column('9',width=100,anchor='center')
    tree.column('10',width=100,anchor='center')
    tree.column('11',width=100,anchor='center')
    tree.column('12',width=100,anchor='center')
    tree.column('13',width=100,anchor='center')
    tree.column('14',width=100,anchor='center')
    tree.column('15',width=100,anchor='center')
    tree.column('16',width=100,anchor='center')
    tree.column('17',width=100,anchor='center')
    tree.column('18',width=100,anchor='center')
    tree.column('19',width=100,anchor='center')
    tree.column('20',width=100,anchor='center')
    tree.column('21',width=100,anchor='center')
    tree.column('22',width=100,anchor='center')
    tree.column('23',width=100,anchor='center')
    tree.column('24',width=100,anchor='center')
    tree.column('25',width=100,anchor='center')
    tree.column('26',width=100,anchor='center')
    tree.pack()
    sql1='select a.emp_id,a.emp_name,c.paydays,c.present_days,c.CL,c.EL,c.ML,c.LOP,b.PF,b.ESI,b.TDS,b.advance,b.checque_bounce,b.insurance,a.basic,a.hr,a.ta,a.medical,a.washing,a.others,a.incentive,a.advance,a.bonus,b.total_deductions,a.total_earnings from {} a, {} b,{} c where a.emp_id=b.emp_id and a.emp_id=c.emp_id'.format(q1,q2,q)
    cur.execute(sql1)
    r=cur.fetchall()
    for i in r:
        tree.insert("",'end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],int(i[24])-int(i[23])))
    viewform.mainloop()
#####################################################################################################
def wind2(): 
    global wind11
    try:
        wind.destroy()
    except:
        pass
    wind11=Tk()
    wind11.title("ADMIN ACCESS")
    wind11.geometry('700x600+200+100')
    wind11.configure(background="black")
    Label(wind11,text='ADMIN PAGE',font=('times',40,'underline'),bg='black',fg='white').pack()
    b123=Button(wind11,text="COMPANY DETAILS",bd=3,width=30,command=companyinfo,bg="black",fg="white",font=("arial",25))
    b123.pack()
    b2=Button(wind11,text="EMPLOYEE DETAILS",bd=3,width=30,command=emp,bg="black",fg="white",font=("arial",25))
    b2.pack()
    b3=Button(wind11,text="LEAVE DETAILS",bd=3,width=30,command=attendance,bg="black",fg="white",font=("arial",25))
    b3.pack()
    b4=Button(wind11,text="EARNING",bd=3,width=30,command=earn_page,bg="black",fg="white",font=("arial",25))
    b4.pack()
    b5=Button(wind11,text="DEDUCTION",bd=3,width=30,command=ded_page,bg="black",fg="white",font=("arial",25))
    b5.pack()
    b6=Button(wind11,text="SALARY SHEET REPORT",bd=3,width=30,command=sal_sheet,bg="black",fg="white",font=("arial",25))
    b6.pack()
    b7=Button(wind11,text="LOG OUT",bd=3,width=30,command=logout1,bg="black",fg="white",font=("arial",25))
    b7.pack()
    wind11.mainloop()
def back1():
    wind.destroy()
    main_page()
def wind1(): 
    global wind
    try:
        window.destroy()
    except:
        pass
    wind=Tk()
    ur=StringVar()
    pw=StringVar()
    def submit_check():
        us=ur.get()
        pwd=pw.get()
        cur.execute('select * from login_info')
        r=cur.fetchall()
        for i in r:
            if i[0]==us and i[1]==pwd:
                return wind2()  
        else:
            messagebox.showinfo('warning','incorrect username or password')
    wind.title(" ADMIN LOGIN")
    wind.configure(background="black")
    l1=Label(wind,text="ADMIN LOGIN",bg="black",fg="white",font=('times',50,'underline'))
    l1.grid(row=0,columnspan=3)
    l1=Label(wind,text="USERNAME:",bg="black",fg="white",font=("arial",25))
    l1.grid(row=1,column=1,sticky=W)
    textentry=Entry(wind,bd=3,textvariable=ur,font=("arial",25),width=20,bg="white")
    textentry.grid(row=1,column=2)
    l2=Label(wind,text="PASSWORD:",bg="black",fg="white",font=("arial",25))
    l2.grid(row=2,column=1,sticky=W)
    textentry=Entry(wind,bd=3,show='*',font=("arial",25),textvariable=pw,width=20,bg="white")
    textentry.grid(row=2,column=2)
    b3=Button(wind,text="SUBMIT",command=submit_check,bg="black",fg="white",font=("arial",25))
    b3.grid(row=3,columnspan=3)
    b4=Button(wind,text='BACK',bg="black",fg="white",command=back1,font=("arial",25))
    b4.grid(row=4,columnspan=3)
    wind.mainloop()
def main_page():
    global window
    window=Tk()
    window.resizable(0,0)  
    window.title("payroll management system")
    window.configure(background="black")
    window.geometry("1200x650+50+50")
    Label(window,text='LOGIN PAGE',font=('times',50,'underline'),bg='black',fg='white').pack()
    b1=Button(window,text="ADMINISTRATIVE LOGIN",width=40,bg="black",fg="white",font=("arial",25),command=wind1)
    b1.place(x=200,y=280)
    b2=Button(window,text="QUIT",width=20,bg="black",fg="white",font=("arial",25),command= lambda: window.destroy())
    b2.place(x=400,y=380)
    window.mainloop()
main_page()
