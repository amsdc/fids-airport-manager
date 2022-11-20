import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
import json
import datetime

import pymysql
from pymysql.err import OperationalError, Error as PYMErr, InterfaceError

from fids_common import login
from fids_common import themes
from fids_common import settings
from fids_common import reloader
from fids_common import quickdialog
from fids_common import airlinepics


class DataFrame(
    tk.Frame,
):
    def __init__(self, parent, con, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # initialize parent tk

        self.__con = con
        self._parent = parent
        self._data = data

        self["bg"] = themes.get_style("body")["background"]
        # self["bg"] = "black"

        try:
            cur = self.__con.cursor()
            cur.execute(
                "SELECT `sta`, `ifid`,`from`, `belt`, `eta`"
                "FROM `flight` WHERE "
                "`sta` BETWEEN NOW() AND NOW() + INTERVAL 1 DAY"
                " ORDER BY `sta` ASC;"
            )
        except OperationalError as e:
            lbl = tk.Label(
                self,
                text=("Failed to update data\n" "Sorry for inconvinience"),
                **themes.get_label_attr(themes.get_style("error"))
            )
            lbl.grid(row=0, column=0, **themes.get_grid_attr(themes.get_style("error")))
            tk.Grid.columnconfigure(self, 0, weight=1)
        except InterfaceError as e:
            reloader.restart()
        else:
            # Table adding
            self.__heading_1 = tk.Label(self, text="Airline", **themes.get_label_attr(themes.get_style("header")))
            self.__heading_1.grid(row=0, column=0, **themes.get_grid_attr(themes.get_style("header")))
            self.__heading_2 = tk.Label(self, text="STA", **themes.get_label_attr(themes.get_style("header")))
            self.__heading_2.grid(row=0, column=1, **themes.get_grid_attr(themes.get_style("header")))
            self.__heading_3 = tk.Label(self, text="Flight No.", **themes.get_label_attr(themes.get_style("header")))
            self.__heading_3.grid(row=0, column=2, **themes.get_grid_attr(themes.get_style("header")))
            self.__heading_4 = tk.Label(self, text="From", **themes.get_label_attr(themes.get_style("header")))
            self.__heading_4.grid(row=0, column=3, **themes.get_grid_attr(themes.get_style("header")))
            self.__heading_5 = tk.Label(self, text="Belt", **themes.get_label_attr(themes.get_style("header")))
            self.__heading_5.grid(row=0, column=4, **themes.get_grid_attr(themes.get_style("header")))
            self.__heading_6 = tk.Label(self, text="ETA", **themes.get_label_attr(themes.get_style("header")))
            self.__heading_6.grid(row=0, column=5, **themes.get_grid_attr(themes.get_style("header")))

            i = 1

            for i in range(1, 5):
                tk.Grid.columnconfigure(self, i, weight=1)

            self._airimg = []

            for data in cur.fetchall():
                iata = data[0][:2]
                fnum = data[0][2:]
                self._airimg.append(airlinepics.get_airline_logo(iata, themes.current_theme["icons"]["airline_logo"]["size"]))
                if i % 2 == 1:
                    style = themes.get_style("body")
                else:
                    style = themes.get_style("body2")
                    
                
                l0 = tk.Label(self, image=self._airimg[-1], **themes.get_label_attr(style))
                l0.grid(row=i, column=0, **themes.get_grid_attr(style))

                l1 = tk.Label(self, text=data[0].strftime("%H:%M"), **themes.get_label_attr(style))
                l1.grid(row=i, column=1, **themes.get_grid_attr(style))

                l2 = tk.Label(self, text=data[1], **themes.get_label_attr(style))
                l2.grid(row=i, column=2, **themes.get_grid_attr(style))

                l3 = tk.Label(self, text=self._data.get(data[2], data[2]), **themes.get_label_attr(style))
                l3.grid(row=i, column=3, **themes.get_grid_attr(style))

                l4 = tk.Label(self, text=data[3], **themes.get_label_attr(style))
                l4.grid(row=i, column=4, **themes.get_grid_attr(style))

                l5 = tk.Label(self, text=data[4].strftime("%H:%M"), **themes.get_label_attr(style))
                l5.grid(row=i, column=5, **themes.get_grid_attr(style))

                i += 1
        finally:
            cur.close()


class HomeScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize parent tk
        self.bind_all("<Control-q>", self.exit)
        
        self.configure(bg="#000066")

        self.title("Arrival Screen")
        self.attributes("-fullscreen", True)
        
        try:
            self.__con = login.login(self)
        except OperationalError:
            self.wm_iconify()
            quickdialog.show_conrestore()
            reloader.restart()

        self.__logout_btn = tk.Label(self, text="ARRIVALS", **themes.get_label_attr(themes.get_style("title")))
        self.__logout_btn.grid(row=0, column=1, **themes.get_grid_attr(themes.get_style("title")))

        self._timelbl = tk.Label(self, text="...", **themes.get_label_attr(themes.get_style("time")))
        self._timelbl.grid(row=0, column=2, **themes.get_grid_attr(themes.get_style("time")))

        with open("op.json", "r") as f1:
            self._data = json.load(f1)

        self.__dframe = tk.Label(self, text="...")
        self.__dframe.grid(
            row=1, column=0, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self._refresh_table()
        self._showdt()

        tk.Grid.columnconfigure(self, 1, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        # tk.Grid.columnconfigure(self, 1, weight=1)
        

    def _refresh_table(self):
        self.__dframe.destroy()
        self.__dframe = DataFrame(self, self.__con, self._data)
        self.__dframe.grid(
            row=1, column=0, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.after(5000, self._refresh_table)

    def _showdt(self):
        dt = datetime.datetime.now().strftime("%c")
        self._timelbl["text"] = dt
        self.after(1000, self._showdt)

    def exit(self, evt):
        self.destroy()


if __name__ == "__main__":
    themes.load_theme("themes/aai.toml")
    root = HomeScreen()
    root.mainloop()
