import rclpy
import math
import numpy as np
from rclpy.node import Node
from std_msgs.msg import Int64
from collections import deque
from driver_msgs.msg import Target


class IncrementalPID:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.previous_error = np.array([0.0, 0.0, 0.0])
        self.output = np.array([0.0, 0.0, 0.0])
        self.output_limits = (-2, 2)  # 设置输出限制

    def update(self, set_point, current):
        set_point = np.array(set_point)
        print("set_point:", set_point)
        current = np.array(current)
        print("current:", current)
        error = set_point - current
        print("error:", error)
        delta_error = error - self.previous_error
        print("delta_error:", delta_error)
        self.output += self.kp * delta_error + self.ki * error * self.dt + self.kd * delta_error / self.dt
        self.output = np.clip(self.output, self.output_limits[0], self.output_limits[1])
        print("output:", self.output)
        self.previous_error = error
        return self.output


class PID:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.integral = np.array([0.0, 0.0, 0.0])
        self.previous_error = np.array([0.0, 0.0, 0.0])
        self.output_limits = (-1.0, 1.0)

    def update(self, target, current):
        error = np.array(target) - np.array(current)
        self.integral += (error * self.dt)
        derivative = (error - self.previous_error) / self.dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        output = [max(min(ot, self.output_limits[1]), self.output_limits[0]) for ot in output]
        self.previous_error = error
        print("output:",output)
        return output


class ProcessNode(Node):
    def __init__(self):
        super().__init__('process_node')
        self.subscription = self.create_subscription(
            Target,
            'target',
            self.listener_callback,
            10
        )
        self.publisher = self.create_publisher(Target, 'command', 10)
        self.msg_window = deque(maxlen=5)
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.current = [0.0, 0.0, 0.0]
        self.pid = PID(0.01, 0.00001, 0.00001, 0.01)
        # self.pid = IncrementalPID(1, 0.1, 0.01, 0.01)

    def listener_callback(self, msg):
        self.msg_window.append(msg)
        # self.get_logger().info(f'Received message: count={msg.count}, time={msg.time},target={msg.target}')

    def timer_callback(self):
        if self.msg_window:
            last_msg = self.msg_window[-1]
            set_point = [last_msg.target.x, last_msg.target.y, last_msg.target.z]
            self.current = self.pid.update(set_point, self.current)
            command_msg = Target()
            command_msg.target.x, command_msg.target.y, command_msg.target.z = self.current
            now = self.get_clock().now()  # 获取当前时间
            command_msg.time = now.seconds_nanoseconds()[0] + now.seconds_nanoseconds()[1] * 1e-9  # 转换为浮点数
            command_msg.count = last_msg.count
            self.publisher.publish(command_msg)
            # self.get_logger().info(f'Published command: count={command_msg.count}, time={command_msg.time}, target={command_msg.target}')
        else:
            self.get_logger().warn('No messages have been received yet.')


def main(args=None):
    rclpy.init(args=args)
    process_node = ProcessNode()
    rclpy.spin(process_node)
    process_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
