from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
import os
from tkinter import ttk
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import csv
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


def comboclick(event):
    global search_option_click
    search_option_click = combobox.get()


def logout():
    exit_mainpage = messagebox.askquestion("Logout", "Do you want to logout")
    if exit_mainpage == "yes":
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=os.environ.get("sql_pass"),
            database="schoolmanagement"
        )
        cursor = mydb.cursor()
        cursor.execute(
            "UPDATE login set log='loggedout' where log like 'loggedin'")
        mydb.commit()
        root_main_page.destroy()
        login_page()
    else:
        pass


def login_exit():
    exit_mainpage = messagebox.askquestion("Exit", "Do you want to exit")
    if exit_mainpage == "yes":
        login_user_root.destroy()
        portal()
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
    username = register_entry_username.get()
    password1 = register_entry_password.get()
    password = password1.encode()
    log = "loggedout"
    mysalt = b'\x1e\x82\xd90f\x16>u\x05\x0f\x99m\x98r\xcc\x19'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )
    key1 = base64.urlsafe_b64encode(kdf.derive(password))
    key = key1.decode()
    cursor.execute("SELECT * from login")
    data = cursor.fetchall()
    flag_username = 0
    if username == "":
        messagebox.showerror("Error", "enter a valid username")
    elif password == "":
        messagebox.showerror("Error", "enter a valid password")
    elif len(username) < 5:
        messagebox.showerror(
            "Error", "username must be more than 4 characters")
    elif len(password1) < 8 or len(password1) > 16:
        messagebox.showerror(
            "Error", "password must be between 8 - 16 characters")
    else:
        for check in data:
            if username == check[0]:
                flag_username = flag_username+1

        if flag_username > 0:
            messagebox.showerror("Error", "username already exist!")
        else:
            qry = "INSERT into login values('{}','{}','{}')".format(
                username, key, log)
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
    username = user_entry_username.get()
    password1 = user_entry_password.get()
    password = password1.encode()
    mysalt = b'\x1e\x82\xd90f\x16>u\x05\x0f\x99m\x98r\xcc\x19'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )
    key1 = base64.urlsafe_b64encode(kdf.derive(password))
    key = key1.decode()
    flag = 0
    for check in data:
        if username == check[0] and key == check[1]:
            messagebox.showinfo("Alert", "login successful")
            qry = "UPDATE login set log='loggedin' where username like '{}'".format(
                username)
            cursor.execute(qry)
            mydb.commit()
            flag = flag+1
            pass
            login_user_root.destroy()
            userportal()
        elif username == check[0] and key != check[1]:
            flag = flag+1
            messagebox.showerror("Error", "incorrect password")
            break
    if flag == 0:
        messagebox.showerror("Error", "user does not exist")

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


def searchdatadb(admno, name, standard):
    mydb_functions = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )
    cursorobj = mydb_functions.cursor()
    if search_option_click == "admno":
        qry = "SELECT * from studentdata where admno={}".format(
            admno)
        cursorobj.execute(qry)
        rows = cursorobj.fetchall()
        return rows
    elif search_option_click == "name":
        qry = "SELECT * from studentdata where studentname like '{}%' ".format(
            name)
        cursorobj.execute(qry)
        rows = cursorobj.fetchall()
        return rows
    elif search_option_click == "class":
        qry = "SELECT * from studentdata where class like '{}%'".format(
            standard)
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
    try:
        mydb_functions = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=os.environ.get("sql_pass"),
            database="schoolmanagement"
        )
        cursorobj = mydb_functions.cursor()
        qry = "SELECT * from studentdata where admno={}".format(
            entry_Student_ID.get())
        cursorobj.execute(qry)
        fetch = cursorobj.fetchall()
        if fetch == []:
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
            messagebox.showerror("Error", "Student already exists")
    except:
        messagebox.showerror("Error", "enter a valid admno")


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
    try:
        if len(str(search_entry.get())) == 0:
            messagebox.showinfo("Alert", "Enter a value to search")
        else:
            for record in student_list.get_children():
                student_list.delete(record)
            flag = 0
            for row in searchdatadb(search_entry.get(), search_entry.get(), search_entry.get()):
                student_list.insert(parent='', index='end',
                                    text='', values=row)
                flag = flag+1
            if flag == 0:
                messagebox.showinfo("Alert", "not found")
    except:
        messagebox.showinfo("Alert", "enter the correct value")


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
        userportal()
    else:
        pass


