# 🎮 Le marché du jeu vidéo, 1980 – 2016

**Projet de travail individuel — Visualisation de données**
Axel · BUT 2 Informatique, parcours VCOD · Octobre 2026

![Dashboard](dashboard.png)

## Le projet

Tableau de bord interactif réalisé avec **Streamlit** et **Python** (pandas, Plotly) pour explorer plus de 36 ans de ventes de jeux vidéo : quels genres, plateformes et éditeurs dominent le marché, et comment les goûts diffèrent d'une région du monde à l'autre.

## Les données

- **Source :** [Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales) (Kaggle, données VGChartz)
- **Contenu :** 16 598 jeux vendus à plus de 100 000 exemplaires, avec plateforme, année, genre, éditeur et ventes par région (Amérique du Nord, Europe, Japon, reste du monde), en millions d'unités
- **Nettoyage :** suppression des 271 jeux sans année et des 4 jeux postérieurs à 2016, éditeurs manquants regroupés sous « Inconnu », genres traduits en français. Il reste **16 323 jeux**. L'année 2016 est incomplète dans la source.

## Le tableau de bord

**Filtres (barre latérale)** — période, marché analysé (Monde ou une région), genres et plateformes. Tous les indicateurs et graphiques se recalculent selon la sélection.

| Visualisation | Type | Ce qu'elle montre |
|---|---|---|
| Indicateurs clés | Cartes KPI | Ventes totales, nombre de jeux, ventes moyennes par jeu, genre n°1 |
| Évolution des ventes | Courbe (aire) | Ventes annuelles, avec le pic mis en évidence |
| Ventes par genre | Barres horizontales triées | Classement des genres, le premier en couleur d'accent |
| Préférences par marché | Barres groupées (%) | Part de chaque genre dans les ventes de chaque région |
| Top 10 des éditeurs | Barres horizontales | Concentration du marché |
| Plateformes | Treemap | Poids relatif des 15 plateformes les plus vendeuses |
| Top 10 des jeux | Tableau | Les meilleures ventes pour le marché choisi |

**Choix de visualisation appliqués :**
- Titres qui énoncent le constat (« Les ventes culminent en 2008 ») plutôt qu'une simple description
- Une couleur principale (bleu) et une couleur d'accent (orange) réservée à l'élément à remarquer
- Barres triées, valeurs affichées directement, grille discrète, pas d'effet 3D ni de camembert
- Palette des régions testée pour rester lisible par les personnes daltoniennes, et chaque région garde toujours la même couleur
- Infobulles au survol sur tous les graphiques

## Ce que révèlent les données

- **Un pic en 2008** (≈ 679 M d'unités vendues), porté par la Wii, la DS, la PS3 et la Xbox 360, puis un net recul (≈ 264 M en 2015), en partie lié à la montée du jeu mobile et dématérialisé, absent de ces données.
- **L'Amérique du Nord pèse près de la moitié du marché** (49 %), devant l'Europe (27 %) et le Japon (15 %).
- **Le Japon a des goûts à part :** le RPG y représente 27 % des ventes contre environ 8 % en Amérique du Nord et en Europe, tandis que les jeux de tir n'y pèsent que 3 % (contre 13 % ailleurs).
- **Action et Sport** sont les deux genres les plus vendus au niveau mondial ; **Nintendo** domine nettement les éditeurs et la **PS2** reste la plateforme la plus vendeuse.

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure

```
├── app.py               # application Streamlit
├── data/vgsales.csv     # jeu de données
├── dashboard.png        # capture du tableau de bord
├── requirements.txt
└── .streamlit/config.toml
```
