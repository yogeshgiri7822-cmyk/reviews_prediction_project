try:
    import pymysql
except ImportError:
    pass
from tkinter import *
import re
import pickle
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk




root1 = Tk()
root1.geometry('1400x900')
main = "Restaurant Review Analysis System/"
root1.title(main+"Welcome Page")


foods = ["Idly", "Dosa", "Vada", "Roti", "Meals", "Veg Biryani",
         "Egg Biryani", "Chicken Biryani", "Mutton Biryani",
         "Ice Cream", "Noodles", "Manchooriya", "Orange juice",
         "Apple Juice", "Pineapple juice", "Banana juice"]




def take_review():
    root2 = Toplevel()
    root2.geometry('1400x900')
    root2.title(main+"give review")


    label = Label(root2, text="RESTAURANT REVIEW ANALYSIS SYSTEM",
                         bd=2, font=('Arial', 47, 'bold', 'underline'))


    req1 = Label(root2, text="Select the item(s) you have taken.....")
     
    chk_btns = []
    selected_foods = []
    req2 = Label(root2, text="Give your review below....")
    rev_tf = Entry(root2,width=100,fg='red',borderwidth=5,font=('times new roman',14,'bold'))
    req3 = Label(root2, text="NOTE : Use not instead of n't.",
                 font=('times new roman',12,'bold'))
    global req4
    req4 = Label(root2, text="Review is ",
                 height=4,width=20,bg='skyblue',font=('times new roman',14,'bold'))
    global variables
    variables = []
    chk_btns = []


    for i in range(len(foods)):
        var = IntVar()
        chk = Checkbutton(root2, text=foods[i], variable=var)
        variables.append(var)
        chk_btns.append(chk)


    label.grid(row=0, column=0, columnspan=4)
    req1.grid(row=1, column=0, columnspan=4)
    #req4.grid(row=1,column=0,columnspan=6)
    req1.config(font=("Helvetica", 30))


    for i in range(4):
        for j in range(4):
            c = chk_btns[i*4+j]
            c.grid(row=i+3, column=j, columnspan=1,sticky=S)




    submit_review = Button(root2, text="Submit Review", font=(
       'Arial', 20), padx=100, pady=20, command=lambda: [
             estimate(rev_tf.get())])


    req2.grid(row=7, column=0, columnspan=4, sticky=W+E)
    req2.config(font=("Helvetica", 20))
    rev_tf.grid(row=8, column=1, rowspan=3, columnspan=2, sticky=S)
    req3.grid(row=11, column=1, columnspan=2)
    submit_review.grid(row=12, column=0, columnspan=4)
    req4.grid(row=12, column=2, columnspan=4)
   


def estimate(s):
    with open('cv','rb') as f:
        cv=pickle.load(f)
    with open('lg','rb') as f:
        model=pickle.load(f)
       
    if s=='':
        messagebox.showinfo('info','please give feedback ')
        take_review()
    else:
        s=s.lower()
        arr=cv.transform([s])
        result=model.predict(arr)
        if 'not' in s:
            result[0]=abs(result[0]-1)
        if result[0]==1:
            r='Good Review'
            print(r)
        else:
            r='Bad Review'
            print(r)
        req4.config(text=r)
       
       
        selected_foods = []
        for i in range(len(foods)):
            if variables[i].get() == 1:
                selected_foods.append(foods[i])
        #print(selected_foods)
        conn=pymysql.connect(user='root',password='Root',
                             host='localhost',database='rest_review_db')
        qur='select * from reviews_table'
        mycur=conn.cursor()
        mycur.execute(qur)
        total=mycur.fetchall()
        #print(total)
        for i in total:
            food1=list(i)
            if food1[0] in selected_foods:
                food_name=food1[0]
                c=food1[3]+1
                p=food1[1]
                n=food1[2]
                if result[0]==1:
                    p=p+1
                else:
                    n=n+1
                conn=pymysql.connect(user='root',password='Root',
                                     host='localhost',database='rest_review_db')
                qur='UPDATE reviews_table SET good_review=%d,bad_review=%d,customer=%d WHERE food="%s"'%(p,n,c,food_name)
                mycur=conn.cursor()
                mycur.execute(qur)
                conn.commit()
                mycur.close()
                conn.close()
        selected_foods=[]


           
   




