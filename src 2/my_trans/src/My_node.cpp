#include "My_Filter.h"

My_Filter::My_Filter(const std::string& laserName, const std::string& cloudName){
    scan_sub_ = node_.subscribe<sensor_msgs::LaserScan> (laserName, 100, &My_Filter::scanCallback, this);

    //发布LaserScan转换为PointCloud2的后的数据
    point_cloud_publisher_ = node_.advertise<sensor_msgs::PointCloud2> (cloudName, 100, false);  

}


void My_Filter::scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan){
    sensor_msgs::PointCloud2 cloud;
    projector_.transformLaserScanToPointCloud(scan->header.frame_id, *scan, cloud, tfListener_);
    point_cloud_publisher_.publish(cloud);
}

