# Jean Salomon, Isidore Billard, Elliot Goralczyk
import tkinter as tk
import csv, random, unidecode, webbrowser
from PIL import ImageTk, Image

#------------------Fonctions-----------------------------

def code_principal():
    """fonction principale du code qui vérifie l'état du jeu et s'occupe d'appeler les autes fonctions, c'est le cerveau du code"""
    # ajouter une partie verifiant si return est appuyé, si c'est le cas lancer la fonction traiter_lettre
    fenetre.after(50, code_principal) # on appelle la fonction principale pour qu'elle tourne en boucle
    def etat_du_jeu():
        '''fonction qui vérifie constament l'état du jeu et est appelé dans code_principal'''
        global etat_jeu, numero_pendu
        # vérifie si le pendu est terminé (lorsque tout les traits sont tirés), si oui : perdu!
        if numero_pendu == 10:
            etat_jeu = 2        # met l'état_jeu à 2 (perdu)
            perdu()             # appelle la fonction destinée à faire perdre le joueur
        # vérifie si le mot a été trouvé (lorsque tout les tirets ont été remplacé), si oui : gagné!
        elif '_' not in proposition:
            etat_jeu = 1        # met l'état_jeu à 1 (gagné)
            gagner()            # appelle la fonction destinée à faire gagner le joueur
    def perdu():
        """fonction qui intervient si etat_jeu = 2, soit on a perdu"""
        defaite = toile.create_text(400,200, text = "Vous avez perdu ! :,(\n     le mot était :", font=('Comic Sans MS', 48), fill='red') # Affiche sur le canva le texte de défaite
        mot = toile.create_text(400,330, text= mot_secret , font=('Comic Sans MS', 48)) # annonce le mot qui était à deviner
        texte.config(text='Fin de la partie, veuillez appuyer sur «MENU»')              # informe l'utilisateur de la fin de la partie
        zoneDeTexte.bind('<Return>', menu)  # lorsque que entrée est pressé : menu
    def gagner():
        """foncton qui intervient en cas de victoire du joueur, soit si etat_jeu = 1"""
        victoire = toile.create_text(400,200, text = 'Vous avez gagné !', font=('Impact', 48), fill='green') # Affiche sur le canva le texte de victoire
        texte.config(text='Fin de la partie, veuillez appuyer sur «MENU»')    # informe l'utilisateur de la fin de la partie
        zoneDeTexte.bind('<Return>', menu)  # lorsque que entrée est pressé : menu
    etat_du_jeu()                     # vérifie l'état du jeu
def choix_mot_secret(a):
    """fonction qui ouvre le fichier csv où se trouve le dictionnaire
     de mots à faire deviner puis choisit aléatoirement un mot secret"""
    with open("code.csv","r",encoding = 'utf-8') as file:   # ouvre le fichier csv où se trouvent les mots à deviner
        table=list(csv.reader(file,delimiter=";"))
    mot_secret1=table[random.randint(0,len(table)-1)][0]    # choisit un mot aléatoire pour devenir le mot secret
    mot_secret = unidecode.unidecode(mot_secret1)           # enlève les accents du mot secret
    # choisi le mot en fonction de la difficulté choisie par le joueur
    if a == 0:
        # facile : le mot fera moins de 5 lettres (boucle jusqu'à trouver un mot adéquat)
        if len(mot_secret)<5:
            return mot_secret.strip().lower()  # renvoie le mot secret sans accents
        else : return choix_mot_secret(a)      # si le mot fait plus de 5 lettres : pioche un nouveau mot
    elif a == 1:
        # moyen : mot compris entre 5 et 8 lettres (boucle jusqu'à trouver un mot adéquat)
        if len(mot_secret)<9 and len(mot_secret)>4:
            return mot_secret.strip().lower()  # renvoie le mot secret sans accents
        else : return choix_mot_secret(a)      # si le mot n'est pas adéquat : pioche un nouveau mot
    elif a == 2:
        # difficile : mot plus que 8 lettres (boucle jusqu'à trouver un mot adéquat)
        if len(mot_secret)>8:
            return mot_secret.strip().lower()  # renvoie le mot secret sans accents
        else : return choix_mot_secret(a)      # si le mot n'est pas adéquat : pioche un nouveau mot
    else : 
        return mot_secret.strip().lower()      # renvoie le mot secret sans accents directement si rien n'est choisi  
