cmake_minimum_required(VERSION 3.2)
project(all-entitled-datasets)

option(BUILD_SHARED_LIBS "Build shared libraries" ON)

find_package(AWSSDK REQUIRED COMPONENTS dataexchange)
add_executable(all-entitled-datasets main.cpp)

target_compile_features(all-entitled-datasets PUBLIC cxx_std_11)
target_link_libraries(all-entitled-datasets ${AWSSDK_LINK_LIBRARIES})
