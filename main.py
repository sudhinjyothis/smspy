from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
import os
from tkinter import ttk

# backend
# login and register


def studentrec(event):
    global sd
    searchstd = student_list.focus()
    sd = student_list.item(searchstd, 'values')
    entry_Student_ID.delete(0, END)
    entry_Student_ID.insert(END, sd[0])
    entry_firstname.delete(0, END)
    entry_firstname.insert(END, sd[1])
    entry_surname.delete(0, END)
    entry_surname.insert(END, sd[2])
    entry_address.delete(0, END)
    entry_address.insert(END, sd[3])
    entry_gender.delete(0, END)
    entry_gender.insert(END, sd[4])
    entry_mobile.delete(0, END)
    entry_mobile.insert(END, sd[5])
    entry_fees.delete(0, END)
    entry_fees.insert(END, sd[6])


def logout():
    exit_mainpage = messagebox.askquestion("Logout", "Do you want to logout")
    if exit_mainpage == "yes":
        root_main_page.destroy()
        login_page()
    else:
        pass


def login_exit():
    exit_mainpage = messagebox.askquestion("Exit", "Do you want to exit")
    if exit_mainpage == "yes":
        login_root.destroy()
    else:
        pass


def register():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )

    cursor = mydb.cursor()
    cursor.execute(
        "CREATE table if not exists login(username varchar(100),password varchar(100))")
    username = register_entry_username.get()
    password = register_entry_password.get()
    cursor.execute("SELECT * from login")
    data = cursor.fetchall()
    flag_username = 0
    if username == "":
        messagebox.showinfo("Alert", "enter a valid username")
    elif password == "":
        messagebox.showinfo("Alert", "enter a valid password")
    else:
        for check in data:
            if username == check[0]:
                flag_username = flag_username+1

        if flag_username > 0:
            messagebox.showinfo("Alert", "username already exist!")
        else:
            qry = "INSERT into login values('{}','{}')".format(
                username, password)
            cursor.execute(qry)
            mydb.commit()
            messagebox.showinfo("Alert", "user registered succefully ")
            register_root.destroy()
            login_page()


def login_to_register():
    login_root.destroy()
    register_page()


def register_to_login():
    register_root.destroy()
    login_page()


def login():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM login")
    data = cursor.fetchall()
    username = entry_username.get()
    password = entry_password.get()
    flag = 0
    for check in data:
        if username == check[0] and password == check[1]:
            messagebox.showinfo("Alert", "login successful")
            flag = flag+1
            pass
            login_root.destroy()
            mainpage()
        elif username == check[0] and password != check[1]:
            flag = flag+1
            messagebox.showinfo("Alert", "incorrect password")
            break
    if flag == 0:
        messagebox.showinfo("Alert", "user does not exist")

# database


def addstudent(admno, firstname, surname, addresss, gender, mobile, fees):
    mydb_functions = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )
    cursorobj = mydb_functions.cursor()
    qry = "INSERT into studentdata values({},'{}','{}','{}','{}','{}','{}')".format(
        admno, firstname, surname, addresss, gender, mobile, fees)
    cursorobj.execute(qry)
    mydb_functions.commit()
    mydb_functions.close()


def viewdata():
    mydb_functions = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )
    cursorobj = mydb_functions.cursor()
    cursorobj.execute("SELECT * from studentdata order by admno")
    rows = cursorobj.fetchall()
    return rows
    mydb_functions.close()


def deleterec(admno):
    mydb_functions = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )
    cursorobj = mydb_functions.cursor()
    qry = "DELETE from studentdata where admno={}".format(admno)
    cursorobj.execute(qry)
    mydb_functions.commit()
    mydb_functions.close()


def searchdatadb(admno):
    mydb_functions = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )
    cursorobj = mydb_functions.cursor()
    qry = "SELECT * from studentdata where admno={}".format(
        admno)
    cursorobj.execute(qry)
    rows = cursorobj.fetchall()
    return rows
    mydb_functions.close()


# mainpage


def clear():
    entry_Student_ID.delete(0, END)
    entry_firstname.delete(0, END)
    entry_surname.delete(0, END)
    entry_address.delete(0, END)
    entry_gender.delete(0, END)
    entry_mobile.delete(0, END)
    entry_fees.delete(0, END)
    for record in student_list.get_children():
        student_list.delete(record)


