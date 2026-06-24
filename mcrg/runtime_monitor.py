from __future__ import annotations

import importlib.util
import os
import platform
import resource
import shutil
import subprocess
import time


def dependency_status(*, chem_ready: bool, pd_obj, image_obj) -> str:
    rdkit = "RDKit ok" if chem_ready else "RDKit loading"
    pandas = "Pandas ok" if pd_obj is not None else "Pandas loading"
    pillow = "Pillow ok" if image_obj is not None else "Pillow loading"
    admet = "ADMET ok" if importlib.util.find_spec("admet_ai") is not None else "ADMET optional"
    return f"{rdkit} | {pandas} | {pillow} | {admet}"


def _rss_mb() -> float:
    try:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        rss = float(getattr(usage, "ru_maxrss", 0.0) or 0.0)
        # macOS reports bytes; Linux reports KiB.
        if platform.system() == "Darwin":
            return rss / (1024.0 * 1024.0)
        return rss / 1024.0
    except Exception:
        return 0.0


def _gpu_status() -> str:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return "GPU: n/a"
    try:
        res = subprocess.run(
            [
                nvidia_smi,
                "--query-gpu=utilization.gpu,memory.used",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=0.35,
            check=False,
        )
        line = (res.stdout or "").strip().splitlines()[0]
        util, mem = [part.strip() for part in line.split(",", 1)]
        return f"GPU: {util}% | VRAM: {mem} MB"
    except Exception:
        return "GPU: n/a"


def sample_usage(previous: dict | None = None) -> tuple[str, dict]:
    now = time.monotonic()
    cpu_now = time.process_time()
    cores = max(1, os.cpu_count() or 1)
    previous = previous or {}
    prev_t = float(previous.get("wall", now) or now)
    prev_cpu = float(previous.get("cpu", cpu_now) or cpu_now)
    wall_delta = max(1e-6, now - prev_t)
    cpu_delta = max(0.0, cpu_now - prev_cpu)
    cpu_pct = min(999.0, (cpu_delta / wall_delta) * 100.0 / cores)
    ram_mb = _rss_mb()
    gpu = _gpu_status()
    text = f"CPU: {cpu_pct:4.1f}% | RAM: {ram_mb:,.0f} MB | {gpu}"
    return text, {"wall": now, "cpu": cpu_now}
