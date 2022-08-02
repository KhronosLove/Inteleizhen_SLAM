#include "My_Filter.h"

int main(int argc, char** argv)
{
    ros::init(argc, argv, "Mynode");

    My_Filter filter1("scan_wj_1","scan1_cloud2");
    My_Filter filter2("scan_wj_2","scan2_cloud2");

    ros::spin();

    return 0;
}