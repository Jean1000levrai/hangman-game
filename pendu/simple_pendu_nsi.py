# Jean Salomon, Isidore Billard, Elliot Goralczyk
import tkinter as tk
import unidecode

def code_principal():
    """fonction principale du code qui vérifie l'état du jeu et s'occupe d'appeler les autes fonctions, c'est le cerveau du code"""
    fenetre.after(50, code_principal) # on appelle la fonction principale pour qu'elle tourne en boucle    
    def etat_du_jeu():
        '''fonction qui vérifie constament l'état du jeu et est appelé dans code_principal'''
        global etat_jeu, numero_pendu
        # si tout les traits du pendu sont tirés : perdu
        if numero_pendu == 10:
            etat_jeu = 2    # met l'état du jeu à 2 soit perdu
            perdu()         # appelle la fonction perdu
            zoneDeTexte.config(state='disabled')    # empêche à l'utilisateur de continuer lors de la fin de la partie
        # si il n'y a plus de "_" dans la proposition soit le mot est trouvé : gagné
        elif '_' not in proposition:
            etat_jeu = 1    # met l'état du jeu à 1 soit gagner
            gagner()        # appelle la fonction gagner
            zoneDeTexte.config(state='disabled')    # empêche à l'utilisateur de continuer lors de la fin de la partie
    def perdu():
        """fonction qui intervient si etat_jeu = 2, soit on a perdu"""
        defaite = toile.create_text(400,200, text = "Vous avez perdu !", font=('Comic Sans MS', 48), fill='red')    # Affiche sur le canva le texte de défaite
    def gagner():
        """foncton qui intervient en cas de victoire du joueur, soit si etat_jeu = 1"""
        victoire = toile.create_text(400,200, text = 'Vous avez gagné !', font=('Impact', 48), fill='green')            # Affiche sur le canva le texte de victoire
    etat_du_jeu()   # vérifie l'état du jeu

def traiter_lettre(*args):
    """fonction appelée lorsque la touche "return" est enfoncée. La fonction récupère ce qui a été écrit dans la zone de saisie
    et le traite pour ajouter une lettre dans la variable globale "proposition" ou pour ajouter un élément au pendu"""
    global lettres_utilisees, proposition, numero_pendu
    l = zoneDeTexte.get().lower().strip()# on récupère ce qui a été entré dans la zone de saisie
    zoneDeTexte.delete(0, 'end')         # on efface le contenu de la zone de saisie
    list_mot_secret = list(mot_secret)  # crée une liste du mot secret, utile pour vérifier chaque lettre
    lettre_valide = False   # variable permettant de savoir si la lettre peut être validée ou pas pour soit tirer un trait ou soit remplir la proposition
    # si la lettre a déjà été utilisé : 
    if l in lettres_utilisees:
        texte.config(text='Déjà Utilisé ;(')    # change le texte d'indication pour afficher une erreur
        fenetre.after(2000, lambda : texte.config(text='Choisir une lettre et appuyer sur la touche Entrée'))   # retourne à sa phrase d'origine au bout de 2 sec
    # si il y a plusieurs lettres entrées :
    elif len(l) > 1:
        texte.config(text='Il faut marquer seulement une lettre')    # change le texte d'indication pour afficher une erreur
        fenetre.after(2000, lambda : texte.config(text='Choisir une lettre et appuyer sur la touche Entrée'))   # retourne à sa phrase d'origine au bout de 2 sec
    # si ce n'est pas une lettre :
    elif l.isalpha() == False: 
        texte.config(text="C'est un nombre, il faut une lettre")    # change le texte d'indication pour afficher une erreur
        fenetre.after(2000, lambda : texte.config(text='Choisir une lettre et appuyer sur la touche Entrée'))   # retourne à sa phrase d'origine au bout de 2 sec
    # si la lettre est juste :
    elif l in list_mot_secret:
        # regarde si la lettre (l) entrée est juste sur chacune des lettres du mot secret (sous forme de liste) et ajoute le nombre correspondant aux indices presents dans le mot secret à cette liste
        list2 = [i for i in range(len(list_mot_secret)) if list_mot_secret[i] == l]
        # boucle le même nombre de fois qu'il y a de lettres justes entrée dans le mot secret
        for index in list2:
            proposition[index] = l  # remplace la lettre à l'indice correspondant dans la proposition
        toile.itemconfig(indice,text = str(" ".join(proposition)))  # met à jour la proposition sur la toile
        lettre_valide = True    # valide la lettre pour être ajoutée aux lettres utilisées
    # si la lettre est fausse et n'a pas déjà été utilisée :
    elif l not in mot_secret and l not in lettres_utilisees:
        dessiner_pendu(liste_traits_pendu)  # dessine nu trait au pendu
        numero_pendu += 1   # ajoute 1 au numero du pendu
        lettre_valide = True    # valide la lettre pour être ajoutée aux lettres utilisées
    # si la lettre n'a pas déjà été utilisée :
    if lettre_valide == True:
        lettres_utilisees.append(l) # rajoute la lettre aux lettres utilisées
        toile.itemconfig(label_lettres_utilisees, text = " ".join(sorted(lettres_utilisees)))   # l'actualise sur la toile
        lettre_valide = False   # remet cette variable fausse pour ne pas que les futures lettres(probablement fausses) soit valides