def traiter_lettre(*args):
    """fonction appelée lorsque la touche "return" est enfoncée. La fonction récupère ce qui a été écrit dans la zone de saisie
    et le traite pour ajouter une lettre dans la variable globale "proposition" ou pour ajouter un élément au pendu"""
    global nbr_lettres_trouvees, lettres_utilisees, proposition, numero_pendu
    lettre_valide = False                 # crée une variable qui sert à savoir si c'est une lettre ou pas
    list_mot_secret = list(mot_secret)    # crée une liste du mot secret
    l1 = zoneDeTexte.get().lower().strip()# on récupère ce qui a été entré dans la zone de saisie (en mininuscule et sans espaces)
    l = unidecode.unidecode(l1)           # enlève les accents entrés par l'utilisateur
    zoneDeTexte.delete(0, 'end')          # on efface le contenu de la zone de saisie
    # vérifie que le jeu est en cours
    if etat_jeu == 0 :
    # revoie une erreur à l'utilisateur si la lettre a déjà été utilisée
        if l in lettres_utilisees:
            texte.config(text='Déjà Utilisé ;(') # renvoie l'erreur
            fenetre.after(2000, text)            # délai de 2 secondes avant de réinitialiser le texte
        # sinon revoie une erreur à l'utilisateur si plusieurs lettres sont entrées
        elif len(l) > 1:
            texte.config(text='Il faut marquer seulement une lettre') # renvoie l'erreur
            fenetre.after(2000, text)                                 # délai de 2 secondes avant de réinitialiser le texte
        # sinon revoie une erreur à l'utilisateur si ce n'est pas une lettre
        elif l.isalpha() == False:
            texte.config(text="il faut une lettre :)") # renvoie l'erreur
            fenetre.after(2000, text)                  # délai de 2 secondes avant de réinitialiser le texte
        # si la lettre est valide, l'ajoute au mot secret
        elif l in list_mot_secret:
            # regarde si la lettre (l) entrée est juste sur chacune des lettres du mot secret (sous forme de liste) et ajoute le nombre correspondant aux indices presents dans le mot secret à cette liste
            list2 = [i for i in range(len(list_mot_secret)) if list_mot_secret[i] == l] 
            # boucle le même nombre de fois qu'il y a de lettres justes entrée dans le mot secret
            for index in list2:
                proposition[index] = l              # remplace la lettre à l'indice correspondant dans la proposition
            toile.itemconfig(indice,  text = str(" ".join(proposition))) # met à jour la proposition sur la toile
            lettre_valide = True                    # valide la lettre pour être ajoutée aux lettres utilisées
        # si la lettres n'est pas valide et/ou n'a pas déjà été utilisée, ajoute un trait au pendu
        elif l not in mot_secret and l not in lettres_utilisees:
            dessiner_pendu(liste_traits_pendu)  # ajoute un trait au pendu en utilisant la fonction "liste_traits_pendu"
            numero_pendu += 1                   # ajoute 1 à la variable (perdu quand = 10 )
            nbr_lettres_trouvees -= 1           # enlève 1 aux nombres de lettres trouvées
            nbr_essais.config(text='nombre de tentatives restantes : ' + str(nbr_lettres_trouvees))
            lettre_valide = True                # valide la lettre pour être ajoutée aux lettres utilisées
        # ajoute la lettre aux lettres utilisées si c'est bien une lettre
        if lettre_valide == True:
            lettres_utilisees.append(l)         # ajoute la lettre aux lettres utilisées
            lettres_utilisees.sort()            # trie ces lettres dans l'ordre alphabetique
            lettre_valide = False               # remet cette variable fausse pour ne pas que les futures lettres(probablement fausses) soit valides
            label_lettres_utilisees.config(text = lettres_utilisees, font=("Courier",22))    # met à jour le label des lettres utilisées           
