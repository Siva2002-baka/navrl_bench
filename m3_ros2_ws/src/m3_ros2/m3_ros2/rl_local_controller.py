import math
import numpy as np
import onnxruntime as ort
from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
import os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, Path
import tf2_ros
from rclpy.duration import Duration
from sensor_msgs.msg import LaserScan
from rclpy.time import Time


def wrap_to_pi(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


def yaw_from_quat(q):
<<<<<<< HEAD
    # geometry_msgs Quaternion: x, y, z, w
=======
>>>>>>> 14e3b3c (RL Local Controller)
    return math.atan2(
        2.0 * (q.w * q.z + q.x * q.y),
        1.0 - 2.0 * (q.y * q.y + q.z * q.z),
    )


class RLLocalController(Node):
    def __init__(self):
        super().__init__("rl_local_controller")
<<<<<<< HEAD
        pkg_share = get_package_share_directory('m3_ros2')
        self.declare_parameter("onnx_path", os.path.join(pkg_share, 'rl_policies', 'policy.onnx'))
=======

        pkg_share = get_package_share_directory("m3_ros2")

        self.declare_parameter("onnx_path", os.path.join(pkg_share, "rl_policies", "policy_63600.onnx"))
>>>>>>> 14e3b3c (RL Local Controller)
        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("path_topic", "/plan")
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("map_frame", "map")
        self.declare_parameter("base_frame", "base_link")

        self.declare_parameter("num_path_points", 8)
        self.declare_parameter("path_step", 8)
<<<<<<< HEAD
        self.declare_parameter("num_scan_rays", 72)

        self.declare_parameter("max_vx", 0.5)
        self.declare_parameter("max_vy", 0.5)
        self.declare_parameter("max_wz", 1.0)

        self.onnx_path = self.get_parameter("onnx_path").value
        if not self.onnx_path:
            raise RuntimeError("onnx_path parameter is empty")

        self.session = ort.InferenceSession(
            self.onnx_path,
            providers=["CPUExecutionProvider"],
        )
=======
        self.declare_parameter("path_window_normalization_m", 4.0)
        self.declare_parameter("num_scan_rays", 144)
        self.declare_parameter("scan_max_range", 4.0)

        self.declare_parameter("max_vx", 0.75)
        self.declare_parameter("max_vy", 0.75)
        self.declare_parameter("max_wz", 2.0)
        self.declare_parameter("max_delta_vx", 0.025)
        self.declare_parameter("max_delta_vy", 0.025)
        self.declare_parameter("max_delta_wz", 0.08)
        self.declare_parameter("control_rate_hz", 30.0)

        self.declare_parameter("enable_action_rate_limit", True)
        self.declare_parameter("emergency_stop_scan_m", 0.18)
        self.declare_parameter("enable_motion", False)
        self.declare_parameter("goal_tolerance_m", 0.08)
        self.declare_parameter("goal_slowdown_m", 0.50)
        self.declare_parameter("goal_stop_m", 0.05)
        self.declare_parameter("debug_log_period_s", 2.0)
        self.debug_log_period_s = float(self.get_parameter("debug_log_period_s").value)
        self.last_debug_log_time = self.get_clock().now()

        self.goal_slowdown_m = float(self.get_parameter("goal_slowdown_m").value)
        self.goal_stop_m = float(self.get_parameter("goal_stop_m").value)
        self.goal_tolerance_m = float(self.get_parameter("goal_tolerance_m").value)
        self.enable_motion = bool(self.get_parameter("enable_motion").value)

        self.onnx_path = self.get_parameter("onnx_path").value
        self.session = ort.InferenceSession(self.onnx_path, providers=["CPUExecutionProvider"])
>>>>>>> 14e3b3c (RL Local Controller)

        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

<<<<<<< HEAD
        self.num_path_points = int(self.get_parameter("num_path_points").value)
        self.path_step = int(self.get_parameter("path_step").value)
        self.num_scan_rays = int(self.get_parameter("num_scan_rays").value)
=======
        input_shape = self.session.get_inputs()[0].shape
        self.expected_obs_dim = input_shape[1] if len(input_shape) > 1 and isinstance(input_shape[1], int) else None

        self.num_path_points = int(self.get_parameter("num_path_points").value)
        self.path_step = int(self.get_parameter("path_step").value)
        self.path_norm_m = float(self.get_parameter("path_window_normalization_m").value)
        self.num_scan_rays = int(self.get_parameter("num_scan_rays").value)
        self.scan_max_range = float(self.get_parameter("scan_max_range").value)
>>>>>>> 14e3b3c (RL Local Controller)

        self.max_vx = float(self.get_parameter("max_vx").value)
        self.max_vy = float(self.get_parameter("max_vy").value)
        self.max_wz = float(self.get_parameter("max_wz").value)

<<<<<<< HEAD
=======
        self.max_delta = np.array(
            [
                float(self.get_parameter("max_delta_vx").value),
                float(self.get_parameter("max_delta_vy").value),
                float(self.get_parameter("max_delta_wz").value),
            ],
            dtype=np.float32,
        )

        self.enable_action_rate_limit = bool(self.get_parameter("enable_action_rate_limit").value)
        self.emergency_stop_scan_m = float(self.get_parameter("emergency_stop_scan_m").value)

>>>>>>> 14e3b3c (RL Local Controller)
        self.map_frame = self.get_parameter("map_frame").value
        self.base_frame = self.get_parameter("base_frame").value

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.latest_scan = None
<<<<<<< HEAD
        self.latest_odom = None
        self.latest_path = None
        self.previous_action = np.zeros(3, dtype=np.float32)
        self._last_tf_warn_ns = 0

        self.create_subscription(
            LaserScan,
            self.get_parameter("scan_topic").value,
            self.scan_callback,
            10,
        )

        self.create_subscription(
            Odometry,
            self.get_parameter("odom_topic").value,
            self.odom_callback,
            10,
        )

        self.create_subscription(
            Path,
            self.get_parameter("path_topic").value,
            self.path_callback,
            10,
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            self.get_parameter("cmd_vel_topic").value,
            10,
        )

        self.timer = self.create_timer(0.05, self.control_loop)  # 20 Hz

        self.get_logger().info(f"Loaded ONNX policy: {self.onnx_path}")
=======
        self.latest_scan_m = None
        self.latest_odom = None
        self.latest_path = None

        self.previous_action = np.zeros(3, dtype=np.float32)
        self.applied_cmd = np.zeros(3, dtype=np.float32)

        self._last_tf_warn_ns = 0
        self._debug_count = 0

        self.create_subscription(LaserScan, self.get_parameter("scan_topic").value, self.scan_callback, 10)
        self.create_subscription(Odometry, self.get_parameter("odom_topic").value, self.odom_callback, 10)
        self.create_subscription(Path, self.get_parameter("path_topic").value, self.path_callback, 10)

        self.cmd_pub = self.create_publisher(Twist, self.get_parameter("cmd_vel_topic").value, 10)

        rate_hz = float(self.get_parameter("control_rate_hz").value)
        self.timer = self.create_timer(1.0 / rate_hz, self.control_loop)

        self.get_logger().info(f"Loaded ONNX policy: {self.onnx_path}")
        self.get_logger().info(f"Expected ONNX obs dim: {self.expected_obs_dim}; expected new actor obs dim = 168")
>>>>>>> 14e3b3c (RL Local Controller)

    def scan_callback(self, msg: LaserScan):
        ranges = np.array(msg.ranges, dtype=np.float32)

        ranges = np.nan_to_num(
            ranges,
            nan=msg.range_max,
            posinf=msg.range_max,
            neginf=msg.range_max,
        )

        ranges = np.clip(ranges, msg.range_min, msg.range_max)

<<<<<<< HEAD
        # Resample scan to exactly 72 rays if needed.
        if len(ranges) != self.num_scan_rays:
            old_idx = np.linspace(0, len(ranges) - 1, len(ranges))
            new_idx = np.linspace(0, len(ranges) - 1, self.num_scan_rays)
            ranges = np.interp(new_idx, old_idx, ranges).astype(np.float32)

        # IsaacLab scan was normalized by max_range.
        scan_norm = ranges / float(msg.range_max)
        scan_norm = np.clip(scan_norm, 0.0, 1.0)

        self.latest_scan = scan_norm.astype(np.float32)
=======
        old_angles = msg.angle_min + np.arange(len(ranges), dtype=np.float32) * msg.angle_increment
        target_angles = np.linspace(-math.pi, math.pi, self.num_scan_rays, dtype=np.float32)

        order = np.argsort(old_angles)
        old_angles = old_angles[order]
        ranges = ranges[order]

        ranges_resampled = np.interp(
            target_angles,
            old_angles,
            ranges,
            left=msg.range_max,
            right=msg.range_max,
        ).astype(np.float32)

        ranges_m = np.clip(ranges_resampled, 0.0, self.scan_max_range)
        scan_norm = np.clip(ranges_m / self.scan_max_range, 0.0, 1.0).astype(np.float32)

        self.latest_scan = scan_norm
        self.latest_scan_m = ranges_m.astype(np.float32)
>>>>>>> 14e3b3c (RL Local Controller)

    def odom_callback(self, msg: Odometry):
        self.latest_odom = msg

    def path_callback(self, msg: Path):
        if len(msg.poses) < 2:
            return

<<<<<<< HEAD
        pts = []
        for p in msg.poses:
            pts.append([p.pose.position.x, p.pose.position.y])

        self.latest_path = np.array(pts, dtype=np.float32)
=======
        self.latest_path = np.array(
            [[p.pose.position.x, p.pose.position.y] for p in msg.poses],
            dtype=np.float32,
        )
>>>>>>> 14e3b3c (RL Local Controller)

    def build_local_path_obs(self, robot_xy, robot_yaw):
        path = self.latest_path

        if path is None or len(path) < 2:
            return (
                np.zeros(self.num_path_points * 2, dtype=np.float32),
                np.array([0.0], dtype=np.float32),
                np.array([0.0], dtype=np.float32),
            )

        d = np.linalg.norm(path - robot_xy[None, :], axis=1)
        nearest_idx = int(np.argmin(d))

<<<<<<< HEAD
=======
        c = math.cos(-robot_yaw)
        s = math.sin(-robot_yaw)

>>>>>>> 14e3b3c (RL Local Controller)
        local_points = []

        for k in range(self.num_path_points):
            idx = nearest_idx + (k + 1) * self.path_step
            idx = min(idx, len(path) - 1)

            rel = path[idx] - robot_xy

<<<<<<< HEAD
            c = math.cos(-robot_yaw)
            s = math.sin(-robot_yaw)

=======
>>>>>>> 14e3b3c (RL Local Controller)
            x_b = c * rel[0] - s * rel[1]
            y_b = s * rel[0] + c * rel[1]

            local_points.extend([x_b, y_b])

<<<<<<< HEAD
        local_path_window = np.array(local_points, dtype=np.float32)

        next_idx = min(nearest_idx + 3, len(path) - 1)
=======
        local_path_window = np.clip(
            np.array(local_points, dtype=np.float32) / self.path_norm_m,
            -2.0,
            2.0,
        ).astype(np.float32)

        next_idx = min(nearest_idx + 4, len(path) - 1)
>>>>>>> 14e3b3c (RL Local Controller)
        p0 = path[nearest_idx]
        p1 = path[next_idx]

        path_yaw = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        heading_error = np.array([wrap_to_pi(path_yaw - robot_yaw)], dtype=np.float32)

        cross_track = np.array([float(np.min(d))], dtype=np.float32)

        return local_path_window, heading_error, cross_track

<<<<<<< HEAD
=======
    def get_robot_pose_in_map(self):
        try:
            tf = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
                timeout=Duration(seconds=0.20),
            )
        except Exception as e:
            now_ns = self.get_clock().now().nanoseconds
            if now_ns - self._last_tf_warn_ns > int(2.0 * 1e9):
                self.get_logger().warn(f"TF lookup failed {self.map_frame}->{self.base_frame}: {e}")
                self._last_tf_warn_ns = now_ns
            return None

        robot_xy = np.array(
            [
                tf.transform.translation.x,
                tf.transform.translation.y,
            ],
            dtype=np.float32,
        )

        robot_yaw = yaw_from_quat(tf.transform.rotation)
        return robot_xy, robot_yaw
    
    # def reached_path_end(self, robot_xy: np.ndarray) -> bool:
    #     if self.latest_path is None or len(self.latest_path) < 2:
    #         return False

    #     d = np.linalg.norm(self.latest_path - robot_xy[None, :], axis=1)
    #     nearest_idx = int(np.argmin(d))

    #     goal_xy = self.latest_path[-1]
    #     dist_to_goal = float(np.linalg.norm(goal_xy - robot_xy))

    #     # Must be close to final path point AND nearest to final segment.
    #     return nearest_idx >= len(self.latest_path) - 2 and dist_to_goal <= self.goal_tolerance_m
    def reached_path_end(self, robot_xy: np.ndarray) -> bool:
        if self.latest_path is None or len(self.latest_path) < 2:
            return False

        goal_xy = self.latest_path[-1]
        dist_to_goal = float(np.linalg.norm(goal_xy - robot_xy))

        return dist_to_goal <= self.goal_stop_m

