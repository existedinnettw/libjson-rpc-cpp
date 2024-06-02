file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/include/example)

add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/include/example/abstractstubserver.h
        COMMAND jsonrpcstub ARGS ${CMAKE_CURRENT_SOURCE_DIR}/spec.json --cpp-server=AbstractStubServer --cpp-server-file=${CMAKE_BINARY_DIR}/include/example/abstractstubserver.h
        MAIN_DEPENDENCY spec.json
        DEPENDS jsonrpcstub
        COMMENT "Generating Server Stubfiles"
        VERBATIM
)

add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/include/example/stubclient.h
        COMMAND jsonrpcstub ARGS ${CMAKE_CURRENT_SOURCE_DIR}/spec.json --cpp-client=StubClient --cpp-client-file=${CMAKE_BINARY_DIR}/include/example/stubclient.h
        MAIN_DEPENDENCY spec.json
        DEPENDS jsonrpcstub
        COMMENT "Generating Client Stubfile"
        VERBATIM
)

add_custom_target(common_stubs
        DEPENDS ${CMAKE_BINARY_DIR}/include/example/abstractstubserver.h ${CMAKE_BINARY_DIR}/include/example/stubclient.h
        )

add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/include/example/xbmcremote.h
        COMMAND jsonrpcstub ARGS ${CMAKE_CURRENT_SOURCE_DIR}/xbmc_remote.json --cpp-client=XbmcRemoteClient --cpp-client-file=${CMAKE_BINARY_DIR}/include/example/xbmcremote.h
        MAIN_DEPENDENCY xbmc_remote.json
        DEPENDS jsonrpcstub
        COMMENT "Generating Client XBMC Stubfile"
        VERBATIM
)

include_directories(..)
include_directories(${CMAKE_BINARY_DIR})
include_directories(${MHD_INCLUDE_DIRS})

if (UNIX)
    if (UNIX_DOMAIN_SOCKET_SERVER AND UNIX_DOMAIN_SOCKET_CLIENT)
        add_executable(unixdomainsocketserversample unixdomainsocketserver.cpp)
        target_link_libraries(unixdomainsocketserversample jsonrpcserver)
        add_executable(unixdomainsocketclientsample unixdomainsocketclient.cpp)
        target_link_libraries(unixdomainsocketclientsample jsonrpcclient)
    endif ()

    if (FILE_DESCRIPTOR_SERVER AND FILE_DESCRIPTOR_CLIENT)
        add_executable(filedescriptorserversample filedescriptorserver.cpp)
        target_link_libraries(filedescriptorserversample jsonrpcserver)
        add_executable(filedescriptorclientsample filedescriptorclient.cpp)
        target_link_libraries(filedescriptorclientsample jsonrpcclient)
    endif ()
endif (UNIX)

if (TCP_SOCKET_SERVER AND TCP_SOCKET_CLIENT)
    add_executable(tcpsocketclient tcpsocketclient.cpp)
    target_link_libraries(tcpsocketclient jsonrpcclient)
    add_executable(tcpsocketserver tcpsocketserver.cpp)
    target_link_libraries(tcpsocketserver jsonrpcserver)
endif ()

if (SERIAL_PORT_SERVER AND SERIAL_PORT_CLIENT)
    add_executable(serialportclient serialportclient.cpp)
    target_link_libraries(serialportclient jsonrpcclient)
    add_executable(serialportserver serialportserver.cpp)
    target_link_libraries(serialportserver jsonrpcserver)
endif ()

if (HTTP_SERVER)
    add_executable(simpleserversample simpleserver.cpp)
    target_link_libraries(simpleserversample jsonrpcserver)
endif ()

if (HTTP_CLIENT)
    add_executable(simpleclientsample simpleclient.cpp)
    target_link_libraries(simpleclientsample jsonrpcclient)
endif ()

if (REDIS_SERVER)
    add_executable(redisserversample redisserver.cpp)
    target_link_libraries(redisserversample jsonrpcserver)
endif ()

if (REDIS_CLIENT)
    add_executable(redisclientsample redisclient.cpp)
    target_link_libraries(redisclientsample jsonrpcclient)
endif ()

if (COMPILE_STUBGEN)
    if (HTTP_CLIENT)
        add_executable(stubclientsample stubclient.cpp)
        target_include_directories(stubclientsample PRIVATE ${CMAKE_BINARY_DIR}/include/example)
        target_link_libraries(stubclientsample jsonrpcclient)
        add_dependencies(stubclientsample common_stubs)

        add_executable(xbmcremote xbmcremote.cpp ${CMAKE_BINARY_DIR}/include/example/xbmcremote.h)
        target_include_directories(xbmcremote PRIVATE ${CMAKE_BINARY_DIR}/include/example)
        target_link_libraries(xbmcremote jsonrpcclient)
    endif ()

    if (HTTP_SERVER)
        add_executable(stubserversample stubserver.cpp)
        target_include_directories(stubserversample PRIVATE ${CMAKE_BINARY_DIR}/include/example)
        target_link_libraries(stubserversample jsonrpcserver)
        add_dependencies(stubserversample common_stubs)
    endif ()
endif ()