def dessiner_pendu(l):
    """fonction qui gère l'évolution du pendu"""
    global numero_pendu, etat_jeu
    # Verifie que le jeu est en cours
    if etat_jeu==0:
        if l[numero_pendu][0]==1:                                                                                               # Vérifie si il faut tracer un trait ou une ellipse
            line=toile.create_line(l[numero_pendu][1][0],l[numero_pendu][1][1],l[numero_pendu][2][0],l[numero_pendu][2][1])     # Trace le trait
        else:
            line=toile.create_oval(l[numero_pendu][1][0],l[numero_pendu][1][1],l[numero_pendu][2][0],l[numero_pendu][2][1])     # Trace l'ellipse

def text():
    '''fonction permettant de réinitialiser le texte d'échange avec l'utilisateur'''
    texte.config(text='Choisir une lettre et appuyer sur entrée', fg='red', font='bold') # remet le texte initial
def new_game():
    """Fonction qui réinitialise le jeu ---si des variable sont rajoutés : les réinitialiser ici---"""
    global etat_jeu, numero_pendu, nbr_lettres, nbr_lettres_trouvees, proposition, lettres_utilisees, difficulte
    # remet les variables à leurs valeurs initiales
    toile.delete('all')
    etat_jeu = 0
    numero_pendu = 0    
    nbr_lettres_trouvees = 10
    lettres_utilisees = []
    label_lettres_utilisees.config(text = lettres_utilisees)
    proposition=[]
    indice_difficulte.config(text='Difficulté : Aléatoire', fg='purple')
    nbr_essais.config(text='nombre de tentatives restantes : ' + str(nbr_lettres_trouvees))
    text()
def clear():
    '''fonction qui retire tout les éléments de la fenêtre ---si des éléments sont rajoutés : element.pack_forget()---'''
    text()
    zoneDeTexte.bind('<Return>', traiter_lettre)
    texte_2p.pack_forget()
    texte_2p.config(state='disabled')   # empêche de pouvoir continuer à modifier le mot secret quand validé
    zoneDeTexte.pack_forget()
    texte.pack_forget()
    error.pack_forget()
    label_lettres_utilisees.pack_forget()
    nbr_essais.pack_forget()
    ng_button.pack_forget()
    toile.pack_forget()
    Jouer2.pack_forget()
    Jouer1.pack_forget()
    b_settings.pack_forget()
    b_dark.pack_forget()
    b_white.pack_forget()
    rick_roll_button.pack_forget()
    text_menu.pack_forget()
    text_setting.pack_forget()
    trou.pack_forget()
    vert_slider.pack_forget()
    hori_slider.pack_forget()
    save.pack_forget()
    text_taille_fenetre.pack_forget()
    credit.pack_forget()
    b_facile.pack_forget()
    b_moyen.pack_forget()
    b_difficile.pack_forget()
    b_lancer.pack_forget()
    indice_difficulte.pack_forget()
    b_tuto.pack_forget()
    l_tuto.pack_forget()
    text_tuto.pack_forget()
    frame_tuto.pack_forget()
def pack_fenetre():
    '''fonction chargée de la mise en place des éléments de la fenêtre'''
    clear() # enlève les boutons du menu
    # ajoute les boutons, informations et zones de saisie du jeu dans l'ordre (le premier étant en haut de la fenêtre et le dernier en bas)
    toile.pack()
    ng_button.pack(fill= tk.X)
    label_lettres_utilisees.pack()
    zoneDeTexte.pack()
    texte.pack()
    nbr_essais.pack()
    # place le bouton quitter en bas
    bouton_quitter.pack_forget()# l'enleve 
    bouton_quitter.pack()       # puis le remet

