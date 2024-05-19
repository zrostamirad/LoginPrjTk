from tkinter import *
from tkinter import ttk, messagebox
import cls
from sqlalchemy import or_
import os


class App(Frame):
    def __init__(self, screen=None):
        super().__init__(screen)
        self.master = screen
        self.CreateWidget()

    def CreateWidget(self):
        # Frame Register
        self.frmRegister = Frame(self.master, width=270, height=425, highlightbackground="gray", highlightthickness=1)
        self.frmRegister.place(x=520, y=50)

        # lables
        Label(self.frmRegister, text="فرم ثبت کاربر", font="nazanin 15 bold").place(x=90, y=0)
        Label(self.frmRegister, text=":نام", anchor="w", width=10).place(x=180, y=60)
        Label(self.frmRegister, text=":نام خانوادگی", anchor="w", width=10).place(x=180, y=90)
        Label(self.frmRegister, text=":تاریخ تولد", anchor="w", width=10).place(x=180, y=120)
        Label(self.frmRegister, text=":جنسیت", anchor="w", width=10).place(x=180, y=150)

        # Images
        self.imgsrch = PhotoImage(file="img/srch.png")
        self.imgclose = PhotoImage(file="img/close.png")
        self.imgexit = PhotoImage(file="img/exit.png")

        # var string
        self.varName = StringVar()
        self.varFamily = StringVar()
        self.varAge = StringVar()
        self.varSearch = StringVar()
        self.varSex = IntVar()
        self.varIsAdmin = BooleanVar()

        # Entrys
        self.txtname = Entry(self.frmRegister, justify="center", textvariable=self.varName)
        self.txtname.place(x=30, y=60)
        self.txtfamily = Entry(self.frmRegister, justify="center", textvariable=self.varFamily).place(x=30, y=90)

        # Combobox
        self.comboage = ttk.Combobox(self.frmRegister, state="readonly", textvariable=self.varAge, justify="right")
        self.comboage["values"] = self.GetComboVal()
        self.comboage.current(40)
        self.comboage.place(x=30, y=120)

        # RadioButton
        self.radio1 = Radiobutton(self.frmRegister, text="زن", variable=self.varSex, value=1).place(x=80, y=150)
        self.radio2 = Radiobutton(self.frmRegister, text="مرد", variable=self.varSex, value=0).place(x=30, y=150)

        # Checkbox
        self.chk1 = Checkbutton(self.frmRegister, text="آیا ادمین شود؟", variable=self.varIsAdmin,
                                command=self.ToggleUserPassFrame)
        self.chk1.place(x=30, y=200)

        # buttons
        # button Register
        self.btnRegister = Button(self.frmRegister, text="ثبت نام", command=self.ClickReg)
        self.btnRegister.configure(bg="green", fg="white")
        self.btnRegister.place(x=30, y=370)
        # button Cancel
        self.btnCancel = Button(self.frmRegister, bg="gray", text="كنسل", command=self.ClickCancel)
        self.btnCancel.configure(fg="white")
        self.btnCancel.place_forget()
        # button Delete
        self.btnDelete = Button(self.frmRegister, text="حذف", command=self.ClickDelete)
        self.btnDelete.configure(bg="red", fg="white")
        self.btnDelete.place_forget()
        # button Edit
        self.btnEdit = Button(self.frmRegister, text="ویرایش", command=self.ClickEdit)
        self.btnEdit.configure(bg="#5887fc", fg="white")
        self.btnEdit.place_forget()
        # button Show Search
        self.btnShowSearch = Button(screen, text="*", command=self.ClickShowSearch, image=self.imgsrch)
        self.btnShowSearch.configure(width=25, height=25)
        self.btnShowSearch.place(x=475, y=20)

        # tbl
        self.tbl = ttk.Treeview(self.master, columns=("c1", "c2", "c3", "c4", "c5"), show="headings", height=20)
        self.tbl.column("# 5", width=100, anchor=E)
        self.tbl.heading("# 5", text="نام")
        self.tbl.column("# 4", width=100, anchor=E)
        self.tbl.heading("# 4", text="نام خانوادگی")
        self.tbl.column("# 3", width=100, anchor=E)
        self.tbl.heading("# 3", text="تاریخ تولد")
        self.tbl.column("# 2", width=100, anchor=E)
        self.tbl.heading("# 2", text="جنسیت")
        self.tbl.column("# 1", width=100, anchor=E)
        self.tbl.heading("# 1", text="نقش کاربر")
        self.tbl.bind("<Button-1>", self.GetSelection)
        self.tbl.place(x=5, y=50)
        self.LoadTable(self.QueryAll())

        # Frame UserPass
        self.varUsername = StringVar()
        self.varPassword = StringVar()
        self.frmUserPass = Frame(self.frmRegister, width=240, height=95)
        self.frmUserPass.place_forget()
        Label(self.frmUserPass, text=":لطفا نام کاربری و پسورد را وارد کنید", anchor="w", width=25).place(x=50, y=0)
        Label(self.frmUserPass, text=":نام کاربری", anchor="w", width=10).place(x=170, y=30)
        Label(self.frmUserPass, text=":کلمه عبور", anchor="w", width=10).place(x=170, y=60)
        self.txtusername = Entry(self.frmUserPass, justify="center", textvariable=self.varUsername)
        self.txtusername.place(x=30, y=30)
        self.txtpassword = Entry(self.frmUserPass, justify="center", textvariable=self.varPassword).place(x=30, y=60)

        # Frame Search
        self.frmSearch = Frame(self.master, width=500, height=40)
        self.frmSearch.place_forget()
        Label(self.frmSearch, text=":مقدار جستجو", anchor="w", width=10).place(x=380, y=10)
        self.txtsearch = Entry(self.frmSearch, justify="center", width=49, textvariable=self.varSearch).place(x=75,
                                                                                                              y=10)
        self.btnsearch = Button(self.frmSearch, text="جستجو", command=self.Search)
        self.btnsearch.configure(height=1, width=8)
        self.btnsearch.place(x=0, y=8)
        self.btnclosefrm = Button(self.frmSearch, text="*", image=self.imgclose, width=18, height=18,
                                  command=self.ClickCloseSearch)
        self.btnclosefrm.place(x=479, y=8)
        self.btnexit=Button(self.master,text="*",image=self.imgexit, command=self.Exit)
        self.btnexit.place(x=750,y=12)

    #Event
    def GetComboVal(self):
        count = []
        for i in range(1340, 1400):
            count.append(i)
        return count

    def GetIndexAge(self, x):
        count = []
        for i in range(1340, 1400):
            count.append(i)
        return (count.index(x))

    def ToggleUserPassFrame(self):
        if self.varIsAdmin.get() == 1:
            self.frmUserPass.place(x=0, y=250)
        else:
            self.frmUserPass.place_forget()

    def ClickReg(self):
        self.query = []
        print(":2" + str(self.query))
        repos = cls.Repository()
        if self.varSex.get() == 0:
            self.gender = False
        else:
            self.gender = True

        self.query = (cls.session.query(cls.user).filter(cls.user.family == self.varFamily.get(),
                                                         cls.user.name == self.varName.get(),
                                                         cls.user.age == self.varAge.get(),
                                                         cls.user.sex == self.gender)
                      .first())
        if self.query:
            messagebox.showwarning("خطا...", "اين كاربر قبلا ثبت نام شده است.")
            return

        if self.varIsAdmin.get() == True:
            print(f"Family: '{self.varFamily.get()}'")
            print(f"Name: '{self.varName.get()}'")
            print(f"Username: '{self.varUsername.get()}'")
            print(f"Password: '{self.varPassword.get()}'")

            if ((self.varFamily.get() == '') or (self.varName.get() == '') or (self.varUsername.get() == '')
                    or (self.varPassword.get() == '')):
                messagebox.showwarning("خطا...", "همه فيلد ها را پر كن")
                print("x")
            else:
                self.users = cls.user(name=self.varName.get(), family=self.varFamily.get(), age=self.varAge.get(),
                                      sex=self.gender, is_admin=self.varIsAdmin.get())
                self.queryusername = cls.session.query(cls.userpass).filter(
                    cls.userpass.username == self.varUsername.get()).first()
                if self.queryusername:
                    messagebox.showwarning("خطا...", "نام کاربری تکراری است.")
                else:
                    repos.Insert(self.users)
                    self.admininfo = cls.userpass(username=self.varUsername.get(), password=self.varPassword.get(),
                                                  userid=self.users.id)
                    repos.Insert(self.admininfo)
                    self.varPassword.set("")
                    self.varUsername.set("")
                    messagebox.showinfo("ok...", "کاربر مورد نظر ثبت شد")

        else:
            if len(self.varFamily.get()) != 0 and len(self.varName.get()) != 0:
                self.users = cls.user(name=self.varName.get(), family=self.varFamily.get(), age=self.varAge.get(),
                                      sex=self.gender, is_admin=self.varIsAdmin.get())
                repos.Insert(self.users)
            else:
                messagebox.showwarning("خطا...", "تمام فیلد ها را تکمیل کنید")
        self.ClearTable()
        self.LoadTable(self.QueryAll())
        self.varName.set("")
        self.varFamily.set("")

    def QueryAll(self):
        self.query = cls.session.query(cls.user).order_by(cls.user.id.desc()).all()
        return self.query

    def LoadTable(self, list):
        for self.item in list:
            if self.item.sex == True:
                self.gender = "زن"
            else:
                self.gender = "مرد"
            self.admin = "مدیر" if self.item.is_admin else ""
            self.tbl.insert('', "end",
                            values=[self.admin, self.gender, self.item.age, self.item.family, self.item.name])

    def ClearTable(self):
        for item in self.tbl.get_children():
            sel = (str(item),)
            self.tbl.delete(sel)

    def ClearForm(self):
        list = [self.varName, self.varFamily, self.varUsername, self.varPassword]
        for item in list:
            item.set("")
        self.varIsAdmin.set(False)
        self.varSex.set(0)
        self.comboage.current(40)
        self.frmUserPass.place_forget()

    def GetSelectRow(self):
        self.selectionrow = self.tbl.selection()
        if self.selectionrow != ():
            if self.tbl.item(self.selectionrow)["values"][1] == "مرد":
                self.gender = False
            else:
                self.gender = True
            self.record = cls.session.query(cls.user).filter(
                cls.user.name == self.tbl.item(self.selectionrow)["values"][4],
                cls.user.family == self.tbl.item(self.selectionrow)["values"][3],
                cls.user.age == self.tbl.item(self.selectionrow)["values"][2],
                cls.user.sex == self.gender
            ).first()
            return self.record

    def GetSelection(self, e):
        self.record = self.GetSelectRow()
        if self.record != None:
            self.btnEdit.place(x=150, y=370)
            self.btnDelete.place(x=90, y=370)
            self.btnRegister.place_forget()
            self.btnCancel.place(x=30, y=370)
            self.varName.set(self.record.name)
            self.varFamily.set(self.record.family)
            self.comboage.current(self.GetIndexAge(self.record.age))
            if self.record.sex == True:
                self.varSex.set(1)
            else:
                self.varSex.set(0)
            if self.record.is_admin == True:
                self.varIsAdmin.set(True)
                self.frmUserPass.place(x=0, y=250)
                querypass = cls.session.query(cls.userpass).filter(cls.userpass.user_id == self.record.id).first()
                if querypass:
                    self.varUsername.set(querypass.username)
                    self.varPassword.set(querypass.password)
                else:
                    self.varUsername.set("")
                    self.varPassword.set("")
            else:
                self.varIsAdmin.set(False)
                self.frmUserPass.place_forget()

    def ClickCancel(self):
        self.btnEdit.place_forget()
        self.btnDelete.place_forget()
        self.btnCancel.place_forget()
        self.btnRegister.place(x=30, y=370)
        self.ClearForm()

    def ClickDelete(self):
        if self.varName.get() != "":
            result = messagebox.askquestion("هشدار", "آیا مطمئن هستید که میخواهید حذف کنید؟")
            if result == "yes":
                self.record = self.GetSelectRow()
                self.Delete(self.record)

    def Delete(self, rec):
        print("hi del")
        repos = cls.Repository()
        self.query = cls.session.query(cls.userpass).filter(cls.userpass.user_id == rec.id).first()
        if self.query:
            repos.Delete(cls.userpass, self.query.id)
        repos.Delete(cls.user, rec.id)
        self.ClearTable()
        self.LoadTable(self.QueryAll())
        self.ClickCancel()

    def ClickEdit(self):
        self.record = self.GetSelectRow()
        if not self.record:
            messagebox.showerror("خطا...", "هیچ رکوردی انتخاب نشده است.")
            return
        repos = cls.Repository()
        a = repos.Update(cls.user, self.record.id, name=self.varName.get(),
                         family=self.varFamily.get(),
                         age=self.varAge.get(),
                         sex=self.varSex.get(),
                         is_admin=self.varIsAdmin.get())
        if self.record.is_admin == True:
            if ((self.varUsername.get() == '') or (self.varPassword.get() == '')):
                messagebox.showwarning("خطا...", "نام كاربري و كلمه عبور را وارد كن")
            else:
                self.query = cls.session.query(cls.userpass).filter(cls.userpass.user_id == self.record.id).first()
                if self.query:
                    self.queryusername = cls.session.query(cls.userpass).filter(
                        cls.userpass.username == self.varUsername.get()).all()
                    if len(self.queryusername) == 1:
                        if self.queryusername[0].user_id == self.query.user_id:
                            b = repos.Update(cls.userpass, self.query.id, username=self.varUsername.get(),
                                             password=self.varPassword.get())
                            self.ClearTable()
                            self.LoadTable(self.QueryAll())
                            self.ClickCancel()
                        else:
                            messagebox.showwarning("خطا...", "نام کاربری تکراری است.")
                    elif len(self.queryusername) > 1:
                        messagebox.showwarning("خطا...", "نام کاربری تکراری است.")
                    else:
                        b = repos.Update(cls.userpass, self.query.id, username=self.varUsername.get(),
                                         password=self.varPassword.get())
                        self.ClearTable()
                        self.LoadTable(self.QueryAll())
                        self.ClickCancel()
                else:
                    self.queryusername = cls.session.query(cls.userpass).filter(
                        cls.userpass.username == self.varUsername.get()).first()
                    if self.queryusername:
                        messagebox.showwarning("خطا...", "نام کاربری تکراری است.")
                    else:
                        repos.Insert(cls.userpass(username=self.varUsername.get(), password=self.varPassword.get(),
                                                  userid=self.record.id))
                        self.ClearTable()
                        self.LoadTable(self.QueryAll())
                        self.ClickCancel()
        else:
            self.varUsername.set("")
            self.varPassword.set("")
            self.query = cls.session.query(cls.userpass).filter(cls.userpass.user_id == self.record.id).first()
            print(self.query.id)
            repos.Delete(cls.userpass, self.query.id)
            self.ClearTable()
            self.LoadTable(self.QueryAll())
            self.ClickCancel()

    def ClickShowSearch(self):
        self.frmSearch.place(x=5, y=10)
        self.btnShowSearch.place_forget()

    def ClickCloseSearch(self):
        self.frmSearch.place_forget()
        self.btnShowSearch.place(x=475, y=20)
        self.ClearTable()
        self.LoadTable(self.QueryAll())

    def Search(self):
        q = self.varSearch.get()
        if q != "":
            if q == "زن":
                qs = True
            elif q == "مرد":
                qs = False
            else:
                qs = None
            if q == "مدير":
                qr = True
            else:
                qr = None

            result = cls.session.query(cls.user).filter(or_(  #تابع or بايداول ايمپورت شه
                cls.user.name.contains(q),
                cls.user.family.contains(q),
                cls.user.age.contains(q),
                cls.user.sex == qs,
                cls.user.is_admin == qr
            )).all()
            self.ClearTable()
            self.LoadTable(result)
        else:
            self.ClearTable()
            self.LoadTable(self.QueryAll())

    def Exit(self):
        messagebox.showinfo("", "خدانگهدار")
        self.master.destroy()  # بستن فايل
        os.system(f"python main.py")  # انتقال

if __name__ == "__main__":
    screen = Tk()
    screen.geometry("%dx%d+%d+%d" % (800, 500, 350, 30))
    screen.resizable=(False,False)
    screen.title("User Managment")
    pageMe = App(screen)
    screen.mainloop()
    pass
