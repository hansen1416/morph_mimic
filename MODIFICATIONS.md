# Modifications to ProtoMotions

Comparison with ProtoMotions at commit a87d2f3 (2026-05-03), for the files in this repository.
Generated; see NOTICE for the summary.

## Modified files from ProtoMotions (44)

- `.gitignore`
- `.license-header.txt`
- `.pre-commit-config.yaml`
- `protomotions/agents/base_agent/agent.py`
- `protomotions/agents/base_agent/config.py`
- `protomotions/agents/common/config.py`
- `protomotions/agents/common/transformer.py`
- `protomotions/agents/evaluators/base_evaluator.py`
- `protomotions/agents/evaluators/config.py`
- `protomotions/agents/evaluators/metrics.py`
- `protomotions/agents/evaluators/mimic_evaluator.py`
- `protomotions/agents/ppo/agent.py`
- `protomotions/agents/ppo/config.py`
- `protomotions/agents/utils/normalization.py`
- `protomotions/components/motion_lib.py`
- `protomotions/components/pose_lib.py`
- `protomotions/envs/action/__init__.py`
- `protomotions/envs/action/action_functions.py`
- `protomotions/envs/base_env/env.py`
- `protomotions/envs/component_factories.py`
- `protomotions/envs/context_views.py`
- `protomotions/envs/control/mimic_control.py`
- `protomotions/envs/motion_manager/config.py`
- `protomotions/envs/motion_manager/mimic_motion_manager.py`
- `protomotions/envs/motion_manager/motion_manager.py`
- `protomotions/envs/obs/__init__.py`
- `protomotions/envs/obs/humanoid.py`
- `protomotions/envs/obs/humanoid_historical.py`
- `protomotions/envs/rewards/__init__.py`
- `protomotions/envs/rewards/base.py`
- `protomotions/envs/rewards/tracking.py`
- `protomotions/envs/terminations/__init__.py`
- `protomotions/envs/terminations/tracking.py`
- `protomotions/inference_agent.py`
- `protomotions/robot_configs/base.py`
- `protomotions/robot_configs/factory.py`
- `protomotions/simulator/base_simulator/config.py`
- `protomotions/simulator/base_simulator/simulator.py`
- `protomotions/simulator/factory.py`
- `protomotions/simulator/isaacgym/config.py`
- `protomotions/simulator/isaacgym/simulator.py`
- `protomotions/train_agent.py`
- `protomotions/utils/component_builder.py`
- `protomotions/utils/simulator_imports.py`

## New files (38)

- `data/preprocessing/valid_ids_sorted_by_difficulty.txt`
- `data/splits/hhi_stage2_v1/split_metadata.json`
- `examples/experiments/mimic/mlp_wide_discover_attention.py`
- `examples/experiments/mimic/mlp_wide_discover_attention_adaln.py`
- `examples/experiments/mimic/mlp_wide_discover_attention_slot_type.py`
- `examples/experiments/mimic/mlp_wide_discover_historical_lookahead.py`
- `examples/experiments/mimic/mlp_wide_stage2_discover_attention.py`
- `examples/experiments/mimic/mlp_wide_stage2_discover_attention_slot_type.py`
- `examples/experiments/mimic/mlp_wide_stage2_discover_attention_slot_type_fulldata.py`
- `protomotions/agents/common/morphology_transformer.py`
- `protomotions/components/collision_geometry.py`
- `protomotions/components/global_clip_pool.py`
- `protomotions/components/motion_lib_pool.py`
- `protomotions/evaluate_test_split.py`
- `protomotions/evaluate_validation_split.py`
- `protomotions/robot_configs/smpl_mor.py`
- `protomotions/tests/test_global_clip_pool_splits.py`
- `protomotions/tests/test_sampling_strategy.py`
- `protomotions/tests/test_train_150_evalfix_ablation.py`
- `tools/aggregate_morphology_motion_interaction.py`
- `tools/analyze_morphology_motion_interaction.py`
- `tools/analyze_unseen_morphology_generalization.py`
- `tools/classify_clip_semantics.py`
- `tools/compare_checkpoints_unseen_morphology.py`
- `tools/compute_humos_frame0_offsets.py`
- `tools/convert_amass_to_motionlib_with_morphology.py`
- `tools/create_hhi_split_manifests.py`
- `tools/export_humos_to_amass_npz.py`
- `tools/generate_smpl_mor_asset_info.py`
- `tools/merge_motion_shards.py`
- `tools/prepare_stage2_data.py`
- `tools/refine_humos_motion.py`
- `tools/refine_humos_r2_per_clip.py`
- `tools/repackage_stage2_per_clip.py`
- `tools/run_frame0_offsets.sh`
- `tools/test_morphology_motion_variance_significance.py`
- `tools/train_150_evalfix_ablation.sh`
- `tools/train_150_evalfix_unrefined.sh`

Not listed above: the 389 body-model and shape-coefficient files under
`protomotions/data/assets/`, which are described in the third-party section of NOTICE.

The other 83 files that come from ProtoMotions are unchanged.
