"""
Dashboard interactif — Ventes mondiales de jeux vidéo (1980-2016)
Auteur : Axel — BUT 2 Informatique (VCOD)
Lancer : streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration & palette (palette catégorielle testée daltonisme)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Jeux vidéo — Dashboard", page_icon="🎮", layout="wide")

BLEU = "#2a78d6"          # couleur principale (une seule série)
BLEU_CLAIR = "#86b6ef"
ACCENT = "#eb6834"        # mise en avant ponctuelle
TEXTE = "#52514e"
GRILLE = "#e8e7e3"
REGIONS = {               # ordre fixe : une couleur = une région, jamais réattribuée
    "Amérique du Nord": "#2a78d6",
    "Europe": "#eb6834",
    "Japon": "#1baf7a",
    "Reste du monde": "#eda100",
}
COLS_REGION = {
    "NA_Sales": "Amérique du Nord",
    "EU_Sales": "Europe",
    "JP_Sales": "Japon",
    "Other_Sales": "Reste du monde",
}
GENRES_FR = {
    "Action": "Action", "Sports": "Sport", "Shooter": "Tir", "Role-Playing": "RPG",
    "Platform": "Plateforme", "Misc": "Divers", "Racing": "Course", "Fighting": "Combat",
    "Simulation": "Simulation", "Puzzle": "Puzzle", "Adventure": "Aventure",
    "Strategy": "Stratégie",
}


@st.cache_data
def charger_donnees() -> pd.DataFrame:
    df = pd.read_csv(Path(__file__).parent / "data" / "vgsales.csv")
    df = df.dropna(subset=["Year"])            # 271 jeux sans année
    df["Year"] = df["Year"].astype(int)
    df = df[df["Year"] <= 2016]                # 2017+ : 4 lignes isolées
    df["Publisher"] = df["Publisher"].fillna("Inconnu")
    df["Genre"] = df["Genre"].map(GENRES_FR)
    return df


def style_fig(fig: go.Figure, hauteur: int = 340) -> go.Figure:
    """Style commun : fond neutre, grille discrète, police lisible."""
    fig.update_layout(
        height=hauteur,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", size=13, color=TEXTE),
        hoverlabel=dict(bgcolor="white", font_size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title=None),
    )
    fig.update_xaxes(showgrid=False, linecolor=GRILLE, title=None)
    fig.update_yaxes(gridcolor=GRILLE, zeroline=False, title=None)
    return fig


df = charger_donnees()

# ---------------------------------------------------------------------------
# Filtres (barre latérale)
# ---------------------------------------------------------------------------
st.sidebar.header("🎛️ Filtres")
annees = st.sidebar.slider("Période", 1980, 2016, (1980, 2016))
region = st.sidebar.radio(
    "Marché analysé",
    ["Monde"] + list(COLS_REGION.values()),
    help="Toutes les mesures du tableau de bord sont recalculées pour ce marché.",
)
genres = st.sidebar.multiselect("Genres", sorted(df["Genre"].unique()), placeholder="Tous les genres")
top_plateformes = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).index
plateformes = st.sidebar.multiselect("Plateformes", list(top_plateformes), placeholder="Toutes les plateformes")
st.sidebar.caption("Laisser un filtre vide = tout sélectionner.")
st.sidebar.divider()
st.sidebar.caption(
    "Source : VGChartz via Kaggle (*Video Game Sales*, G. Smith). "
    "Jeux vendus à plus de 100 000 exemplaires. Ventes en **millions d'unités**. "
    "2016 est une année incomplète."
)

f = df[df["Year"].between(*annees)]
if genres:
    f = f[f["Genre"].isin(genres)]
if plateformes:
    f = f[f["Platform"].isin(plateformes)]

col_ventes = "Global_Sales" if region == "Monde" else {v: k for k, v in COLS_REGION.items()}[region]

# ---------------------------------------------------------------------------
# En-tête & KPI
# ---------------------------------------------------------------------------
st.title("🎮 Le marché du jeu vidéo, 1980 – 2016")
st.markdown(
    f"Ventes de **{len(df):,}** jeux sur 31 plateformes · marché affiché : **{region}** · "
    f"période **{annees[0]}–{annees[1]}**".replace(",", " ")
)

if f.empty:
    st.warning("Aucun jeu ne correspond à ces filtres.")
    st.stop()

total = f[col_ventes].sum()
nb_jeux = len(f)
par_genre = f.groupby("Genre")[col_ventes].sum().sort_values()
meilleur = f.loc[f[col_ventes].idxmax()]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ventes totales", f"{total:,.0f} M".replace(",", " "))
k2.metric("Jeux référencés", f"{nb_jeux:,}".replace(",", " "))
k3.metric("Ventes moyennes / jeu", f"{total / nb_jeux * 1000:,.0f} k".replace(",", " "))
k4.metric("Genre n°1", par_genre.index[-1])
k4.caption(f"{par_genre.iloc[-1] / total:.0%} des ventes du marché")

st.divider()

# ---------------------------------------------------------------------------
# Ligne 1 : évolution temporelle + genres
# ---------------------------------------------------------------------------
c1, c2 = st.columns([3, 2])

with c1:
    par_an = f.groupby("Year")[col_ventes].sum().reset_index()
    pic = par_an.loc[par_an[col_ventes].idxmax()]
    st.subheader(f"Les ventes culminent en {int(pic['Year'])}")
    st.caption("Ventes annuelles (millions d'unités)")
    fig = go.Figure(go.Scatter(
        x=par_an["Year"], y=par_an[col_ventes], mode="lines",
        line=dict(color=BLEU, width=2.5), fill="tozeroy", fillcolor="rgba(42,120,214,0.10)",
        hovertemplate="<b>%{x}</b><br>%{y:.1f} M d'unités<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[pic["Year"]], y=[pic[col_ventes]], mode="markers+text",
        marker=dict(color=ACCENT, size=10, line=dict(color="white", width=2)),
        text=[f"{pic[col_ventes]:.0f} M"], textposition="top center",
        textfont=dict(color=TEXTE), hoverinfo="skip",
    ))
    fig.update_layout(showlegend=False, hovermode="x unified")
    st.plotly_chart(style_fig(fig), width="stretch")

with c2:
    st.subheader(f"{par_genre.index[-1]} : le genre le plus vendu")
    st.caption("Ventes par genre (millions d'unités)")
    couleurs = [ACCENT if g == par_genre.index[-1] else BLEU for g in par_genre.index]
    fig = go.Figure(go.Bar(
        x=par_genre.values, y=par_genre.index, orientation="h",
        marker=dict(color=couleurs, cornerradius=4),
        text=[f"{v:.0f}" for v in par_genre.values], textposition="outside",
        textfont=dict(color=TEXTE),
        hovertemplate="<b>%{y}</b><br>%{x:.1f} M d'unités<extra></extra>",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False, range=[0, par_genre.max() * 1.18])
    fig.update_traces(cliponaxis=False)
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(style_fig(fig), width="stretch")

# ---------------------------------------------------------------------------
# Ligne 2 : genres × régions + éditeurs
# ---------------------------------------------------------------------------
c3, c4 = st.columns([3, 2])

with c3:
    st.subheader("Chaque marché a ses préférences")
    st.caption("Répartition des ventes de chaque région par genre (%) — le RPG pèse bien plus au Japon")
    long = f.melt(id_vars=["Genre"], value_vars=list(COLS_REGION), var_name="Région", value_name="Ventes")
    long["Région"] = long["Région"].map(COLS_REGION)
    pivot = long.groupby(["Région", "Genre"])["Ventes"].sum().reset_index()
    pivot["Part"] = pivot["Ventes"] / pivot.groupby("Région")["Ventes"].transform("sum")
    ordre_genres = list(par_genre.index[::-1])
    fig = px.bar(
        pivot, x="Genre", y="Part", color="Région", barmode="group",
        category_orders={"Genre": ordre_genres, "Région": list(REGIONS)},
        color_discrete_map=REGIONS,
        custom_data=["Région", "Ventes"],
    )
    fig.update_traces(
        marker_cornerradius=3,
        hovertemplate="<b>%{x}</b> — %{customdata[0]}<br>%{y:.1%} des ventes de la région"
                      "<br>%{customdata[1]:.1f} M d'unités<extra></extra>",
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(bargap=0.25, bargroupgap=0.08)
    st.plotly_chart(style_fig(fig, 380), width="stretch")

with c4:
    editeurs = f.groupby("Publisher")[col_ventes].sum().nlargest(10).sort_values()
    st.subheader("Top 10 des éditeurs")
    st.caption(f"Les 10 premiers réalisent {editeurs.sum() / total:.0%} des ventes")
    fig = go.Figure(go.Bar(
        x=editeurs.values, y=editeurs.index, orientation="h",
        marker=dict(color=BLEU, cornerradius=4),
        text=[f"{v:.0f}" for v in editeurs.values], textposition="outside",
        textfont=dict(color=TEXTE),
        hovertemplate="<b>%{y}</b><br>%{x:.1f} M d'unités<extra></extra>",
    ))
    fig.update_xaxes(showticklabels=False, range=[0, editeurs.max() * 1.18])
    fig.update_traces(cliponaxis=False)
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(style_fig(fig, 380), width="stretch")

# ---------------------------------------------------------------------------
# Ligne 3 : plateformes + top jeux
# ---------------------------------------------------------------------------
c5, c6 = st.columns([3, 2])

with c5:
    plat = f.groupby("Platform")[col_ventes].sum().nlargest(15).reset_index()
    st.subheader(f"{plat.iloc[0]['Platform']} en tête des plateformes")
    st.caption("Les 15 plateformes les plus vendeuses — surface proportionnelle aux ventes")
    # Couleur séquentielle (une teinte, clair -> foncé) calculée explicitement
    vmin, vmax = plat[col_ventes].min(), plat[col_ventes].max()
    norm = ((plat[col_ventes] - vmin) / (vmax - vmin or 1)).tolist()
    couleurs = sample_colorscale([[0, "#cde2fb"], [0.35, "#6da7ec"], [0.7, "#2a78d6"], [1, "#184f95"]], norm)
    fig = go.Figure(go.Treemap(
        ids=["racine"] + plat["Platform"].tolist(),
        labels=[""] + plat["Platform"].tolist(),
        parents=[""] + ["racine"] * len(plat),
        values=[plat[col_ventes].sum()] + plat[col_ventes].tolist(),
        branchvalues="total",
        marker=dict(colors=["#fcfcfb"] + couleurs, line=dict(color="#fcfcfb", width=2)),
        texttemplate="<b>%{label}</b><br>%{value:.0f} M", tiling=dict(pad=2),
        pathbar=dict(visible=False), marker_pad=dict(t=0, l=0, r=0, b=0),
        hovertemplate="<b>%{label}</b><br>%{value:.1f} M d'unités<extra></extra>",
    ))
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig, 340), width="stretch", theme=None)

with c6:
    st.subheader("Les 10 jeux les plus vendus")
    st.caption(f"Marché : {region}")
    top = (f.nlargest(10, col_ventes)[["Name", "Platform", "Year", col_ventes]]
           .rename(columns={"Name": "Jeu", "Platform": "Plateforme", "Year": "Année", col_ventes: "Ventes (M)"}))
    st.dataframe(
        top, hide_index=True, width="stretch", height=388,
        column_config={
            "Année": st.column_config.NumberColumn(format="%d"),
            "Jeu": st.column_config.TextColumn(width="medium"),
            "Ventes (M)": st.column_config.NumberColumn(format="%.1f"),
        },
    )

with st.expander("📄 Voir les données filtrées"):
    st.dataframe(f, hide_index=True, width="stretch")
