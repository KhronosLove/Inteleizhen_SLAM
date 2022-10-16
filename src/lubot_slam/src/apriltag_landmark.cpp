#include "ros/ros.h"
#include "cartographer_ros_msgs/LandmarkList.h"
#include "cartographer_ros_msgs/LandmarkEntry.h"
#include "geometry_msgs/Pose.h"
#include "std_msgs/String.h"
#include "std_msgs/Header.h"
#include "apriltag_ros/AprilTagDetectionArray.h"
#include "apriltag_ros/AprilTagDetection.h"

static ros::Publisher* landmarkPtr;

void tag_cb(const apriltag_ros::AprilTagDetectionArrayConstPtr& msg)
{
	unsigned int size = msg->detections.size();
	if(!size)
	{
	  ROS_WARN("No tag detected !");
	  sleep(1);
	  return;
	}
	int ret = system("clear");
	int id = msg->detections[0].id[0];
	double pos_x = msg->detections[0].pose.pose.pose.position.x;
	double pos_y = msg->detections[0].pose.pose.pose.position.y;
	double pos_z = msg->detections[0].pose.pose.pose.position.z;

	double ori_x = msg->detections[0].pose.pose.pose.orientation.x;
	double ori_y = msg->detections[0].pose.pose.pose.orientation.y;
	double ori_z = msg->detections[0].pose.pose.pose.orientation.z;
	double ori_w = msg->detections[0].pose.pose.pose.orientation.w;

	cartographer_ros_msgs::LandmarkList  landmark;

    landmark.header.stamp = ros::Time::now();
    landmark.header.frame_id = "camera";    // 根据lua配置坐标系
    landmark.landmarks.resize(1);

	std::stringstream ss;
	ss << id;

	landmark.landmarks[0].id = ss.str();
	landmark.landmarks[0].tracking_from_landmark_transform.position.x = pos_x;
	landmark.landmarks[0].tracking_from_landmark_transform.position.y = pos_y;
	landmark.landmarks[0].tracking_from_landmark_transform.position.z = pos_z;
	landmark.landmarks[0].tracking_from_landmark_transform.orientation.w = ori_w;
	landmark.landmarks[0].tracking_from_landmark_transform.orientation.x = ori_x;
	landmark.landmarks[0].tracking_from_landmark_transform.orientation.y = ori_y;
	landmark.landmarks[0].tracking_from_landmark_transform.orientation.z = ori_z;
	landmark.landmarks[0].translation_weight = 9999.9;   // double  很大的数
	landmark.landmarks[0].rotation_weight = 9999.9;

	landmarkPtr->publish(landmark);
}

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "apriltag_landmark");
    ros::NodeHandle nh;

    ros::Publisher landmark_pub = nh.advertise<cartographer_ros_msgs::LandmarkList>("landmark", 10);
    ros::Subscriber tag_sub = nh.subscribe<apriltag_ros::AprilTagDetectionArray>("tag_detections", 
                            20, tag_cb);
    landmarkPtr = &landmark_pub;
    ros::spin();
    return 0;
}