def menu(*args):
    '''création du menu'''   
    clear()     # efface tout les éléments
    new_game()  # réinitialise les variables
    # ajoute les éléments du menu
    text_menu.pack()
    Jouer1.pack()
    Jouer2.pack()
    b_settings.pack()
    texte_2p.config(state='normal')
    trou.pack()
    bouton_quitter.pack_forget()
    bouton_quitter.pack()
def settings():
    '''fonction chargée d'afficher les paramètres fonctionnels'''
    clear() # efface tout les éléments
    # ajoute les éléments des paramètres
    text_setting.pack()
    b_dark.pack()
    b_white.pack()
    text_taille_fenetre.pack()
    vert_slider.pack()
    hori_slider.pack()
    save.pack()
    b_tuto.pack()
    trou.pack()
    ng_button.pack()
    bouton_quitter.pack_forget()
    bouton_quitter.pack()
    rick_roll_button.pack(side='bottom')
    credit.pack(side='bottom')
def tuto():
    clear()
    text_tuto.pack()
    img1_tuto.pack()
    exp_tuto1.pack()
    img2_tuto.pack()
    frame_tuto.pack()
    b_settings.pack()
    bouton_quitter.pack_forget()
    bouton_quitter.pack()    
def light():
    '''fonction en charge de changer le thème du jeu en lumineux ---si des éléments sont rajoutés : element.config(bg='#EEEEEE')---'''
    fenetre.configure(bg='#EEEEEE')
    trou.config(bg='#EEEEEE')
    text_menu.config(fg='black', bg='#EEEEEE')
    Jouer2.config(fg='black',bg='#EEEEEE')
    Jouer1.config(fg='black',bg='#EEEEEE')
    error.config(bg='#EEEEEE')
    texte.config(bg='#EEEEEE')
    label_lettres_utilisees.config(bg='#EEEEEE', fg='blue')
    nbr_essais.config(bg='#EEEEEE', fg= 'purple')
    text_setting.config(fg='black',bg='#EEEEEE')
    b_settings.config(fg='black',bg='#EEEEEE')
    credit.config(fg='black',bg='#EEEEEE')
    save.config(fg='black',bg='#EEEEEE')
    text_taille_fenetre.config(fg='black',bg='#EEEEEE')
    vert_slider.config(fg='black',bg='#EEEEEE')
    hori_slider.config(fg='black',bg='#EEEEEE')
    b_lancer.config(fg='black',bg='#EEEEEE')
    indice_difficulte.config(fg='black',bg='#EEEEEE')
    b_tuto.config(fg='black',bg='#EEEEEE')
    l_tuto.config(fg='black',bg='#EEEEEE')
    text_tuto.config(fg='black',bg='#EEEEEE')
def dark():
    '''fonction en charge de changer le thème du jeu en sombre ---si des éléments sont rajoutés : element.config(bg='#404040')---'''
    fenetre.configure(bg='#404040')
    trou.config(bg='#404040')
    text_menu.config(fg='white', bg='#404040')
    Jouer2.config(fg='white',bg='#404040')
    Jouer1.config(fg='white',bg='#404040')
    error.config(bg='#404040')
    texte.config(bg='#404040')
    label_lettres_utilisees.config(fg='#ADD8E6',bg='#404040')
    nbr_essais.config(fg='#F4BBFF',bg='#404040')
    text_setting.config(fg='white',bg='#404040')
    b_settings.config(fg='white',bg='#404040')
    credit.config(fg='white',bg='#404040')
    save.config(fg='white',bg='#404040')
    text_taille_fenetre.config(fg='white',bg='#404040')
    vert_slider.config(fg='white',bg='#404040')
    hori_slider.config(fg='white',bg='#404040')
    b_lancer.config(fg='white',bg='#404040')
    indice_difficulte.config(fg='white',bg='#404040')
    b_tuto.config(fg='white',bg='#404040')
    l_tuto.config(fg='white',bg='#404040')
    text_tuto.config(fg='white',bg='#404040')

