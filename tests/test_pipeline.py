"""Pruebas del pipeline sintético: generación, preproceso, clustering y clasificación."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from alteration_ml.constants import CHEMICAL_COLUMNS, DOMAINS, SPECTRAL_MINERALS
from alteration_ml.evaluate import evaluate_model, metrics_table
from alteration_ml.preprocess import impute_median_by_hole, prepare_feature_matrix
from alteration_ml.spectral import assemblage_flags, drop_zero_mean_minerals
from alteration_ml.supervised import split_labeled, train_models
from alteration_ml.synthetic import generate_synthetic_deposit, write_synthetic_tables
from alteration_ml.unsupervised import fit_kmeans, fit_pca, mineral_hierarchical_clusters


@pytest.fixture(scope="module")
def tiny_deposit() -> pd.DataFrame:
    return generate_synthetic_deposit(n_holes=10, samples_per_hole=(70, 95), seed=0)


def test_synthetic_has_six_domains_and_minerals(tiny_deposit: pd.DataFrame) -> None:
    assert set(tiny_deposit["MOD_ALT"].unique()) == set(DOMAINS)
    for mineral in SPECTRAL_MINERALS:
        assert mineral in tiny_deposit.columns
        assert tiny_deposit[mineral].between(0, 100).all()
    for col in CHEMICAL_COLUMNS:
        assert col in tiny_deposit.columns
    assert tiny_deposit["labeled"].mean() > 0.7


def test_domain_signatures_are_distinct(tiny_deposit: pd.DataFrame) -> None:
    means = tiny_deposit.groupby("MOD_ALT")[["Pyrophyllite", "WhiteMica", "Chlorite", "Hematite"]].mean()
    assert means.loc["ArgAvd", "Pyrophyllite"] > means.loc["Fil", "Pyrophyllite"]
    assert means.loc["Fil", "WhiteMica"] > means.loc["Pro", "WhiteMica"]
    assert means.loc["Pro", "Chlorite"] > means.loc["ArgAvd", "Chlorite"]
    assert means.loc["Oxd", "Hematite"] > means.loc["Fil", "Hematite"]


def test_write_tables(tmp_path) -> None:
    paths = write_synthetic_tables(tmp_path, n_holes=4, samples_per_hole=(20, 25), seed=1)
    merged = pd.read_csv(paths["merged"])
    spectral = pd.read_csv(paths["spectral"])
    assert len(merged) == len(spectral)
    assert "MOD_ALT" in merged.columns


def test_imputation_removes_nans(tiny_deposit: pd.DataFrame) -> None:
    cols = ["Au_ppm", "As_ppm", "W_ppm"]
    filled = impute_median_by_hole(tiny_deposit, cols)
    assert filled[cols].isna().sum().sum() == 0


def test_prepare_feature_matrix_zscore(tiny_deposit: pd.DataFrame) -> None:
    ready, z_cols, scaler = prepare_feature_matrix(tiny_deposit, feature_kind="chemistry")
    assert len(z_cols) >= 20
    z = ready[z_cols].to_numpy()
    assert np.nanmax(np.abs(z.mean(axis=0))) < 1e-6
    assert scaler.n_features_in_ == len(z_cols)


def test_spectral_filters(tiny_deposit: pd.DataFrame) -> None:
    kept = drop_zero_mean_minerals(tiny_deposit)
    assert set(SPECTRAL_MINERALS).issubset(set(kept))
    flags = assemblage_flags(tiny_deposit)
    assert flags["ensamble_argavd"].any()
    assert flags["ensamble_oxd"].any()


def test_unsupervised_runs(tiny_deposit: pd.DataFrame) -> None:
    ready, z_cols, _ = prepare_feature_matrix(tiny_deposit, feature_kind="spectral")
    X = ready[z_cols].to_numpy()
    pca, scores, var = fit_pca(X, n_components=4)
    assert scores.shape[1] == 4
    assert var.sum() > 0.5
    _, labels, sil = fit_kmeans(X, n_clusters=5)
    assert set(labels) <= set(range(5))
    assert sil > 0.05
    z, table = mineral_hierarchical_clusters(tiny_deposit, n_clusters=5)
    assert len(table) == 13
    assert table["cluster_h"].nunique() == 5
    assert z.shape[0] == 12


def test_supervised_better_than_chance(tiny_deposit: pd.DataFrame) -> None:
    ready, z_cols, _ = prepare_feature_matrix(tiny_deposit, feature_kind="chemistry")
    split = split_labeled(ready, z_cols, test_size=0.25, random_state=0)
    models = train_models(split, profile="thesis")
    results = {name: evaluate_model(model, split.X_test, split.y_test) for name, model in models.items()}
    table = metrics_table(results)
    assert set(models) == {"random_forest", "knn", "neural_network", "svm"}
    # Seis clases: azar ≈ 0.17. Los modelos de árbol/vecinos deben superar eso.
    tree_like = table[table["modelo"].isin(["random_forest", "knn"])]
    assert (tree_like["accuracy"] > 0.35).all()
    assert table["f1"].max() > 0.35
