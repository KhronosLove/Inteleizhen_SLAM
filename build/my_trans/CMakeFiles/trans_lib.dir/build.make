# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/xjtlu/catkin_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/xjtlu/catkin_ws/build

# Include any dependencies generated for this target.
include my_trans/CMakeFiles/trans_lib.dir/depend.make

# Include the progress variables for this target.
include my_trans/CMakeFiles/trans_lib.dir/progress.make

# Include the compile flags for this target's objects.
include my_trans/CMakeFiles/trans_lib.dir/flags.make

my_trans/CMakeFiles/trans_lib.dir/src/My_node.cpp.o: my_trans/CMakeFiles/trans_lib.dir/flags.make
my_trans/CMakeFiles/trans_lib.dir/src/My_node.cpp.o: /home/xjtlu/catkin_ws/src/my_trans/src/My_node.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/xjtlu/catkin_ws/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object my_trans/CMakeFiles/trans_lib.dir/src/My_node.cpp.o"
	cd /home/xjtlu/catkin_ws/build/my_trans && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/trans_lib.dir/src/My_node.cpp.o -c /home/xjtlu/catkin_ws/src/my_trans/src/My_node.cpp

my_trans/CMakeFiles/trans_lib.dir/src/My_node.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/trans_lib.dir/src/My_node.cpp.i"
	cd /home/xjtlu/catkin_ws/build/my_trans && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/xjtlu/catkin_ws/src/my_trans/src/My_node.cpp > CMakeFiles/trans_lib.dir/src/My_node.cpp.i

my_trans/CMakeFiles/trans_lib.dir/src/My_node.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/trans_lib.dir/src/My_node.cpp.s"
	cd /home/xjtlu/catkin_ws/build/my_trans && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/xjtlu/catkin_ws/src/my_trans/src/My_node.cpp -o CMakeFiles/trans_lib.dir/src/My_node.cpp.s

# Object files for target trans_lib
trans_lib_OBJECTS = \
"CMakeFiles/trans_lib.dir/src/My_node.cpp.o"

# External object files for target trans_lib
trans_lib_EXTERNAL_OBJECTS =

/home/xjtlu/catkin_ws/devel/lib/libtrans_lib.so: my_trans/CMakeFiles/trans_lib.dir/src/My_node.cpp.o
/home/xjtlu/catkin_ws/devel/lib/libtrans_lib.so: my_trans/CMakeFiles/trans_lib.dir/build.make
/home/xjtlu/catkin_ws/devel/lib/libtrans_lib.so: my_trans/CMakeFiles/trans_lib.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/xjtlu/catkin_ws/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library /home/xjtlu/catkin_ws/devel/lib/libtrans_lib.so"
	cd /home/xjtlu/catkin_ws/build/my_trans && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/trans_lib.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
my_trans/CMakeFiles/trans_lib.dir/build: /home/xjtlu/catkin_ws/devel/lib/libtrans_lib.so

.PHONY : my_trans/CMakeFiles/trans_lib.dir/build

my_trans/CMakeFiles/trans_lib.dir/clean:
	cd /home/xjtlu/catkin_ws/build/my_trans && $(CMAKE_COMMAND) -P CMakeFiles/trans_lib.dir/cmake_clean.cmake
.PHONY : my_trans/CMakeFiles/trans_lib.dir/clean

my_trans/CMakeFiles/trans_lib.dir/depend:
	cd /home/xjtlu/catkin_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/xjtlu/catkin_ws/src /home/xjtlu/catkin_ws/src/my_trans /home/xjtlu/catkin_ws/build /home/xjtlu/catkin_ws/build/my_trans /home/xjtlu/catkin_ws/build/my_trans/CMakeFiles/trans_lib.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : my_trans/CMakeFiles/trans_lib.dir/depend

