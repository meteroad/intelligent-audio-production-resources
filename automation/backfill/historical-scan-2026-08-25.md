# Historical literature scan: intelligent audio production

Date: 2026-08-25

## Scope

This is a first-pass candidate inventory for backfilling the website. It covers:

- automatic mixing and processing-graph estimation;
- audio-effects and production-style representations;
- differentiable audio processors and effects modeling;
- effect recognition, parameter inference, inversion, and removal;
- automatic mastering and mastering evaluation.

Spatial audio is intentionally deferred to a later pass. General music generation,
source separation, speech enhancement, and generic music representations are excluded
unless the work directly addresses an audio-production task.

## First-pass result

- 54 unique paper candidates are listed below: 37 core imports, 10 historical or
  supporting works, 1 already indexed paper, and 6 papers already pending in the
  weekly-scout pull request.
- The AutomaticMixingPapers seed contains 89 records from 2000--2025 and 31 non-empty
  code fields. It also contains duplicate records and links of mixed quality, so it is
  used as a discovery source rather than copied into the website.
- This pass found a separate initial set of 10 high-value resource candidates. Their
  licenses, weights, runnable inference paths, datasets, and maintenance status still
  need project-level verification.

## How to read the list

- **A**: central work with a verified paper/project page; import first.
- **B**: useful historical or supporting work; import after the core list.
- **Indexed**: already present in the website data.
- **Pending PR**: already proposed by the weekly scout and should not be duplicated.
- A code link means that a public implementation or research repository was found. A
  blank code column does not prove that no code exists; it means code was not verified
  in this pass.

## Automatic mixing and graph control

