import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import pymysql
from pymysql.err import OperationalError


class HomeScreen(tk.Tk):
    def __init__(self, con, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialize parent tk

        self.title("User home")
        self.__con = con

        self.__logout_btn = ttk.Button(self, text="Login", command=self.__print)
        self.__logout_btn.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.__menu = tk.Menu(self)
        self.__user_menu = tk.Menu(self.__menu, tearoff=0)
        self.__user_menu.add_command(label="Logout", command=self.__logout)
        self.__menu.add_cascade(label="User", menu=self.__user_menu)
        
        self.config(menu=self.__menu)

        

        # Table adding
        self.__heading_1 = tk.Label(self, text="Host")
        self.__heading_1.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_1 = tk.Label(self, text="User")
        self.__heading_1.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_1 = tk.Label(self, text="Password")
        self.__heading_1.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_1 = tk.Label(self, text="Button")
        self.__heading_1.grid(row=1, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

        cur = self.__con.cursor()
        cur.execute("select host, user, password, plugin from user")

        i = 2

        self.__matrix = []

        for data in cur.fetchall():
            self.__matrix.append([])
            l1 = tk.Label(self, text=data[0])
            l1.grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            self.__matrix[-1].append(l1)
            l2 = tk.Label(self, text=data[1])
            l2.grid(row=i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
            self.__matrix[-1].append(l2)
            l3 = tk.Label(self, text=data[2])
            l3.grid(row=i, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
            self.__matrix[-1].append(l3)
            
            
            
            b4 = ttk.Button(self, text="Show plugin"+data[3], command=lambda: print(data[3]))
            b4.grid(row=i,column=3)
            i += 1

        

        
        cur.close()
        

    def __logout(self):
        self.__con.close()
        self.destroy()

    def __print(self):
        print("Hii")

    def __msgbox(self, plug):
        print("The user has", plug)

class LoginWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialize parent tk

        self.title("User sign in")
        
        # username
        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.grid(column = 0, row = 0, sticky = tk.W, padx = 10, pady = 10)

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column = 1, row = 0, sticky = tk.E, padx = 10, pady = 10)

        # password
        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(column = 0, row = 1, sticky = tk.W, padx = 10, pady = 5)

        self.password_entry = ttk.Entry(self, show = "*")
        self.password_entry.grid(column = 1, row = 1, sticky = tk.E, padx = 10, pady = 5)

        # login button
        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.grid(column = 1, row = 3, sticky = tk.S, padx = 5, pady = 5)

    def login(self):
        try:
            u = self.username_entry.get()
            p = self.password_entry.get()
            con = pymysql.connect(host="localhost",
                                  user=u,
                                  password=p,
                                  database="mysql")
        except OperationalError as e:
            messagebox.showerror("OperationalError", str(e))
        else:
            HomeScreen(con)
            
            self.destroy()
            

if __name__ == "__main__":
    root = LoginWindow()
    root.mainloop()
