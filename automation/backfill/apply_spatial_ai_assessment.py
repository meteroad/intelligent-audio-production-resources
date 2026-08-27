#!/usr/bin/env python3
"""Apply the documented AI Highlight rubric to the spatial backfill."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPERS_PATH = ROOT / "data/papers.json"
ASSESSED_AT = "2026-08-27"

HIGHLIGHTS = {
    "arxiv-1812-04204": {
        "en": "Establishes a clear visual-to-binaural task with substantive evaluation and releases both code and the FAIR-Play dataset.",
        "zh": "建立清晰的视觉到双耳音频任务，进行了充分实验，并公开代码与 FAIR-Play 数据集。",
    },
    "arxiv-2205-14807": {
        "en": "Introduces a coherent two-stage diffusion formulation for binaural synthesis, validates spatial fidelity, and provides an official implementation.",
        "zh": "提出完整的两阶段双耳合成扩散框架，验证空间保真度，并提供官方实现。",
    },
    "arxiv-2302-02088": {
        "en": "Defines novel-position audio-visual scene synthesis, develops a unified neural-field method, and releases code and supporting resources.",
        "zh": "定义新位置音视频场景合成任务，提出统一神经场方法，并公开代码和配套资源。",
    },
    "arxiv-2308-09514": {
        "en": "Provides a large, richly annotated Ambisonic corpus with a transparent generation process and direct public access for reproducible research.",
        "zh": "提供大规模、丰富标注的 Ambisonics 语料，生成流程透明且可直接获取，支持可复现研究。",
    },
    "arxiv-2402-17907": {
        "en": "Combines neural fields with stable IIR filters for a technically coherent HRTF model, with substantive evaluation and released code.",
        "zh": "将神经场与稳定 IIR 滤波器结合形成完整 HRTF 模型，并提供充分实验与开源代码。",
    },
    "arxiv-2405-13428": {
        "en": "Unifies neural upmixing through spherical-harmonic generation, evaluates the formulation across channel settings, and releases the implementation.",
        "zh": "以球谐生成统一神经上混，在多种声道设置下验证方法，并公开实现。",
    },
    "arxiv-2410-10676": {
        "en": "Adds language-driven spatial control to generative audio and releases a large dataset, checkpoints, inference code, and evaluation tools.",
        "zh": "为生成式音频引入语言驱动的空间控制，并公开大规模数据集、权重、推理代码与评测工具。",
    },
    "arxiv-2504-14906": {
        "en": "Addresses 360-video spatial-audio generation with an integrated method, broad empirical comparisons, and an official implementation.",
        "zh": "以完整方法解决 360 度视频空间音频生成，进行了广泛实验比较，并提供官方实现。",
    },
    "arxiv-2506-12199": {
        "en": "Introduces direct video-to-Ambisonics generation together with a sizable dataset, spatial metrics, checkpoints, and reproducible code.",
        "zh": "提出直接从视频生成 Ambisonics，并配套发布大规模数据集、空间指标、权重与可复现代码。",
    },
    "arxiv-2507-05053": {
        "en": "Substantially expands public personalized-HRTF data and pairs it with an open metrics toolbox for reproducible analysis and evaluation.",
        "zh": "显著扩展公开个体化 HRTF 数据，并提供开放指标工具箱以支持可复现分析与评测。",
    },
}


def main() -> None:
    data = json.loads(PAPERS_PATH.read_text(encoding="utf-8"))
    known = {paper["id"] for paper in data["papers"]}
    missing = sorted(set(HIGHLIGHTS) - known)
    if missing:
        raise ValueError(f"Unknown spatial highlight IDs: {missing}")

    spatial_count = 0
    for paper in data["papers"]:
        if "spatial-audio" not in paper["areas"]:
            continue
        spatial_count += 1
        rationale = HIGHLIGHTS.get(paper["id"])
        paper["aiAssessment"] = {
            "rating": "highlighted" if rationale else "standard",
            "rationale": rationale or {"en": "", "zh": ""},
            "assessor": "Codex",
            "rubricVersion": "1.0",
            "assessedAt": ASSESSED_AT,
        }

    PAPERS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Assessed {spatial_count} spatial papers; highlighted {len(HIGHLIGHTS)}.")


if __name__ == "__main__":
    main()
