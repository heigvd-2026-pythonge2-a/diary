# 🎰 Lucky Slots

Machine à sous animée pour le terminal, écrite en Python moderne avec [Rich](https://github.com/Textualize/rich) et gérée par [uv](https://docs.astral.sh/uv/).

```bash
uv run slot
```

## Commandes

| Touche        | Action                          |
| ------------- | ------------------------------- |
| `Espace`/`↵`  | Lancer les rouleaux             |
| `+` / `-`     | Augmenter / diminuer la mise    |
| `M`           | Mise maximale                   |
| `A`           | Activer / couper l'auto-spin    |
| `R`           | Recharger quand on est à sec    |
| `Q` / `Échap` | Quitter                         |

## Règles

- 3 rouleaux, 5 lignes de gain (3 horizontales + 2 diagonales).
- Une partie coûte `mise × 5` crédits.
- 3 symboles identiques sur une ligne rapportent `multiplicateur × mise`, deux 🍒 en début de ligne rapportent `4 × mise`.
- Le taux de redistribution est d'environ 96 %.

## Structure

- `src/slot/machine.py` : logique du jeu (rouleaux, tirage, calcul des gains), sans affichage.
- `src/slot/keyboard.py` : lecture non bloquante du clavier (Linux/macOS/Windows).
- `src/slot/app.py` : interface Rich animée.
