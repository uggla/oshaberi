# coding=utf-8

import json
import tkinter as tk

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
        #tk.Label(edition, text="A l'intérieure de la frame").pack()
        self.sentence = tk.Text(edition)
        self.sentence.pack()
        #edit = tk.Button(edition, text='Edit').pack()
        self.add_button = tk.Button(edition, text='Add', width=65)
        self.add_button.pack()
        self.remove_button = tk.Button(edition, text='Remove', width=65)
        self.remove_button.pack()




# Main
if __name__ == "__main__":
    # Functions
    def read_sentences(json_file):
        # read json file
        with open(json_file) as json_data:
            sentences = json.load(json_data)
            json_data.close()
        #print(sentences)    
        return sentences
    
    def write_sentences(data, json_file):
        with open(json_file, 'w') as json_file_handler:
            json.dump(data, json_file_handler)
            json_file_handler.close()
    
    def create_sentence_buttons(sentences):
        for index, sentence in enumerate(sentences):
            button_container_frame = tk.Frame(scframe.interior, padx=5)
            button_container_frame.pack(side=tk.TOP)
            sentence_button = tk.Button(button_container_frame,
                                        height=sentence.count("\n")+1,
                                        width=60, 
                                        #relief=tk.FLAT, 
                                        #bg="gray99", fg="purple3",
                                        font="Dosis",
                                        text=sentences[index],
                command=lambda sentences_index=index,x=sentence: choose_sentence(sentences_index))
            sentence_button.pack(padx=5, pady=5, side=tk.LEFT)
            sentence_button_up = tk.Button(button_container_frame,
                                        height=sentence.count("\n")+1,
                                        width=1, 
                                        #relief=tk.FLAT, 
                                        #bg="gray99", fg="purple3",
                                        font="Dosis",
                                        text="+",
                command=lambda sentences_index=index,x=sentence: choose_sentence_up(sentences_index))
            sentence_button_up.pack(padx=5, pady=5, side=tk.LEFT)
            sentence_button_down = tk.Button(button_container_frame,
                                        height=sentence.count("\n")+1,
                                        width=1, 
                                        #relief=tk.FLAT, 
                                        #bg="gray99", fg="purple3",
                                        font="Dosis",
                                        text="-",
                command=lambda sentences_index=index,x=sentence: choose_sentence_down(sentences_index))
            sentence_button_down.pack(padx=5, pady=5, side=tk.LEFT)
    
    def add_sentences(event):
        if editframe.sentence.get(1.0, tk.END).rstrip() != "":
            print('add sentences "{}"'.format(editframe.sentence.get(1.0, tk.END).rstrip()))
            sentences.append(editframe.sentence.get(1.0, tk.END).rstrip())
            refresh_sentence_buttons(sentences)
    
    def remove_sentences(event):
        if editframe.sentence.get(1.0, tk.END).rstrip() != "":
            print('remove sentences "{}"'.format(editframe.sentence.get(1.0, tk.END).rstrip()))
            sentences.remove(editframe.sentence.get(1.0, tk.END).rstrip())
            refresh_sentence_buttons(sentences)
    
    def refresh_sentence_buttons(sentences):
        for widget in scframe.interior.winfo_children():
            widget.destroy()
        create_sentence_buttons(sentences)
        
    def choose_sentence(sentences_index):
        print('sentence "{}" selected'.format(sentences[sentences_index]))
        editframe.sentence.delete(1.0, tk.END)
        editframe.sentence.insert(1.0, sentences[sentences_index])
        # Copy to clipboard
        print('sentence "{}" copied to clipboard'.format(editframe.sentence.get(1.0, tk.END).rstrip()))
        root.clipboard_clear()
        root.clipboard_append(editframe.sentence.get(1.0, tk.END).rstrip())

    def choose_sentence_up(sentence_index):
        sentence = sentences[sentence_index]
        sentence_length = len(sentences)
        del sentences[sentence_index]
        if sentence_index == 0:
            sentences.insert(sentence_length - 1, sentence)
        else:
            sentences.insert(sentence_index - 1, sentence)
        refresh_sentence_buttons(sentences)
        
    def choose_sentence_down(sentence_index):
        sentence = sentences[sentence_index]
        sentence_length = len(sentences)
        del sentences[sentence_index]
        if sentence_index == sentence_length -1:
            sentences.insert(0, sentence)
        else:
            sentences.insert(sentence_index + 1, sentence)
        refresh_sentence_buttons(sentences)

        
    def on_closing():
        write_sentences(sentences, "taupie.json")
        root.destroy()

    # Gui definition
    root = tk.Tk()
    root.title("Taupie Wakfu fast chat")
    #root.configure(background="gray99")
 
    # Define handler closing the main window
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Create the scrolling frame and the edit frame
    scframe = VerticalScrolledFrame(root)
    editframe = EditFrame(root)
    scframe.pack(side=tk.LEFT, expand="yes", fill="both")
    editframe.pack(side=tk.RIGHT, expand="yes", fill="both")    
    
    # Define handlers for the Add and Remove buttons
    editframe.add_button.bind("<Button-1>", add_sentences)
    editframe.remove_button.bind("<Button-1>", remove_sentences)
     
    # Get sentences and create the buttons
    sentences = read_sentences("taupie.json")
    create_sentence_buttons(sentences)
    
    # Set minsize to avoid shrink windows
    root.update()
    root.geometry()
    root.minsize(root.winfo_width()+2, root.winfo_height()+2)
       
    # Run the Gui
    root.mainloop()
