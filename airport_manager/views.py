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
        self.__heading_2 = tk.Label(self, text="Outgoing Flight ID")
        self.__heading_2.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_3 = tk.Label(self, text="From")
        self.__heading_3.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_4 = tk.Label(self, text="To")
        self.__heading_4.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_5 = tk.Label(self, text="STA")
        self.__heading_5.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_6 = tk.Label(self, text="ETA")
        self.__heading_6.grid(row=0, column=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_7 = tk.Label(self, text="STD")
        self.__heading_7.grid(row=0, column=6, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_8 = tk.Label(self, text="ETD")
        self.__heading_8.grid(row=0, column=7, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_9 = tk.Label(self, text="Check-in counter")
        self.__heading_9.grid(row=0, column=8, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_10 = tk.Label(self, text="Status")
        self.__heading_10.grid(row=0, column=9, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_11 = tk.Label(self, text="Belt status")
        self.__heading_11.grid(row=0, column=10, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_12 = tk.Label(self, text="Gate")
        self.__heading_12.grid(row=0, column=11, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_13 = tk.Label(self, text="Belt")
        self.__heading_13.grid(row=0, column=12, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_14 = tk.Label(self, text="Edit")
        self.__heading_14.grid(row=0, column=13, sticky=tk.N+tk.S+tk.E+tk.W)
        self.__heading_15 = tk.Label(self, text="Delete")
        self.__heading_15.grid(row=0, column=14, sticky=tk.N+tk.S+tk.E+tk.W)


        cur = self.__con.cursor()
        cur.execute("SELECT `id`, `ifid`, `ofid`, `from`, `to`, `sta`, `eta`,"
                    " `std`, `etd`, `checkinctr`, `status`, `beltstatus`, "
                    "`gate`, `belt` FROM `flight`;")

        i = 1

        self.__matrix = []

        for data in cur.fetchall():
            l1 = tk.Label(self, text=data[1])
            l1.grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            l2 = tk.Label(self, text=data[2])
            l2.grid(row=i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

            l3 = tk.Label(self, text=data[3])
            l3.grid(row=i, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

            l4 = tk.Label(self, text=data[4])
            l4.grid(row=i, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
            l5 = tk.Label(self, text=data[5])
            l5.grid(row=i, column=4, sticky=tk.N+tk.S+tk.E+tk.W)

            l6 = tk.Label(self, text=data[6])
            l6.grid(row=i, column=5, sticky=tk.N+tk.S+tk.E+tk.W)
            l7 = tk.Label(self, text=data[7])
            l7.grid(row=i, column=6, sticky=tk.N+tk.S+tk.E+tk.W)
            l8 = tk.Label(self, text=data[8])
            l8.grid(row=i, column=7, sticky=tk.N+tk.S+tk.E+tk.W)

            l9 = tk.Label(self, text=data[9])
            l9.grid(row=i, column=8, sticky=tk.N+tk.S+tk.E+tk.W)
            l10 = tk.Label(self, text=data[10])
            l10.grid(row=i, column=9, sticky=tk.N+tk.S+tk.E+tk.W)
            l11 = tk.Label(self, text=data[11])
            l11.grid(row=i, column=10, sticky=tk.N+tk.S+tk.E+tk.W)

            l12 = tk.Label(self, text=data[12])
            l12.grid(row=i, column=11, sticky=tk.N+tk.S+tk.E+tk.W)
            l13=tk.Label(self,text=data[13])
            l13.grid(row=i, column=12,sticky=tk.N+tk.S+tk.E+tk.W )




            
            def __edit(idd=data[0]):
                    messagebox.showinfo("ID",idd)
                    
            def __delete(idd=data[0]):
                    messagebox.showinfo("ID",idd)
            
            b14 = ttk.Button(self, text="Edit", command=__edit)
            b14.grid(row=i,column=13, sticky=tk.N+tk.S+tk.E+tk.W)
            b15 = ttk.Button(self, text="Delete", command=__delete)
            b15.grid(row=i,column=14, sticky=tk.N+tk.S+tk.E+tk.W)

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
'''
`ifid`, `ofid`, `from`, `to`, `sta`, `eta`,"
                    " `std`, `etd`, `checkinctr`, `status`, `beltstatus`, "
                    "`gate`, `belt` FROM `flight`;")
'''
class EditFlightWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialize parent tk

        self.title("Edit Flight")
        
        self.__ifid_label = tk.Label(self, text="Incoming Flight ID:")
        self.__ifid_label.grid(column = 0, row = 0, sticky = tk.W, padx = 10, pady = 10)

        self.__ifid_entry = ttk.Entry(self)
        self.__ifid_entry.grid(column = 1, row = 0, sticky = tk.E, padx = 10, pady = 10)

        self.__ofid_label = tk.Label(self, text="Outgoing Flight ID:")
        self.__ofid_label.grid(column = 0, row = 1, sticky = tk.W, padx = 10, pady = 10)

        self.__ofid_entry = ttk.Entry(self)
        self.__ofid_entry.grid(column = 1, row = 1, sticky = tk.E, padx = 10, pady = 10)

        self.__from_label = tk.Label(self, text="From:")
        self.__from_label.grid(column = 0, row = 2, sticky = tk.W, padx = 10, pady = 10)

        self.__from_entry = ttk.Entry(self)
        self.__from_entry.grid(column = 1, row = 2, sticky = tk.E, padx = 10, pady = 10)

        self.__to_label = tk.Label(self, text="To:")
        self.__to_label.grid(column = 0, row = 3, sticky = tk.W, padx = 10, pady = 10)

        self.__to_entry = ttk.Entry(self)
        self.__to_entry.grid(column = 1, row = 3, sticky = tk.E, padx = 10, pady = 10)

        self.__sta_label = tk.Label(self, text="STA:")
        self.__sta_label.grid(column = 0, row = 4, sticky = tk.W, padx = 10, pady = 10)

        self.__sta_entry = ttk.Entry(self)
        self.__sta_entry.grid(column = 1, row = 4, sticky = tk.E, padx = 10, pady = 10)

        self.__eta_label = tk.Label(self, text="ETA:")
        self.__eta_label.grid(column = 0, row = 5, sticky = tk.W, padx = 10, pady = 10)

        self.__eta_entry = ttk.Entry(self)
        self.__eta_entry.grid(column = 1, row = 5, sticky = tk.E, padx = 10, pady = 10)

        self.__std_label = tk.Label(self, text="STD:")
        self.__std_label.grid(column = 0, row = 6, sticky = tk.W, padx = 10, pady = 10)

        self.__std_entry = ttk.Entry(self)
        self.__std_entry.grid(column = 1, row = 6, sticky = tk.E, padx = 10, pady = 10)

        self.__etd_label = tk.Label(self, text="ETD:")
        self.__etd_label.grid(column = 0, row = 7, sticky = tk.W, padx = 10, pady = 10)

        self.__etd_entry = ttk.Entry(self)
        self.__etd_entry.grid(column = 1, row = 7, sticky = tk.E, padx = 10, pady = 10)

        self.__checkinctr_label = tk.Label(self, text="Check-in Counter:")
        self.__checkinctr_label.grid(column = 0, row = 8, sticky = tk.W, padx = 10, pady = 10)

        self.__checkinctr_entry = ttk.Entry(self)
        self.__checkinctr_entry.grid(column = 1, row = 8, sticky = tk.E, padx = 10, pady = 10)

        self.__status_label = tk.Label(self, text="Status:")
        self.__status_label.grid(column = 0, row = 9, sticky = tk.W, padx = 10, pady = 10)

        self.__status_entry = ttk.Entry(self)
        self.__status_entry.grid(column = 1, row = 9, sticky = tk.E, padx = 10, pady = 10)

        self.__beltstatus_label = tk.Label(self, text="Belt status:")
        self.__beltstatus_label.grid(column = 0, row = 10, sticky = tk.W, padx = 10, pady = 10)

        self.__beltstatus_entry = ttk.Entry(self)
        self.__beltstatus_entry.grid(column = 1, row = 10, sticky = tk.E, padx = 10, pady = 10)

        self.__gate_label = tk.Label(self, text="Gate:")
        self.__gate_label.grid(column = 0, row = 11, sticky = tk.W, padx = 10, pady = 10)

        self.__gate_entry = ttk.Entry(self)
        self.__gate_entry.grid(column = 1, row = 11, sticky = tk.E, padx = 10, pady = 10)

        self.__belt_label = tk.Label(self, text="Belt:")
        self.__belt_label.grid(column = 0, row = 12, sticky = tk.W, padx = 10, pady = 10)

        self.__belt_entry = ttk.Entry(self)
        self.__belt_entry.grid(column = 1, row = 12, sticky = tk.E, padx = 10, pady = 10)

if __name__ == "__main__":
    root = EditFlightWindow()
    root.mainloop()
