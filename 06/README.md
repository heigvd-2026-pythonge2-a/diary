# Semaine 06/16

- [x] Fonction de hashage
- [x] Git

## Fonction de Hashage

Une fonction de hashage est une fonction qui prend en entrée des données de taille variable et produit une sortie de taille fixe, appelée "empreinte" ou "hash". Les fonctions de hashage sont largement utilisées en cryptographie, en sécurité informatique et dans les structures de données.

Il s'agit d'une transformation mathématique **non-bijective**. L'opération dans un sens est triviale et rapide, mais l'opération inverse est extrêmement difficle, voire impossible, car il existe une infinité de valeurs d'entrée possibles pour une valeur de sortie donnée.

Les fonctions de hachage les plus courantes sont:

- [MD5](https://fr.wikipedia.org/wiki/MD5) (RFC [1321](https://www.rfc-editor.org/rfc/rfc1321))
- [SHA-1](https://fr.wikipedia.org/wiki/SHA-1) (RFC [3174](https://www.rfc-editor.org/rfc/rfc3174))
- [SHA-256](https://fr.wikipedia.org/wiki/SHA-2) (RFC [6234](https://www.rfc-editor.org/rfc/rfc6234))
- [SHA-512](https://fr.wikipedia.org/wiki/SHA-2)
- [SHA-3](https://fr.wikipedia.org/wiki/SHA-3)
- [Blake2](https://fr.wikipedia.org/wiki/BLAKE_(fonction_de_hachage))

Elles fonctionnent toutes sur le même principe: elles prennent un message en entrée le mélangent avec des opérations logiques et arithmétiques pour produire un hash unique.

Par exemple une fonction simplifiée de hashage inspirée de MD5 pourrait ressembler à ceci:

```python
def mddummy(message):
    """Hachage jouet inspiré de MD5. Didactique uniquement, aucune sécurité."""
    if isinstance(message, str):
        message = message.encode("utf-8")

    # Valeurs uniques définie dans le protocole
    MASK = 0xFFFFFFFF
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

Dans un terminal Linux vous pouvez utiliser les fonctions de hachage pour vérifier l'intégrité d'un fichier:

```bash
echo "Hello World" > test.txt
md5sum test.txt # affiche le hash MD5 du fichier
sha1sum test.txt # affiche le hash SHA-1 du fichier
sha256sum test.txt # affiche le hash SHA-256 du fichier
```

## Git

Git est un système de contrôle de version distribué qui ne fonctionne pas sur une successions de numéro de versions. Au lieu de cela, Git utilise un système de hashage pour identifier de manière unique chaque état du projet. Chaque commit dans Git est identifié par un hash SHA-1, ce qui permet de garantir l'intégrité et la traçabilité des modifications.

### Plomberie Git

Prenons un exemple:

```bash
mkdir project # On crée un dossier de projet
cd project    # On se place dans le dossier
git init      # On initialise un dépôt Git

rm -rf .git/hooks # On supprime les hooks qui ne nous intéressent pas ici
tree .git # On affiche l'arborescence du dossier .git
```

On va obtenir ceci:

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

Il s'agit de la base de données Git. Le dossier `project` est maintnant un **référentiel** Git. Ajoutons un fichier à la base:

```bash
echo "Foo" > foo.txt     # On crée un fichier foo.txt
git add foo.txt          # On ajoute le fichier à l'index (il va être ajouté à la base de données)
tree .git/objects        # On affiche l'arborescence du dossier .git/objects
```

On observe qu'un fichier a été créé:

```text
.git/objects
├── bc
│   └── 56c4d89448a963d0b6486989809d653dab9a97
├── info
└── pack
```

Le fichier `bc/56c4d89448a963d0b6486989809d653dab9a97` est le **blob** qui contient le contenu du fichier `foo.txt`. Le nom du fichier est le hash SHA-1 du contenu du fichier. Pour vérifier cela, on peut calculer le hash du contenu de `foo.txt` mais Git ajoute devant le contenu un en-tête `blob <taille>\0`. Pour vérifier le hash, on peut utiliser la commande suivante:

```bash
$ { printf 'blob %s\0' "$(wc -c < foo.txt)"; cat foo.txt; } | sha1sum
bc56c4d89448a963d0b6486989809d653dab9a97  -
```

Autre détail le fichier stocké dans l'aborescence Git est compressé avec l'algorithme zlib (une sorte de .zip). Pour vérifier on peut décompresser le fichier avec Python:

```python
$ python3 -c "import zlib; print(zlib.decompress(open('.git/objects/bc/56c4d89448a963d0b6486989809d653dab9a97', 'rb').read()))"

b'blob 4\x00Foo\n'
```

On retrouve bien le contenu du fichier `foo.txt` précédé de l'en-tête `blob 4\0`. Le `4` correspond à la taille du contenu du fichier (4 octets pour "Foo\n").

Retenons simplement qu'un objet `blob` c'est le fichier lui-même.

Si on fait maintenant un `commit`:

```bash
git commit -m "Premier commit" # On fait un commit
tree .git/objects # On affiche l'arborescence du dossier .git/objects
```

On obtient:

```text
.git/objects
├── 3c
│   └── ae430e9afab284dcebb550c84a6959b78706ca
├── 8f
│   └── 3761e066d5f3c0d3fa733fa2cb20e4806b952e
├── bc
│   └── 56c4d89448a963d0b6486989809d653dab9a97
├── info
└── pack
```

On connaît déjà `bc/56c4d` c'est notre contenu `Foo`. La commande `git` `cat-file` permet de faire pour nous la décompression et afficher le contenu de l'objet, c'est plus simple:

```bash
$ git cat-file -p 8f37
100644 blob bc56c4d89448a963d0b6486989809d653dab9a97    foo.txt
```

Ce fichier est nommé un `tree` (arbre). Il contient la liste des fichiers d'un dossier. Il lie le nom du fichier `foo.txt` à son contenu via son hash `bc56c4`. Le `100644` est le mode du fichier (droits d'accès).

Enfin le troisième fichier est le `commit`:

```bash
$ git cat-file -p 3cae43
tree 8f3761e066d5f3c0d3fa733fa2cb20e4806b952e
author Yves Chevallier <yves.chevallier@heig-vd.ch> 1793029399 +0100
committer Yves Chevallier <yves.chevallier@heig-vd.ch> 1793029399 +0100

Premier commit
```

C'est donc aussi un fichier texte qui contient le hash du `tree`.

On a donc trois fichiers liés entre eux par des hash SHA-1:

```text
commit 3cae43 --> tree 8f3761 --> blob bc56c4
```

Si on change le contenu du fichier `foo.txt` le `tree` est corrompu donc il faut changer son hash, ce qui invalide le `commit`. C'est ainsi que Git garantit l'intégrité de l'historique des versions. Changer un fichier revient est donc impossible.

### Fichier de configuration

Git utilise principalement deux fichiers de configuration:

`.git/config`
: fichier de configuration local au dépôt Git. Il contient les paramètres spécifiques à ce dépôt, tels que les informations sur le dépôt distant, les branches, les hooks, etc.

`~/.gitconfig`
: fichier de configuration global pour l'utilisateur. Il contient les paramètres qui s'appliquent à tous les dépôts Git de l'utilisateur, tels que le nom d'utilisateur, l'adresse e-mail, les alias de commandes, etc.

Dans votre fichier global vous aurez par exemple:

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

Vous y retrouvez votre éditeur préféré pour les messages de commit, votre nom et votre email. Vous pouvez aussi configurer le comportement par défaut de `git pull` et `git push`.

Quand vous exécutez les commandes suivantes vous ne faites que modifier le fichier de configuration global `~/.gitconfig`:

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@exemple.com"
```

### Commandes utiles

Voici les commandes de base fondamentales pour travailler avec Git:

```text
git init    # Crée un nouveau dépôt Git dans le répertoire actuel (crée le dossier `.git`)
git fetch   # Récupère les modifications depuis le dépôt distant sans les fusionner avec votre branche locale.
git status  # Affiche l'état actuel du dépôt, y compris les fichiers modifiés, les fichiers en attente de commit et les branches.
git add     # Ajoute des fichiers à l'index (staging area) pour les préparer à être commités.
git commit  # Enregistre les modifications dans l'historique du dépôt avec un message de commit.
git push    # Envoie les commits locaux vers le dépôt distant.
git log     # Affiche l'historique des commits dans le dépôt.
```

En plus de cela vous avez des "méta-commandes" qui combinent plusieurs étapes en une seule commande:

```text
git clone   # Crée une copie locale d'un dépôt distant (git init + git fetch + git remote add + git checkout)
git pull    # Récupère les modifications depuis le dépôt distant et les fusionne avec votre branche locale (git fetch + git merge)
git commit -am "message" # Fait un git add de tous les fichiers modifiés puis commit avec le message `message`
```

Si vous travaillez avec un dépôt distant (qui peut être un dossier sur un serveur ou un service comme GitHub) vous avez besoin d'ajouter des informations sur ce dépôt distant. Pour cela vous utilisez la commande `git remote add`:

```bash
git remote add origin <url>  # Ajoute un dépôt distant nommé "origin" avec l'URL spécifiée
git remote -v                # Affiche les dépôts distants configurés
```

`origin` est une convention pour nommer le dépôt distant principal, mais vous pouvez utiliser n'importe quel nom. L'URL peut être un chemin local ou une URL HTTP/HTTPS/SSH vers un dépôt Git.
Vous pouvez donc avoir autant de dépôts distants que vous le souhaitez, chacun avec un nom unique.

Pour synchroniser votre dépôt local avec le dépôt distant vous devez respecter une règle importante:

> Vous ne pouvez pas pousser vos modifications vers le dépôt distant si votre branche locale est en retard par rapport à la branche distante. Dans ce cas, vous devez d'abord récupérer les modifications du dépôt distant avec `git pull`, résoudre les éventuels conflits, puis pousser vos modifications avec `git push`.

L'opération de `pull` va exécuter selon votre préférence l'une ou l'autre des stratégie de fusion:

1. merge: ajoute un nouveau commit avec deux parents.
2. rebase: rejoue le commit par dessus celui récupéré du dépôt distant.

En règle général, on préfère de loin le `rebase` qui pollue moins l'historique

### Paramétrer Git

Le plus utile c'est paramétrer un alias pour avoir un `log` plus lisible. Je vous recommande celui-ci:

```bash
git config --global alias.lg "log --graph --all --decorate --color=auto -n 30 --pretty=format:'%C(bold blue)%h%C(reset) %C(green)%<(14,trunc)%ar%C(reset) %s %C(auto)%d%C(dim white) - %an%C(reset)'"
```

Ca vous permet d'utiliser `git lg` à la place de `git log`.

