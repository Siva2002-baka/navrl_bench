<<<<<<< HEAD
# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
=======
# Copyright (c) 2022-2025, The Isaac Lab Project Developers
>>>>>>> 14e3b3c (RL Local Controller)
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass

<<<<<<< HEAD
from isaaclab_rl.rsl_rl import RslRlOnPolicyRunnerCfg, RslRlPpoActorCriticCfg, RslRlPpoAlgorithmCfg
=======
from isaaclab_rl.rsl_rl import (
    RslRlOnPolicyRunnerCfg,
    RslRlPpoActorCriticCfg,
    RslRlPpoAlgorithmCfg,
)


@configclass
class RslRlPpoAuxAlgorithmCfg(RslRlPpoAlgorithmCfg):
    class_name: str = "ppo_mod.PPO"
    aux_loss_coef: float = 0.01
>>>>>>> 14e3b3c (RL Local Controller)


@configclass
class PPORunnerCfg(RslRlOnPolicyRunnerCfg):
<<<<<<< HEAD
    num_steps_per_env = 16
    max_iterations = 150
    save_interval = 100
    experiment_name = "m3_obstacle_avoidance"
    policy = RslRlPpoActorCriticCfg(
        init_noise_std=1.0,
        actor_obs_normalization=False,
        critic_obs_normalization=False,
        actor_hidden_dims=[256, 128],
        critic_hidden_dims=[256, 128],
        activation="elu",
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.005,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=1.0e-3,
=======
    num_steps_per_env = 32
    max_iterations = 12000
    save_interval = 200
    experiment_name = "m3_transformer_aux_ttc_blocked"

    policy = RslRlPpoActorCriticCfg(
        class_name="ActorCriticScanTransformer",
        init_noise_std=0.3,
        actor_obs_normalization=True,
        critic_obs_normalization=True,
        actor_hidden_dims=[256, 128],
        critic_hidden_dims=[256, 256, 128],
        activation="elu",
    )

    algorithm = RslRlPpoAuxAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.00,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=5.0e-4,
>>>>>>> 14e3b3c (RL Local Controller)
        schedule="adaptive",
        gamma=0.99,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
<<<<<<< HEAD
=======

        # New auxiliary transformer loss coefficient
        aux_loss_coef=0.01,
>>>>>>> 14e3b3c (RL Local Controller)
    )