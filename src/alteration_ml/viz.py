"""Figuras del pipeline: EDA, PCA, dendrograma, matrices de confusión y ROC."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
from scipy.cluster.hierarchy import dendrogram

from alteration_ml.constants import (
    DOMAIN_COLORS,
    DOMAIN_LABELS,
    DOMAINS,
    SPECTRAL_MINERALS,
)

CLUSTER_COLORS = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f")

sns.set_theme(style="whitegrid", context="talk", font_scale=0.7)


def _save(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_domain_counts(frame: pd.DataFrame, path: Path) -> Path:
    counts = frame.loc[frame.get("labeled", True) == True, "MOD_ALT"].value_counts().reindex(DOMAINS)  # noqa: E712
    fig, ax = plt.subplots(figsize=(8, 4.2))
    colors = [DOMAIN_COLORS[d] for d in counts.index]
    ax.bar(counts.index.map(DOMAIN_LABELS), counts.values, color=colors)
    ax.set_ylabel("Intervalos")
    ax.set_title("Distribución de dominios de alteración (datos sintéticos)")
    ax.tick_params(axis="x", rotation=20)
    return _save(fig, path)


def plot_mineral_boxplot(frame: pd.DataFrame, path: Path) -> Path:
    minerals = [m for m in SPECTRAL_MINERALS if m in frame.columns]
    melted = frame.melt(id_vars=["MOD_ALT"], value_vars=minerals, var_name="mineral", value_name="score")
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.boxplot(data=melted, x="mineral", y="score", hue="MOD_ALT", ax=ax, fliersize=1, palette=DOMAIN_COLORS)
    ax.set_title("Abundancias espectrales por dominio")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(title="Dominio", bbox_to_anchor=(1.02, 1), loc="upper left")
    return _save(fig, path)


def plot_pca(scores: np.ndarray, labels: np.ndarray | pd.Series, path: Path, title: str) -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 6))
    series = pd.Series(labels)
    for domain in series.unique():
        mask = series.to_numpy() == domain
        color = DOMAIN_COLORS.get(str(domain), "#888888")
        ax.scatter(scores[mask, 0], scores[mask, 1], s=12, alpha=0.65, label=str(domain), color=color)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title(title)
    ax.legend(markerscale=1.6, frameon=True, fontsize=8)
    return _save(fig, path)


def plot_dendrogram(z: np.ndarray, labels: list[str], path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    dendrogram(z, labels=labels, leaf_rotation=35, ax=ax, color_threshold=None)
    ax.set_title("Clustering jerárquico de minerales SWIR")
    ax.set_ylabel("Distancia (Ward)")
    return _save(fig, path)


def plot_confusion(matrix: np.ndarray, labels: list[str], path: Path, title: str) -> Path:
    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        xticklabels=labels,
        yticklabels=labels,
        ax=ax,
    )
    ax.set_xlabel("Predicho")
    ax.set_ylabel("Real")
    ax.set_title(title)
    return _save(fig, path)


def plot_roc(results: dict, path: Path) -> Path:
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))
    axes = axes.ravel()
    for i, domain in enumerate(DOMAINS):
        ax = axes[i]
        for name, res in results.items():
            curves = res.get("roc_curves", {})
            if domain not in curves:
                continue
            fpr, tpr = curves[domain]
            ax.plot(fpr, tpr, label=name, linewidth=1.6)
        ax.plot([0, 1], [0, 1], "--", color="#999999", linewidth=1)
        ax.set_title(DOMAIN_LABELS[domain])
        ax.set_xlabel("FPR")
        ax.set_ylabel("TPR")
        ax.legend(fontsize=7)
    return _save(fig, path)


def plot_metrics_bar(table: pd.DataFrame, path: Path) -> Path:
    melted = table.melt(id_vars=["modelo"], value_vars=["AUC", "precision", "recall", "f1"], var_name="métrica", value_name="valor")
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    sns.barplot(data=melted, x="modelo", y="valor", hue="métrica", ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_title("Comparación de modelos supervisados")
    ax.legend(loc="lower right")
    return _save(fig, path)


def plot_map_xy(frame: pd.DataFrame, path: Path, color_col: str = "MOD_ALT") -> Path:
    fig, ax = plt.subplots(figsize=(6.8, 6.2))
    for domain, group in frame.groupby(color_col):
        ax.scatter(
            group["x"],
            group["y"],
            s=10,
            alpha=0.7,
            color=DOMAIN_COLORS.get(str(domain), "#888"),
            label=str(domain),
        )
    ax.set_aspect("equal")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title(f"Planta de sondajes coloreada por {color_col}")
    ax.legend(markerscale=2, fontsize=8)
    return _save(fig, path)


def plot_section(frame: pd.DataFrame, path: Path, color_col: str = "MOD_ALT") -> Path:
    """Sección aproximada: Y vs profundidad."""
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for domain, group in frame.groupby(color_col):
        ax.scatter(
            group["y"],
            group["z"],
            s=10,
            alpha=0.7,
            color=DOMAIN_COLORS.get(str(domain), "#888"),
            label=str(domain),
        )
    ax.invert_yaxis()
    ax.set_xlabel("Y (m)")
    ax.set_ylabel("Profundidad (m)")
    ax.set_title(f"Sección Y–Z coloreada por {color_col}")
    ax.legend(markerscale=2, fontsize=8)
    return _save(fig, path)


def plot_assignment_schema(path: Path) -> Path:
    """Esquema del ciclo algoritmo + juicio del geólogo (no sustituye al logueo)."""
    fig, ax = plt.subplots(figsize=(11.2, 6.4))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_title("Asignación de dominios: clustering espectral + juicio geológico", loc="left", fontsize=13, pad=8)

    boxes = [
        (0.3, 4.6, 2.4, 1.2, "#d9f0d3", "1. Scores SWIR/VNIR\n13 minerales + óxidos"),
        (3.1, 4.6, 2.6, 1.2, "#d0e1f2", "2. PCA, dendrograma\ny K-Means (k = 5)"),
        (6.2, 4.6, 2.4, 1.2, "#fde2cc", "3. Ensamble mineral\n(Tabla de reglas)"),
        (8.9, 4.6, 2.0, 1.2, "#f4d6e7", "4. Juicio del\ngeólogo en 3D"),
        (2.6, 2.3, 3.0, 1.3, "#c7e9c0", "5. Dominio MOD_ALT\nArg · ArgAvd · Fil\nOxd · Pro · Sk"),
        (6.4, 2.3, 3.0, 1.3, "#c6dbef", "6. Tramos de control\npara entrenar RF/kNN/MLP/SVM"),
    ]
    for x, y, w, h, color, text in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.04,rounding_size=0.12",
                facecolor=color,
                edgecolor="#333",
                linewidth=1.1,
            )
        )
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.5)

    ax.annotate("", xy=(3.1, 5.2), xytext=(2.7, 5.2), arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))
    ax.annotate("", xy=(6.2, 5.2), xytext=(5.7, 5.2), arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))
    ax.annotate("", xy=(8.9, 5.2), xytext=(8.6, 5.2), arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))
    ax.annotate("", xy=(5.6, 3.6), xytext=(9.9, 4.6), arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))
    ax.annotate("", xy=(6.4, 2.95), xytext=(5.6, 2.95), arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))
    ax.annotate(
        "Si no cuadra con el logueo:\najustar k o recortar tramos",
        xy=(3.1, 4.65),
        xytext=(0.4, 0.55),
        arrowprops=dict(arrowstyle="->", color="#a50f15", lw=1.3, connectionstyle="arc3,rad=0.15"),
        fontsize=8,
        color="#a50f15",
    )
    ax.add_patch(
        FancyBboxPatch((0.25, 0.25), 3.6, 1.15, boxstyle="round,pad=0.03,rounding_size=0.1", facecolor="#fff2cc", edgecolor="#a50f15", linewidth=1.0)
    )
    return _save(fig, path)


def plot_assignment_rules(path: Path) -> Path:
    """Tarjetas de reglas usadas junto al geólogo (sección 3.12.2)."""
    fig, axes = plt.subplots(2, 3, figsize=(11.4, 6.2))
    rules = [
        ("ArgAvd", "Núcleo ácido", "Pirofilita + alunita\n± diásporo ± zunyita", "Validar continuidad del litocap"),
        ("Fil", "Halo fílico", "Mica blanca dominante\n(ilita / sericita)", "No mezclar con ArgAvd si hay alunita"),
        ("Arg", "Argílica intermedia", "Caolinita + mica blanca", "Clase rara: firmar tramos, no generalizar"),
        ("Pro", "Periferia distante", "Clorita + montmorillonita\n± carbonato ± epidota", "Separar de skarn por Ca–Fe y posición"),
        ("Sk", "Raíz cálcica", "Clorita + montmor. +\nmica + caolinita", "Confirmar con geoquímica Ca–Fe–Mn–Cu"),
        ("Oxd", "Sombrero de óxidos", "Hematita / goethita VNIR\n± yeso / sílice hidratada", "Cortar contra profundidad y S bajo"),
    ]
    for ax, (code, role, minerals, judgment) in zip(axes.ravel(), rules):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.add_patch(
            FancyBboxPatch(
                (0.03, 0.05),
                0.94,
                0.9,
                boxstyle="round,pad=0.03,rounding_size=0.08",
                facecolor=DOMAIN_COLORS[code],
                edgecolor="#222",
                linewidth=1.2,
                alpha=0.38,
            )
        )
        ax.text(0.5, 0.84, f"{code}  ·  {DOMAIN_LABELS[code]}", ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(0.5, 0.68, role, ha="center", va="center", fontsize=8.5, style="italic")
        ax.text(0.5, 0.44, minerals, ha="center", va="center", fontsize=8)
        ax.text(0.5, 0.16, f"Geólogo: {judgment}", ha="center", va="center", fontsize=7.2)
    fig.suptitle("Reglas de ensamble + corte geológico para etiquetar MOD_ALT", fontsize=13, y=0.98)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_cluster_vs_domain(frame: pd.DataFrame, path: Path, cluster_col: str = "cluster_k5") -> Path:
    """Un clúster estadístico se parte al asignar el dominio geológico."""
    table = pd.crosstab(frame[cluster_col].map(lambda c: f"C{int(c) + 1}"), frame["MOD_ALT"])
    table = table.reindex(columns=list(DOMAINS), fill_value=0)
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    sns.heatmap(table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    ax.set_xlabel("Dominio asignado por el geólogo (MOD_ALT)")
    ax.set_ylabel("Clúster K-Means")
    ax.set_title("Un clúster no equivale a un dominio geológico")
    return _save(fig, path)


def plot_pca_cluster_and_domain(scores: np.ndarray, clusters, domains, path: Path) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 5.0), sharex=True, sharey=True)
    cluster_series = pd.Series(clusters)
    for value in sorted(cluster_series.unique()):
        mask = cluster_series.to_numpy() == value
        color = CLUSTER_COLORS[int(value) % len(CLUSTER_COLORS)]
        axes[0].scatter(scores[mask, 0], scores[mask, 1], s=10, alpha=0.65, color=color, label=f"C{int(value) + 1}")
    axes[0].set_title("A. Propuesta del algoritmo (K-Means)")
    axes[0].set_xlabel("PC1")
    axes[0].set_ylabel("PC2")
    axes[0].legend(fontsize=8, markerscale=1.6)

    domain_series = pd.Series(domains)
    for domain in DOMAINS:
        mask = domain_series.to_numpy() == domain
        if not mask.any():
            continue
        axes[1].scatter(scores[mask, 0], scores[mask, 1], s=10, alpha=0.65, color=DOMAIN_COLORS[domain], label=domain)
    axes[1].set_title("B. Dominio tras el juicio geológico")
    axes[1].set_xlabel("PC1")
    axes[1].legend(fontsize=8, markerscale=1.6)
    fig.suptitle("El geólogo reetiqueta: misma nube PCA, distinta semántica", fontsize=12)
    return _save(fig, path)


def plot_diagnostic_minerals(frame: pd.DataFrame, path: Path) -> Path:
    cols = [c for c in ("Pyrophyllite", "Alunite", "WhiteMica", "Kaolinite", "Chlorite", "Hematite") if c in frame.columns]
    means = frame.groupby("MOD_ALT")[cols].mean().reindex(DOMAINS)
    melted = means.reset_index().melt(id_vars="MOD_ALT", var_name="mineral", value_name="score")
    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    sns.barplot(data=melted, x="mineral", y="score", hue="MOD_ALT", palette=DOMAIN_COLORS, ax=ax)
    ax.set_ylabel("Score medio (0–100)")
    ax.set_xlabel("")
    ax.set_title("Minerales diagnóstico con los que el geólogo firma cada dominio")
    ax.legend(title="MOD_ALT", bbox_to_anchor=(1.02, 1), loc="upper left")
    return _save(fig, path)


def plot_hole_assignment_logs(frame: pd.DataFrame, path: Path, n_holes: int = 4) -> Path:
    """Tiras de sondaje: clúster vs dominio (análogo a las figuras 24–26 de la tesis)."""
    diversity = frame.groupby("holeid")["MOD_ALT"].nunique().sort_values(ascending=False)
    holes = list(diversity.head(n_holes).index)
    fig, axes = plt.subplots(len(holes), 2, figsize=(10.6, 2.15 * max(len(holes), 1)), sharey=True)
    if len(holes) == 1:
        axes = np.array([axes])
    for row, hole in enumerate(holes):
        sub = frame[frame["holeid"] == hole].sort_values("from_m")
        for col, field, title in (
            (0, "cluster_k5", f"{hole} · clúster K-Means"),
            (1, "MOD_ALT", f"{hole} · dominio del geólogo"),
        ):
            ax = axes[row, col]
            for _, rec in sub.iterrows():
                if field == "cluster_k5":
                    color = CLUSTER_COLORS[int(rec[field]) % len(CLUSTER_COLORS)]
                else:
                    color = DOMAIN_COLORS.get(str(rec[field]), "#888")
                ax.barh(0, rec["to_m"] - rec["from_m"], left=rec["from_m"], height=0.55, color=color, linewidth=0)
            ax.set_yticks([])
            ax.set_title(title, fontsize=9, loc="left")
            ax.set_xlabel("Profundidad (m)" if row == len(holes) - 1 else "")
            ax.set_ylim(-0.6, 0.6)
    fig.suptitle("El mismo sondaje: propuesta estadística (izq.) y etiqueta geológica (der.)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return path
