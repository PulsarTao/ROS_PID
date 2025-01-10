//
// Created by Pulsar-V on 2025/1/9.
//
#include "driver/driver_node.h"
using namespace std::chrono_literals;
void DriverNode::publish_target_vis(double x, double y, double z) {
    visualization_msgs::msg::Marker delete_marker;
    delete_marker.header.frame_id = "world";
    delete_marker.header.stamp = this->get_clock()->now();
    delete_marker.ns = "marker";
    delete_marker.id = 0;
    delete_marker.action = visualization_msgs::msg::Marker::DELETE;
    marker_publisher_->publish(delete_marker);

    rclcpp::sleep_for(std::chrono::milliseconds(1));

    visualization_msgs::msg::Marker marker;
    marker.header.frame_id = "world";
    marker.header.stamp = this->get_clock()->now();
    marker.ns = "marker";
    marker.id = 0;
    marker.type = visualization_msgs::msg::Marker::SPHERE;
    marker.action = visualization_msgs::msg::Marker::ADD;
    marker.pose.position.x = x;
    marker.pose.position.y = y;
    marker.pose.position.z = z;
    marker.scale.x = 0.1;
    marker.scale.y = 0.1;
    marker.scale.z = 0.1;
    marker.color.a = 1.0;
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;
    marker_publisher_->publish(marker);
}
void DriverNode::timer_callback() {
    count++;
    auto message = driver_msgs::msg::Target();
    message.name = "targ";
    message.count = count;
    message.time = this->get_clock()->now().seconds();

    double t = message.time;
    message.target.x = sin(t);
    message.target.y = cos(t);
    message.target.z = sin(t * 2);
    RCLCPP_INFO(
            this->get_logger(),
            "Target coordinates: (x: %f, y: %f, z: %f) Count:%d",
            message.target.x,
            message.target.y,
            message.target.z,
            message.count
    );

    publisher_->publish(message);
    this->publish_target_vis(message.target.x,message.target.y,message.target.z);
}
DriverNode::DriverNode() : Node("driver_node"), count(0) {

    auto message = driver_msgs::msg::Target();
    message.name = "targ";
    message.count = count;
    message.time = this->get_clock()->now().seconds();

    publisher_ = this->create_publisher<driver_msgs::msg::Target>("target", 10);
    marker_publisher_ = this->create_publisher<visualization_msgs::msg::Marker>("visualization_marker", 10);
    timer_ = this->create_wall_timer(2ms, std::bind(&DriverNode::timer_callback, this));
}

