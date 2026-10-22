# MorphMimic

**Physics-Based Motion Imitation for Diverse Human Body Shapes**

Longzhen Han, Beck Farrington-Wheeler, Sajjad Hussain, Awes Mubarak, Almas Baimagambetov, Nikolaos Polatidis
University of Brighton

[Project page](https://hansen1416.github.io/morph_mimic/) | Paper: coming soon (arXiv) | [Checkpoint](https://huggingface.co/YugoAmaryl/morph-mimic) (Hugging Face)

MorphMimic is one policy that tracks motion references on 128 SMPL body shapes in physics simulation. This repository contains the code to prepare references, train the policy and evaluate it, as used for the paper. It is derived from [ProtoMotions](https://github.com/NVlabs/ProtoMotions) and runs on Isaac Gym only (see [NOTICE](NOTICE) and [MODIFICATIONS.md](MODIFICATIONS.md)).

## What is here

| Path | Contents |
|---|---|
| `protomotions/` | The framework, plus the additions for this work: the `smpl_mor` robot, `GlobalClipPool` (streamed clip sampling), the validation and test evaluators |
| `examples/experiments/mimic/` | The experiment files behind the paper: the full-scale run and the 150-clip design comparison |
| `tools/` | Reference generation, refinement, packaging, unseen-body evaluation and analysis scripts |
| `protomotions/data/assets/` | The 128 trained body models (`mjcf/smpl_mor/`), the two 128-body unseen panels (`mjcf/smpl_mor_unseen_inside/`, `mjcf/smpl_mor_unseen_outside/`), all derived from SMPL (see Third-party material), and the shape coefficients (`all_betas.pt`) |
| `data/` | The clip-id list ordered by difficulty (`preprocessing/`) and the record of the train, validation and test split (`splits/`); identifiers only, no motion data |

## What is not here

- **The motion corpus.** It is derived from AMASS and HumanML3D, whose licences restrict redistribution, and is not distributed. See Data.
- **The SMPL model files, AMASS, HumanML3D, HUMOS and Isaac Gym.** Obtain each from its original source and accept its terms.
- **Other simulators and robots.** Only Isaac Gym and the `smpl_mor` robot are supported.

## Installation

Isaac Gym Preview 4 is not redistributable; install it from NVIDIA first. Then:

```bash
pip install -e .
pip install -r requirements_isaacgym.txt
```

`Dockerfile.isaacgym` builds an image with Python 3.8 and CUDA 12.1.

## Data

The corpus pairs every clip with all 128 bodies (64 shape vectors on a male and a female template). To build your own, you need AMASS, the SMPL model files and a HUMOS checkpoint; each step has usage notes in its tool's docstring:

1. The 128 body models are included (`protomotions/data/assets/mjcf/smpl_mor/`). To regenerate them or make new bodies, use SMPLSim with the SMPL model files, then register the result with `tools/generate_smpl_mor_asset_info.py`.
2. Generate references with HUMOS (external repository), one file per clip containing all 128 variants.
3. Convert them to motion libraries with grounding offsets. `tools/prepare_stage2_data.py` does this in resumable batches (export to AMASS-style files with `tools/export_humos_to_amass_npz.py`, convert with `tools/convert_amass_to_motionlib_with_morphology.py`, frame-zero offsets with `tools/compute_humos_frame0_offsets.py`). The clip order comes from `data/preprocessing/valid_ids_sorted_by_difficulty.txt` (pass it as `--valid-ids`). For a small set, run those tools directly; `DATA_DIR=/path/to/humos_proto bash tools/run_frame0_offsets.sh` runs the offsets over 16 chunks.
4. Refine the references: `tools/refine_humos_motion.py` for a motion file, or `tools/refine_humos_r2_per_clip.py` for per-clip files on an rclone remote.
5. For streaming training, `tools/repackage_stage2_per_clip.py` rewrites the shards as one file per clip.

Streaming training reads per-clip files through `rclone`, from a remote (`REMOTE:BUCKET/path/`) or a local directory.

## Training

Full-scale run (six GPUs, 2,048 environments per GPU):

```bash
python -u protomotions/train_agent.py \
    --robot-name smpl_mor --simulator isaacgym \
    --experiment-path examples/experiments/mimic/mlp_wide_stage2_discover_attention_slot_type.py \
    --experiment-name hhi_wide_stage2_discover_attention_slot_type \
    --global-clip-pool-source /path/to/hhi_stage2_per_clip_refined/ \
    --global-clip-pool-cache-dir /workspace/motion_cache \
    --global-clip-pool-size 256 --global-clip-pool-rebuild-every 256 \
    --global-clip-pool-weight-floor 0.05 --global-clip-pool-random-fraction 0.2 \
    --num-envs 6144 --batch-size 24576 --ngpu 6
```

Add `--use-wandb --wandb-project <project> --wandb-entity <entity>` to log to Weights & Biases.

Design comparison on the 150-clip development set (cases A to H; one GPU per run):

```bash
bash tools/train_150_evalfix_ablation.sh --dry-run          # print the commands
bash tools/train_150_evalfix_ablation.sh                    # cases A-E, seed 0, and C seed 1
bash tools/train_150_evalfix_ablation.sh --all-seeds        # also seed 1 of A, B, D and E
ABLATION_RUNS="A:2 B:2 C:2 D:2" bash tools/train_150_evalfix_ablation.sh   # seed 2
bash tools/train_150_evalfix_unrefined.sh                   # cases F-H
```

Set `ABLATION_MOTION_DIR` to the folder holding `small150_128shape.pt` and `small150_128shape_refined.pt`, and `ABLATION_WANDB_ENTITY` to enable W&B logging.

## Evaluation

Held-out clips on trained bodies (one body per clip; the test manifest is read only by the test evaluator):

```bash
python protomotions/evaluate_validation_split.py --checkpoint results/<experiment>/last.ckpt \
    --simulator isaacgym --num-envs 128 --clip-batch-size 128
python protomotions/evaluate_test_split.py --checkpoint results/<experiment>/last.ckpt \
    --simulator isaacgym --num-envs 128 --clip-batch-size 128
```

A checkpoint's stored config points at the clip source used in training. To read the clips from another location, add `--overrides motion_lib.r2_source=/path/to/hhi_stage2_per_clip_refined/`.

Unseen bodies: the two panels (`smpl_mor_unseen_inside`, shape vectors within the training range, and `smpl_mor_unseen_outside`, up to five standard deviations out) are included. Each needs a motion file with every evaluated clip on every body of the panel, which you generate with the Data steps for that panel's bodies. Replay one panel, then compare checkpoints:

```bash
python tools/analyze_unseen_morphology_generalization.py --checkpoint <ckpt> \
    --motion-file <merged motion file> \
    --unseen-asset-folder mjcf/smpl_mor_unseen_inside/ --unseen-asset-info mjcf/smpl_mor_unseen_inside/assets.yaml \
    --envs-per-asset 32 --output inside_<name>.csv
python tools/compare_checkpoints_unseen_morphology.py --baseline <name>=<csv> --candidate <name>=<csv> \
    --output-prefix compare
```

The physical analysis uses `tools/classify_clip_semantics.py`, `tools/analyze_morphology_motion_interaction.py`, `tools/aggregate_morphology_motion_interaction.py` and `tools/test_morphology_motion_variance_significance.py`.

Without the corpus, the evaluators and the training commands cannot run; the checkpoint can still be loaded for inspection.

## Checkpoints

The MorphMimic checkpoint (epoch 28,170) is on [Hugging Face](https://huggingface.co/YugoAmaryl/morph-mimic) under a non-commercial licence (CC BY-NC 4.0). SHA-256 of `last.ckpt`:

```
4b83f20c93bf95fab389fc8935685ef8a2c7e46583f765e8c802421edb4479cb
```

## Citation

The paper reference will be added when the arXiv version is available. Until then:

```bibtex
@misc{han2026morphmimic,
  title  = {MorphMimic: Physics-Based Motion Imitation for Diverse Human Body Shapes},
  author = {Han, Longzhen and Farrington-Wheeler, Beck and Hussain, Sajjad and
            Mubarak, Awes and Baimagambetov, Almas and Polatidis, Nikolaos},
  year   = {2026},
  note   = {Preprint, link to follow}
}
```

Please also cite [ProtoMotions](https://github.com/NVlabs/ProtoMotions), which this code builds on.

## Third-party material

- **SMPL body models.** The files in `protomotions/data/assets/mjcf/smpl_mor/` and in the two `smpl_mor_unseen_*` panels are derived from the SMPL body model of the Max Planck Institute for Intelligent Systems. They are not covered by this repository's Apache License; they are made available with attribution under the SMPL-Body license ([CC BY 4.0](https://smpl.is.tue.mpg.de/bodylicense.html)). Each file is one body shape written as a simulation model of boxes, capsules and spheres; it contains no mesh, shape blendshapes or SMPL model files. Creating new bodies needs the SMPL model files and the [SMPL Model License](https://smpl.is.tue.mpg.de/modellicense.html) (non-commercial research). If you use these files, please cite Loper et al., "SMPL: A Skinned Multi-Person Linear Model", ACM Transactions on Graphics 34(6), 2015. Details are in [NOTICE](NOTICE).
- **Motion data.** AMASS and HumanML3D motions are not included and stay under their own terms ([AMASS licence](https://amass.is.tue.mpg.de/license.html): non-commercial research use; no redistribution without Max-Planck's written permission).
- **ProtoMotions.** This code is derived from [ProtoMotions](https://github.com/NVlabs/ProtoMotions) (Apache-2.0).

## License

Apache License 2.0 for the code; see [LICENSE.md](LICENSE.md) and [NOTICE](NOTICE). The third-party material above keeps its own terms.
