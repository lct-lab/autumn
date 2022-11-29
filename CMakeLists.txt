cmake_minimum_required(VERSION 3.19)
project(DBAccess)

set(CMAKE_CXX_STANDARD 17)


include_directories(../)
include_directories(src/thrift/gen-cpp)
include_directories(src)

# third lib dependency
# root DIR use "" to avoid space
set(LIBROOT "D:/Program Files/cpplibs")

include_directories(${LIBROOT}/inicpp/include)

include_directories(${LIBROOT}/rapidcsv/include)

include_directories(${LIBROOT}/argparse/include)

include_directories(${LIBROOT}/boost_1_80_0/include)
link_directories(${LIBROOT}/boost_1_80_0/lib)

include_directories(${LIBROOT}/log4cplus/include)
link_directories(${LIBROOT}/log4cplus/lib)

include_directories(${LIBROOT}/odbc/include)
link_directories(${LIBROOT}/odbc/lib)

IF (WIN32)
    MESSAGE(STATUS 'windows-system')
    set(SYS_TYPE win64)
elseif (UNIX)
    MESSAGE(STATUS ${UNIX}'UNIX-system')
    set(SYS_TYPE unix)
else ()
    MESSAGE(FATAL_ERROR 'unsupported-system-type')
endif ()

include_directories(${LIBROOT}/thrift_0_16_0/include)
if (CMAKE_BUILD_TYPE AND (CMAKE_BUILD_TYPE STREQUAL "Debug"))
    link_directories(${LIBROOT}/thrift_0_16_0/lib/x64/Debug)
elseif (CMAKE_BUILD_TYPE AND (CMAKE_BUILD_TYPE STREQUAL "Release"))
    link_directories(${LIBROOT}/thrift_0_16_0/lib/x64/Release)
endif ()

set(LIBFILES odbc32 libthrift)
if (CMAKE_BUILD_TYPE AND (CMAKE_BUILD_TYPE STREQUAL "Debug"))
    LIST(APPEND LIBFILES log4cplusD)
elseif (CMAKE_BUILD_TYPE AND (CMAKE_BUILD_TYPE STREQUAL "Release"))
    LIST(APPEND LIBFILES log4cplus)
endif ()

set(THRIFTNAME BasicDataAccess)
file(GLOB_RECURSE TEST_SC_FILES src/dao/nanodbc.cpp src/thrift/gen-cpp/${THRIFTNAME}.cpp src/thrift/gen-cpp/${THRIFTNAME}_types.cpp)
MESSAGE(STATUS testsourcefile:${TEST_SC_FILES})
add_executable(test ${TEST_SC_FILES} src/test/test.cpp)
target_link_libraries(test ${LIBFILES})

set(APPNAME BasicDataAccess)
file(GLOB_RECURSE SERVICE_SC_FILES src/dao/nanodbc.cpp src/thrift/gen-cpp/${THRIFTNAME}.cpp src/thrift/gen-cpp/${THRIFTNAME}_types.cpp)
MESSAGE(STATUS SERVICE_SC_FILES:${SERVICE_SC_FILES})
add_executable(${APPNAME}Srv ${SERVICE_SC_FILES} src/${APPNAME}Application.cpp)
target_link_libraries(${APPNAME}Srv ${LIBFILES})