def dessiner_pendu(l):
    """fonction qui gère l'évolution du pendu"""
    global numero_pendu, etat_jeu
    # Verifie que le jeu est en cours
    if etat_jeu==0:
        # Vérifie si il faut tracer un trait ou une ellipse
        if l[numero_pendu][0]==1: 
            line=toile.create_line(l[numero_pendu][1][0],l[numero_pendu][1][1],l[numero_pendu][2][0],l[numero_pendu][2][1])     # Trace le trait
        else:
            line=toile.create_oval(l[numero_pendu][1][0],l[numero_pendu][1][1],l[numero_pendu][2][0],l[numero_pendu][2][1])     #Trace l'ellipse


#------------------variables globales-----------------------------
liste_traits_pendu=[[1,(100,400),(300,400)],[1,(200,400),(200,50)],[1,(200,50),(400,50)],[1,(200,125),(275,50)],
[1,(400,50),(400,125)],[2,(375,125),(425,175)],[1,(400,175),(400,250)],[1,(350,200),(450,200)],[1,(400,250),(375,325)],[1,(400,250),(425,325)]]
        # liste de tous les traits du pendu. Un trait est représenté par une liste composée d'un entier et de deux tuples :
        # l'entier sera : 1 pour indiquer que l'on doit tracer un segment ou 2 pour indiquer que l'on doit tracer un cercle
        # les deux tuples correspondent aux coordonnées des deux points qui permettent de caractériser le segment ou le cercle à tracer
mot_secret = unidecode.unidecode(input('Quel est le mot secret ?').strip().lower()) # demande à l'utilisateur un mot à faire deviner (les accents, espaces et majuscules seront remplacés)
nbr_lettres=len(mot_secret) # on récupère le nombre de caractères du mot secret
lettres_utilisees=[]     # liste des lettres déjà proposées par le joueur. Cette liste sera affichée pour que le joueur puisse la consulter
numero_pendu=0           # cette variable permet de savoir combien de traits ont déjà été tracés pour le pendu (au bout de 10 : perdu)
etat_jeu=0               # variable qui donne l'état du jeu : 0 =en cours, 1=gagné, 2=perdu.
proposition=["_" for i in range(len(mot_secret))]   # crée la proposition d'autant de tiret que de lettre du mot secret

#----------------éléments de la fenêtre-----------------------
fenetre=tk.Tk()                 # création de la fenêtre
zoneDeTexte = tk.Entry(fenetre) # met en place une zone de texte vide
zoneDeTexte.bind('<Return>', traiter_lettre)  # assigne la touche 'Entrée' à la zone de texte et appelle la fonction traiter_lettre pour traiter la lettre
toile = tk.Canvas(fenetre, width=800, height=500, bg='white')   # création de la toile
bouton = tk.Button(fenetre, text='Quitter', command = fenetre.destroy)  # met en place le bouton quitter
texte = tk.Label(fenetre, text='Choisir une lettre et appuyer sur la touche Entrée', font=('bold', 16))    # met en place le texte d'indication pour le joueur

#-----------------------mise en place des éléments de la fenetre-----------------

toile.pack()    # on ajoute la toile à la fenêtre
texte.pack()    # on ajoute le texte d'indication pour le joueur à la fenêtre
zoneDeTexte.pack()  # on ajoute la zone de texte à la fenêtre
bouton.pack()   # on ajoute le bouton quitter à la fenêtre
indice = toile.create_text(400,430, text = str(" ".join(proposition)), font=("Courier",30)) # on ajoute la proposition à la toile qui sera actualisée tout au long de la partie
label_lettres_utilisees = toile.create_text(400,480, text = " ".join(lettres_utilisees), fill = 'blue', font=("courrier",22))    # on ajoute les lettres utilisées à la toile qui sera actualisée tout au long de la partie

#----------------lancement des fonctions-----------------------
if len(mot_secret)>17 or mot_secret.isalpha() == False:
    print('mot non valide')
    fenetre.destroy()
code_principal()    # appelle le code principal
fenetre.mainloop()  # boucle "d'animation"