>>>>>>> 14e3b3c (RL Local Controller)
    def build_observation(self):
        if self.latest_scan is None or self.latest_odom is None or self.latest_path is None:
            return None

        pose_result = self.get_robot_pose_in_map()
        if pose_result is None:
            return None

        robot_xy, robot_yaw = pose_result
        odom = self.latest_odom

<<<<<<< HEAD
        local_path_window, heading_error, cross_track = self.build_local_path_obs(
            robot_xy,
            robot_yaw,
        )
=======
        local_path_window, heading_error, cross_track = self.build_local_path_obs(robot_xy, robot_yaw)
>>>>>>> 14e3b3c (RL Local Controller)

        base_lin_vel = np.array(
            [
                odom.twist.twist.linear.x,
                odom.twist.twist.linear.y,
            ],
            dtype=np.float32,
        )

        base_ang_vel = np.array(
            [odom.twist.twist.angular.z],
            dtype=np.float32,
        )

        obs = np.concatenate(
            [
<<<<<<< HEAD
                local_path_window,
                heading_error,
                cross_track,
                self.latest_scan,
                base_lin_vel,
                base_ang_vel,
                self.previous_action,
=======
                local_path_window,     # 0:16
                heading_error,         # 16
                cross_track,           # 17
                self.latest_scan,      # 18:162
                base_lin_vel,          # 162:164
                base_ang_vel,          # 164
                self.previous_action,  # 165:168
>>>>>>> 14e3b3c (RL Local Controller)
            ],
            axis=0,
        ).astype(np.float32)

