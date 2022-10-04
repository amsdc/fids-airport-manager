import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import pymysql
from pymysql.err import OperationalError

class DataFrame(tk.Frame):
    def __init__(self, parent, con, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) # initialize parent tk

        self.__con = con

        # Table adding
        self.__heading_1 = tk.Label(self, text="Incoming Flight ID")
        self.__heading_1.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_1 = tk.Label(self, text="Outgoing Flight ID")
        self.__heading_1.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_1 = tk.Label(self, text="Password")
        self.__heading_1.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_1 = tk.Label(self, text="Button")
        self.__heading_1.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

        cur = self.__con.cursor()
        cur.execute("SELECT `id`, `ifid`, `ofid`, `from`, `to`, `sta`, `eta`,"
                    " `std`, `etd`, `checkinctr`, `status`, `beltstatus`, "
                    "`gate`, `belt` FROM `flight`;")

        i = 1

        self.__matrix = []

        for data in cur.fetchall():
            l1 = tk.Label(self, text=data[0])
            l1.grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            l2 = tk.Label(self, text=data[1])
            l2.grid(row=i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

            l3 = tk.Label(self, text=data[2])
            l3.grid(row=i, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

            
            def callback(plugin=data[3]):
                if plugin:
                    messagebox.showinfo("Yes", "Plugin present "+data[3])
                else:
                    print("no")
            
            b4 = ttk.Button(self, text="Show plugin", command=callback)
            b4.grid(row=i,column=3, sticky=tk.N+tk.S+tk.E+tk.W)

            i += 1

        

        
        cur.close()



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

        self.__dframe = DataFrame(self, self.__con)
        self.__dframe.grid(row=1, column=0)
        
        '''
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
            l1 = tk.Label(self, text=data[0])
            l1.grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            l2 = tk.Label(self, text=data[1])
            l2.grid(row=i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

            l3 = tk.Label(self, text=data[2])
            l3.grid(row=i, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

            
            def callback(plugin=data[3]):
                if plugin:
                    messagebox.showinfo("Yes", "Plugin present "+data[3])
                else:
                    print("no")
            
            b4 = ttk.Button(self, text="Show plugin", command=callback)
            b4.grid(row=i,column=3, sticky=tk.N+tk.S+tk.E+tk.W)

            i += 1

        

        
        cur.close()
        '''

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
        self.__username_label = tk.Label(self, text="Username:")
        self.__username_label.grid(column = 0, row = 0, sticky = tk.W, padx = 10, pady = 10)

        self.__username_entry = ttk.Entry(self)
        self.__username_entry.grid(column = 1, row = 0, sticky = tk.E, padx = 10, pady = 10)

        # password
        self.__password_label = tk.Label(self, text="Password:")
        self.__password_label.grid(column = 0, row = 1, sticky = tk.W, padx = 10, pady = 5)

        self.__password_entry = ttk.Entry(self, show = "*")
        self.__password_entry.grid(column = 1, row = 1, sticky = tk.E, padx = 10, pady = 5)

        # database
        self.__db_label = tk.Label(self, text="Database:")
        self.__db_label.grid(column = 0, row = 2, sticky = tk.W, padx = 10, pady = 10)

        self.__db_entry = ttk.Entry(self)
        self.__db_entry.grid(column = 1, row = 2, sticky = tk.E, padx = 10, pady = 10)

        # login button
        self.__login_button = ttk.Button(self, text="Login", command=self.__login)
        self.__login_button.grid(column = 1, row = 3, sticky = tk.S, padx = 5, pady = 5)

    def __login(self):
        try:
            u = self.__username_entry.get()
            p = self.__password_entry.get()
            d = self.__db_entry.get()
            con = pymysql.connect(host="localhost",
                                  user=u,
                                  password=p,
                                  database=d)
        except OperationalError as e:
            messagebox.showerror("OperationalError", str(e))
        else:
            HomeScreen(con)
            
            self.destroy()
            

if __name__ == "__main__":
    root = LoginWindow()
    root.mainloop()
