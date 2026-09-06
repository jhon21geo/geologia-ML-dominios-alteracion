"""Pipeline abierto para delimitar dominios de alteración hidrotermal.

Integra abundancias minerales SWIR/VNIR y geoquímica multielemental
mediante aprendizaje no supervisado (PCA, clustering jerárquico, K-Means)
y supervisado (Random Forest, k-NN, red neuronal, SVM).

La metodología replica el flujo de Mallma (2026) sobre un yacimiento
sintético de alta sulfuración con transiciones a pórfido/skarn, sin datos
confidenciales de la unidad original.
"""

from alteration_ml.constants import CHEMICAL_COLUMNS, DOMAINS, SPECTRAL_MINERALS

__all__ = ["CHEMICAL_COLUMNS", "DOMAINS", "SPECTRAL_MINERALS"]
__version__ = "0.1.0"