<<<<<<< HEAD
        return obs
    
    def get_robot_pose_in_map(self):
        try:
            # Time() means latest available TF.
            tf = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
                timeout=Duration(seconds=0.20),
            )

        except Exception as e:
            # Manual throttled warning because rclpy logger has no warn_throttle().
            now_ns = self.get_clock().now().nanoseconds
            if now_ns - self._last_tf_warn_ns > int(2.0 * 1e9):
                self.get_logger().warn(
                    f"TF lookup failed {self.map_frame}->{self.base_frame}: {e}"
                )
                self._last_tf_warn_ns = now_ns

            return None

        robot_xy = np.array(
            [
                tf.transform.translation.x,
                tf.transform.translation.y,
            ],
            dtype=np.float32,
        )

        q = tf.transform.rotation
        robot_yaw = yaw_from_quat(q)

        return robot_xy, robot_yaw
=======
        if self.expected_obs_dim is not None and obs.shape[0] != self.expected_obs_dim:
            self.get_logger().error(
                f"Observation dim mismatch: built={obs.shape[0]}, "
                f"policy_expected={self.expected_obs_dim}. "
                "New policy should expect 168."
            )
            return None

        return obs
>>>>>>> 14e3b3c (RL Local Controller)

    def control_loop(self):
        obs = self.build_observation()
        if obs is None:
            return

