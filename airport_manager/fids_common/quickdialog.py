import tkinter as tk

class PleaseWait(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.attributes("-fullscreen", True)
        
        l = tk.Label(self, text="PLEASE WAIT\nRESTORING CONNECTION", font=("Ubuntu", 100, "bold"), anchor=tk.CENTER,
                     fg="#FFFFFF", bg="#000000")
        l.grid(row=0, column=0, sticky='nswe')
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

def show_conrestore():
    a = PleaseWait()
    a.after(5000, a.quit)
    a.mainloop()