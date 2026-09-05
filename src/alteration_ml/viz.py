"""Figuras del pipeline: EDA, PCA, dendrograma, matrices de confusión y ROC."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram

from alteration_ml.constants import DOMAIN_COLORS, DOMAIN_LABELS, DOMAINS, SPECTRAL_MINERALS

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