def homebutton():
    root_intro.destroy()
    portal()


def admin_portal():
    portal_intro.destroy()
    login_admin_page()


def adminloginexit():
    exit_mainpage = messagebox.askquestion("Exit", "Do you want to exit")
    if exit_mainpage == "yes":
        login_root.destroy()
        portal()
    else:
        pass


def user_portal():
    portal_intro.destroy()
    login_user_page()


def student_details():
    userportal_intro.destroy()
    studentpage()


def userdetails_():
    userportal_intro.destroy()
    userdetails()


def userdetails_back2():
    user_details.destroy()
    userportal()


def adminlogin():
    username = admin_entry_username.get()
    password1 = admin_entry_password.get()
    password = password1.encode()
    mysalt = b'\x1e\x82\xd90f\x16>u\x05\x0f\x99m\x98r\xcc\x19'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )
    key1 = base64.urlsafe_b64encode(kdf.derive(password))
    key = key1.decode()
    file = open("admin.csv", 'r')
    reader = csv.reader(file)
    for check in reader:
        if username == check[0] and key == check[1]:
            messagebox.showinfo("Alert", "login successful")
            login_root.destroy()
            adminportal()
        if username != check[0]:
            messagebox.showerror("Error", "incorrect username")
        elif key != check[1]:
            messagebox.showerror("Error", "incorrect password")


def adminpasschange__():
    adminportal_intro.destroy()
    changeadminpass()


def adminchangeinfo():
    username = entry_username_admin.get()
    password1 = entry_pass_admin.get()
    newuser = entry_newuser_admin.get()
    newpass = entry_newpass_admin.get()
    password = password1.encode()
    mysalt = b'\x1e\x82\xd90f\x16>u\x05\x0f\x99m\x98r\xcc\x19'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )
    key1 = base64.urlsafe_b64encode(kdf.derive(password))
    key = key1.decode()

    password2 = newpass.encode()
    mysalt = b'\x1e\x82\xd90f\x16>u\x05\x0f\x99m\x98r\xcc\x19'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )
    key2 = base64.urlsafe_b64encode(kdf.derive(password2))
    newkey = key2.decode()

    flag = 0
    file = open("admin.csv", 'r')
    data = csv.reader(file)
    list = [newuser, newkey]
    for check in data:
        if len(newuser) == 0:
            messagebox.showerror("Error", "enter a valid username")
        elif len(newpass) == 0:
            messagebox.showerror("Error", "enter a valid password")
        else:
            if username == check[0] and key == check[1]:
                messagebox.showinfo(
                    "Alert", "username and password changed successfully")
                flag = flag+1
                file1 = open("admin.csv", 'w', newline="")
                writer = csv.writer(file1)
                writer.writerow(list)
                file1.close()
                admin_password_change.destroy()
                adminportal()
            elif username == check[0] and key != check[1]:
                flag = flag+1
                messagebox.showerror("Error", "incorrect password")
                break
            if flag == 0:
                messagebox.showerror("Error", "user does not exist")
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


def hover_home_in(e):
    image = PhotoImage(file="assets/homebutton_2.png")
    home_button.config(image=image)
    home_button.image = image


def hover_home_out(e):
    image = PhotoImage(file="assets/homebutton.png")
    home_button.config(image=image)
    home_button.image = image