def one_player_bis():
    random_dif()    # remet la difficulté du jeu en aléatoire
    clear()         # efface tout les éléments
    # ajoute les éléments du menu
    text_menu.pack()
    Jouer1.pack()
    b_facile.pack()
    b_moyen.pack()
    b_difficile.pack()
    b_lancer.pack()
    trou.pack()
    ng_button.pack()
    bouton_quitter.pack_forget()
    bouton_quitter.pack()
    indice_difficulte.pack()
def one_player():
    """Fonction pour 1 joueur : mot secret choisit à partir de la base de donnée"""
    global mot_secret, proposition, indice
    # commence une nouvelle partie
    new_game()          # réinitialise tout les éléments
    pack_fenetre()      # affiche les éléments du jeu, caché par le menu
    # choisi un nouveau mot secret et le met en place
    mot_secret=choix_mot_secret(difficulte)           # on choisit un mot au hasard dans code.csv grace a la fonction choix_mot_secret()
    proposition = ["_" for i in range(len(mot_secret))]     # remplit la proposition d'autant de lettres que dans le mot secret
    indice = toile.create_text(400,430, text = str(" ".join(proposition)), font=("Courier",30)) # affiche la proposition sur la toile
def easy():
    '''fonction qui change la difficulté du jeu en Facile'''
    global difficulte
    difficulte = 0
    indice_difficulte.config(text='Difficulté : Facile', fg='Green')
def medium():
    '''fonction qui change la difficulté du jeu en Moyen'''
    global difficulte
    difficulte = 1
    indice_difficulte.config(text='Difficulté : Moyen', fg='yellow')
def hard():
    '''fonction qui change la difficulté du jeu en Difficile'''
    global difficulte
    difficulte = 2
    indice_difficulte.config(text='Difficulté : Difficile', fg='red')
def random_dif():
    '''fonction qui change la difficulté du jeu en Aléatoire'''
    global difficulte
    difficulte = None
    indice_difficulte.config(text='Difficulté : Aléatoire', fg='purple')

def two_player_bis():
    '''fonction qui crée la zone de saisie du mot secret à faire
      deviner lorsque le "bouton faire" deviner est pressé'''
    clear() # enlève tout les éléments
    menu()  # rajoute le menu pour au cas où des éléments non désirés se seraient ajoutés
    indice_difficulte.pack_forget()          # enlève la difficulté car inutile
    error.pack()                             # indication pour le joueur
    texte_2p.pack()                          # ajoute la zone de saisie à la fenêtre
    texte_2p.bind('<Return>', two_player)    # appelle la fonction two_player lorsque 'Return' est pressé pour commencer le jeu
    texte_2p.delete(0, 'end')                # on efface le contenu de la zone de saisie
def two_player(*args):
    """Fonction pour 2 joueur: mot secret choisit par l'autre joueur"""
    global mot_secret, proposition, lettres_utilisees, indice, texte_2p
    new_game() # réinitialise toutes les variables pour que le jeu puisse commencer
    mot_secret = unidecode.unidecode(texte_2p.get().lower().strip()) # choisi un nouveau mot secret et le met en place(enlève majuscules, accents et espaces)
    # si le caractères n'est pas une lettre de l'alphabet, renvoie une erreur
    if mot_secret.isalpha() == False:
        error.config(text='veuillez ne pas utiliser de caractères spéciaux', fg='red', font='bold') # affiche l'erreur
        fenetre.after(2000,lambda : error.config(text='Entrer le mot à faire deviner ici!', fg='red', font='bold')) # remet l'indication pour le joueur 2 sec plus tard
        texte_2p.delete(0, 'end') # retire ce que l'utilisateur a écrit si invalide
        return None               # interrompt la fonction pour ne pas lancer le jeu si la lettre est invalide
    # ajoute les éléments du jeu si le mot est inférieur à 16 caractères (le mot est considéré comme trop grand au-delà, il ne rentre pas dans la fenêtre)
    if len(mot_secret)< 16:
        pack_fenetre()
    # si le mot est trop long, renvoie une erreur
    else:
        error.config(text='mot trop long', fg='red', font='bold') # affiche l'erreur
        fenetre.after(2000,lambda : error.config(text='Entrer le mot à faire deviner ici!', fg='red', font='bold')) # remet l'indication pour le joueur 2 sec plus tard
        texte_2p.delete(0, 'end') # retire ce que l'utilisateur a écrit si invalide
        return None               # interrompt la fonction pour ne pas lancer le jeu si la lettre est invalide
    proposition = ["_" for i in range(len(mot_secret))] # remplit la proposition d'autant de lettres que dans le mot secret
    indice = toile.create_text(400,430, text = str(" ".join(proposition)), font=("Courier",30)) # ajoute les tirets sur la toile

