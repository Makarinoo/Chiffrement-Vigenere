import random
import os 

#alpha et alphamaj utilisé dans trad
alphamin = "abcdefghijklmnopqrstuvwxyz"
alphamaj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

EXT_CHIFFRE = ".vig"

#init d'un alphabet et d'une tab vide qui va créer la matrice
alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
tab = []

#___________________________________________________________________________________________#
#                                     fonctions                                             #
#___________________________________________________________________________________________#

#------------------------------------------------------#
#                        alphabet                      #
#------------------------------------------------------#

def alphabet():
    """
    Initialise la matrice de Vigenère (variable globale 'tab').
    
    Crée une liste de listes (26x26) où chaque ligne correspond à l'alphabet
    décalé d'un cran vers la gauche par rapport à la ligne précédente.
    
    Returns:
        list: La matrice de Vigenère complète (tableau de tableaux).
    """
    global tab # pour modifier la variable tab definit à l'extérieur de la fonction
    tab = []   # reset de tab à chaque appel de la fonction
    
    # Ajout de la première ligne
    tab.append(alpha)
    
    cpt = 0
    #construit les 25 autres lignes avec décalage
    for y in range(len(alpha)-1):
        cpt +=1
        tab.append(alpha[cpt:]+alpha[:cpt])
    return tab

def affiche(tab):
    """
    Affiche la matrice de Vigenère dans la console.
    
    Args:
        tab (list): La matrice de Vigenère à afficher.
    """
    for i in range(len(tab)):
        for y in range(len(tab[i])):
            print(tab[i][y],end='')
        print("")

#---------------------------------------------------------#
#                      traduire                           #
#---------------------------------------------------------#

def trad(message):
    """
    Normalise le message en le convertissant en minuscules.
    
    Args:
        message (str): La chaîne de caractères à traiter.
        
    Returns:
        str: La chaîne convertie en minuscules.
    """
    return message.lower()

#---------------------------------------------------------#
#                      indice                             #
#---------------------------------------------------------#

def indiceCol(tab,cle):
    """
    Trouve l'index de colonne correspondant à la première lettre de la clé.
    
    Args:
        tab (list): La matrice de Vigenère.
        cle (str): La lettre de la clé (ou chaîne dont on prend le 1er caractère).
        
    Returns:
        int or None: L'index de la colonne si trouvé, sinon None.
    """
    # Sécurité : si la clé est vide ou invalide
    if not cle: return 0
    
    for i  in range(len(tab[0])):
        if cle[0] == tab[0][i]:
            return i
    return None # Retourne None si pas trouvé

def indiceLig(tab,message):
    """
    Trouve l'index de ligne correspondant à la première lettre du message.
    
    Args:
        tab (list): La matrice de Vigenère.
        message (str): La lettre du message (ou chaîne dont on prend le 1er caractère).
        
    Returns:
        int or None: L'index de la ligne si trouvé, sinon None.
    """
    if not message: return 0
    
    for i in range(len(tab)):
            if message[0] == tab[i][0]:
                return i
    return None

#--------------------------------------------------------#
#                chiffrement dechiffrement               #
#--------------------------------------------------------#

def chiffrement(tab, message, cle):
    """
    Chiffre un message selon le code de Vigenère.
    
    Parcourt le message caractère par caractère. Si le caractère est alphabétique,
    il est chiffré en croisant la ligne du message et la colonne de la clé.
    Les caractères non-alphabétiques sont conservés tels quels.
    
    Args:
        tab (list): La matrice de Vigenère.
        message (str): Le texte clair à chiffrer.
        cle (str): La clé de chiffrement.
        
    Returns:
        str: Le message chiffré.
    """
    code = ""
    cpt = 0
    
    # Protection si tab est vide
    if not tab:
        return message

    alphabet_ref = tab[0] 

    while len(message) > 0:
        caractere_actuel = message[0]

        # VERIFICATION :
        if (caractere_actuel in alphabet_ref) and caractere_actuel.isalpha():
            
            lettreAct = cle[cpt % len(cle)]
            idx_lig = indiceLig(tab, caractere_actuel)
            idx_col = indiceCol(tab, lettreAct)
            
            if idx_lig is not None and idx_col is not None:
                code += tab[idx_lig][idx_col]
            else:
                code += caractere_actuel 
        else:
            code += caractere_actuel
            
        message = message[1:]
        cpt += 1 
        
    return code