def studentpage():
    global add_button, display_button, clear_button, delete_button, search_button, update_button, exit_button
    global root_main_page
    global student_list
    global entry_Student_ID, entry_firstname, entry_surname, entry_address, entry_gender, entry_mobile, entry_fees, search_entry
    global logout_button
    global combobox

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
    #logout_button.place(x=1150, y=10)

    # main frame

    # left frame
    frame_left = Frame(root_main_page, width=600, height=500, bg="white")
    frame_left.place(x=11, y=113)

    # content text
    left_frame_font = ("Helvetica", 15)
    Label(frame_left, text="AdmNo.         :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=40)
    Label(frame_left, text="Name            :",
          font=left_frame_font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=100)
    Label(frame_left, text="Class            :",
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
        Image.open("assets\\student-detail_1.png"))
    right_label_title = Label(frame_right,
                              image=right_title_img, bg="#FFFFFF")
    right_label_title.place(x=130, y=0)

    options = ["", "admno", "class", "name"]
    combobox = ttk.Combobox(frame_right, value=options)
    combobox.current(0)
    combobox.bind("<<ComboboxSelected>>", comboclick)
    combobox.place(x=473, y=57)
    combobox_text = Label(
        frame_right, text="Search ", font=right_frame_font, bg="#FFFFFF", fg="black")
    combobox_text.place(x=160, y=57)
    combobox_text_opt = Label(
        frame_right, text="Options : ", font=right_frame_font, bg="#FFFFFF", fg="black")
    combobox_text_opt.place(x=400, y=57)
    search_entry = Entry(frame_right, width=21,
                         border=0, font=right_frame_font)
    search_entry.place(x=210, y=60)
    Frame(frame_right, width=150, height=2, bg="#64FEB5",).place(x=210, y=77)

    # table
    list_box_font = ("Helvetica", 20)
    frame_list = Frame(frame_right, width=640, height=415, bg="black")
    frame_list.place(x=6, y=97)
    scroll_x = Scrollbar(frame_list, orient=HORIZONTAL)
    scroll_y = Scrollbar(frame_list, orient=VERTICAL)
    student_list = ttk.Treeview(frame_list)
    student_list['columns'] = (
        "admno", "firstname", "class", "address", "gender", "mobile no.", "fees")
    # column
    student_list.column("#0", width=0, stretch=NO)
    student_list.column("admno", width=45, minwidth=45, anchor=CENTER)
    student_list.column("firstname", width=120, minwidth=120, anchor=CENTER)
    student_list.column("class", width=40, minwidth=40, anchor=W)
    student_list.column("address", width=200, minwidth=200, anchor=CENTER)
    student_list.column("gender", width=50, minwidth=50, anchor=W)
    student_list.column("mobile no.", width=70, minwidth=70, anchor=W)
    student_list.column("fees", width=85, minwidth=85, anchor=CENTER)
    # heading
    student_list.heading("#0", text="")
    student_list.heading("admno", text="admno")
    student_list.heading("firstname", text="Name")
    student_list.heading("class", text="class", anchor=W)
    student_list.heading("address", text="address")
    student_list.heading("gender", text="gender", anchor=W)
    student_list.heading("mobile no.", text="mobile no.", anchor=W)
    student_list.heading("fees", text="fees remaining", anchor=W)

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


def intropage():
    global root_intro
    global home_button
    root_intro = Tk()
    root_intro.geometry("1280x720+300+100")
    root_intro.title("School Admin Page")
    root_intro.iconbitmap("C:\SJ\py project\icon.ico")
    root_intro.resizable(0, 0)
    # background
    background_img = ImageTk.PhotoImage(Image.open("assets\\introback.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)

    # button
    home_button_img = PhotoImage(file="assets/homebutton.png")
    home_button = Button(root_intro, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                         image=home_button_img, command=homebutton)
    home_button.place(x=575, y=380)

    home_button.bind("<Enter>", hover_home_in)
    home_button.bind("<Leave>", hover_home_out)
    root_intro.mainloop()


def portal():
    global portal_intro
    portal_intro = Tk()
    portal_intro.geometry("1280x720+300+100")
    portal_intro.title("School Admin Page")
    portal_intro.iconbitmap("C:\SJ\py project\icon.ico")
    portal_intro.resizable(0, 0)
    # background
    background_img = ImageTk.PhotoImage(Image.open("assets\\portal_back.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)

    portal_button_img = PhotoImage(file="assets/adminbutton.png")
    portal_button = Button(portal_intro, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                           image=portal_button_img, command=admin_portal)
    portal_button.place(x=275, y=380)

    user_button_img = PhotoImage(file="assets/userbutton_2.png")
    user_button = Button(portal_intro, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                         image=user_button_img, command=user_portal)
    user_button.place(x=675, y=380)

    portal_intro.mainloop()


def adminportal():
    global adminportal_intro
    adminportal_intro = Tk()
    adminportal_intro.geometry("1280x720+300+100")
    adminportal_intro.title("School Admin Page")
    adminportal_intro.iconbitmap("C:\SJ\py project\icon.ico")
    adminportal_intro.resizable(0, 0)
    # background
    background_img = ImageTk.PhotoImage(Image.open("assets\\admin_back.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)

    portal_button_img = PhotoImage(file="assets/adminpassbutton_2.png")
    portal_button = Button(adminportal_intro, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                           image=portal_button_img, command=adminpasschange__)
    portal_button.place(x=550, y=310)

    user_button_img = PhotoImage(file="assets/register_adminbutton.png")
    user_button = Button(adminportal_intro, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                         image=user_button_img)
    user_button.place(x=550, y=430)

    adminportal_intro.mainloop()


def userportal():
    global userportal_intro
    userportal_intro = Tk()
    userportal_intro.geometry("1280x720+300+100")
    userportal_intro.title("School Admin Page")
    userportal_intro.iconbitmap("C:\SJ\py project\icon.ico")
    userportal_intro.resizable(0, 0)
    # background
    background_img = ImageTk.PhotoImage(Image.open("assets\\user_back.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)

    portal_button_img = PhotoImage(file="assets/studentbutton_2.png")
    portal_button = Button(userportal_intro, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                           image=portal_button_img, command=student_details)
    portal_button.place(x=100, y=330)

    user_button_img = PhotoImage(file="assets/userdetailsbutton.png")
    user_button = Button(userportal_intro, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                         image=user_button_img, command=userdetails_)
    user_button.place(x=100, y=450)

    font = ("Helvetica", 50)
    mydb_functions = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ.get("sql_pass"),
        database="schoolmanagement"
    )
    cursorobj = mydb_functions.cursor()
    cursorobj.execute("SELECT count(*) from studentdata")
    a = cursorobj.fetchall()
    b = a[0]
    c = b[0]
    total_label = Label(
        userportal_intro, text="TOTAL NUMBER  ", font=font, bg="#ADFF90", fg="#FFFFFF")
    total2_label = Label(
        userportal_intro, text="OF STUDENTS : " + str(c), font=font, bg="#6AFCB1", fg="#FFFFFF")

    total_label.place(x=450, y=350)
    total2_label.place(x=450, y=430)

    userportal_intro.mainloop()


def userdetails():
    global user_details
    user_details = Tk()
    user_details.geometry("1280x720+300+100")
    user_details.title("User Details")
    user_details.iconbitmap("C:\SJ\py project\icon.ico")
    user_details.resizable(0, 0)
    # background
    font = ("Helvetica", 30)
    background_img = ImageTk.PhotoImage(
        Image.open("assets\\userdetailsback.png"))
    label_background = Label(image=background_img)
    label_background.pack()
    label_name = Label(user_details, text="Name         : ",
                       font=font, bg="#C1FF9A", fg="#3d403f").place(x=100, y=250)
    label_age = Label(user_details, text="Age            : ",
                      font=font, bg="#C1FF9A", fg="#3d403f").place(x=100, y=325)
    label_username = Label(user_details, text="Mobile        : ",
                           font=font, bg="#C1FF9A", fg="#3d403f").place(x=100, y=400)
    label_username = Label(user_details, text="Username  : ",
                           font=font, bg="#C1FF9A", fg="#3d403f").place(x=100, y=475)
    user_back_img = PhotoImage(file="assets/userdetailsbackbutton.png")
    user_back_button = Button(user_details, bg="#9DFF8E", border=0, activebackground="#9DFF8E",
                              image=user_back_img, command=userdetails_back2)
    user_back_button.place(x=550, y=600)
    mainloop()


def changeadminpass():
    global admin_password_change
    global entry_pass_admin, entry_username_admin, entry_newuser_admin, entry_newpass_admin
    admin_password_change = Tk()
    admin_password_change.geometry("1280x720+300+100")
    admin_password_change.title("User Details")
    admin_password_change.iconbitmap("C:\SJ\py project\icon.ico")
    admin_password_change.resizable(0, 0)
    # background
    font = ("Helvetica", 25)
    background_img = ImageTk.PhotoImage(
        Image.open("assets\\adminpasschange.png"))
    label_background = Label(image=background_img)
    label_background.pack()
    frame_change = Frame(admin_password_change, width=800,
                         height=450, bg="white")
    frame_change.place(x=240, y=200)
    Label(frame_change, text="Username          :",
          font=font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=20)

    entry_username_admin = Entry(frame_change, width=20,
                                 border=0, font=font)
    entry_username_admin.place(x=350, y=25)
    Frame(frame_change, width=363, height=2, bg="#64FEB5",).place(x=350, y=65)

    Label(frame_change, text="Password           :",
          font=font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=105)
    entry_pass_admin = Entry(frame_change, width=20,
                             border=0, font=font, show="*")
    entry_pass_admin.place(x=350, y=110)

    Frame(frame_change, width=363, height=2, bg="#64FEB5",).place(x=350, y=150)

    Label(frame_change, text="New username   :",
          font=font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=190)

    entry_newuser_admin = Entry(frame_change, width=20,
                                border=0, font=font)
    entry_newuser_admin.place(x=350, y=195)
    Frame(frame_change, width=363, height=2, bg="#64FEB5",).place(x=350, y=235)

    Label(frame_change, text="New Password   :",
          font=font, bg="#FFFFFF", fg="#2c3036").place(x=40, y=275)
    entry_newpass_admin = Entry(frame_change, width=20,
                                border=0, font=font, show="*")
    entry_newpass_admin.place(x=350, y=280)
    Frame(frame_change, width=363, height=2, bg="#64FEB5",).place(x=350, y=320)

    add_button_img = PhotoImage(file="assets/adminpasschangebutton.png")
    change_button = Button(frame_change, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                           image=add_button_img, command=adminchangeinfo)
    change_button.place(x=300, y=350)

    mainloop()


def registeruser():
    register_user = Tk()
    register_user.geometry("1280x720+300+100")
    register_user.title("School Admin Page - LOGIN")
    register_user.iconbitmap("C:\SJ\py project\icon.ico")
    register_user.resizable(0, 0)

    background_img = ImageTk.PhotoImage(
        Image.open("assets\\userregisterback.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)


def login_admin_page():
    global login_root, admin_entry_username, admin_entry_password
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
    admin_entry_username = Entry(login_root, width=20, border=0,)
    admin_entry_username.config(font=username_font)
    admin_entry_username.place(x=580, y=250)
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
    admin_entry_password = Entry(login_root, width=20, border=0, show="*")
    admin_entry_password.config(font=password_font)
    admin_entry_password.place(x=580, y=320)
    Frame(login_root, width=180, height=2, bg="#64FEB5").place(x=580, y=342)
    password_img = PhotoImage(file="assets/password.png")
    label_password_img = Label(
        image=password_img, width=25, height=25, bg="#FFFFFF")
    label_password_img.place(x=550, y=320)

    # button
    login_button_img = PhotoImage(file="assets/login_button.png")
    login_button = Button(login_root, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                          image=login_button_img, command=adminlogin)
    login_button.place(x=570, y=400)

    register_button_img = PhotoImage(file="assets/register_button.png")
    register_button_log = Button(login_root, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                                 image=register_button_img, command=login_to_register)
    #register_button_log.place(x=570, y=470)

    exit_button_img = PhotoImage(file="assets/loginexit.png")
    login_exit_button = Button(login_frame, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                               image=exit_button_img, command=adminloginexit)
    login_exit_button.place(x=725, y=95)

    login_button.bind("<Enter>", hover_login_in)
    login_button.bind("<Leave>", hover_login_out)

    register_button_log.bind("<Enter>", hover_register_log_in)
    register_button_log.bind("<Leave>", hover_register_log_out)

    login_exit_button.bind("<Enter>", hover_login_page_exit_in)
    login_exit_button.bind("<Leave>", hover_login_page_exit_out)

    login_root.mainloop()


def login_user_page():
    global login_user_root, user_entry_username, user_entry_password
    global login_button
    global register_button_log
    global login_exit_button
    login_user_root = Tk()
    login_user_root.geometry("1280x720+300+100")
    login_user_root.title("School Admin Page - LOGIN")
    login_user_root.iconbitmap("C:\SJ\py project\icon.ico")
    login_user_root.resizable(0, 0)

    background_img = ImageTk.PhotoImage(Image.open("assets\\background.png"))
    label_background = Label(image=background_img)
    label_background.place(x=0, y=0)

    # login_frame
    login_frame = Frame(login_user_root, width=400, height=500,
                        bg="white").place(x=450, y=90)
    frame1 = Frame(login_user_root, width=30, height=40, bg="white")

    # Login
    login_img = ImageTk.PhotoImage(Image.open("assets\\Login.png"))
    label_login = Label(image=login_img, border=0, bg="#FFFFFF")
    label_login.place(x=510, y=120)

    # username
    label_username_text = Label(
        login_user_root, text="Username ", bg="#FFFFFF")
    username_font = ("Helvetica", 13)
    label_username_text.config(font=username_font)
    label_username_text.place(x=470, y=250)
    user_entry_username = Entry(login_user_root, width=20, border=0,)
    user_entry_username.config(font=username_font)
    user_entry_username.place(x=580, y=250)
    Frame(login_user_root, width=180, height=2,
          bg="#64FEB5").place(x=580, y=272)
    username_img = PhotoImage(file="assets/username.png")
    label_username_img = Label(
        image=username_img, width=25, height=25, bg="#FFFFFF")
    label_username_img.place(x=550, y=250)

    # password
    label_password_text = Label(
        login_user_root, text="Password ", bg="#FFFFFF")
    password_font = ("Helvetica", 13)
    label_password_text.config(font=password_font)
    label_password_text.place(x=470, y=320)
    user_entry_password = Entry(login_user_root, width=20, border=0, show="*")
    user_entry_password.config(font=password_font)
    user_entry_password.place(x=580, y=320)
    Frame(login_user_root, width=180, height=2,
          bg="#64FEB5").place(x=580, y=342)
    password_img = PhotoImage(file="assets/password.png")
    label_password_img = Label(
        image=password_img, width=25, height=25, bg="#FFFFFF")
    label_password_img.place(x=550, y=320)

    # button
    login_button_img = PhotoImage(file="assets/login_button.png")
    login_button = Button(login_user_root, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                          image=login_button_img, command=login)
    login_button.place(x=570, y=400)

    register_button_img = PhotoImage(file="assets/register_button.png")
    register_button_log = Button(login_user_root, bg="#FFFFFF", border=0, activebackground="#FFFFFF",
                                 image=register_button_img, command=login_to_register)
    #register_button_log.place(x=570, y=470)

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

    login_user_root.mainloop()


database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=os.environ.get("sql_pass"),
)

cursorobject = database.cursor()
cursorobject.execute("CREATE database if not exists schoolmanagement")
cursorobject.execute("USE schoolmanagement")
# cursorobject.execute(
# "CREATE table if not exists login(username varchar(100),password varchar(100),mobile varchar(20),age int(10),name varchar(100),log varchar(10))")
# cursorobject.execute(
# "CREATE table if not exists studentdata(admno int(10),studentname varchar(100),class varchar(20),addresss varchar(200),gender varchar(10),mobile varchar(20),fees varchar(5000))")
cursorobject.execute("SELECT * from login")
fetch = cursorobject.fetchall()
# for check in fetch:
# if check[2] == "loggedin":
# userportal()
# else:
intropage()
database.close()