def adddata():
    if(len(entry_Student_ID.get()) != 0):
        addstudent(entry_Student_ID.get(), entry_firstname.get(), entry_surname.get(
        ), entry_address.get(), entry_gender.get(), entry_mobile.get(), entry_fees.get())
        entry_Student_ID.delete(0, END)
        entry_firstname.delete(0, END)
        entry_surname.delete(0, END)
        entry_address.delete(0, END)
        entry_gender.delete(0, END)
        entry_mobile.delete(0, END)
        entry_fees.delete(0, END)
        displaydata()
        messagebox.showinfo("Success", "student added successfully")
    else:
        messagebox.showinfo("Alert", "enter a valid admission number")


def displaydata():
    for record in student_list.get_children():
        student_list.delete(record)
    for row in viewdata():
        student_list.insert(parent='', index='end', text='', values=row)


def deletedata():
    if(len(entry_Student_ID.get()) != 0):
        deleterec(sd[0])
        clear()
        displaydata()
        messagebox.showinfo("Deleted", "Student Deleted Successfully")
    else:
        messagebox.showinfo("Alert", "Enter a valid admission number")


def searchdata():
    if(len(entry_Student_ID.get()) == 0):
        messagebox.showinfo("Alert", "Enter a valid admission number")
    else:
        for record in student_list.get_children():
            student_list.delete(record)
        flag = 0
        for row in searchdatadb(entry_Student_ID.get()):
            student_list.insert(parent='', index='end', text='', values=row)
            flag = flag+1
        if flag == 0:
            messagebox.showinfo("Alert", "Student not found")


def updatedata():
    if(len(entry_Student_ID.get()) != 0):
        deleterec(sd[0])
    else:
        messagebox.showinfo("Alert", "Enter a valid admission number")
    if(len(entry_Student_ID.get()) != 0):
        addstudent(entry_Student_ID.get(), entry_firstname.get(), entry_surname.get(
        ), entry_address.get(), entry_gender.get(), entry_mobile.get(), entry_fees.get())
        entry_Student_ID.delete(0, END)
        entry_firstname.delete(0, END)
        entry_surname.delete(0, END)
        entry_address.delete(0, END)
        entry_gender.delete(0, END)
        entry_mobile.delete(0, END)
        entry_fees.delete(0, END)
        displaydata()
        messagebox.showinfo("Updated", "Student Details Updated Successfully")


def main_exit():
    exit_mainpage = messagebox.askquestion("Exit", "Do you want to exit")
    if exit_mainpage == "yes":
        root_main_page.destroy()
    else:
        pass


# frontend
# hover effects
# login page
# login
def hover_login_page_exit_in(e):
    image = PhotoImage(file="assets/loginexit_2.png")
    login_exit_button.config(image=image)
    login_exit_button.image = image


def hover_login_page_exit_out(e):
    image = PhotoImage(file="assets/loginexit.png")
    login_exit_button.config(image=image)
    login_exit_button.image = image


def hover_main_page_logout_in(e):
    image = PhotoImage(file="assets/logout_2.png")
    logout_button.config(image=image)
    logout_button.image = image


def hover_main_page_logout_out(e):
    image = PhotoImage(file="assets/logout.png")
    logout_button.config(image=image)
    logout_button.image = image


def hover_login_in(e):
    image = PhotoImage(file="assets/login_button_2.png")
    login_button.config(image=image)
    login_button.image = image


def hover_login_out(e):
    image = PhotoImage(file="assets/login_button.png")
    login_button.config(image=image)
    login_button.image = image


def hover_register_log_in(e):
    image = PhotoImage(file="assets/register_button_2.png")
    register_button_log.config(image=image)
    register_button_log.image = image


def hover_register_log_out(e):
    image = PhotoImage(file="assets/register_button.png")
    register_button_log.config(image=image)
    register_button_log.image = image


# register


def hover_register_in(e):
    image = PhotoImage(file="assets/register_button_2.png")
    register_button.config(image=image)
    register_button.image = image


def hover_register_out(e):
    image = PhotoImage(file="assets/register_button.png")
    register_button.config(image=image)
    register_button.image = image


