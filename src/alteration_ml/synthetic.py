"""Generador de sondajes sintéticos con zonación hidrotermal.

El volumen replica un sistema epitermal de alta sulfuración con transiciones
a pórfido/skarn: núcleo ácido (ArgAvd), halo fílico, argílica intermedia,
propilítica distal, skarn profundo y óxidos someros.

Las abundancias minerales y las leyes geoquímicas se muestrean con ruido
log-normal y solapamiento entre dominios vecinos, de modo que el problema
de clasificación no sea trivial.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from alteration_ml.constants import (
    CHEMICAL_COLUMNS,
    DOMAIN_PROPORTIONS,
    DOMAINS,
    SPECTRAL_MINERALS,
    VNIR_MINERALS,
)

# Medias de abundancia espectral (0–100) por dominio. Valores altos marcan
# el ensamble diagnóstico; el resto queda como trazas.
_MINERAL_MEANS: dict[str, dict[str, float]] = {
    "ArgAvd": {
        "Pyrophyllite": 55,
        "Alunite": 32,
        "Diaspore": 18,
        "Zunyite": 8,
        "Dickite": 10,
        "Kaolinite": 6,
        "WhiteMica": 4,
        "Water_silica": 8,
    },
    "Fil": {
        "WhiteMica": 58,
        "Kaolinite": 8,
        "Dickite": 6,
        "Montmor": 5,
        "Gypsum": 6,
        "Water_silica": 5,
        "Alunite": 3,
    },
    "Arg": {
        "Kaolinite": 48,
        "WhiteMica": 22,
        "Dickite": 12,
        "Montmor": 8,
        "Gypsum": 4,
    },
    "Pro": {
        "Chlorite": 28,
        "Montmor": 18,
        "Carbonate": 16,
        "Epidote": 8,
        "WhiteMica": 6,
    },
    "Sk": {
        "Chlorite": 22,
        "Montmor": 14,
        "WhiteMica": 16,
        "Kaolinite": 12,
        "Carbonate": 10,
        "Epidote": 6,
    },
    "Oxd": {
        "Water_silica": 18,
        "Gypsum": 14,
        "Kaolinite": 10,
        "Alunite": 8,
        "WhiteMica": 6,
    },
}

# Geoquímica: media de una log-normal aproximada (unidades de cada columna).
_CHEM_MEANS: dict[str, dict[str, float]] = {
    "ArgAvd": {
        "Au_ppm": 0.85,
        "Cu_pct": 0.18,
        "As_ppm": 420,
        "S_pct": 3.8,
        "Ag_ppm": 4.2,
        "Al_pct": 9.5,
        "K_pct": 1.1,
        "Na_pct": 0.12,
        "Ca_pct": 0.18,
        "Fe_pct": 2.4,
        "Sb_ppm": 18,
        "Bi_ppm": 8,
        "Mo_ppm": 12,
        "Ba_ppm": 180,
        "Tl_ppm": 4.5,
    },
    "Fil": {
        "Au_ppm": 0.22,
        "Cu_pct": 0.08,
        "As_ppm": 85,
        "S_pct": 1.6,
        "Ag_ppm": 1.8,
        "Al_pct": 8.4,
        "K_pct": 3.4,
        "Na_pct": 0.35,
        "Ca_pct": 0.45,
        "Fe_pct": 2.8,
        "Rb_ppm": 95,
        "Ba_ppm": 420,
        "Mo_ppm": 6,
    },
    "Arg": {
        "Au_ppm": 0.12,
        "Cu_pct": 0.04,
        "As_ppm": 55,
        "S_pct": 0.9,
        "Al_pct": 10.2,
        "K_pct": 1.6,
        "Na_pct": 0.28,
        "Ca_pct": 0.35,
        "Fe_pct": 2.1,
        "Ba_ppm": 260,
    },
    "Pro": {
        "Au_ppm": 0.04,
        "Cu_pct": 0.03,
        "As_ppm": 18,
        "S_pct": 0.25,
        "Ca_pct": 4.8,
        "Mg_pct": 2.6,
        "Fe_pct": 5.2,
        "Mn_pct": 0.18,
        "Na_pct": 1.4,
        "K_pct": 1.2,
        "Al_pct": 7.2,
        "Sr_ppm": 280,
        "Zn_ppm": 95,
    },
    "Sk": {
        "Au_ppm": 0.15,
        "Cu_pct": 0.42,
        "As_ppm": 35,
        "S_pct": 0.55,
        "Ca_pct": 12.5,
        "Fe_pct": 8.4,
        "Mn_pct": 0.55,
        "Mg_pct": 1.8,
        "Al_pct": 4.5,
        "W_ppm": 18,
        "Zn_ppm": 220,
        "Mo_ppm": 22,
        "Bi_ppm": 6,
    },
    "Oxd": {
        "Au_ppm": 0.55,
        "Cu_pct": 0.06,
        "As_ppm": 310,
        "S_pct": 0.12,
        "Fe_pct": 7.8,
        "Al_pct": 8.1,
        "Ca_pct": 0.22,
        "Mn_pct": 0.08,
        "Sb_ppm": 12,
        "Ba_ppm": 140,
        "Pb_ppm": 45,
    },
}

_CHEM_DEFAULTS: dict[str, float] = {
    "Ag_ppm": 0.8,
    "Al_pct": 7.5,
    "As_ppm": 25,
    "Au_ppm": 0.05,
    "Ba_ppm": 220,
    "Be_ppm": 0.6,
    "Bi_ppm": 1.5,
    "Ca_pct": 1.2,
    "Cd_ppm": 0.4,
    "Co_ppm": 8,
    "Cr_ppm": 35,
    "Cu_pct": 0.04,
    "Fe_pct": 3.2,
    "K_pct": 1.8,
    "Mg_pct": 0.9,
    "Mn_pct": 0.05,
    "Mo_ppm": 3,
    "Na_pct": 1.1,
    "Ni_ppm": 12,
    "P_pct": 0.08,
    "Pb_ppm": 18,
    "S_pct": 0.4,
    "Sb_ppm": 3,
    "Sc_ppm": 10,
    "Si_pct": 28,
    "Sr_ppm": 90,
    "Ti_pct": 0.35,
    "V_ppm": 80,
    "W_ppm": 2,
    "Zn_ppm": 55,
    "Ga_ppm": 16,
    "Rb_ppm": 40,
    "Tl_ppm": 0.8,
    "Cs_ppm": 2.5,
}


def _domain_from_xyz(x: np.ndarray, y: np.ndarray, z: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Zonación hidrotermal clásica con jitter, sin reetiquetado aleatorio."""
    radius = np.sqrt(x**2 + y**2)
    r = radius + rng.normal(0, 18, size=x.shape)
    z_j = z + rng.normal(0, 8, size=z.shape)

    domain = np.full(x.shape, "Pro", dtype=object)
    domain[r <= 205] = "Fil"
    domain[(r > 155) & (r <= 190)] = "Arg"
    domain[r <= 135] = "ArgAvd"
    domain[(z_j >= 110) & (r < 165)] = "Sk"
    domain[z_j <= 38] = "Oxd"
    # Transiciones locales (~12 %) hacia el vecino espacial, no a un dominio aleatorio.
    neighbor = {
        "ArgAvd": "Fil",
        "Fil": "Arg",
        "Arg": "Fil",
        "Pro": "Fil",
        "Sk": "Pro",
        "Oxd": "ArgAvd",
    }
    flip = rng.random(x.shape) < 0.12
    for src, dst in neighbor.items():
        mask = flip & (domain == src)
        domain[mask] = dst
    return domain


