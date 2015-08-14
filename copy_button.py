
from tkinter import *



class Application(Frame):
	"La classe generale"

	def __init__(self):
		"Constructeur"
		Frame.__init__(self)
		self.master.title("Super Bouton")
		self.pack()
		self.bouton1=Bouton(self.master,"Le texte a afficher","Le texte a copier")



class Bouton:
	"Le bouton qui sert a copier du texte dans le press-papier"

	def __init__(self,fenetre,texteaffiche,textecopie):
		"Constructeur"
		self.fenetre=fenetre
		self.texteaffiche=texteaffiche
		self.textecopie=textecopie
		bouton=Button(self.fenetre,text=self.texteaffiche,command=self.copie)
		bouton.pack()

	def copie(self):
		"Copie textecopie dans le press-papier"
		self.fenetre.clipboard_clear()
		self.fenetre.clipboard_append(self.textecopie)
 
 
 
if __name__=="__main__":
	application=Application()
	application.mainloop()