def dechiffrement(tab, code, cle):
    """
    Déchiffre un message codé avec Vigenère.
    
    Pour chaque caractère chiffré, la fonction repère la colonne correspondant
    à la lettre de la clé actuelle, cherche le caractère chiffré dans cette colonne,
    et en déduit la ligne (lettre claire) correspondante.
    
    Args:
        tab (list): La matrice de Vigenère.
        code (str): Le texte chiffré.
        cle (str): La clé utilisée pour le chiffrement.
        
    Returns:
        str: Le message déchiffré (texte clair).
    """
    message_clair = ""
    cpt = 0
    
    if not tab: return code
    alphabet_ref = tab[0]

    while len(code) > 0:
        caractere_actuel = code[0]
        
        # Même logique que le chiffrement : on ne traite que les lettres connues
        if (caractere_actuel in alphabet_ref) and caractere_actuel.isalpha():
            
            lettreAct = cle[cpt % len(cle)]
            colonne_cle = indiceCol(tab, lettreAct) 

            if colonne_cle is not None:
                found = False
                for i in range(len(tab)):
                    if tab[i][colonne_cle] == caractere_actuel:
                        message_clair += tab[i][0] 
                        found = True
                        break
                if not found:
                    message_clair += caractere_actuel
            else:
                message_clair += caractere_actuel
        else:
            message_clair += caractere_actuel

        code = code[1:]
        cpt += 1
        
    return message_clair

#--------------------------------------------------------------#
#                cle aleatoire                                 #
#--------------------------------------------------------------#
    
def generer_cle(longueur):
    """
    Génère une clé aléatoire composée de lettres minuscules.
    
    Args:
        longueur (int): La taille souhaitée pour la clé.
        
    Returns:
        str: La clé générée.
        None: Si la longueur demandée est inférieure à 8.
    """
    key = []
    i = 0
    if longueur < 8:
        print("La clé doit faire au minimum 8 lettres")
        return None
    
    while i < longueur:
        lettre = random.choice(alphamin)
        key.append(lettre) 
        i = i + 1
    return ''.join(key)