def _rebalance_domains(domain: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Ajusta la mezcla para acercarse a las proporciones de la Tabla 17."""
    n = len(domain)
    target = {k: max(8, int(round(v * n))) for k, v in DOMAIN_PROPORTIONS.items()}
    leftover = n - sum(target.values())
    target["Fil"] += leftover

    out = np.empty(n, dtype=object)
    idx = rng.permutation(n)
    start = 0
    for name in DOMAINS:
        count = target[name]
        out[idx[start : start + count]] = name
        start += count
    return out


def _sample_abundance(mean: float, size: int, rng: np.random.Generator) -> np.ndarray:
    if mean <= 0:
        noise = rng.normal(0, 0.8, size=size)
        return np.clip(noise, 0, 8)
    sigma = max(2.5, mean * 0.45)
    values = rng.normal(mean, sigma, size=size)
    spike = rng.random(size) < 0.08
    values[spike] += rng.uniform(10, 35, size=int(spike.sum()))
    return np.clip(values, 0, 100)


def _sample_chem(mean: float, size: int, rng: np.random.Generator) -> np.ndarray:
    # Sigma alto: las clases se solapan como en un sistema real con transiciones.
    sigma = 0.95 if mean < 1 else 0.75
    samples = rng.lognormal(mean=np.log(max(mean, 1e-4)), sigma=sigma, size=size)
    return np.clip(samples, 0, None)


_NEIGHBORS = {
    "ArgAvd": ("Fil", "Arg", "Oxd"),
    "Fil": ("ArgAvd", "Arg", "Pro"),
    "Arg": ("Fil", "ArgAvd", "Pro"),
    "Pro": ("Fil", "Sk", "Arg"),
    "Sk": ("Pro", "Fil", "ArgAvd"),
    "Oxd": ("ArgAvd", "Arg", "Fil"),
}


def generate_synthetic_deposit(
    n_holes: int = 24,
    samples_per_hole: tuple[int, int] = (90, 160),
    seed: int = 42,
    rebalance: bool = False,
) -> pd.DataFrame:
    """Genera una tabla de intervalos de sondaje con espectro + geoquímica."""
    rng = np.random.default_rng(seed)

    collars = []
    for i in range(n_holes):
        angle = 2 * np.pi * i / n_holes + rng.uniform(-0.15, 0.15)
        dist = rng.uniform(15, 210)
        collars.append(
            {
                "holeid": f"SYN-{i + 1:03d}",
                "x0": dist * np.cos(angle),
                "y0": dist * np.sin(angle),
                "azimuth": rng.uniform(0, 2 * np.pi),
                "dip": rng.uniform(np.deg2rad(55), np.deg2rad(88)),
                "n": int(rng.integers(samples_per_hole[0], samples_per_hole[1] + 1)),
            }
        )

    rows: list[dict] = []
    sample_counter = 1
    for collar in collars:
        depth = 0.0
        dx = np.sin(collar["dip"]) * np.cos(collar["azimuth"])
        dy = np.sin(collar["dip"]) * np.sin(collar["azimuth"])
        dz = np.cos(collar["dip"])
        for _ in range(collar["n"]):
            length = float(rng.choice([1.0, 1.5, 2.0], p=[0.25, 0.5, 0.25]))
            from_m = depth
            to_m = depth + length
            mid = from_m + length / 2
            x = collar["x0"] + dx * mid
            y = collar["y0"] + dy * mid
            z = mid  # positivo hacia abajo
            rows.append(
                {
                    "sample_id": f"S{sample_counter:05d}",
                    "holeid": collar["holeid"],
                    "from_m": round(from_m, 2),
                    "to_m": round(to_m, 2),
                    "depth_m": round(mid, 2),
                    "x": round(x, 2),
                    "y": round(y, 2),
                    "z": round(z, 2),
                }
            )
            sample_counter += 1
            depth = to_m

    frame = pd.DataFrame(rows)
    spatial_domain = _domain_from_xyz(
        frame["x"].to_numpy(),
        frame["y"].to_numpy(),
        frame["z"].to_numpy(),
        rng,
    )
    frame["MOD_ALT"] = spatial_domain
    present = set(frame["MOD_ALT"].unique())
    missing = [d for d in DOMAINS if d not in present]
    if missing:
        idx = rng.choice(len(frame), size=len(missing) * 12, replace=False)
        for i, name in enumerate(missing):
            frame.loc[idx[i * 12 : (i + 1) * 12], "MOD_ALT"] = name

    n = len(frame)
    for mineral in SPECTRAL_MINERALS:
        values = np.zeros(n)
        for domain in DOMAINS:
            mask = frame["MOD_ALT"].to_numpy() == domain
            mean = _MINERAL_MEANS[domain].get(mineral, 1.2)
            values[mask] = _sample_abundance(mean, int(mask.sum()), rng)
        frame[mineral] = np.round(values, 2)

    hematite = np.zeros(n)
    goethite = np.zeros(n)
    oxd = frame["MOD_ALT"].to_numpy() == "Oxd"
    hematite[oxd] = _sample_abundance(42, int(oxd.sum()), rng)
    goethite[oxd] = _sample_abundance(28, int(oxd.sum()), rng)
    hematite[~oxd] = _sample_abundance(2, int((~oxd).sum()), rng)
    goethite[~oxd] = _sample_abundance(3, int((~oxd).sum()), rng)
    frame["Hematite"] = np.round(hematite, 2)
    frame["Goethite"] = np.round(goethite, 2)

    vnir = np.full(n, "None", dtype=object)
    vnir[hematite >= goethite] = np.where(hematite[hematite >= goethite] > 15, "Hematite", "None")
    vnir[goethite > hematite] = np.where(goethite[goethite > hematite] > 15, "Goethite", "None")
    frame["VNIRMinerals"] = vnir
    frame["aiMineral1"] = frame[list(SPECTRAL_MINERALS)].idxmax(axis=1)

    chem_domain = frame["MOD_ALT"].to_numpy().copy()
    mix = rng.random(n) < 0.28
    for i in np.where(mix)[0]:
        chem_domain[i] = rng.choice(_NEIGHBORS[str(chem_domain[i])])

    hole_bias = {hole: rng.normal(0, 0.18) for hole in frame["holeid"].unique()}

    for col in CHEMICAL_COLUMNS:
        values = np.zeros(n)
        for domain in DOMAINS:
            mask = chem_domain == domain
            mean = _CHEM_MEANS[domain].get(col, _CHEM_DEFAULTS[col])
            values[mask] = _sample_chem(mean, int(mask.sum()), rng)
        for hole, bias in hole_bias.items():
            sel = frame["holeid"].to_numpy() == hole
            values[sel] *= float(np.exp(bias))
        values *= rng.lognormal(0, 0.25, size=n)
        frame[col] = np.round(values, 5)

    # Datos faltantes (~6 %) e imputación posterior en preprocess.
    sparse = ["W_ppm", "Tl_ppm", "Cs_ppm", "Be_ppm", "Cd_ppm", "Mo_ppm"]
    for col in sparse:
        drop = rng.random(n) < 0.12
        frame.loc[drop, col] = np.nan
    for col in CHEMICAL_COLUMNS:
        drop = rng.random(n) < 0.03
        frame.loc[drop, col] = np.nan

    frame["labeled"] = True
    unlabeled = rng.random(n) < 0.18
    frame.loc[unlabeled, "labeled"] = False
    return frame


def inject_outliers(frame: pd.DataFrame, seed: int = 42, fraction: float = 0.015) -> pd.DataFrame:
    """Inserta colas erráticas (p. ej. leyes anómalas) antes del clipping p99."""
    rng = np.random.default_rng(seed)
    out = frame.copy()
    n = len(out)
    k = max(1, int(n * fraction))
    for col in ("Au_ppm", "Cu_pct", "As_ppm", "S_pct"):
        idx = rng.choice(out.index, size=k, replace=False)
        out.loc[idx, col] = out.loc[idx, col] * rng.uniform(8, 25, size=k)
    return out


def write_synthetic_tables(output_dir: str | Path, **kwargs) -> dict[str, Path]:
    """Escribe CSV listos para el pipeline y un diccionario de datos."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = inject_outliers(generate_synthetic_deposit(**kwargs))

    spectral_cols = ["sample_id", "holeid", "from_m", "to_m", "x", "y", "z", "depth_m"]
    spectral_cols += list(SPECTRAL_MINERALS) + list(VNIR_MINERALS) + ["VNIRMinerals", "aiMineral1"]
    chem_cols = ["sample_id", "holeid", "from_m", "to_m", "x", "y", "z", "depth_m"] + list(CHEMICAL_COLUMNS)
    labels_cols = ["sample_id", "holeid", "MOD_ALT", "labeled"]

    paths = {
        "merged": output_dir / "synthetic_merged.csv",
        "spectral": output_dir / "synthetic_spectral.csv",
        "geochemistry": output_dir / "synthetic_geochemistry.csv",
        "labels": output_dir / "synthetic_labels.csv",
    }
    data.to_csv(paths["merged"], index=False)
    data[spectral_cols].to_csv(paths["spectral"], index=False)
    data[chem_cols].to_csv(paths["geochemistry"], index=False)
    data[labels_cols].to_csv(paths["labels"], index=False)
    return paths
