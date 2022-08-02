#include <iostream>

#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <laser_geometry/laser_geometry.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/LaserScan.h>


class My_Filter {
     public:
        My_Filter();
        My_Filter(const std::string& laserName, const std::string& cloudName);
        //订阅 LaserScan　数据，并发布 PointCloud2 点云 
        void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan);



     private:
        ros::NodeHandle node_;
        laser_geometry::LaserProjection projector_;
        tf::TransformListener tfListener_;

        //发布　"PointCloud2"
        ros::Publisher point_cloud_publisher_;

        //订阅 "/scan"
        ros::Subscriber scan_sub_;

        
};