def login():
    user=a1.get()
    password=a2.get()
    a1.set('')
    a2.set('')
    if (user=='abc') and (password=='12345'):
        win=Tk()
        #win.configure(bg='skyblue')
        win.geometry('1400x900')
       
        def disp():
            treev.delete(*treev.get_children())
            conn = pymysql.connect(user='root', password='Root',
                                           host='localhost', database='rest_review_db')
            qur = 'select * from reviews_table'
            mycur = conn.cursor()
            mycur.execute(qur)
            result = mycur.fetchall()
            for i in result:
                treev.insert("", 'end', values=(i[0], i[1], i[2], i[3]))
            mycur.close()
            conn.close()


        def percent():
            # owner_food=cb.get()
            conn = pymysql.connect(user='root', password='Root',
                                           host='localhost', database='rest_review_db')
            qur = 'select * from reviews_table'
            mycur = conn.cursor()
            mycur.execute(qur)
            result = mycur.fetchall()
            per = []
            for i in result:
                food_name = i[0]
                try:
                    pos_percent = round((i[1] / i[3]) * 100, 1)
                except ZeroDivisionError:
                    pos_percent = 0


                try:
                    neg_percent = round((i[2] / i[3]) * 100, 1)
                except ZeroDivisionError:
                    neg_percent = 0
                per.append((food_name, pos_percent, neg_percent))
            return per
       
        def plot(list1):
            global canvas
            try:
                canvas.get_tk_widget().destroy()
            except:
                pass
            if sum(list1) != 0:
                global fig
                fig = Figure(figsize=(5, 3), dpi=100)
                plot1 = fig.add_subplot(111)
                name = ['POSITIVE', 'NEGATIVE']
                plot1.pie(list1, labels=name, autopct="%0.1f%%",
                          shadow=True, explode=[0.1, 0.1], colors=['b', 'r'])
               
                canvas = FigureCanvasTkAgg(fig,
                                           master=win)
                canvas.draw()
                canvas.get_tk_widget().place(x=150, y=300)
            else:
                global l20
                l20 = Label(win, text='SORRY NO COUNT', height=2, fg='red', bd=5, relief='ridge',
                           font=('times new roman', 18, 'bold'))
                l20.place(x=300, y=400)


        def per_show():
            per1 = percent()
            owner_food = cb.get()
            for i in per1:
                if owner_food == i[0]:
                    pos_percent = i[1]
                    neg_percent = i[2]
                    print(pos_percent)
                    print(neg_percent)
                    name = ['POSITIVE', 'NEGATIVE']
                    list1 = [pos_percent, neg_percent]
                    plot(list1)
       
       
        def clear_canvas():
            #fig.clf()
            canvas.get_tk_widget().destroy()
            try:
                l20.destroy()
            except:
                pass




       
       
        def clear():
            treev.delete(*treev.get_children())
       
       
        l1 = Label(win, text='REVIEW STATISTICAL ANALYSIS', height=2, width=40, relief='ridge',
                   bd=5, font=('times new roman', 14, 'bold'))
        l1.place(x=400, y=40)
        b1 = Button(win, text='SHOW COUNT', command=disp, width=20, relief='ridge',
                    bd=5, font=('times new roman', 14, 'bold'))
        b1.place(x=100, y=120)
        b2 = Button(win, text='EXIT', width=20, command=win.destroy, relief='ridge',
                    bd=5, font=('times new roman', 14, 'bold'))
        b2.place(x=400, y=120)
       
        l2 = Label(win, text='Select food >>>>', width=20, relief='ridge',
                   bd=5, font=('times new roman', 12, 'bold'))
        l2.place(x=100, y=200)


        n = StringVar()
        cb = ttk.Combobox(win, textvariable=n)
        cb['state'] = 'readonly'
        cb['values'] = ("Idly", "Dosa", "Vada", "Roti", "Meals", "Veg Biryani",
                        "Egg Biryani", "Chicken Biryani", "Mutton Biryani",
                        "Ice Cream", "Noodles", "Manchooriya", "Orange juice",
                        "Apple Juice", "Pineapple juice", "Banana juice")
        cb.current(0)
        cb.place(x=300, y=200, height=30)


        b3 = Button(win, text='Percentage plot', width=20, command=per_show, relief='ridge',
                    bd=5, font=('times new roman', 12, 'bold'))
        b3.place(x=160, y=240)


        # b4 = Button(win, text='Negative review > 40%', command=above40, relief='ridge',
        #             bd=5, font=('times new roman', 12, 'bold'))
        # b4.place(x=500, y=240)
        b5 = Button(win, text='Clear Chart', command=clear_canvas, relief='ridge',
                    bd=5, font=('times new roman', 12, 'bold'))
        b5.place(x=360, y=600)
        # b6 = Button(win, text='Negative review > 20%', command=above20, relief='ridge',
        #             bd=5, font=('times new roman', 12, 'bold'))
        # b6.place(x=500, y=200)


        treev = ttk.Treeview(win, selectmode='browse', height=20)
        treev.place(x=700, y=110, width=500)


        treev["columns"] = ("1", "2", "3", "4")
        treev['show'] = 'headings'


        treev.column("1", width=90, anchor='c')
        treev.column("2", width=90, anchor='se')
        treev.column("3", width=90, anchor='se')
        treev.column("4", width=90, anchor='se')


        treev.heading("1", text="Food name")
        treev.heading("2", text="Good review count")
        treev.heading("3", text="Bad review count")
        treev.heading("4", text="No of customer")
        cleartbtn = Button(win, text=' Clear', width=20, command=clear)
        cleartbtn.place(x=900, y=550)


       
        win.mainloop()




label = Label(root1, text="RESTAURANT REVIEW ANALYSIS SYSTEM",
              bd=2, font=('Arial', 44, 'bold', 'underline'))
 
ques = Label(root1, text="Are you a Customer or Owner ???")
 
cust = Button(root1, text="Customer Click Here",bd=5,relief='ridge',font=('Arial', 20),
              padx=30, pady=20, command=take_review)
 
owner = Label(root1, text="Owner Login here >>>",bd=5,relief='ridge',font=('Arial', 20),
               padx=30, pady=20)
a1=StringVar()
a2=StringVar()


lbl1 = Label(root1, text="Owner Username",bd=5,width=20,height=2,relief='ridge',font=('Arial', 12))
lbl2 = Label(root1, text="Password", bd=5,width=20,height=2,relief='ridge',font=('Arial', 12))
e1=Entry(root1,bd=5,width=11,textvariable=a1,relief='ridge',font=('Arial', 20))
e2=Entry(root1,bd=5,width=11,textvariable=a2,relief='ridge',font=('Arial', 20),show='*')
owner_l = Button(root1, text="Login", font=('Arial', 20),command=login)


label.grid(row=0, column=0)
ques.grid(row=1, column=0, sticky=W+E)
ques.config(font=("Helvetica", 30))
cust.grid(row=2, column=0)
owner.grid(row=3, column=0)
lbl1.place(x=870,y=230)
lbl2.place(x=870,y=280)
e1.place(x=1070,y=230)
e2.place(x=1070,y=280)
owner_l.place(x=1100,y=340)




root1.mainloop()






