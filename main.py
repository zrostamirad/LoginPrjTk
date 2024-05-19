from tkinter import *
import messagebox
from tkinter import ttk
import cls
import os

class App(Frame):
    def __init__(self, screen=None):
        super().__init__(screen)
        self.master = screen
        self.CreateWidget()

    def CreateWidget(self):
        # Frame Register
        self.frmLogin = Frame(self.master, width=270, height=325, highlightbackground="gray", highlightthickness=1)
        self.frmLogin.place(x=15, y=50)
        # Image
        self.img = PhotoImage(file="img/login.png")
        # lables
        Label(self.frmLogin, text="*", image=self.img).place(x=60, y=0)
        Label(self.frmLogin, text="ورود کاربر", font="nazanin 15 bold").place(x=90, y=130)
        Label(self.frmLogin, text=":نام کاربری", anchor="w", width=10).place(x=180, y=180)
        Label(self.frmLogin, text=":کلمه عبور", anchor="w", width=10).place(x=180, y=210)
        # Images
        self.imgsrch = PhotoImage(file="img/srch.png")
        # var string
        self.TxtUserName = StringVar()
        self.TxtPassword = StringVar()
        # Entrys
        self.usernameEntry = Entry(self.frmLogin, justify="center", textvariable=self.TxtUserName)
        self.usernameEntry.place(x=30, y=180)
        self.passwordEntry = Entry(self.frmLogin, justify="center", textvariable=self.TxtPassword).place(x=30, y=210)
        # button Register
        self.btn = Button(self.frmLogin, text="ورود", command=self.clickLogin)
        self.btn.configure(bg="green", fg="white")
        self.btn.place(x=30, y=280)


    # Event

    def clickLogin(self):
        try:
            if not self.TxtUserName.get()  or not self.TxtPassword.get():
                messagebox.showwarning("اخطار", "نام کاربری و کلمه عبور را وارد کنید")
            else:
                user = cls.session.query(cls.userpass).filter_by(username=self.TxtUserName.get(), password=self.TxtPassword.get()).first()
                if user:
                    self.message=" خوش آمدي . به صفحه مدیریت منتقل میشی "+user.user.name +" "+ user.user.family
                    messagebox.showinfo("خوش آمديد", self.message)
                    self.master.destroy()# بستن فايل
                    os.system(f"python Managment.py") #انتقال
                else:
                    messagebox.showwarning("اخطار", "نام کاربری و کلمه عبور یافت نشد")
        except:
            messagebox.showerror("خطا...", "خطاي تعريف نشده، لطفا بعدا سعي كنيد.")



if __name__ == "__main__":
    screen = Tk()
    screen.geometry("%dx%d+%d+%d" % (300, 400, 630, 30))
    screen.resizable=(False,False)
    screen.title("Login")
    pageMe = App(screen)
    screen.mainloop()
    pass
