"""Interfaz de línea de comandos: generate | run | info."""

from __future__ import annotations

import argparse
from pathlib import Path

from alteration_ml.pipeline import run_pipeline
from alteration_ml.synthetic import write_synthetic_tables


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pipeline abierto de dominios de alteración (SWIR + geoquímica + ML)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Genera el yacimiento sintético")
    gen.add_argument("--out", default="data/synthetic")
    gen.add_argument("--holes", type=int, default=24)
    gen.add_argument("--seed", type=int, default=42)

    run = sub.add_parser("run", help="Ejecuta el flujo completo y guarda figuras")
    run.add_argument("--data", default="data/synthetic")
    run.add_argument("--out", default="outputs")
    run.add_argument("--profile", choices=["thesis", "robust"], default="thesis")
    run.add_argument("--regenerate", action="store_true")
    run.add_argument("--holes", type=int, default=24)
    run.add_argument("--seed", type=int, default=42)

    args = parser.parse_args(argv)

    if args.command == "generate":
        paths = write_synthetic_tables(args.out, n_holes=args.holes, seed=args.seed)
        for key, path in paths.items():
            print(f"{key}: {path}")
        return 0

    summary = run_pipeline(
        data_dir=args.data,
        output_dir=args.out,
        profile=args.profile,
        regenerate=args.regenerate,
        n_holes=args.holes,
        seed=args.seed,
    )
    print(f"Muestras: {summary['n_samples']} (etiquetadas: {summary['n_labeled']})")
    print(f"Varianza PC1+PC2: {sum(summary['variance_pc1_pc2']):.3f}")
    print(f"Silhouette K-Means: {summary['silhouette_kmeans']:.3f}")
    print(f"Mejor modelo: {summary['best_model']}")
    print(summary["ranking"].to_string(index=False))
    print(f"Figuras en {Path(args.out) / 'figures'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
