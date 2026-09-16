# Outil de chiffrement de Vigenère

Implémentation en Python du chiffrement de Vigenère, avec application sur du texte
saisi au clavier, sur un fichier ou sur un répertoire complet.

Projet réalisé dans un cadre scolaire. Le chiffre de Vigenère est cassé depuis le
XIXᵉ siècle : cet outil est un exercice d'algorithmique et de manipulation de
fichiers, **pas un moyen de protéger des données réelles**. Voir la section
[Limites](#limites).

---

## Fonctionnement

Le chiffrement repose sur la table de Vigenère : une matrice 26×26 où chaque ligne
est l'alphabet décalé d'un cran par rapport à la précédente. Pour chaque lettre du
message, on croise la ligne de la lettre claire avec la colonne de la lettre
courante de la clé ; le caractère à l'intersection est la lettre chiffrée.

La clé est répétée cycliquement sur toute la longueur du message. Le déchiffrement
fait l'opération inverse : on cherche, dans la colonne de la lettre de clé, la
position du caractère chiffré, et on remonte à la lettre claire en tête de ligne.

## Utilisation

```bash
python main.py
```

ou via le script fourni :

```bash
chmod +x application.sh
./application.sh
```

Le programme se déroule en trois étapes :

1. **Clé** — génération aléatoire (8 caractères minimum) ou saisie manuelle.
   Une clé générée peut être sauvegardée dans `cle.txt`.
2. **Action** — chiffrer ou déchiffrer.
3. **Support** — texte saisi dans le terminal, fichier unique, ou répertoire complet.

### Exemple

```
Clé      : maclesecrete
Message  : bonjour tout le monde
Chiffré  : nopusmv ksnx lg qgrfv
```

## Structure

| Fichier | Rôle |
|---|---|
| `main.py` | Programme complet : matrice, chiffrement, déchiffrement, gestion des fichiers, interface en ligne de commande |
| `application.sh` | Script de lancement |
| `cle.txt` | Clé sauvegardée lors d'une génération aléatoire |

### Principales fonctions

- `alphabet()` — construit la matrice de Vigenère 26×26
- `chiffrement(tab, message, cle)` / `dechiffrement(tab, code, cle)` — cœur de l'algorithme
- `generer_cle(longueur)` — génère une clé aléatoire en minuscules
- `trouver_chemin_fichier(nom, dossier)` — recherche récursive d'un fichier
- `chiffrerFich()` / `dechiffrerFich()` — traitement d'un fichier, écriture sur place
- `chifrepertoire()` / `dechifrepertoire()` — traitement récursif d'un répertoire

---

## Limites

**Sécurité.** Vigenère est vulnérable à l'analyse de Kasiski et au test de
Friedman : dès que le texte est long par rapport à la clé, la longueur de celle-ci
se déduit des répétitions dans le chiffré, et chaque position se ramène alors à un
simple chiffre de César, cassable par analyse fréquentielle. Aucune protection
d'intégrité n'est présente non plus. Pour du chiffrement réel, utiliser une
primitive authentifiée (AES-GCM, ChaCha20-Poly1305) via une bibliothèque éprouvée.

**Perte d'information.** Le message est passé en minuscules avant traitement : la
casse d'origine n'est pas restituée au déchiffrement.

**Caractères non alphabétiques.** Les espaces, la ponctuation et les caractères
accentués sont recopiés tels quels. Sur du texte français, les accents laissent
donc apparaître une partie de la structure du message clair.

**Position de la clé.** Le compteur de clé avance sur *tous* les caractères, y
compris les espaces et la ponctuation, et non uniquement sur les lettres. Le
comportement reste cohérent entre chiffrement et déchiffrement, mais diffère du
Vigenère classique : les messages ne sont pas interopérables avec une autre
implémentation.

**Recherche de fichier par nom.** Si l'argument fourni n'est pas un chemin
existant, `chiffrerFich()` recherche un fichier de ce nom depuis le dossier
utilisateur et retient la première correspondance. Préférer un chemin explicite
pour éviter de tomber sur un homonyme.

**Perte de la clé.** Le fichier source n'étant pas supprimé, aucune donnée n'est
perdue en cas de clé oubliée — mais le `.vig` correspondant devient inexploitable.

## Traitement des fichiers

Le fichier source n'est jamais écrasé :

- **Chiffrement** — le résultat est écrit dans `<fichier>.vig`
- **Déchiffrement** — l'extension `.vig` est retirée ; à défaut, le résultat est
  écrit dans `<fichier>.clair`
- Si le fichier de sortie existe déjà, rien n'est écrit
- En mode répertoire, les `.vig` sont ignorés au chiffrement, et seuls les `.vig`
  sont traités au déchiffrement

## Pistes d'amélioration

- Préserver la casse et gérer les caractères accentués
- Séparer la logique de l'interface et ajouter des tests unitaires sur le
  round-trip chiffrement/déchiffrement
