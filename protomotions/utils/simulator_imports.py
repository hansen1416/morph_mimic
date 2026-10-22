# SPDX-FileCopyrightText: Copyright (c) 2025-2026 The ProtoMotions Developers
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Utility for importing the simulator module before torch.

IsaacGym has a strict requirement that it must be imported before torch.
This module provides a utility to handle that import order correctly.
"""


def import_simulator_before_torch(simulator_name):
    """
    Import isaacgym when it is the selected simulator.

    This must be called before any imports that might bring in torch (directly or transitively).
    Typically called right after parsing arguments.

    Args:
        simulator_name: Name of the simulator (this release supports 'isaacgym' only)

    Example:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--simulator", type=str, required=True)
        args = parser.parse_args()

        from protomotions.utils.simulator_imports import import_simulator_before_torch
        import_simulator_before_torch(args.simulator)

        # Now safe to import torch
        import torch
    """
    if simulator_name == "isaacgym":
        import isaacgym  # noqa: F401