#------------------variables globales-----------------------------

liste_traits_pendu=[[1,(100,400),(300,400)],[1,(200,400),(200,50)],[1,(200,50),(400,50)],[1,(200,125),(275,50)],
[1,(400,50),(400,125)],[2,(375,125),(425,175)],[1,(400,175),(400,250)],[1,(350,200),(450,200)],[1,(400,250),(375,325)],[1,(400,250),(425,325)]]
    # liste de tous les traits du pendu. Un trait est représenté par une liste composée d'un entier et de deux tuples :
    # l'entier sera : 1 pour indiquer que l'on doit tracer un segment ou 2 pour indiquer que l'on doit tracer un cercle
    # les deux tuples correspondent aux coordonnées des deux points qui permettent de caractériser le segment ou le cercle à tracer
proposition=[]              # crée la proposition
mot_secret = None           # crée la variable du mot secret
nbr_lettres_trouvees=10     # variable qui permet de savoir combien d'essais restant
lettres_utilisees=[]        # liste des lettres déjà proposées par le joueur. Cette liste sera affichée pour que le joueur puisse la consulter
numero_pendu=0              # cette variable permet de savoir combien de traits ont déjà été tracés pour le pendu
etat_jeu=0                  # variable qui donne l'état du jeu : 0 =en cours, 1=gagné, 2=perdu.
difficulte = None           # variable qui la difficulté du mot aléatoire : 0=facile(1-4 lettres), 1=moyen(5-8 lettres), 2=difficile(8+ lettres)

#----------------éléments de la fenêtre----------------------

#-----éléments globaux-----
fenetre=tk.Tk()              # création de la fenêtre
fenetre.geometry('800x660')  # défini la taille initiale de la fenetre
fenetre.title('Jeu du Pendu')# donne un nom à la fenêtre
toile = tk.Canvas(fenetre, width=800, height=500) # création de la toile
bouton_quitter = tk.Button(fenetre, text='Quitter',bg='#F01000', command = fenetre.destroy) # création du bouton Quitter
trou = tk.Label(fenetre) # label permettant de séparer certains éléments (mise en page)
ng_button = tk.Button(fenetre, bg='#50F023', text='MENU', command = menu)           # création du bouton Recommencer

#-----éléments menu-----
text_menu = tk.Label(fenetre, text= 'MENU', font=('bold', 25))                             # texte d'accueil du menu
Jouer2 = tk.Button(fenetre, text='Faire Deviner', command = two_player_bis)                # création du bouton Jouer avec 2 Joueurs
Jouer1 = tk.Button(fenetre, text='Mot Aléatoire', command = one_player_bis)                # création du bouton 1 Joueur
error = tk.Label(fenetre, text='Entrer le mot à faire deviner ici!', fg='red', font='bold')# création de la zone chargée de donner des indications à l'utilisateur
texte_2p = tk.Entry(fenetre)                       # met en place une zone de texte vide pour le choix du mot secret pour 2 joueurs
l_tuto = tk.Label(fenetre, text='Le tutoriel est disponible dans les paramètres ;)', font=(100,25))      # texte rappel du tutoriel (appelé seulement une fois au lancement du jeu)
# éléments difficulté du jeu (mode aléatoire)
b_facile = tk.Button(fenetre, text='facile',bg='#8fce00', command = easy)
b_moyen = tk.Button(fenetre, text='moyen',bg='#ffd966', command = medium)
b_difficile = tk.Button(fenetre, text='difficile',bg='#dd6a6a', command = hard)
b_lancer = tk.Button(fenetre, text='Lancer le jeu', command = one_player)
indice_difficulte = tk.Label(fenetre, text='Difficulté : Aléatoire', fg= 'purple')

