import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import datetime

import pymysql
from pymysql.err import OperationalError, Error as PYMErr, InterfaceError

from fids_common import login

STYLE = dict(
    title=dict(font=("Calibri", 60, "bold"), fg="#ffffff", bg="#666699"),
    time=dict(font=("Consolas", 40, "bold"), fg="#ffffff", bg="#666699"),
    header=dict(font=("Calibri", 40, "bold"), fg="#ffffff", bg="#666699"),
    body=dict(font=("Calibri", 35, "bold"), fg="#ffffff", bg="#000066"),
    body2=dict(font=("Calibri", 35, "bold"), fg="#ffffff", bg="#0066ff"),
    err=dict(font=("Calibri", 60, "bold"), fg="#ff0000", bg="#000066"),
)


class DataFrame(
    tk.Frame,
):
    def __init__(self, parent, con, data, style, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # initialize parent tk

        self.__con = con
        self._parent = parent
        self._data = data
        self._style = style

        self["bg"] = self._style["body"]["bg"]

        try:
            cur = self.__con.cursor()
            cur.execute(
                "SELECT `ofid`, `to`, "
                " `std`, `etd`, `checkinctr`, `status` "
                "FROM `flight` WHERE "
                "`std`BETWEEN NOW() AND NOW() + INTERVAL 1 DAY"
                " ORDER BY `std` ASC;"
            )
        except OperationalError as e:
            lbl = tk.Label(
                self,
                text=("Failed to update data\n" "Sorry for inconvinience"),
                **self._style["err"]
            )
            lbl.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
            tk.Grid.columnconfigure(self, 0, weight=1)
        except InterfaceError as e:
            lbl = tk.Label(
                self,
                text=("Cannot update data\n" "Please restart application"),
                **self._style["err"]
            )
            lbl.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
            rst = tk.Button(
                self, text="Restart", command=exit, font=("Adani Regular", 40, "bold")
            )
            rst.grid(row=1, column=0, sticky=tk.N + tk.S)
            tk.Grid.columnconfigure(self, 0, weight=1)
        else:
            # Table adding
            self.__heading_2 = tk.Label(self, text="Flight No", **self._style["header"])
            self.__heading_2.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
            self.__heading_4 = tk.Label(self, text="To", **self._style["header"])
            self.__heading_4.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
            self.__heading_7 = tk.Label(self, text="STD", **self._style["header"])
            self.__heading_7.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
            self.__heading_8 = tk.Label(self, text="ETD", **self._style["header"])
            self.__heading_8.grid(row=0, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
            self.__heading_9 = tk.Label(
                self, text="Check-in counter", **self._style["header"]
            )
            self.__heading_9.grid(row=0, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
            self.__heading_10 = tk.Label(self, text="Status", **self._style["header"])
            self.__heading_10.grid(row=0, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
            i = 1

            for i in range(6):
                tk.Grid.columnconfigure(self, i, weight=1)

            # self.__matrix = []

            for data in cur.fetchall():
                if i % 2 == 1:
                    style = self._style["body"]
                else:
                    style = self._style["body2"]
                l1 = tk.Label(self, text=data[0], **style)
                l1.grid(row=i, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
                # print(self._data.get(data[1], data[1]), data[1])
                l2 = tk.Label(self, text=self._data.get(data[1], data[1]), **style)
                l2.grid(row=i, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

                l3 = tk.Label(self, text=data[2].strftime("%H:%M"), **style)
                l3.grid(row=i, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

                l4 = tk.Label(self, text=data[3].strftime("%H:%M"), **style)
                l4.grid(row=i, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
                l5 = tk.Label(self, text=data[4], **style)
                l5.grid(row=i, column=4, sticky=tk.N + tk.S + tk.E + tk.W)

                l6 = tk.Label(self, text=data[5].title(), **style)
                l6.grid(row=i, column=5, sticky=tk.N + tk.S + tk.E + tk.W)

                i += 1
        finally:
            cur.close()


class HomeScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize parent tk

        self.configure(bg="#000066")

        self.title("Departure Screen")
        self.attributes("-fullscreen", True)

        self.__con = login.login(self)

        self.__logout_btn = tk.Label(self, text="DEPARTURES", **STYLE["title"])
        self.__logout_btn.grid(row=0, column=0, sticky=tk.E + tk.W)

        self._timelbl = tk.Label(self, text="...", **STYLE["time"])
        self._timelbl.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        with open("op.json", "r") as f1:
            self._data = json.load(f1)

        self.__dframe = tk.Label(self, text="...")
        self.__dframe.grid(
            row=1, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self._refresh_table()
        self._showdt()

        tk.Grid.columnconfigure(self, 0, weight=1)
        # tk.Grid.columnconfigure(self, 1, weight=1)
        self.bind_all("<Control-q>", self.exit)

    def _refresh_table(self):
        self.__dframe.destroy()
        self.__dframe = DataFrame(self, self.__con, self._data, STYLE)
        self.__dframe.grid(
            row=1, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.after(5000, self._refresh_table)

    def _showdt(self):
        dt = datetime.datetime.now().strftime("%c")
        self._timelbl["text"] = dt
        self.after(1000, self._showdt)

    def exit(self, evt):
        self.destroy()


if __name__ == "__main__":
    root = HomeScreen()
    root.mainloop()
