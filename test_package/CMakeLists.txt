cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(libjson-rpc-cpp CONFIG REQUIRED)

# file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/include)

# not yet in run env add_custom_command( OUTPUT ${CMAKE_BINARY_DIR}/include/abstractstubserver.h COMMAND jsonrpcstub
# ARGS ${CMAKE_CURRENT_SOURCE_DIR}/spec.json --cpp-server=AbstractStubServer
# --cpp-server-file=${CMAKE_BINARY_DIR}/include/abstractstubserver.h MAIN_DEPENDENCY spec.json COMMENT "Generating
# Server Stubfiles" VERBATIM)

add_executable(example example.cpp)
# target_sources(example PRIVATE "${CMAKE_BINARY_DIR}/include/abstractstubserver.h")
target_link_libraries(example libjson-rpc-cpp::libjson-rpc-cpp)
