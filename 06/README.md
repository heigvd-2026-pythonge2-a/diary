# Semaine 06/16

- [x] Fonction de hachage
- [x] Git

## Fonction de hachage

### L'idée

Une fonction de hachage prend en entrée des données de **taille quelconque** (un mot, un fichier de 10 Go, une image...) et produit en sortie une valeur de **taille fixe**, appelée *empreinte* (ou *hash*, ou *condensat*). On peut la voir comme une empreinte digitale: elle est courte, elle identifie quasiment à coup sûr son propriétaire, mais elle ne permet pas de le reconstituer.

Essayons en Python avec le module standard `hashlib`:

```python
>>> import hashlib
>>> hashlib.sha256(b"Hello World").hexdigest()
'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
>>> hashlib.sha256(b"Hello World!").hexdigest()
'7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069'
```

Quatre propriétés sont importantes à retenir:

1. **Déterministe**: la même entrée donne toujours la même empreinte.
2. **Taille fixe**: SHA-256 produit toujours 256 bits (64 caractères hexadécimaux), que l'entrée fasse 1 octet ou 1 To.
3. **Effet avalanche**: un seul caractère de différence (le `!` ci-dessus) change complètement l'empreinte. Impossible de deviner que les deux entrées se ressemblent.
4. **À sens unique**: calculer l'empreinte est rapide, mais retrouver l'entrée à partir de l'empreinte est en pratique impossible.

Pourquoi est-ce impossible de revenir en arrière ? Parce que la fonction n'est pas **bijective**: il existe une infinité d'entrées possibles mais seulement $2^{256}$ sorties. Plusieurs entrées différentes partagent donc forcément la même empreinte (on parle de *collision*). Il n'y a pas « une » entrée à retrouver, et une bonne fonction de hachage est justement conçue pour qu'on ne puisse pas en fabriquer une volontairement.

### Les fonctions courantes

