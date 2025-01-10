//
// Created by Pulsar-V on 2025/1/9.
//

#ifndef COLCON_WS_DRIVER_NODE_H
#define COLCON_WS_DRIVER_NODE_H
#include <visualization_msgs/msg/marker.hpp>
#include "driver_msgs/msg/target.hpp"
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/int64.hpp>
#include <chrono>
#include <cmath>
class DriverNode : public rclcpp::Node {
public:
    DriverNode();
private:
    void timer_callback();
    void publish_target_vis(double x, double y, double z);
    rclcpp::Publisher<driver_msgs::msg::Target>::SharedPtr publisher_;
    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr marker_publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    int count;
};
#endif//COLCON_WS_DRIVER_NODE_H