def hover_login_reg_in(e):
    image = PhotoImage(file="assets/login_button_2.png")
    login_button_reg.config(image=image)
    login_button_reg.image = image


def hover_login_reg_out(e):
    image = PhotoImage(file="assets/login_button.png")
    login_button_reg.config(image=image)
    login_button_reg.image = image

# mainpage


def hover_add_button_in(e):
    image = PhotoImage(file="assets/newstud_2.png")
    add_button.config(image=image)
    add_button.image = image


def hover_add_button_out(e):
    image = PhotoImage(file="assets/newstud.png")
    add_button.config(image=image)
    add_button.image = image


def hover_display_in(e):
    image = PhotoImage(file="assets/display_2.png")
    display_button.config(image=image)
    display_button.image = image


def hover_display_out(e):
    image = PhotoImage(file="assets/display.png")
    display_button.config(image=image)
    display_button.image = image


def hover_clear_in(e):
    image = PhotoImage(file="assets/clear_2.png")
    clear_button.config(image=image)
    clear_button.image = image


def hover_clear_out(e):
    image = PhotoImage(file="assets/clear.png")
    clear_button.config(image=image)
    clear_button.image = image


def hover_delete_in(e):
    image = PhotoImage(file="assets/delete_2.png")
    delete_button.config(image=image)
    delete_button.image = image


def hover_delete_out(e):
    image = PhotoImage(file="assets/delete.png")
    delete_button.config(image=image)
    delete_button.image = image


def hover_search_in(e):
    image = PhotoImage(file="assets/search_2.png")
    search_button.config(image=image)
    search_button.image = image


def hover_search_out(e):
    image = PhotoImage(file="assets/search.png")
    search_button.config(image=image)
    search_button.image = image


def hover_update_in(e):
    image = PhotoImage(file="assets/update_2.png")
    update_button.config(image=image)
    update_button.image = image


def hover_update_out(e):
    image = PhotoImage(file="assets/update.png")
    update_button.config(image=image)
    update_button.image = image


def hover_exit_in(e):
    image = PhotoImage(file="assets/exit_2.png")
    exit_button.config(image=image)
    exit_button.image = image


def hover_exit_out(e):
    image = PhotoImage(file="assets/exit.png")
    exit_button.config(image=image)
    exit_button.image = image