| Fonction | Taille de l'empreinte | Statut |
|----------|-----------------------|--------|
| [MD5](https://fr.wikipedia.org/wiki/MD5) (RFC [1321](https://www.rfc-editor.org/rfc/rfc1321)) | 128 bits | Cassée, à éviter pour la sécurité |
| [SHA-1](https://fr.wikipedia.org/wiki/SHA-1) (RFC [3174](https://www.rfc-editor.org/rfc/rfc3174)) | 160 bits | Cassée, encore utilisée par Git |
| [SHA-256](https://fr.wikipedia.org/wiki/SHA-2) (RFC [6234](https://www.rfc-editor.org/rfc/rfc6234)) | 256 bits | Standard actuel |
| [SHA-512](https://fr.wikipedia.org/wiki/SHA-2) | 512 bits | Standard actuel |
| [SHA-3](https://fr.wikipedia.org/wiki/SHA-3) | variable | Standard récent |
| [Blake2](https://fr.wikipedia.org/wiki/BLAKE_(fonction_de_hachage)) | variable | Rapide, moderne |

« Cassée » signifie qu'on sait fabriquer deux entrées différentes avec la même empreinte. Pour vérifier qu'un téléchargement n'est pas corrompu, MD5 suffit encore. Pour de la sécurité (mots de passe, signatures), il faut SHA-256 ou mieux.

### Comment ça marche à l'intérieur

Toutes ces fonctions suivent le même schéma:

1. On **complète** le message pour que sa longueur soit un multiple d'une taille de bloc (64 octets pour MD5).
2. On part d'un **état initial** fixé par la norme (quelques nombres de 32 bits).
3. On **mélange** chaque bloc du message avec l'état, en répétant des dizaines de fois des additions, des opérations logiques (ET, OU, OU-exclusif) et des rotations de bits.
4. L'état final, converti en hexadécimal, est l'empreinte.

Le but du mélange est que chaque bit de l'entrée influence tous les bits de la sortie. Voici une version jouet inspirée de MD5 (le vrai algorithme est dans [md5.py](md5.py), cette version simplifiée dans [mddummy.py](mddummy.py)). Inutile de comprendre chaque ligne: repérez simplement les 5 étapes numérotées dans les commentaires.

```python
def mddummy(message):
    """Hachage jouet inspiré de MD5. Didactique uniquement, aucune sécurité."""
    if isinstance(message, str):
        message = message.encode("utf-8")

    # Constantes définies dans la norme (ici une version réduite)
    MASK = 0xFFFFFFFF  # Pour rester sur 32 bits
    K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a]
    S = [7, 12, 17, 22, 5, 9]

    # 1. Remplissage : 0x80, des zéros, puis la longueur sur 8 octets
    length = (len(message) * 8).to_bytes(8, "little")
    message += b"\x80"
    message += b"\x00" * ((56 - len(message) % 64) % 64)
    message += length

    # 2. État initial : quatre registres de 32 bits
    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

    # 3. Traitement par blocs de 64 octets (16 mots de 32 bits)
    for off in range(0, len(message), 64):
        M = [int.from_bytes(message[off + 4 * j: off + 4 * j + 4], "little") for j in range(16)]
        A, B, C, D = a0, b0, c0, d0

        for i in range(64):
            # Une fonction booléenne différente par tour de 16 étapes
            if i < 16:
                F = (B & C) | (~B & D)
            elif i < 32:
                F = (D & B) | (~D & C)
            elif i < 48:
                F = B ^ C ^ D
            else:
                F = C ^ (B | (~D & MASK))

            # Mélange : addition, rotation, puis permutation des registres
            F = (F + A + K[i % 6] + M[i % 16]) & MASK
            s = S[i % 6]
            rot = ((F << s) | (F >> (32 - s))) & MASK
            A, B, C, D = D, (B + rot) & MASK, B, C

        # 4. On ajoute le résultat du bloc à l'état courant
        a0, b0, c0, d0 = [(x + y) & MASK for x, y in zip((a0, b0, c0, d0), (A, B, C, D))]

    # 5. Condensat : concaténation des quatre registres
    return b"".join(x.to_bytes(4, "little") for x in (a0, b0, c0, d0)).hex()
```

### En pratique dans un terminal

Les fonctions de hachage servent très souvent à vérifier l'**intégrité** d'un fichier: un site de téléchargement publie l'empreinte de son fichier, vous calculez celle du fichier reçu, et si les deux sont identiques le fichier n'a pas été altéré en route.

```bash
echo "Hello World" > test.txt
md5sum test.txt     # affiche le hash MD5 du fichier
sha1sum test.txt    # affiche le hash SHA-1 du fichier
sha256sum test.txt  # affiche le hash SHA-256 du fichier
```

```text
$ sha256sum test.txt
d2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26  test.txt
```

Modifiez une lettre dans `test.txt` et relancez la commande: l'empreinte est entièrement différente.

## Git

Pourquoi parler de hachage avant Git ? Parce que Git repose entièrement dessus. Beaucoup d'outils de gestion de versions numérotent les versions (v1, v2, v3...). Git fait autrement: **chaque contenu est identifié par son empreinte SHA-1**. Un fichier, un dossier ou un commit ont pour « nom » le hash de leur contenu. Deux conséquences:

- Deux machines qui ont le même contenu calculent le même identifiant, sans avoir besoin de se coordonner. C'est ce qui rend Git *distribué*.
- Si on modifie un contenu, son identifiant change. On ne peut donc pas altérer l'historique discrètement.

Les hash font 40 caractères hexadécimaux, mais Git accepte qu'on n'en tape que les premiers (en général 7 suffisent) tant qu'il n'y a pas d'ambiguïté.

### Plomberie Git

Pour comprendre comment Git stocke les choses, regardons ce qu'il écrit réellement sur le disque. Créons un dépôt vide:

```bash
mkdir project # On crée un dossier de projet
cd project    # On se place dans le dossier
git init      # On initialise un dépôt Git

rm -rf .git/hooks # On supprime les hooks qui ne nous intéressent pas ici
tree .git # On affiche l'arborescence du dossier .git
```

On obtient ceci:

```text
.git
├── config
├── description
├── HEAD
├── info
└── objects
    ├── info
    └── pack
```

Le dossier caché `.git` est la **base de données** de Git: tout l'historique du projet y sera stocké. Le dossier `project` est maintenant un **dépôt** Git (on dit aussi *référentiel* ou *repository*). Pour l'instant `objects` est vide. Ajoutons un fichier:

```bash
echo "Foo" > foo.txt     # On crée un fichier foo.txt
git add foo.txt          # On ajoute le fichier à l'index (il va être ajouté à la base de données)
tree .git/objects        # On affiche l'arborescence du dossier .git/objects
```

Un fichier est apparu dans `objects`:

```text
.git/objects
├── bc
│   └── 56c4d89448a963d0b6486989809d653dab9a97
├── info
└── pack
```

#### Le blob: le contenu d'un fichier

Ce fichier `bc/56c4d89448a963d0b6486989809d653dab9a97` est un **blob**. Il contient le contenu de `foo.txt`, et son nom est le hash SHA-1 de ce contenu (Git découpe le hash en `bc` + le reste pour ne pas avoir des milliers de fichiers dans un seul dossier).

Vérifions-le nous-mêmes. Attention, Git ne hache pas le contenu brut: il place devant un petit en-tête `blob <taille>\0` (le type d'objet, un espace, la taille en octets, puis un octet nul). Si on refait la même chose à la main, on retrouve exactement le même hash:

```bash
$ { printf 'blob %s\0' "$(wc -c < foo.txt)"; cat foo.txt; } | sha1sum
bc56c4d89448a963d0b6486989809d653dab9a97  -
```

Autre détail: le fichier stocké dans `.git/objects` est compressé avec zlib (le même algorithme que dans un `.zip`), c'est pourquoi on ne peut pas le lire avec `cat`. On peut le décompresser avec Python:

```python
$ python3 -c "import zlib; print(zlib.decompress(open('.git/objects/bc/56c4d89448a963d0b6486989809d653dab9a97', 'rb').read()))"

b'blob 4\x00Foo\n'
```

On retrouve bien l'en-tête `blob 4` suivi du contenu `Foo\n`. Le `4` est la taille du contenu: trois lettres plus le retour à la ligne ajouté par `echo`.

À retenir: **un blob, c'est le contenu d'un fichier, rien d'autre**. Il ne connaît ni son nom, ni sa date, ni son auteur.

#### Le tree et le commit

Faisons maintenant un commit:

```bash
git commit -m "Premier commit" # On fait un commit
tree .git/objects # On affiche l'arborescence du dossier .git/objects
```

Deux nouveaux objets sont apparus:

```text
.git/objects
├── 3c
│   └── ae430e9afab284dcebb550c84a6959b78706ca
├── 8f
│   └── 3761e066d5f3c0d3fa733fa2cb20e4806b952e
├── bc
│   └── 56c4d89448a963d0b6486989809d653dab9a97
├── info
└── pack
```

On connaît déjà `bc56c4`, c'est notre blob `Foo`. Pour lire les autres, plutôt que de décompresser à la main, Git fournit la commande `git cat-file -p` qui affiche n'importe quel objet de façon lisible:

```bash
$ git cat-file -p 8f37
100644 blob bc56c4d89448a963d0b6486989809d653dab9a97    foo.txt
```

Cet objet est un **tree** (arbre). Il représente un **dossier**: la liste de ses fichiers, avec pour chacun son nom, ses droits d'accès (`100644` = fichier normal) et le hash du blob qui contient son contenu. C'est lui qui fait le lien entre le nom `foo.txt` et le contenu `bc56c4`. Si le dossier contenait des sous-dossiers, le tree pointerait vers d'autres trees.

Le troisième objet est le **commit**:

```bash
$ git cat-file -p 3cae43
tree 8f3761e066d5f3c0d3fa733fa2cb20e4806b952e
author Yves Chevallier <yves.chevallier@heig-vd.ch> 1793029399 +0100
committer Yves Chevallier <yves.chevallier@heig-vd.ch> 1793029399 +0100

Premier commit
```

C'est aussi un simple fichier texte. Il contient le hash du tree racine (l'état complet du projet à cet instant), l'auteur, la date (en secondes depuis 1970) et le message. Les commits suivants contiendront en plus une ligne `parent` avec le hash du commit précédent: c'est ainsi que se forme l'historique, en chaîne.

#### Pourquoi l'historique est infalsifiable

Nos trois objets sont liés par leurs hash:

```text
commit 3cae43 --> tree 8f3761 --> blob bc56c4
```

| Objet | Ce qu'il représente | Ce qu'il contient |
|-------|---------------------|-------------------|
| blob | un fichier | le contenu brut |
| tree | un dossier | noms de fichiers → hash de blobs ou de trees |
| commit | une version du projet | hash du tree racine, auteur, date, message, hash du commit parent |

Imaginons qu'on veuille modifier `foo.txt` dans un ancien commit sans que personne ne s'en aperçoive. Le contenu change, donc le hash du blob change. Le tree contient ce hash, donc le tree change et son hash aussi. Le commit contient le hash du tree, donc le commit change à son tour, puis tous les commits qui le suivent. Toute modification du passé se propage jusqu'au présent et devient visible. C'est ainsi que Git garantit l'intégrité de l'historique.

### Fichiers de configuration

Git lit principalement deux fichiers de configuration:

`.git/config`
: configuration **locale** au dépôt. Elle contient les paramètres propres à ce projet: l'adresse du dépôt distant, les branches suivies, etc.

`~/.gitconfig`
: configuration **globale** de l'utilisateur. Elle s'applique à tous vos dépôts: votre nom, votre e-mail, votre éditeur, vos alias de commandes, etc.

Un paramètre local a priorité sur le même paramètre global. Votre fichier global ressemble à ceci:

```text
$ cat ~/.gitconfig
[user]
    name = Yves Chevallier
    email = yves.chevallier@heig-vd.ch
[core]
    editor = vim
[pull]
    rebase = true
[push]
    default = current
```

On y trouve le nom et l'e-mail qui apparaîtront dans la ligne `author` de vos commits, l'éditeur ouvert pour saisir les messages de commit, et le comportement par défaut de `git pull` et `git push`.

Les commandes suivantes, que vous avez sûrement déjà tapées, ne font rien d'autre qu'écrire dans ce fichier. Vous pouvez donc aussi l'éditer directement:

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@exemple.com"
```

### Commandes utiles

Pour comprendre les commandes, il faut avoir en tête les quatre zones entre lesquelles circulent vos modifications:

```text
 Répertoire de     git add      Index         git commit     Dépôt local    git push     Dépôt distant
 travail         ---------->  (staging)    ------------>   (.git)       ---------->   (GitHub, ...)
 (vos fichiers)                                                          <----------
                                                                          git fetch
```

- Le **répertoire de travail** contient les fichiers que vous éditez.
- L'**index** (ou *staging area*) est la liste de ce qui fera partie du prochain commit. Il permet de ne valider qu'une partie de vos modifications.
- Le **dépôt local** est la base de données `.git` vue plus haut.
- Le **dépôt distant** est une copie du dépôt sur un serveur, partagée avec les autres.

Les commandes de base, une par étape:

```text
git init    # Crée un nouveau dépôt Git dans le répertoire actuel (crée le dossier .git)
git status  # Affiche l'état du dépôt: fichiers modifiés, fichiers dans l'index, branche courante
git add     # Ajoute des fichiers à l'index pour les préparer à être commités
git commit  # Enregistre le contenu de l'index dans l'historique avec un message
git log     # Affiche l'historique des commits
git fetch   # Récupère les commits du dépôt distant sans toucher à votre branche locale
git push    # Envoie vos commits locaux vers le dépôt distant
```

En plus de cela, certaines commandes enchaînent plusieurs étapes en une seule:

```text
git clone <url>          # Copie un dépôt distant (git init + git remote add + git fetch + git checkout)
git pull                 # Récupère et intègre les commits distants (git fetch + git merge ou git rebase)
git commit -am "message" # git add de tous les fichiers déjà suivis puis commit (ne prend pas les nouveaux fichiers)
```

#### Dépôt distant

Pour travailler avec un dépôt distant (un dossier sur un serveur ou un service comme GitHub), il faut dire à Git où il se trouve avec `git remote add`:

```bash
git remote add origin <url>  # Ajoute un dépôt distant nommé "origin" avec l'URL spécifiée
git remote -v                # Affiche les dépôts distants configurés
```

`origin` est le nom conventionnel du dépôt distant principal (c'est celui que `git clone` crée automatiquement), mais vous pouvez en choisir un autre. L'URL peut être un chemin local ou une URL HTTPS ou SSH. Un même dépôt local peut avoir plusieurs dépôts distants, chacun avec un nom différent.

#### Synchroniser avec le dépôt distant

Une règle importante:

> Vous ne pouvez pas pousser vos commits si la branche distante contient des commits que vous n'avez pas. Dans ce cas, vous devez d'abord récupérer ces commits avec `git pull`, résoudre les éventuels conflits, puis pousser avec `git push`.

Cette situation arrive dès que vous êtes plusieurs: un collègue a poussé pendant que vous travailliez. Votre historique et le sien ont divergé à partir d'un commit commun:

```text
          A---B   (vous, en local)
         /
    ---o
         \
          C       (origin, poussé par un collègue)
```

Lors du `git pull`, Git doit réconcilier les deux. Il existe deux stratégies, et le fichier de configuration (section `[pull]`) choisit laquelle utiliser par défaut:

1. **merge**: crée un commit de fusion `M` avec deux parents. L'historique garde la trace de la divergence.

   ```text
             A---B---M
            /       /
       ---o--------C
   ```

2. **rebase**: déplace vos commits `A` et `B` pour les rejouer par dessus `C`. L'historique reste une ligne droite, comme si vous aviez commencé votre travail après votre collègue.

   ```text
       ---o---C---A'---B'
   ```

En règle générale, on préfère le rebase: il donne un historique linéaire, bien plus lisible. C'est pourquoi le `~/.gitconfig` plus haut contient `rebase = true`.

### Paramétrer Git

Le réglage le plus utile au quotidien est un alias pour obtenir un `log` plus lisible. Je vous recommande celui-ci:

```bash
git config --global alias.lg "log --graph --all --decorate --color=auto -n 30 --pretty=format:'%C(bold blue)%h%C(reset) %C(green)%<(14,trunc)%ar%C(reset) %s %C(auto)%d%C(dim white) - %an%C(reset)'"
```

Vous pouvez ensuite taper `git lg` à la place de `git log`: chaque commit tient sur une ligne, avec son hash court, son âge, son message, ses branches et son auteur, et les branches sont dessinées sous forme de graphe.
