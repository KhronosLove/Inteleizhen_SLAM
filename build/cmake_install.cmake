# Install script for directory: /home/xjtlu/catkin_ws/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/xjtlu/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/xjtlu/catkin_ws/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/xjtlu/catkin_ws/install" TYPE PROGRAM FILES "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/_setup_util.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/xjtlu/catkin_ws/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/xjtlu/catkin_ws/install" TYPE PROGRAM FILES "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/env.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/xjtlu/catkin_ws/install/setup.bash;/home/xjtlu/catkin_ws/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/xjtlu/catkin_ws/install" TYPE FILE FILES
    "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/setup.bash"
    "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/local_setup.bash"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/xjtlu/catkin_ws/install/setup.sh;/home/xjtlu/catkin_ws/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/xjtlu/catkin_ws/install" TYPE FILE FILES
    "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/setup.sh"
    "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/local_setup.sh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/xjtlu/catkin_ws/install/setup.zsh;/home/xjtlu/catkin_ws/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/xjtlu/catkin_ws/install" TYPE FILE FILES
    "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/setup.zsh"
    "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/xjtlu/catkin_ws/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/xjtlu/catkin_ws/install" TYPE FILE FILES "/home/xjtlu/catkin_ws/build/catkin_generated/installspace/.rosinstall")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/xjtlu/catkin_ws/build/gtest/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_time/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/astrapro_launch/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/catkin_simple/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_offline_calibration/ethz_apriltag2/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/imu_tools/imu_tools/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/opencv2_catkin/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/python_module/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/ros_arduino_bridge/ros_arduino_bridge/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/ros_arduino_bridge/ros_arduino_firmware/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/ros_arduino_bridge/ros_arduino_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_common/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_boost/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_logging/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_matrix_archive/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_opencv/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_property_tree/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_random/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_eigen/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_kinematics/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_cameras/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_cv_serialization/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_timing/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_optimizer/sparse_block_matrix/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_optimizer/aslam_backend/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_optimizer/aslam_backend_expressions/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_cv_backend/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_nonparametric_estimation/bsplines/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_incremental_calibration/incremental_calibration/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/ros_arduino_bridge/ros_arduino_msgs/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/teleop_twist_keyboard/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/lubot_slam/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/numpy_eigen/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_optimizer/aslam_backend_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_imgproc/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_nonparametric_estimation/aslam_splines/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_cv_error_terms/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_nonparametric_estimation/bsplines_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_nonparametric_estimation/aslam_splines_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_incremental_calibration/incremental_calibration_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/Schweizer-Messer/sm_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_cameras_april/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_cv_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_cv/aslam_cv_backend_python/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/kalibr/aslam_offline_calibration/kalibr/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/ros_astra_camera/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/imu_tools/imu_complementary_filter/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/cam_laser/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/mul-lidar_cal/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/sanchi_amov/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/imu_tools/imu_filter_madgwick/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/my_trans/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/imu_tools/rviz_imu_plugin/cmake_install.cmake")
  include("/home/xjtlu/catkin_ws/build/wj_716_lidar/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/xjtlu/catkin_ws/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
