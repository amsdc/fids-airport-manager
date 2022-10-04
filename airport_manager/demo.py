import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

import pymysql
from pymysql.err import OperationalError



class DataFrame(tk.Frame,):
    def __init__(self, parent, con, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) # initialize parent tk

        self.__con = con
        self._parent = parent
        self._data = data
        

        # Table adding
        self.__heading_2 = tk.Label(self, text="Flight No", font=("Adani Regular", 20, "bold"), fg="#ffffff", bg="#800000")
        self.__heading_2.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_4 = tk.Label(self, text="To", font=("Adani Regular", 20, "bold"), fg="#ffffff", bg="#800000")
        self.__heading_4.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_7 = tk.Label(self, text="STD", font=("Adani Regular", 20, "bold"), fg="#ffffff", bg="#800000")
        self.__heading_7.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_8 = tk.Label(self, text="ETD", font=("Adani Regular", 20, "bold"), fg="#ffffff", bg="#800000")
        self.__heading_8.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_9 = tk.Label(self, text="Check-in counter", font=("Adani Regular", 20, "bold"), fg="#ffffff", bg="#800000")
        self.__heading_9.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_10 = tk.Label(self, text="Status", font=("Adani Regular", 20, "bold"), fg="#ffffff", bg="#800000")
        self.__heading_10.grid(row=0, column=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_12 = tk.Label(self, text="Gate", font=("Adani Regular", 20, "bold"), fg="#ffffff", bg="#800000")
        self.__heading_12.grid(row=0, column=6, sticky=tk.N+tk.S+tk.E+tk.W)
        
        for i in range(7):
            tk.Grid.columnconfigure(self, i, weight=1)


        cur = self.__con.cursor()
        cur.execute("SELECT `ofid`, `to`, "
                    " `std`, `etd`, `checkinctr`, `status`, "
                    "`gate`FROM `flight`;")

        i = 1

        self.__matrix = []

        for data in cur.fetchall():
            l1 = tk.Label(self, text=data[0], font=("Comic Sans", 15, "bold"), fg="#ffffff", bg="#000066")
            l1.grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            print(self._data.get(data[1], data[1]), data[1])
            l2 = tk.Label(self, text=self._data.get(data[1], data[1]), font=("Comic Sans", 15, "bold"), fg="#ffffff", bg="#000066")
            l2.grid(row=i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

            l3 = tk.Label(self, text=data[2], font=("Comic Sans", 15, "bold"), fg="#ffffff", bg="#000066")
            l3.grid(row=i, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

            l4 = tk.Label(self, text=data[3], font=("Comic Sans", 15, "bold"), fg="#ffffff", bg="#000066")
            l4.grid(row=i, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
            l5 = tk.Label(self, text=data[4], font=("Comic Sans", 15, "bold"), fg="#ffffff", bg="#000066")
            l5.grid(row=i, column=4, sticky=tk.N+tk.S+tk.E+tk.W)

            l6 = tk.Label(self, text=data[5], font=("Comic Sans", 15, "bold"), fg="#ffffff", bg="#000066")
            l6.grid(row=i, column=5, sticky=tk.N+tk.S+tk.E+tk.W)
            l7 = tk.Label(self, text=data[6], font=("Comic Sans", 15, "bold"), fg="#ffffff", bg="#000066")
            l7.grid(row=i, column=6, sticky=tk.N+tk.S+tk.E+tk.W)

            i += 1

        

        
        cur.close()

class HomeScreen(tk.Tk):
    def __init__(self, con, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialize parent tk
        
        self.configure(bg="#000066")

        self.title("User home")
        self.attributes("-fullscreen", True) 
        
        self.__con = con

        self.__logout_btn = tk.Label(self, text="DEPARTURES", font=("Adani Regular", 40, "bold"), fg="#ffffff", bg="#800000")
        self.__logout_btn.grid(row=0, column=0, sticky=tk.E+tk.W)
        
        with open('op.json', 'r') as f1:
            self._data = json.load(f1)

        self.__dframe = DataFrame(self, self.__con, self._data)
        self.__dframe.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self._refresh_table()
        
        tk.Grid.columnconfigure(self, 0, weight=1)
        
    def _refresh_table(self):
        self.__dframe.destroy()
        self.__dframe = DataFrame(self, self.__con, self._data)
        self.__dframe.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.after(5000, self._refresh_table)


class LoginWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialize parent tk

        self.title("User sign in")
        
        # host
        self.__host_label = tk.Label(self, text="Host:")
        self.__host_label.grid(column = 0, row = 0, sticky = tk.W, padx = 10, pady = 10)

        self.__host_entry = ttk.Entry(self)
        self.__host_entry.grid(column = 1, row = 0, sticky = tk.E, padx = 10, pady = 10)
        
        # username
        self.__username_label = tk.Label(self, text="Username:")
        self.__username_label.grid(column = 0, row = 1, sticky = tk.W, padx = 10, pady = 10)

        self.__username_entry = ttk.Entry(self)
        self.__username_entry.grid(column = 1, row = 1, sticky = tk.E, padx = 10, pady = 10)

        # password
        self.__password_label = tk.Label(self, text="Password:")
        self.__password_label.grid(column = 0, row = 2, sticky = tk.W, padx = 10, pady = 5)

        self.__password_entry = ttk.Entry(self, show = "*")
        self.__password_entry.grid(column = 1, row = 2, sticky = tk.E, padx = 10, pady = 5)

        # database
        self.__db_label = tk.Label(self, text="Database:")
        self.__db_label.grid(column = 0, row = 3, sticky = tk.W, padx = 10, pady = 10)

        self.__db_entry = ttk.Entry(self)
        self.__db_entry.grid(column = 1, row = 3, sticky = tk.E, padx = 10, pady = 10)

        # login button
        self.__login_button = ttk.Button(self, text="Login", command=self.__login)
        self.__login_button.grid(column = 1, row = 4, sticky = tk.S, padx = 5, pady = 5)

    def __login(self):
        try:
            h = self.__host_entry.get()
            u = self.__username_entry.get()
            p = self.__password_entry.get()
            d = self.__db_entry.get()
            con = pymysql.connect(host=h,
                                  user=u,
                                  password=p,
                                  database=d)
            con.autocommit(True)
        except OperationalError as e:
            messagebox.showerror(str(type(e)), str(e))
        else:
            HomeScreen(con)
            
            self.destroy()

if __name__ == "__main__":
    root = LoginWindow()
    root.mainloop()