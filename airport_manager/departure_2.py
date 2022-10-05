import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import datetime

import pymysql
from pymysql.err import OperationalError, Error as PYMErr, InterfaceError

STYLE = dict(
    title=dict(font=("Calibri", 60, "bold"), fg="#ffffff", bg="#666699"),
    time=dict(font=("Consolas", 40, "bold"), fg="#ffffff", bg="#666699"),
    header=dict(font=("Calibri", 40, "bold"), fg="#ffffff", bg="#666699"),
    body=dict(font=("Calibri", 35, "bold"), fg="#ffffff", bg="#000066"),
    body2=dict(font=("Calibri", 35, "bold"), fg="#ffffff", bg="#0066ff"),
    err=dict(font=("Calibri", 60, "bold"), fg="#ff0000", bg="#000066")
)

class DataFrame(tk.Frame,):
    def __init__(self, parent, con, data, style, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) # initialize parent tk
        
       
        self.__con = con
        self._parent = parent
        self._data = data
        self._style = style
        
        self["bg"] = self._style["body"]["bg"]

        
        

        try:
            cur = self.__con.cursor()
            cur.execute("SELECT `etd`, `ofid`, `to`, `gate`, `status` "
                        "FROM `flight` WHERE "
                        "`etd`BETWEEN NOW() AND NOW() + INTERVAL 1 DAY"
                        " ORDER BY `etd` ASC;")
        except OperationalError as e:
            lbl = tk.Label(self, text=("Failed to update data\n"
                                       "Sorry for inconvinience"), **self._style["err"])
            lbl.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            tk.Grid.columnconfigure(self, 0, weight=1)
        except InterfaceError as e:
            lbl = tk.Label(self, text=("Cannot update data\n"
                                       "Please restart application"), **self._style["err"])
            lbl.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            rst = tk.Button(self, text="Restart", command=exit, font=("Adani Regular", 40, "bold"))
            rst.grid(row=1, column=0, sticky=tk.N+tk.S)
            tk.Grid.columnconfigure(self, 0, weight=1)
        else:
            # Table adding
            self.__heading_1 = tk.Label(self, text="ETD", **self._style["header"])
            self.__heading_1.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            self.__heading_2 = tk.Label(self, text="Flight No.", **self._style["header"])
            self.__heading_2.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
            self.__heading_3 = tk.Label(self, text="Destination", **self._style["header"])
            self.__heading_3.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
            self.__heading_4 = tk.Label(self, text="Gate", **self._style["header"])
            self.__heading_4.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
            self.__heading_5 = tk.Label(self, text="Status", **self._style["header"])
            self.__heading_5.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W)

            i = 1
            
            for i in range(5):
                tk.Grid.columnconfigure(self, i, weight=1)

            # self.__matrix = []

            for data in cur.fetchall():
                if i % 2 == 1:
                    style = self._style["body"]
                else:
                    style = self._style["body2"]
                
                l1 = tk.Label(self, text=data[0].strftime("%H:%M"), **self._style["body"])
                l1.grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

                l2 = tk.Label(self, text=data[1], **self._style["body"])
                l2.grid(row=i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

                l3 = tk.Label(self, text=self._data.get(data[2], data[2]), **self._style["body"])
                l3.grid(row=i, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

                l4 = tk.Label(self, text=data[3], **self._style["body"])
                l4.grid(row=i, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

                l5 = tk.Label(self, text=data[4], **self._style["body"])
                l5.grid(row=i, column=4, sticky=tk.N+tk.S+tk.E+tk.W)

                i += 1

        finally:
            cur.close()


class HomeScreen(tk.Tk):
    def __init__(self, con, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialize parent tk
        
        self.configure(bg="#000066")

        self.title("User home")
        self.attributes("-fullscreen", False) 
        
        self.__con = con

        self.__logout_btn = tk.Label(self, text="DEPARTURES", **STYLE["title"])
        self.__logout_btn.grid(row=0, column=0, sticky=tk.E+tk.W)
        
        self._timelbl = tk.Label(self, text="...", **STYLE["time"])
        self._timelbl.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        
        with open('op.json', 'r') as f1:
            self._data = json.load(f1)

        self.__dframe = tk.Label(self, text="...")
        self.__dframe.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self._refresh_table()
        self._showdt()
        
        tk.Grid.columnconfigure(self, 0, weight=1)
        # tk.Grid.columnconfigure(self, 1, weight=1)
        
    def _refresh_table(self):
        self.__dframe.destroy()
        self.__dframe = DataFrame(self, self.__con, self._data, STYLE)
        self.__dframe.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.after(5000, self._refresh_table)
        
    def _showdt(self):
        dt = datetime.datetime.now().strftime("%c")
        self._timelbl["text"] = dt
        self.after(1000, self._showdt)


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