# coding=utf-8

import tkinter as tk
from tkinter.constants import RIGHT

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class EditFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            
        #tk.Label(self, text="Frame 1").pack(padx=10, pady=10)
        edition = tk.LabelFrame(self, text="Edition",padx=10, pady=10)
        
        
        edition.pack(padx=10, pady=10, fill="both", expand="yes")
        tk.Label(edition, text="A l'intérieure de la frame").pack()
        sentence = tk.Text(edition).pack()
        edit = tk.Button(edition, text='Edit').pack()
        add = tk.Button(edition, text='Add').pack()
        remove = tk.Button(edition, text='Remove').pack()

# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Taupie Wakfu fast chat")
    #root.configure(background="gray99")
    
    scframe = VerticalScrolledFrame(root)
    editframe = EditFrame(root)
    scframe.pack(side=tk.LEFT, expand="yes", fill="both")
    editframe.pack(side=tk.RIGHT, expand="yes", fill="both")
    
    lis = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for i, x in enumerate(lis):
        btn = tk.Button(scframe.interior, height=1, width=60, 
            #relief=tk.FLAT, 
            #bg="gray99", fg="purple3",
            font="Dosis", text='Button ' + lis[i],
            command=lambda i=i,x=x: openlink(i))
        btn.pack(padx=10, pady=5, side=tk.TOP)
    
    def openlink(i):
        print(lis[i])
    root.mainloop()