def mainpage():
    global add_button, display_button, clear_button, delete_button, search_button, update_button, exit_button
    global root_main_page
    global student_list
    global entry_Student_ID, entry_firstname, entry_surname, entry_address, entry_gender, entry_mobile, entry_fees
    global logout_button

    root_main_page = Tk()
    root_main_page.geometry("1280x720+300+100")
    root_main_page.title("School Admin Page")
    root_main_page.iconbitmap("C:\SJ\py project\icon.ico")
    root_main_page.resizable(0, 0)
    # background
    background_img = ImageTk.PhotoImage(Image.open("assets\\background.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)
    # top frame
    title_img = ImageTk.PhotoImage(Image.open("assets\\title_1.png"))
    label_title = Label(image=title_img, width=1257, bg="#FFFFFF")
    label_title.place(x=10, y=5)

    # logout
    logout_button_img = PhotoImage(file="assets/logout.png")
    logout_button = Button(root_main_page, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                           image=logout_button_img, command=logout)
    logout_button.place(x=1150, y=10)

    # main frame

    # left frame
    frame_left = Frame(root_main_page, width=600, height=500, bg="white")
    frame_left.place(x=11, y=113)

    # content text
    left_frame_font = ("Helvetica", 15)
    Label(frame_left, text="AdmNo.         :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=40)
    Label(frame_left, text="Firstname      :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=100)
    Label(frame_left, text="Surname       :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=160)
    Label(frame_left, text="Address        :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=220)
    Label(frame_left, text="Gender         :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=280)
    Label(frame_left, text="Mobile No.    :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=340)
    Label(frame_left, text="Fees remaining :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=400)

    # content entry fields

    entry_Student_ID = Entry(frame_left, width=30,
                             border=0, font=left_frame_font)
    entry_Student_ID.place(x=200, y=40)

    entry_firstname = Entry(frame_left, width=30,
                            border=0, font=left_frame_font)
    entry_firstname.place(x=200, y=100)

    entry_surname = Entry(frame_left, width=30,
                          border=0, font=left_frame_font)
    entry_surname.place(x=200, y=162)

    entry_address = Entry(frame_left, width=30,
                          border=0, font=left_frame_font)
    entry_address.place(x=200, y=223)

    entry_gender = Entry(frame_left, width=30,
                         border=0, font=left_frame_font)
    entry_gender.place(x=200, y=285)

    entry_mobile = Entry(frame_left, width=30,
                         border=0, font=left_frame_font)
    entry_mobile.place(x=200, y=343)

    entry_fees = Entry(frame_left, width=30,
                       border=0, font=left_frame_font)
    entry_fees.place(x=200, y=403)

    Frame(frame_left, width=331, height=2, bg="#64FEB5",).place(x=200, y=68)
    Frame(frame_left, width=331, height=2, bg="#64FEB5",).place(x=200, y=127)
    Frame(frame_left, width=331, height=2, bg="#64FEB5",).place(x=200, y=189)
    Frame(frame_left, width=331, height=2, bg="#64FEB5",).place(x=200, y=250)
    Frame(frame_left, width=331, height=2, bg="#64FEB5",).place(x=200, y=311)
    Frame(frame_left, width=331, height=2, bg="#64FEB5",).place(x=200, y=370)
    Frame(frame_left, width=331, height=2, bg="#64FEB5",).place(x=200, y=430)

    # right frame
    right_frame_font = ("Helvetica", 9)
    frame_right = Frame(root_main_page, width=651, height=500, bg="white")
    frame_right.place(x=619, y=113)
    # content
    right_title_img = ImageTk.PhotoImage(
        Image.open("assets\\student-detail.png"))
    right_label_title = Label(frame_right,
                              image=right_title_img, bg="#FFFFFF")
    right_label_title.place(x=150, y=0)

    # table
    list_box_font = ("Helvetica", 20)
    frame_list = Frame(frame_right, width=640, height=415, bg="black")
    frame_list.place(x=6, y=80)
    scroll_x = Scrollbar(frame_list, orient=HORIZONTAL)
    scroll_y = Scrollbar(frame_list, orient=VERTICAL)
    student_list = ttk.Treeview(frame_list)
    student_list['columns'] = (
        "admno", "firstname", "surname", "address", "gender", "mobile no.", "fees")
    # column
    student_list.column("#0", width=0, stretch=NO)
    student_list.column("admno", width=45, anchor=CENTER)
    student_list.column("firstname", width=80, anchor=CENTER)
    student_list.column("surname", width=80, anchor=CENTER)
    student_list.column("address", width=200, anchor=CENTER)
    student_list.column("gender", width=50, anchor=CENTER)
    student_list.column("mobile no.", width=70, anchor=CENTER)
    student_list.column("fees", width=85, anchor=CENTER)
    # heading
    student_list.heading("#0", text="")
    student_list.heading("admno", text="admno")
    student_list.heading("firstname", text="firstname")
    student_list.heading("surname", text="surname")
    student_list.heading("address", text="address")
    student_list.heading("gender", text="gender")
    student_list.heading("mobile no.", text="mobile no.")
    student_list.heading("fees", text="fees remaining")

    style = ttk.Style()

    style.configure("Treeview",
                    background="#c8ded8",
                    foreground="black",
                    rowheight=35,
                    fieldbackground="#c8ded8"
                    )
    style.map("Treeview",
              background=[('selected', '#0DEFBB')],
              foreground=[('selected', 'black')]
              )

    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=student_list.xview)
    scroll_y.config(command=student_list.yview)
    student_list.pack()
    student_list.bind("<ButtonRelease-1>", studentrec)

    # footer buttons frame
    frame_buttons = Frame(root_main_page, width=1260, height=95, bg="white")
    frame_buttons.place(x=10, y=617)

    # footer buttons
    add_button_img = PhotoImage(file="assets/newstud.png")
    add_button = Button(frame_buttons, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                        image=add_button_img, command=adddata)
    add_button.place(x=30, y=20)

    display_button_img = PhotoImage(file="assets/display.png")
    display_button = Button(frame_buttons, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                            image=display_button_img, command=displaydata)
    display_button.place(x=200, y=20)

    clear_button_img = PhotoImage(file="assets/clear.png")
    clear_button = Button(frame_buttons, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                          image=clear_button_img, command=clear)
    clear_button.place(x=370, y=20)

    delete_button_img = PhotoImage(file="assets/delete.png")
    delete_button = Button(frame_buttons, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                           image=delete_button_img, command=deletedata)
    delete_button.place(x=540, y=20)

    search_button_img = PhotoImage(file="assets/search.png")
    search_button = Button(frame_buttons, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                           image=search_button_img, command=searchdata)
    search_button.place(x=710, y=20)

    update_button_img = PhotoImage(file="assets/update.png")
    update_button = Button(frame_buttons, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                           image=update_button_img, command=updatedata)
    update_button.place(x=880, y=20)

    exit_button_img = PhotoImage(file="assets/exit.png")
    exit_button = Button(frame_buttons, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                         image=exit_button_img, command=main_exit)
    exit_button.place(x=1050, y=20)

    add_button.bind("<Enter>", hover_add_button_in)
    add_button.bind("<Leave>", hover_add_button_out)

    display_button.bind("<Enter>", hover_display_in)
    display_button.bind("<Leave>", hover_display_out)

    clear_button.bind("<Enter>", hover_clear_in)
    clear_button.bind("<Leave>", hover_clear_out)

    delete_button.bind("<Enter>", hover_delete_in)
    delete_button.bind("<Leave>", hover_delete_out)

    search_button.bind("<Enter>", hover_search_in)
    search_button.bind("<Leave>", hover_search_out)

    update_button.bind("<Enter>", hover_update_in)
    update_button.bind("<Leave>", hover_update_out)

    exit_button.bind("<Enter>", hover_exit_in)
    exit_button.bind("<Leave>", hover_exit_out)

    logout_button.bind("<Enter>", hover_main_page_logout_in)
    logout_button.bind("<Leave>", hover_main_page_logout_out)

    root_main_page.mainloop()


def login_page():
    global login_root, entry_username, entry_password
    global login_button
    global register_button_log
    global login_exit_button
    login_root = Tk()
    login_root.geometry("1280x720+300+100")
    login_root.title("School Admin Page - LOGIN")
    login_root.iconbitmap("C:\SJ\py project\icon.ico")
    login_root.resizable(0, 0)

    background_img = ImageTk.PhotoImage(Image.open("assets\\background.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)

    # login_frame
    login_frame = Frame(login_root, width=400, height=500,
                        bg="white").place(x=450, y=90)
    frame1 = Frame(login_root, width=30, height=40, bg="white")

    # Login
    login_img = ImageTk.PhotoImage(Image.open("assets\\Login.png"))
    label_login = Label(image=login_img, border=0, bg="#FFFFFF")
    label_login.place(x=510, y=120)

    # username
    label_username_text = Label(login_root, text="Username ", bg="#FFFFFF")
    username_font = ("Helvetica", 13)
    label_username_text.config(font=username_font)
    label_username_text.place(x=470, y=250)
    entry_username = Entry(login_root, width=20, border=0,)
    entry_username.config(font=username_font)
    entry_username.place(x=580, y=250)
    Frame(login_root, width=180, height=2, bg="#64FEB5").place(x=580, y=272)
    username_img = PhotoImage(file="assets/username.png")
    label_username_img = Label(
        image=username_img, width=25, height=25, bg="#FFFFFF")
    label_username_img.place(x=550, y=250)

    # password
    label_password_text = Label(login_root, text="Password ", bg="#FFFFFF")
    password_font = ("Helvetica", 13)
    label_password_text.config(font=password_font)
    label_password_text.place(x=470, y=320)
    entry_password = Entry(login_root, width=20, border=0, show="*")
    entry_password.config(font=password_font)
    entry_password.place(x=580, y=320)
    Frame(login_root, width=180, height=2, bg="#64FEB5").place(x=580, y=342)
    password_img = PhotoImage(file="assets/password.png")
    label_password_img = Label(
        image=password_img, width=25, height=25, bg="#FFFFFF")
    label_password_img.place(x=550, y=320)

    # button
    login_button_img = PhotoImage(file="assets/login_button.png")
    login_button = Button(login_root, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                          image=login_button_img, command=login)
    login_button.place(x=570, y=400)

    register_button_img = PhotoImage(file="assets/register_button.png")
    register_button_log = Button(login_root, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                                 image=register_button_img, command=login_to_register)
    register_button_log.place(x=570, y=470)

    exit_button_img = PhotoImage(file="assets/loginexit.png")
    login_exit_button = Button(login_frame, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                               image=exit_button_img, command=login_exit)
    login_exit_button.place(x=725, y=95)

    login_button.bind("<Enter>", hover_login_in)
    login_button.bind("<Leave>", hover_login_out)

    register_button_log.bind("<Enter>", hover_register_log_in)
    register_button_log.bind("<Leave>", hover_register_log_out)

    login_exit_button.bind("<Enter>", hover_login_page_exit_in)
    login_exit_button.bind("<Leave>", hover_login_page_exit_out)

    login_root.mainloop()


def register_page():
    global register_root, register_entry_username, register_entry_password
    global register_button, login_button_reg
    register_root = Tk()
    register_root.geometry("1280x720+300+100")
    register_root.title("School Admin Page - REGISTER")
    register_root.iconbitmap("C:\SJ\py project\icon.ico")
    register_root.resizable(0, 0)
    # background
    background_img = ImageTk.PhotoImage(Image.open("assets\\background.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)

    # register_frame
    Frame(register_root, width=400, height=500, bg="white").place(x=450, y=90)
    frame1 = Frame(register_root, width=30, height=40, bg="white")

    # register
    login_img = ImageTk.PhotoImage(Image.open("assets\\register_img.png"))
    label_login = Label(image=login_img, border=0, bg="#FFFFFF")
    label_login.place(x=510, y=120)

    # username
    label_username_text = Label(register_root, text="Username ", bg="#FFFFFF")
    username_font = ("Helvetica", 13)
    label_username_text.config(font=username_font)
    label_username_text.place(x=470, y=250)
    register_entry_username = Entry(register_root, width=20, border=0,)
    register_entry_username.config(font=username_font)
    register_entry_username.place(x=580, y=250)
    Frame(register_root, width=180, height=2, bg="#64FEB5").place(x=580, y=272)
    username_img = PhotoImage(file="assets/username.png")
    label_username_img = Label(
        image=username_img, width=25, height=25, bg="#FFFFFF")
    label_username_img.place(x=550, y=250)

    # password
    label_password_text = Label(register_root, text="Password ", bg="#FFFFFF")
    password_font = ("Helvetica", 13)
    label_password_text.config(font=password_font)
    label_password_text.place(x=470, y=320)
    register_entry_password = Entry(
        register_root, width=20, border=0, show="*")
    register_entry_password.config(font=password_font)
    register_entry_password.place(x=580, y=320)
    Frame(register_root, width=180, height=2, bg="#64FEB5").place(x=580, y=342)
    password_img = PhotoImage(file="assets/password.png")
    label_password_img = Label(
        image=password_img, width=25, height=25, bg="#FFFFFF")
    label_password_img.place(x=550, y=320)

    # button
    register_button_img = PhotoImage(file="assets/register_button.png")
    register_button = Button(register_root, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                             image=register_button_img, command=register)
    register_button.place(x=570, y=400)

    login_button_img = PhotoImage(file="assets/login_button.png")
    login_button_reg = Button(register_root, width=250, height=50, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                              image=login_button_img, command=register_to_login)
    login_button_reg.place(x=520, y=470)
    register_button.bind("<Enter>", hover_register_in)
    register_button.bind("<Leave>", hover_register_out)

    login_button_reg.bind("<Enter>", hover_login_reg_in)
    login_button_reg.bind("<Leave>", hover_login_reg_out)

    register_root.mainloop()


database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=os.environ.get("sql_pass"),
    database="schoolmanagement"
)

cursorobject = database.cursor()
cursorobject.execute(
    "CREATE table if not exists login(username varchar(100),password varchar(100))")
cursorobject.execute(
    "CREATE table if not exists studentdata(admno int(10),firstname varchar(100),surname varchar(100),addresss varchar(200),gender varchar(10),mobile varchar(20),fees varchar(5000))")
database.close()
login_page()