def chemin_cle_txt() -> str:
    """
    Retourne le chemin de 'cle.txt', situé à côté du script.
    
    Returns:
        str: Le chemin absolu du fichier de clé.
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "cle.txt")


def charger_cle() -> str:
    """
    Lit la clé sauvegardée dans 'cle.txt'.
    
    Returns:
        str: La clé lue, en minuscules.
        None: Si le fichier est absent, vide ou illisible.
    """
    chemin = chemin_cle_txt()
    try:
        with open(chemin, "rt", encoding='utf-8') as f:
            cle_lue = trad(f.read().strip())
        if not cle_lue:
            print(f"Le fichier '{chemin}' est vide.")
            return None
        return cle_lue
    except FileNotFoundError:
        print(f"Aucune clé sauvegardée : '{chemin}' est introuvable.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture de la clé : {e}")
        return None

#______________________________________________________________________________________________#
#                               modifier fichier / repertoire                                  #
#______________________________________________________________________________________________#

def trouver_chemin_fichier(nom_fich: str, dossier_depart: str = None) -> str:
    """
    Recherche récursivement un fichier dans un dossier donné.
    
    Args:
        nom_fich (str): Le nom du fichier à trouver (avec extension).
        dossier_depart (str, optional): Le chemin du dossier racine de la recherche. 
                                        Par défaut, le dossier utilisateur.
                                        
    Returns:
        str: Le chemin absolu complet vers le fichier s'il est trouvé.
        None: Si le fichier n'est pas trouvé.
    """
    if os.path.isfile(nom_fich):
        return os.path.abspath(nom_fich)

    if dossier_depart is None:
        dossier_depart = os.path.expanduser("~") #dossier utilisateur par défaut

    print(f"Recherche de '{nom_fich}' dans '{dossier_depart}'")
    

    for root, dirs, files in os.walk(dossier_depart):
        if nom_fich in files:
            chemin_complet = os.path.join(root, nom_fich)
            print(f"Fichier trouvé : {chemin_complet}")
            return chemin_complet
            
    return None


def chiffrerFich(nom_fich: str, cle: str) -> list:
    """
    Localise un fichier, lit son contenu, le chiffre et écrase le fichier original.
    
    Args:
        nom_fich (str): Le nom du fichier cible.
        cle (str): La clé de chiffrement.
        
    Returns:
        list: La liste des lignes chiffrées (ou liste vide en cas d'erreur).
    """
    chemin_complet = trouver_chemin_fichier(nom_fich)
    
    if chemin_complet is None:
        print(f"Erreur : Le fichier '{nom_fich}' est introuvable.")
        return []

    listChif = []

    try:
        # Lecture
        with open(chemin_complet, 'rt', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Chiffrement
        for line in lines:
            # On passe la ligne en minuscule avant de chiffrer
            ligne_minuscule = trad(line) 
            listChif.append(chiffrement(tab, ligne_minuscule, cle)) 

        chemin_sortie = chemin_complet + EXT_CHIFFRE

        if os.path.exists(chemin_sortie):
            print(f"'{chemin_sortie}' existe déjà : rien n'a été écrit.")
            return []

        with open(chemin_sortie, 'wt', encoding='utf-8') as fread:
            fread.writelines(listChif) 
            
        print(f"Fichier chiffré avec succès : {chemin_sortie}")
        return listChif

    except Exception as e:
        print(f"Une erreur est survenue pendant le chiffrement : {e}")
        return []


def dechiffrerFich(nom_fich: str, cle: str) -> list:
    """
    Localise un fichier, lit son contenu chiffré, le déchiffre et écrase le fichier.
    
    Args:
        nom_fich (str): Le nom du fichier cible.
        cle (str): La clé de déchiffrement.
        
    Returns:
        list: La liste des lignes déchiffrées (ou liste vide en cas d'erreur).
    """
    chemin_complet = trouver_chemin_fichier(nom_fich)
    
    if chemin_complet is None:
        print(f"Erreur : Le fichier '{nom_fich}' est introuvable.")
        return []
        
    listClair = []
    
    try:
        with open(chemin_complet, 'rt', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            listClair.append(dechiffrement(tab, line, cle))
            
        if chemin_complet.endswith(EXT_CHIFFRE):
            chemin_sortie = chemin_complet[:-len(EXT_CHIFFRE)]
        else:
            chemin_sortie = chemin_complet + ".clair"

        if os.path.exists(chemin_sortie):
            print(f"'{chemin_sortie}' existe déjà : rien n'a été écrit.")
            return []

        with open(chemin_sortie, 'wt', encoding='utf-8') as fread:
            fread.writelines(listClair)
            
        print(f"Fichier déchiffré avec succès : {chemin_sortie}")
        return listClair
    except Exception as e:
        print(f"Erreur déchiffrement: {e}")
        return []
    
def chifrepertoire(dossier: str, cle: str):
    """
    Parcourt un répertoire complet et chiffre tous les fichiers qu'il contient.
    
    Args:
        dossier (str): Le chemin du répertoire à traiter.
        cle (str): La clé de chiffrement.
    """
    for root, dirs, files in os.walk(dossier):
        for file in files:
            if file.endswith(EXT_CHIFFRE):
                continue
            chiffrerFich(os.path.join(root, file), cle)
            
            
def dechifrepertoire(dossier: str, cle: str):
    """
    Parcourt un répertoire complet et déchiffre tous les fichiers qu'il contient.
    
    Args:
        dossier (str): Le chemin du répertoire à traiter.
        cle (str): La clé de déchiffrement.
    """
    for root, dirs, files in os.walk(dossier):
        for file in files:
            if not file.endswith(EXT_CHIFFRE):
                continue
            dechiffrerFich(os.path.join(root, file), cle)

#______________________________________________________________________________________________#
#                                       MAIN                                                   #
#______________________________________________________________________________________________#

# 1.initialisation de la table de Vigenère
alphabet() 
    
print("##############################################")
print("#           OUTIL DE CHIFFREMENT             #")
print("##############################################")

# --- ÉTAPE 1 : GESTION DE LA CLÉ ---
print("\n--- GESTION DE LA CLÉ ---")
print("1. Générer une clé aléatoire")
print("2. Saisir une clé manuellement")
print("3. Charger la clé depuis 'cle.txt'")
choix_cle = input("Votre choix (1, 2 ou 3) : ")
    
cle = ""
    
if choix_cle == '1':
    try:
        longueur = int(input("Entrez la longueur de la clé (minimum 8) : "))
        cle = generer_cle(longueur)
        if cle:
            print(f"--> Votre clé générée est : {cle}")
            
            # --- SAUVEGARDE CLÉ ---
            save = input("Voulez-vous enregistrer cette clé dans 'cle.txt' ? (o/n) : ")
            if save.lower() == 'o':
                try:
                    chemin_cle = chemin_cle_txt()
                    with open(chemin_cle, "wt", encoding='utf-8') as f:
                        f.write(cle)
                    print(f"-> Clé sauvegardée ici : {chemin_cle}")
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde : {e}")
            # ----------------------
            
        else:
            exit() 
    except ValueError:
        print("Erreur : Veuillez entrer un nombre entier.")
        exit()
            
elif choix_cle == '2':
    cle = input("Entrez votre clé : ")
    cle = trad(cle)
elif choix_cle == '3':
    cle = charger_cle()
    if not cle:
        exit()
    print(f"--> Clé chargée : {cle}")
else:
    print("Choix invalide.")
    exit()

# --- ÉTAPE 2 : CHOIX DE L'ACTION ---
print("\n--- ACTION ---")
print("1. Chiffrer")
print("2. Déchiffrer")
choix_action = input("Votre choix (1 ou 2) : ")
    
if choix_action not in ['1', '2']:
    print("Choix invalide.")
    exit()

# --- ÉTAPE 3 : CHOIX DU SUPPORT ---
print("\n--- SUPPORT ---")
print("1. Dans le terminal (texte direct)")
print("2. Sur un fichier unique")
print("3. Sur un répertoire complet (tous les fichiers)") # NOUVEAU CHOIX
choix_support = input("Votre choix (1, 2 ou 3) : ")

# --- EXÉCUTION ---
if choix_support == '1':
    # Mode Terminal
    texte = input("\nEntrez le message : ")
    texte_traite = trad(texte)
        
    if choix_action == '1':
        resultat = chiffrement(tab, texte_traite, cle)
        print(f"\n[RÉSULTAT CHIFFRÉ] : {resultat}")
    else:
        resultat = dechiffrement(tab, texte_traite, cle)
        print(f"\n[RÉSULTAT DÉCHIFFRÉ] : {resultat}")
            
elif choix_support == '2':
    # Mode Fichier Unique
    nom_fich = input("\nEntrez le nom du fichier (ex: mon_texte.txt) : ")
    print("Traitement en cours...")
        
    if choix_action == '1':
        chiffrerFich(nom_fich, cle)
    else:
        dechiffrerFich(nom_fich, cle)

elif choix_support == '3':
    # Mode Répertoire Complet
    dossier = input("\nEntrez le chemin du dossier : ")
    print("Traitement en cours... (Cela peut être long)")
    
    if choix_action == '1':
        chifrepertoire(dossier, cle)
    else:
        dechifrepertoire(dossier, cle)
            
else:
    print("Choix de support invalide.")