#-----éléments du jeu-----
indice = None                                                                       # crée la variable où sera affiché la proposition
zoneDeTexte = tk.Entry(fenetre)                                                     # met en place une zone de texte vide
zoneDeTexte.bind('<Return>', traiter_lettre)                                        # appelle la fonction traiter_lettre lorsque 'Return' est pressé
texte = tk.Label(fenetre, text='Choisir une lettre et appuyer sur entrée', fg='red')# création de la zone chargée de donner des indications à l'utilisateur
nbr_essais = tk.Label(fenetre, text='nombre de tentatives restantes : ' + str(nbr_lettres_trouvees), fg= 'purple') # création zone du nombre d'essais restant
label_lettres_utilisees = tk.Label(text = lettres_utilisees, font=("Courier",22), fg='blue') # création de la zone où sont répertoriées les lettres utilisées

#-----éléments paramètres-----
text_setting = tk.Label(fenetre, text= 'PARAMETRES', font=('bold', 25)) # texte d'accueil des paramètres
b_settings = tk.Button(fenetre, text='Paramètres', command = settings)  # bouton des paramètres
credit = tk.Label(fenetre, text='Jeu par :\nJean Salomon\nIsidore Billard\nElliot Goralczyk') # les crédits du jeu
rick_roll_button = tk.Button(fenetre, text='La Curiosité est un vilain défaut', command = lambda : webbrowser.open('https://www.youtube.com/watch?v=xvFZjo5PgG0'))
b_tuto = tk.Button(fenetre, text='Tuto', command = tuto)    # bouton du tutoriel
# boutons thème
b_dark = tk.Button(fenetre, text='Thème foncé', bg='#AAAAAA',command = dark)
b_white = tk.Button(fenetre, text='Thème clair', command = light)
# boutons déroulants définissant la taille de la fenêtre
text_taille_fenetre = tk.Label(fenetre, text='Taille de la Fenêtre')
vert_slider = tk.Scale(fenetre, from_=800, to=2000, orient='horizontal')
hori_slider = tk.Scale(fenetre, from_=660, to=1020, orient='horizontal')
# bouton qui valide la taille de la fenêtre
save = tk.Button(fenetre, text='Sauvegarder', command = lambda : fenetre.geometry(str(vert_slider.get()) + 'x' + str(hori_slider.get())))

#------éléments tuto------
text_tuto = tk.Label(fenetre, text='TUTO', font=('bold', 25))
frame_tuto = tk.LabelFrame(fenetre, bg='#ABE0FF', width=500,height=1000)
img1 = ImageTk.PhotoImage(Image.open('img1.PNG'))
img1_tuto = tk.Label(frame_tuto, image = img1)
img2 = ImageTk.PhotoImage(Image.open('img2.PNG'))
img2_tuto = tk.Label(frame_tuto, image = img2)
exp_tuto1 = tk.Label(frame_tuto, bg='#ABE0FF', text='La difficulté change la longueur du mot à deviner :\nFacile : 1 à 4 lettres\nMoyen : 5 à 8 lettres\nDifficile : 9+ lettres')

#--------------------lancement des fonctions--------------------------
menu()               # lance le menu
l_tuto.pack(side='bottom', pady=20)  # ajoute le rappel du tutoriel
code_principal()     # lance le code principal chargé de constamment vérifier l'état du jeu
fenetre.mainloop()   # boucle "d'animation"