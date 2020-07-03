import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
import os
from threading import Thread
from time import sleep
import sip

print("BIENVENUE")

'''---------------------Variable Glabal a tout le programme---------------------'''	
etat_prog = True

app = QApplication(sys.argv)
dossier = "C:/Users/karim/Downloads/"
#dossier = "C:/Users/karim/Desktop/KARIM_project/project_python/test_icone_bar_tache/test_dossier/"

liste_dos = []

types_fichier = [["png", "jpeg", "jpg", "gif"], ["mp4", "mkv", "avi"], ["exe", "msi"], ["pdf"], ["zip", "rar"], ["pptx", "docx", "doc", "xlsx", "dotx", "odp"], ["txt"], ["iso","torrent", "part"], ["java", "c", "o", "py", "jar", "sql", "apk"], ["mp3", "ogg", "wav"]]

black_liste_fichier = [] 


'''---------------------Methode Initialisation---------------------'''
def verif(txt:str):
    succes = False
    with os.scandir(dossier) as fichiers:
        for fichier in fichiers:
            if(fichier.name == txt):
                succes = True
    return succes



def creationDoc(txt:str):
    try:
        os.mkdir(dossier+"/"+txt)
    except OSError:
        print ("Creation du dossier "+txt+" a echouer")
    else:
        print ("Reussite le la creation du dossier "+ txt)

        
def initialisation():
    print("Initialisation")

    liste_dos.append("Dossier")
    liste_dos.append("Image")
    liste_dos.append("Video")
    liste_dos.append("Executable")
    liste_dos.append("Pdf")
    liste_dos.append("Archive")
    liste_dos.append("Document")
    liste_dos.append("Texte")
    liste_dos.append("Iso_et_Torrent")
    liste_dos.append("Programme_Informatique")
    liste_dos.append("Son")

    for dos in liste_dos:
        if verif(dos) == False:
            creationDoc(dos)
            
    print("Initialisation Finie !!")

    
'''---------------------Lancement de l'initialisation---------------------'''	
    
    
initialisation()


'''---------------------methode---------------------'''
def reverse(txt:str):
    chaine = ""
    i = len(txt) - 1
    while i >= 0:
        chaine += txt[i] 
        i -= 1
    return chaine

def dansListe(obj, liste):
    succes = False
    for truc in liste:
        if truc == obj:
            succes = True
    return succes
        
def BLFVerif(nom:str):
    succes = False
    for bl in black_liste_fichier:
        if(bl == nom):
            succes = True
    return succes

def recupExtension(txt:str):
    extension = ""
    i = len(txt) - 1
    while i >= 0:
        if(txt[i] == '.'):
            break
        else:
            extension += txt[i]
        i -= 1
    return reverse(extension)


def deplaceDos(nom_fichier:str, nom_nv_dossier:str):
    
    try:
        os.rename(dossier+nom_fichier, dossier+nom_nv_dossier+"/"+nom_fichier)
    
    except os.error as e:
        print(e)
        black_liste_fichier.append(nom_fichier)
        
    print("Ranger")

def rangeDossier():
        while etat_prog:
                with os.scandir(dossier) as fichiers:
                        for fichier in fichiers:
                            #verif si le fichier n'est pas dans la blackListe
                            if BLFVerif(fichier.name) == False:
                                #si c'est un dossier
                                if fichier.is_dir() and dansListe(fichier.name, liste_dos) == False:
                                    print(dansListe(fichier, liste_dos))
                                    deplaceDos(fichier.name, liste_dos[0])
                                #sinon
                                else: 
                                    i = 1
                                    #recherche dans la liste des liste d'extention 
                                    for extensions in types_fichier :
                                        #verif si l'extension du fichier se trouve dans cet liste
                                        if dansListe(recupExtension(fichier.name), extensions):
                                            #deplacement
                                            deplaceDos(fichier.name, liste_dos[i])
                                            break
                                        i+=1
                sleep(2)

def closeApplication():
	print("Au revoir")
	app.quit()
	sys.exit(app.exec_())
	
'''---------------------Mise en place de l'aspect graphique---------------------'''	
	

bg_prog = Thread(target=rangeDossier)



trayIcon = QSystemTrayIcon(QIcon('C:/Users/karim/Desktop/KARIM_project/project_python/RangementKa/RANKA.ico'), parent=app)
	
menu = QMenu()
exitAction = menu.addAction('Quitter')

trayIcon.setToolTip('RangementKa')
trayIcon.show()
trayIcon.setContextMenu(menu)

'''---------------------methode---------------------'''	
def stopAll():
        global etat_prog
        etat_prog = False
        bg_prog.join()
        closeApplication()

'''---------------------ajout dela reactiviter du code + Lancement du Thread ---------------------'''	
exitAction.triggered.connect(stopAll)

bg_prog.start()

sys.exit(app.exec_())







 




