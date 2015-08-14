

import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        text = tk.Text(self, wrap="none")
        vsb = tk.Scrollbar(orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        text.pack(fill="both", expand=True)

        for i in range(20):
            b = tk.Button(self, text="Button #%s" % i)
            text.window_create("end", window=b)
            text.insert("end", "\n")

        text.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
