cmake_minimum_required(VERSION 3.5)
project(driver)

if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()
file(GLOB SOURCE_FILES src/main.cpp src/driver_node.cpp include/driver_node.h)
add_executable(driver ${SOURCE_FILES})
target_include_directories(driver PRIVATE include)
include_directories(${${PROJECT_NAME}_INCLUDE_DIRS})
include_directories(include)
find_package(geometry_msgs REQUIRED)
find_package(driver_msgs REQUIRED)
find_package(visualization_msgs  REQUIRED)
ament_target_dependencies(driver rclcpp std_msgs driver_msgs visualization_msgs)
install(TARGETS
        driver
        DESTINATION lib/${PROJECT_NAME}
)
#ament_package()
ament_package()