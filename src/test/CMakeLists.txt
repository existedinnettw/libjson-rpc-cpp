
set(CTEST_OUTPUT_ON_FAILURE TRUE)
file(GLOB_RECURSE test_source *.cpp)

include_directories(..)
include_directories(${CMAKE_BINARY_DIR})

file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/include/test)

add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/include/test/abstractstubserver.h
        COMMAND jsonrpcstub ARGS ${CMAKE_CURRENT_SOURCE_DIR}/spec.json --cpp-server=AbstractStubServer --cpp-server-file=${CMAKE_BINARY_DIR}/include/test/abstractstubserver.h
        MAIN_DEPENDENCY spec.json
        DEPENDS jsonrpcstub
        COMMENT "Generating Server Stubfiles"
        VERBATIM
)

add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/include/test/stubclient.h
        COMMAND jsonrpcstub ARGS ${CMAKE_CURRENT_SOURCE_DIR}/spec.json --cpp-client=StubClient --cpp-client-file=${CMAKE_BINARY_DIR}/include/test/stubclient.h
        MAIN_DEPENDENCY spec.json
        DEPENDS jsonrpcstub
        COMMENT "Generating Client Stubfile"
        VERBATIM
)


if (HTTP_CLIENT AND HTTP_SERVER)
    add_definitions(-DHTTP_TESTING)
    file(COPY ${CMAKE_SOURCE_DIR}/src/examples/server.key ${CMAKE_SOURCE_DIR}/src/examples/server.pem DESTINATION ${CMAKE_BINARY_DIR})
    # file(COPY ${CMAKE_SOURCE_DIR}/src/examples/server.key ${CMAKE_SOURCE_DIR}/src/examples/server.pem DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
else ()
    list(REMOVE_ITEM test_source "${CMAKE_CURRENT_SOURCE_DIR}/testhttpserver.cpp")
endif ()

if (REDIS_CLIENT AND REDIS_SERVER)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/redis.conf DESTINATION ${CMAKE_BINARY_DIR})
    # file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/redis.conf DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
    add_definitions(-DREDIS_TESTING)
else ()
    list(REMOVE_ITEM test_source "${CMAKE_CURRENT_SOURCE_DIR}/testredisserver.cpp")
endif ()

if (UNIX_DOMAIN_SOCKET_SERVER AND UNIX_DOMAIN_SOCKET_CLIENT)
    add_definitions(-DUNIXDOMAINSOCKET_TESTING)
endif ()

if (FILE_DESCRIPTOR_SERVER AND FILE_DESCRIPTOR_CLIENT)
    add_definitions(-DFILEDESCRIPTOR_TESTING)
endif ()

if (TCP_SOCKET_SERVER AND TCP_SOCKET_CLIENT)
    add_definitions(-DTCPSOCKET_TESTING)
endif ()

if (COMPILE_STUBGEN)
    add_definitions(-DSTUBGEN_TESTING)
    file(GLOB test_specs *.json)
    file(COPY ${test_specs} DESTINATION ${CMAKE_BINARY_DIR})
    # file(COPY ${test_specs} DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
    # list(APPEND test_source "${CMAKE_BINARY_DIR}/include/test/abstractstubserver.h")
    # list(APPEND test_source "${CMAKE_BINARY_DIR}/include/test/stubclient.h")
endif ()

add_executable(unit_testsuite ${test_source})
if (COMPILE_STUBGEN)
    #should include stubclient, abstractstubserver.h
    target_include_directories(unit_testsuite PRIVATE "${CMAKE_BINARY_DIR}/include/test")
    target_sources(unit_testsuite PRIVATE "${CMAKE_BINARY_DIR}/include/test/abstractstubserver.h" "${CMAKE_BINARY_DIR}/include/test/stubclient.h")
endif()
target_link_libraries(unit_testsuite jsonrpccommon)
target_link_libraries(unit_testsuite jsonrpcserver)
target_link_libraries(unit_testsuite jsonrpcclient)

if (COMPILE_STUBGEN)
    target_link_libraries(unit_testsuite libjsonrpcstub)
    add_dependencies(unit_testsuite libjsonrpcstub)
endif ()

add_test(client unit_testsuite "[client]")
add_test(server unit_testsuite "[server]")
add_test(NAME common WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[common]")

if (HTTP_CLIENT AND HTTP_SERVER)
    add_test(NAME connector_http WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[connector_http]")
endif ()

if (REDIS_CLIENT AND REDIS_SERVER)
    add_test(NAME connector_redis WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[connector_redis]")
endif ()

if (UNIX_DOMAIN_SOCKET_CLIENT AND UNIX_DOMAIN_SOCKET_SERVER)
    add_test(NAME connector_unixdomainsocket WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[connector_unixdomainsocket]")
endif ()

if (FILE_DESCRIPTOR_CLIENT AND FILE_DESCRIPTOR_SERVER)
    add_test(NAME connector_filedescriptor WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[connector_filedescriptor]")
endif ()

if (TCP_SOCKET_CLIENT AND TCP_SOCKET_SERVER)
    add_test(NAME connector_tcpsocket WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[connector_tcpsocket]")
endif ()

if (COMPILE_STUBGEN)
    add_test(NAME stubgen WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[stubgenerator]")
endif ()

if (HTTP_CLIENT AND HTTP_SERVER AND COMPILE_STUBGEN)
    add_test(NAME integration WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND unit_testsuite "[integration]")
endif ()
