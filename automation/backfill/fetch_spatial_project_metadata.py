#!/usr/bin/env python3
"""Fetch first-party license evidence for spatial-production repositories."""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


BACKFILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKFILL_DIR))

from fetch_project_metadata import fetch_repository  # noqa: E402


REPOSITORIES = [
    "AaronZ345/ISDrama",
    "Katarina-Poole/Spatial-Audio-Metrics",
    "PeiwenSun2000/Both-Ears-Wide-Open",
    "SheldonTsui/PseudoBinaural_CVPR2021",
    "SheldonTsui/SepStereo_ECCV2020",
    "SonyResearch/CCStereo",
    "apple/ml-spatial-librispeech",
    "ahogg/HRTF-upsampling-with-a-generative-adversarial-network-using-a-gnomonic-equiangular-projection",
    "ebu/bear",
    "ebu/ear-production-suite",
    "facebookresearch/2.5D-Visual-Sound",
    "facebookresearch/BinauralSpeechSynthesis",
    "feima1024/PINN-for-HRTF-upsampling",
    "ikets/HRTFInterpAE_public",
    "jaeyeonkim99/visage",
    "jin-woo-lee/hrtf-interpolation",
    "jin-woo-lee/nfs-binaural",
    "kronihias/ambix",
    "leomccormack/SPARTA",
    "leomccormack/Spatial_Audio_Framework",
    "liangsusan-git/AV-NeRF",
    "liuhuadai/OmniAudio",
    "merlresearch/neural-IIR-field",
    "microsoft/NeuralSpeech",
    "omeaningless/binaural-audio-generation",
    "pedro-morgado/spatialaudiogen",
    "see2sound/see2sound",
    "sh01k/MeshRIR",
    "tu-studio/IEMPluginSuite",
    "videolabs/libspatialaudio",
    "yongyizang/ambisonizer",
    "yzyouzhang/HRTF_field"
]


def fetch_verified_repository(repository: str) -> dict:
    metadata = fetch_repository(repository)
    request = Request(
        f"https://api.github.com/repos/{repository}/license",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "IntelligentAudioProductionIndex/1.0",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            license_record = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        if error.code not in {403, 404}:
            raise
        license_record = {}
    spdx = (license_record.get("license") or {}).get("spdx_id")
    metadata["spdx"] = spdx if spdx and spdx != "NOASSERTION" else None
    metadata["licenseUrl"] = license_record.get("html_url") or metadata["licenseUrl"]
    return metadata


def main() -> None:
    with ThreadPoolExecutor(max_workers=8) as executor:
        projects = list(executor.map(fetch_verified_repository, REPOSITORIES))
    output = BACKFILL_DIR / "spatial-project-github-metadata.json"
    output.write_text(json.dumps({"projects": projects}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Fetched {len(projects)} spatial project records into {output}.")


if __name__ == "__main__":
    main()