| Priority | Year | Work | Paper | Code / project |
| --- | ---: | --- | --- | --- |
| B | 2017 | Ten Years of Automatic Mixing | [paper](http://www.brechtdeman.com/publications/pdf/WIMP3.pdf) | |
| A | 2021 | Automatic Multitrack Mixing With a Differentiable Mixing Console of Neural Audio Effects | [arXiv](https://arxiv.org/abs/2010.10291) | [automix-toolkit](https://github.com/csteinmetz1/automix-toolkit) |
| A | 2021 | A Deep Learning Approach to Intelligent Drum Mixing with the Wave-U-Net | [paper](http://davemoffat.com/wp/wp-content/uploads/2021/03/21023.pdf) | [Mix-Wave-U-Net](https://github.com/f90/Mix-Wave-U-Net) |
| A | 2022 | Automatic Music Mixing with Deep Learning and Out-of-Domain Data | [arXiv](https://arxiv.org/abs/2208.11428) | [FxNorm-Automix](https://github.com/sony/FxNorm-automix) |
| A | 2023 | Music Mixing Style Transfer: A Contrastive Learning Approach to Disentangle Audio Effects | [arXiv](https://arxiv.org/abs/2211.02247) | [source](https://github.com/jhtonyKoo/music_mixing_style_transfer) |
| A | 2023 | Blind Estimation of Audio Processing Graph | [arXiv](https://arxiv.org/abs/2303.08610) | [project](https://sh-lee97.github.io/apg/) |
| A | 2023 | Audio Mixing Inversion via Embodied Self-supervised Learning | [paper](https://link.springer.com/article/10.1007/s11633-023-1441-9) | |
| A | 2024 | Diff-MST: Differentiable Mixing Style Transfer | [arXiv](https://arxiv.org/abs/2407.08889) | [Diff-MST](https://github.com/sai-soum/Diff-MST) |
| A | 2024 | Searching for Music Mixing Graphs: A Pruning Approach | [arXiv](https://arxiv.org/abs/2406.01049) | [project](https://sh-lee97.github.io/grafx-prune/) |
| A | 2024 | ST-ITO: Controlling Audio Effects for Style Transfer with Inference-Time Optimization | [arXiv](https://arxiv.org/abs/2410.21233) | [ST-ITO](https://github.com/csteinmetz1/st-ito) |
| A | 2025 | Automatic Music Mixing Using a Generative Model of Effect Embeddings | [arXiv](https://arxiv.org/abs/2511.08040) | [MEGAMI](https://github.com/SonyResearch/MEGAMI) |
| A | 2025 | LLM2Fx-Tools: Tool Calling for Music Post-Production | [arXiv](https://arxiv.org/abs/2512.01559) | [LLM2Fx](https://github.com/SonyResearch/LLM2Fx) |
| Pending PR | 2026 | Rethinking Automatic Music Mixing as Sequential Stem Blending | [arXiv](https://arxiv.org/abs/2608.05506) | |
| Pending PR | 2026 | Diff2Mix: Controllable Music Mixing via Diffusion Models and Differentiable Audio Effects | [arXiv](https://arxiv.org/abs/2608.05442) | |

## Effects representation and controllable style

| Priority | Year | Work | Paper | Code / project |
| --- | ---: | --- | --- | --- |
| B | 2020 | One-Shot Parametric Audio Production Style Transfer With Application to Frequency Equalization | [Adobe Research](https://research.adobe.com/publication/one-shot-parametric-audio-production-style-transfer-with-application-to-frequency-equalization/) | [demo](https://js-mim.github.io/sp-demo/) |
| A | 2022 | Style Transfer of Audio Effects with Differentiable Signal Processing | [arXiv](https://arxiv.org/abs/2207.08759) | [DeepAFx-ST](https://github.com/adobe-research/DeepAFx-ST) |
| A | 2024 | Towards Zero-Shot Amplifier Modeling: One-to-Many Amplifier Modeling via Tone Embedding Control | [arXiv](https://arxiv.org/abs/2407.10646) | |
| A | 2024 | Open-Amp: Synthetic Data Framework for Audio Effect Foundation Models | [arXiv](https://arxiv.org/abs/2411.14972) | [OpenAmp](https://github.com/Alec-Wright/OpenAmp) |
| A | 2025 | Text2FX: Harnessing CLAP Embeddings for Text-Guided Audio Effects | [arXiv](https://arxiv.org/abs/2409.18847) | [Text2FX](https://github.com/anniejchu/text2fx) |
| A | 2025 | Fx-Encoder++: Extracting Instrument-Wise Audio Effects Representations from Mixtures | [arXiv](https://arxiv.org/abs/2507.02273) | [Fx-Encoder++](https://github.com/SonyResearch/Fx-Encoder_PlusPlus) |
| A | 2025 | DiffVox: A Differentiable Model for Capturing and Analysing Professional Effects Distributions | [arXiv](https://arxiv.org/abs/2504.14735) | [DiffVox](https://github.com/SonyResearch/diffvox) |
| Indexed | 2026 | Beyond Dry References: Learning Relative Audio Effects Representations via Contrastive Distance Learning | [arXiv](https://arxiv.org/abs/2608.10573) | [RelFx](https://github.com/TMEGalaxyAudioEffect/relfx-ismir2026-release) |
| Pending PR | 2026 | EG-VAE: A Unified Framework for Electric Guitar Tone Transfer and Removal | [arXiv](https://arxiv.org/abs/2608.05513) | |

## Differentiable processors and effects modeling

| Priority | Year | Work | Paper | Code / project |
| --- | ---: | --- | --- | --- |
| B | 2020 | DDSP: Differentiable Digital Signal Processing | [arXiv](https://arxiv.org/abs/2001.04643) | [DDSP](https://github.com/magenta/ddsp) |
| B | 2020 | Differentiable IIR Filters for Machine Learning Applications | [DAFx](https://www.dafx.de/paper-archive/2020/proceedings/papers/DAFx2020_paper_52.pdf) | |
| A | 2020 | Neural Parametric Equalizer Matching Using Differentiable Biquads | [DAFx](https://dafx2020.mdw.ac.at/proceedings/papers/DAFx2020_paper_7.pdf) | |
| A | 2021 | Differentiable Signal Processing With Black-Box Audio Effects | [arXiv](https://arxiv.org/abs/2105.04752) | [DeepAFx](https://github.com/adobe-research/DeepAFx) |
| A | 2022 | Direct Design of Biquad Filter Cascades with Deep Learning by Sampling Random Polynomials | [arXiv](https://arxiv.org/abs/2110.03691) | [IIRNet](https://github.com/csteinmetz1/IIRNet) |
| A | 2022 | Differentiable Artificial Reverberation | [arXiv](https://arxiv.org/abs/2105.13940) | [demo](https://sh-lee97.github.io/DAR-samples/) |
| A | 2024 | GRAFX: An Open-Source Library for Audio Processing Graphs in PyTorch | [arXiv](https://arxiv.org/abs/2408.03204) | [GRAFX](https://github.com/sh-lee97/grafx) |
| A | 2024 | Modeling Analog Dynamic Range Compressors Using Deep Learning and State-Space Models | [arXiv](https://arxiv.org/abs/2403.16331) | [project](https://int0thewind.github.io/s4drc/) |
| A | 2025 | DiffFx: A Toolkit for Differentiable Audio Effects Processors | [ISMIR](https://ismir2025program.ismir.net/lbd_422.html) | [DiffFx](https://github.com/ytsrt66589/diffFx-pytorch) |
| A | 2025 | NablAFx: A Framework for Differentiable Black-Box and Gray-Box Modeling of Audio Effects | [arXiv](https://arxiv.org/abs/2502.11668) | [NablAFx](https://github.com/mcomunita/nablafx) |
| A | 2025 | Differentiable Black-Box and Gray-Box Modeling of Nonlinear Audio Effects | [arXiv](https://arxiv.org/abs/2502.14405) | [code](https://github.com/mcomunita/nablafx) |

## Effect recognition, parameter inference, inversion, and removal

| Priority | Year | Work | Paper | Code / project |
| --- | ---: | --- | --- | --- |
| A | 2021 | Guitar Effects Recognition and Parameter Estimation with Convolutional Neural Networks | [arXiv](https://arxiv.org/abs/2012.03216) | [source](https://github.com/mcomunita/gfx_classifier) |
| A | 2021 | Reverse Engineering of a Recording Mix with Differentiable Digital Signal Processing | [paper](https://pubs.aip.org/jasa/article/150/1/608/606638) | [project](https://jtcolonel.github.io/RevEng/) |
| A | 2022 | Distortion Audio Effects: Learning How to Recover the Clean Signal | [arXiv](https://arxiv.org/abs/2202.01664) | [demo](https://joimort.github.io/distortionremoval/) |
| B | 2022 | Convolutional Neural Networks for the Classification of Guitar Effects and Extraction of Parameter Settings from Instrument Mixes | [paper](https://link.springer.com/article/10.1186/s13636-022-00257-4) | [source](https://github.com/kevingerkens/gitfx) |
| A | 2023 | General Purpose Audio Effect Removal | [arXiv](https://arxiv.org/abs/2308.16177) | [project](https://csteinmetz1.github.io/RemFX/) |
| A | 2023 | Blind Estimation of Audio Effects Using an Auto-Encoder Approach and Differentiable Digital Signal Processing | [arXiv](https://arxiv.org/abs/2310.11781) | |
| B | 2023 | Style Transfer for Non-Differentiable Audio Effects | [arXiv](https://arxiv.org/abs/2309.17125) | |
| A | 2024 | Automatic Equalization for Individual Instrument Tracks Using Convolutional Neural Networks | [arXiv](https://arxiv.org/abs/2407.16691) | |
| A | 2024 | End-to-End Amp Modeling: From Data to Controllable Guitar Amplifier Models | [arXiv](https://arxiv.org/abs/2403.08559) | |
| A | 2025 | Improving Inference-Time Optimisation for Vocal Effects Style Transfer with a Gaussian Prior | [arXiv](https://arxiv.org/abs/2505.11315) | [DiffVox](https://github.com/SonyResearch/diffvox) |
| Pending PR | 2026 | Black-Box Optimization for Identifying and Inverting Audio Dynamic Range Control Effects | [arXiv](https://arxiv.org/abs/2607.19645) | |
| Pending PR | 2026 | Simulation-Based Plate-Reverb Parameter Estimation from a Single Impulse Response | [arXiv](https://arxiv.org/abs/2608.00656) | |
| Pending PR | 2026 | Band-Count Dense Modal Estimation with Fixed-Frequency Differentiable Resonator Refinement | [arXiv](https://arxiv.org/abs/2608.00667) | |

## Mastering and mastering evaluation

| Priority | Year | Work | Paper | Code / project |
| --- | ---: | --- | --- | --- |
| B | 2013 | Automated Tonal Balance Enhancement for Audio Mastering Applications | [AES](https://aes2.org/publications/elibrary-page/?id=16737) | |
| B | 2014 | A Statistical Approach to Automated Offline Dynamic Processing in the Audio Mastering Process | [DAFx](https://dafx.de/paper-archive/2014/dafx14_marcel_hilsamer_a_statistical_approach_to.pdf) | |
| B | 2016 | Deep Neural Networks for Dynamic Range Compression in Mastering Applications | [AES](https://aes2.org/publications/elibrary-page/?id=18237) | |
| B | 2018 | Evaluating Music Mastering Quality Using Machine Learning | [paper](https://bil.eecs.yorku.ca/wp-content/uploads/2018/05/p126-shtern.pdf) | |
| A | 2022 | End-to-End Music Remastering System Using Self-Supervised and Adversarial Training | [arXiv](https://arxiv.org/abs/2202.08520) | [source and weights](https://github.com/jhtonyKoo/e2e_music_remastering_system) |
| A | 2025 | ITO-Master: Inference-Time Optimization for Audio Effects Modeling of Music Mastering Processors | [arXiv](https://arxiv.org/abs/2506.16889) | [demo](https://huggingface.co/spaces/jhtonyKoo/ITO-Master) |
| A | 2025 | SonicMaster: Towards Controllable All-in-One Music Restoration and Mastering | [arXiv](https://arxiv.org/abs/2508.03448) | [SonicMaster](https://github.com/AMAAI-Lab/SonicMaster) |

## Dataset and resource candidates discovered during the scan

These belong in the project/resource index rather than the paper list:

| Resource | Role | Link |
| --- | --- | --- |
| AutomaticMixingPapers | Broad automatic-mixing bibliography and historical seed source | [GitHub](https://github.com/csteinmetz1/AutomaticMixingPapers) |
| automix-toolkit | Training, inference, evaluation, datasets, and pretrained models for automatic mixing | [GitHub](https://github.com/csteinmetz1/automix-toolkit) |
| FxNorm-Automix | Reproducible automatic-mixing implementation using wet data | [GitHub](https://github.com/sony/FxNorm-automix) |
| dasp-pytorch | Differentiable gain, EQ, dynamics, reverb, distortion, and stereo processors | [GitHub](https://github.com/csteinmetz1/dasp-pytorch) |
| GRAFX | Differentiable audio-processing graphs | [GitHub](https://github.com/sh-lee97/grafx) |
| DiffFx | Differentiable audio-effects toolkit | [GitHub](https://github.com/ytsrt66589/diffFx-pytorch) |
| NablAFx | Black-box and gray-box audio-effects modeling framework | [GitHub](https://github.com/mcomunita/nablafx) |
| ToneTwist AFx | Community-extensible dry/wet nonlinear-effects dataset | [GitHub](https://github.com/mcomunita/tonetwist-afx-dataset) |
| Open-Amp | Synthetic guitar amplifier/effects data framework | [GitHub](https://github.com/Alec-Wright/OpenAmp) |
| DeepAFx / DeepAFx-ST | Black-box differentiable effects and production-style transfer implementations | [DeepAFx](https://github.com/adobe-research/DeepAFx), [DeepAFx-ST](https://github.com/adobe-research/DeepAFx-ST) |

## Import recommendation

1. Merge or close the existing weekly-scout PR before backfilling, so its six new
   records have one clear source of truth.
2. Import the **A** papers in small batches by task, with bilingual summaries and
   normalized author/venue metadata.
3. Add the resource candidates separately and verify license, weights, inference,
   training, dataset access, and last activity. A paper having a code link is not
   enough to call the project reproducible.
4. Add **B** papers as historical context after the core open-source landscape is
   useful. Avoid importing all 89 AutomaticMixingPapers entries without link and
   duplicate cleanup.
