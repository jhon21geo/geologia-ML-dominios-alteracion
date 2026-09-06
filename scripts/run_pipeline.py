#!/usr/bin/env python3
"""Atajo local: python scripts/run_pipeline.py [--profile thesis|robust]."""

import sys

from alteration_ml.cli import main

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("run")
    raise SystemExit(main())
