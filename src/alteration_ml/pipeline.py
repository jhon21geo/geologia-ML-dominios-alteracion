"""Orquestación del flujo completo: datos → no supervisado → supervisado."""

from __future__ import annotations

from pathlib import Path
import shutil

import pandas as pd

from alteration_ml.constants import SPECTRAL_MINERALS, TARGET_COLUMN
from alteration_ml.evaluate import evaluate_model, metrics_table, per_domain_table
from alteration_ml.preprocess import prepare_feature_matrix
from alteration_ml.spectral import spectral_summary
from alteration_ml.supervised import predict_frame, split_labeled, train_models
from alteration_ml.synthetic import write_synthetic_tables
from alteration_ml.unsupervised import (
    cluster_mineral_profiles,
    fit_kmeans,
    fit_pca,
    mineral_hierarchical_clusters,
)
from alteration_ml import viz


def ensure_data(data_dir: Path, regenerate: bool = False, **kwargs) -> pd.DataFrame:
    merged = data_dir / "synthetic_merged.csv"
    if regenerate or not merged.exists():
        write_synthetic_tables(data_dir, **kwargs)
    return pd.read_csv(merged)


def run_pipeline(
    data_dir: str | Path = "data/synthetic",
    output_dir: str | Path = "outputs",
    profile: str = "thesis",
    regenerate: bool = False,
    n_holes: int = 24,
    seed: int = 42,
) -> dict:
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    data = ensure_data(data_dir, regenerate=regenerate, n_holes=n_holes, seed=seed)

    spectral_ready, spectral_z, _ = prepare_feature_matrix(data, feature_kind="spectral")
    chem_ready, chem_z, _ = prepare_feature_matrix(data, feature_kind="chemistry")
    work = spectral_ready.copy()
    for col in chem_z:
        work[col] = chem_ready[col]

    minerals = [m for m in SPECTRAL_MINERALS if m in work.columns]
    X_spec = work[spectral_z].to_numpy()
    pca, scores, var_ratio = fit_pca(X_spec, n_components=min(5, X_spec.shape[1]))
    work["pc1"] = scores[:, 0]
    work["pc2"] = scores[:, 1]
    kmeans, clusters, silhouette = fit_kmeans(X_spec, n_clusters=5)
    work["cluster_k5"] = clusters
    z_link, mineral_clusters = mineral_hierarchical_clusters(work, minerals=minerals, n_clusters=5)
    cluster_profile = cluster_mineral_profiles(work, "cluster_k5", minerals)

    labeled = work[work["labeled"]].copy()
    split = split_labeled(labeled, chem_z, test_size=0.20, random_state=seed)
    models = train_models(split, profile=profile)
    results = {name: evaluate_model(model, split.X_test, split.y_test) for name, model in models.items()}
    ranking = metrics_table(results)
    domain_metrics = per_domain_table(results)
    best_name = ranking.iloc[0]["modelo"]
    best_model = models[best_name]
    predicted = predict_frame(best_model, work, chem_z, prefix="best")

    figures = {
        "domains": viz.plot_domain_counts(work, fig_dir / "01_dominios.png"),
        "minerals": viz.plot_mineral_boxplot(work, fig_dir / "02_minerales.png"),
        "pca_true": viz.plot_pca(scores, work[TARGET_COLUMN], fig_dir / "03_pca_dominios.png", "PCA de abundancias SWIR (color = dominio real)"),
        "pca_kmeans": viz.plot_pca(scores, work["cluster_k5"], fig_dir / "04_pca_kmeans.png", "PCA de abundancias SWIR (color = K-Means k=5)"),
        "dendrogram": viz.plot_dendrogram(z_link, minerals, fig_dir / "05_dendrograma.png"),
        "map": viz.plot_map_xy(work, fig_dir / "06_planta_dominios.png"),
        "section": viz.plot_section(work, fig_dir / "07_seccion_dominios.png"),
        "metrics": viz.plot_metrics_bar(ranking, fig_dir / "08_metricas_modelos.png"),
        "roc": viz.plot_roc(results, fig_dir / "09_roc_ovr.png"),
        "confusion_best": viz.plot_confusion(
            results[best_name]["confusion"],
            results[best_name]["labels"],
            fig_dir / "10_confusion_mejor.png",
            f"Matriz de confusión — {best_name}",
        ),
        "map_pred": viz.plot_map_xy(predicted, fig_dir / "11_planta_prediccion.png", color_col="best_pred"),
        "section_pred": viz.plot_section(predicted, fig_dir / "12_seccion_prediccion.png", color_col="best_pred"),
    }
    for name, res in results.items():
        figures[f"cm_{name}"] = viz.plot_confusion(
            res["confusion"],
            res["labels"],
            fig_dir / f"cm_{name}.png",
            f"Matriz de confusión — {name}",
        )

    ranking.to_csv(output_dir / "metrics_ranking.csv", index=False)
    domain_metrics.to_csv(output_dir / "metrics_por_dominio.csv", index=False)
    mineral_clusters.to_csv(output_dir / "clusters_minerales.csv", index=False)
    cluster_profile.to_csv(output_dir / "perfiles_kmeans.csv")
    spectral_summary(work).to_csv(output_dir / "resumen_espectral.csv", index=False)
    predicted.to_csv(output_dir / "predicciones.csv", index=False)

    docs_assets = Path("docs/assets")
    docs_assets.mkdir(parents=True, exist_ok=True)
    snapshot = [
        "01_dominios.png",
        "02_minerales.png",
        "03_pca_dominios.png",
        "04_pca_kmeans.png",
        "05_dendrograma.png",
        "06_planta_dominios.png",
        "07_seccion_dominios.png",
        "08_metricas_modelos.png",
        "09_roc_ovr.png",
        "10_confusion_mejor.png",
        "11_planta_prediccion.png",
        "12_seccion_prediccion.png",
    ]
    for name in snapshot:
        src = fig_dir / name
        if src.exists():
            shutil.copy(src, docs_assets / name)

    summary = {
        "n_samples": int(len(work)),
        "n_labeled": int(work["labeled"].sum()),
        "variance_pc1_pc2": [float(var_ratio[0]), float(var_ratio[1])],
        "silhouette_kmeans": float(silhouette),
        "best_model": best_name,
        "ranking": ranking,
        "domain_metrics": domain_metrics,
        "figures": {k: str(v) for k, v in figures.items()},
        "models": models,
        "results": results,
    }
    return summary
