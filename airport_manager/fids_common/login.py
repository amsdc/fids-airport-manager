import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


import pymysql
import keyring

import fids_common.settings as settings

PWDSTORE_SERVICE_NAME = "AKNP_FIDS_MySQL_DBUser"
USERSTORE_SERVICE_NAME = "AKNP_FIDS_Prefs"


def login(parent=None):
    if settings.get("auth", "autologin") and keyring.get_password(PWDSTORE_SERVICE_NAME, settings.get("auth", "user")):
        pwd = keyring.get_password(PWDSTORE_SERVICE_NAME, settings.get("auth", "user"))
        con = pymysql.connect(
            host=settings.get("auth", "host"),
            user=settings.get("auth", "user"),
            password=pwd,
            database=settings.get("auth", "database"),
        )
    else:
        frm = LoginWindow()
        """
        if parent:
            parent.wait_window(frm)
        else:
        """
        frm.mainloop()

        l = frm.creds
        con = pymysql.connect(host=l[0], user=l[1], password=l[2], database=l[3])
        settings.set("auth", "host", l[0])
        settings.set("auth", "user", l[1])
        keyring.set_password(PWDSTORE_SERVICE_NAME, l[1], l[2])
        settings.set("auth", "database", l[3])
        settings.set("auth", "autologin", True)
    con.autocommit(True)
    return con


class LoginWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize parent tk

        self.title("User Sign In")
        self.attributes("-topmost", True)

        # host
        self.__host_label = tk.Label(self, text="Host:")
        self.__host_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

        self.__host_entry = ttk.Entry(self)
        self.__host_entry.grid(column=1, row=0, sticky=tk.E, padx=10, pady=10)

        # username
        self.__username_label = tk.Label(self, text="Username:")
        self.__username_label.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.__username_entry = ttk.Entry(self)
        self.__username_entry.grid(column=1, row=1, sticky=tk.E, padx=10, pady=10)

        # password
        self.__password_label = tk.Label(self, text="Password:")
        self.__password_label.grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)

        self.__password_entry = ttk.Entry(self, show="*")
        self.__password_entry.grid(column=1, row=2, sticky=tk.E, padx=10, pady=5)

        # database
        self.__db_label = tk.Label(self, text="Database:")
        self.__db_label.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

        self.__db_entry = ttk.Entry(self)
        self.__db_entry.grid(column=1, row=3, sticky=tk.E, padx=10, pady=10)

        # login button
        self.__login_button = ttk.Button(self, text="Login", command=self.__login)
        self.__login_button.grid(column=1, row=4, sticky=tk.S, padx=5, pady=5)

    def __login(self):
        try:
            h = self.__host_entry.get()
            u = self.__username_entry.get()
            p = self.__password_entry.get()
            d = self.__db_entry.get()
            con = pymysql.connect(host=h, user=u, password=p, database=d)
            con.autocommit(True)
        except pymysql.err.OperationalError as e:
            messagebox.showerror(str(type(e)), str(e))
        else:
            con.close()
            self.creds = (h, u, p, d)
            self.destroy()
            self.quit()