<<<<<<< HEAD
        obs_batch = obs.reshape(1, -1)

        action = self.session.run(
            [self.output_name],
            {self.input_name: obs_batch},
        )[0]

        action = np.asarray(action).reshape(-1)[:3]
        action = np.clip(action, -1.0, 1.0)

        self.previous_action = action.astype(np.float32)

        cmd = Twist()
        cmd.linear.x = float(action[0] * self.max_vx)
        cmd.linear.y = float(action[1] * self.max_vy)
        cmd.angular.z = float(action[2] * self.max_wz)

        self.cmd_pub.publish(cmd)

        if not hasattr(self, "_debug_count"):
            self._debug_count = 0

        self._debug_count += 1

        if self._debug_count % 20 == 0:
            self.get_logger().info(
                f"obs: heading={obs[16]:+.3f}, cte={obs[17]:+.3f}, "
                f"scan_min={np.min(obs[18:90]):.3f}, "
                f"raw_action=[{action[0]:+.3f}, {action[1]:+.3f}, {action[2]:+.3f}], "
                f"cmd=[{action[0]*self.max_vx:+.3f}, {action[1]*self.max_vy:+.3f}, {action[2]*self.max_wz:+.3f}]"
            )
=======
        pose_result = self.get_robot_pose_in_map()
        if pose_result is None:
            return
        robot_xy, _ = pose_result
        goal_dist = float("nan")
        if self.latest_path is not None and len(self.latest_path) >= 2:
            goal_xy = self.latest_path[-1]
            goal_dist = float(np.linalg.norm(goal_xy - robot_xy))
        if self.reached_path_end(robot_xy):
            stop_cmd = Twist()
            self.cmd_pub.publish(stop_cmd)
            self.previous_action[:] = 0.0
            self.applied_cmd[:] = 0.0
            return
        
        raw_action = self.session.run(
            [self.output_name],
            {self.input_name: obs.reshape(1, -1)},
        )[0]

        raw_action = np.asarray(raw_action, dtype=np.float32).reshape(-1)[:3]
        raw_action = np.clip(raw_action, -1.0, 1.0)

        target_cmd = np.array(
            [
                raw_action[0] * self.max_vx,
                raw_action[1] * self.max_vy,
                raw_action[2] * self.max_wz,
            ],
            dtype=np.float32,
        )
        goal_xy = self.latest_path[-1]
        goal_dist = float(np.linalg.norm(goal_xy - robot_xy))

        if goal_dist < self.goal_slowdown_m:
            scale = max(0.15, goal_dist / self.goal_slowdown_m)
            target_cmd *= scale

        if self.enable_action_rate_limit:
            delta = np.clip(target_cmd - self.applied_cmd, -self.max_delta, self.max_delta)
            self.applied_cmd = self.applied_cmd + delta
        else:
            self.applied_cmd = target_cmd

        if self.latest_scan_m is not None and float(np.min(self.latest_scan_m)) < self.emergency_stop_scan_m:
            self.applied_cmd[:] = 0.0

        self.previous_action = np.array(
            [
                self.applied_cmd[0] / self.max_vx,
                self.applied_cmd[1] / self.max_vy,
                self.applied_cmd[2] / self.max_wz,
            ],
            dtype=np.float32,
        )
        self.previous_action = np.clip(self.previous_action, -1.0, 1.0)

        cmd = Twist()
        cmd.linear.x = float(self.applied_cmd[0])
        cmd.linear.y = float(self.applied_cmd[1])
        cmd.angular.z = float(self.applied_cmd[2])
        if self.enable_motion:
            self.cmd_pub.publish(cmd)

        self._debug_count += 1
        # if self._debug_count % 30 == 0:
        #     self.get_logger().info(
        #         f"obs_dim={obs.shape[0]}, "
        #         f"heading={obs[16]:+.3f}, "
        #         f"cte={obs[17]:+.3f}, "
        #         f"scan_min_m={float(np.min(self.latest_scan_m)):.3f}, "
        #         f"raw_action=[{raw_action[0]:+.3f}, {raw_action[1]:+.3f}, {raw_action[2]:+.3f}], "
        #         f"cmd=[{cmd.linear.x:+.3f}, {cmd.linear.y:+.3f}, {cmd.angular.z:+.3f}], "
        #         f"prev=[{self.previous_action[0]:+.3f}, {self.previous_action[1]:+.3f}, {self.previous_action[2]:+.3f}]"
        #     )
        now = self.get_clock().now()
        elapsed = (now - self.last_debug_log_time).nanoseconds * 1e-9

        if elapsed >= self.debug_log_period_s:
            self.get_logger().info(
                f"goal_dist={goal_dist:.3f}, "
                f"cmd=[{cmd.linear.x:+.3f}, {cmd.linear.y:+.3f}, {cmd.angular.z:+.3f}]"
            )
            self.last_debug_log_time = now

>>>>>>> 14e3b3c (RL Local Controller)

def main():
    rclpy.init()
    node = RLLocalController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()