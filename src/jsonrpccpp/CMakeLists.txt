# setup common headers and sources
file(GLOB jsonrpc_header *.h)
file(GLOB jsonrpc_header_common common/*.h)
file(GLOB jsonrpc_source_common common/*.c*)

# setup server headers and sources
file(GLOB jsonrpc_install_header_server
        server/requesthandlerfactory.h
        server/abstractserver.h
        server/abstractserverconnector.h
        server/abstractthreadedserver.h
        server/iprocedureinvokationhandler.h
        server/iclientconnectionhandler.h
        server/threadpool.h
        )
file(GLOB jsonrpc_header_server server/*.h)
file(GLOB jsonrpc_source_server server/*.c*)

# setup client headers and sources
file(GLOB jsonrpc_install_header_client
        client/batchcall.h
        client/batchresponse.h
        client/client.h
        client/iclientconnector.h
        )
file(GLOB jsonrpc_header_client client/*.h)
file(GLOB jsonrpc_source_client client/*.c*)

# setup connector variables defaults
set(client_connector_source "")
set(client_connector_header "")
set(client_connector_libs "")
set(server_connector_source "")
set(server_connector_header "")
set(server_connector_libs "")
set(SERVER_LIBS "")
set(CLIENT_LIBS "")

# setup sources for http connectors
if (HTTP_CLIENT)
    list(APPEND client_connector_header "client/connectors/httpclient.h")
    list(APPEND client_connector_source "client/connectors/httpclient.cpp")
    list(APPEND client_connector_libs ${CURL_LIBRARIES})
    set(CLIENT_LIBS "${CLIENT_LIBS} -lcurl")
endif ()

if (HTTP_SERVER)
    list(APPEND server_connector_header "server/connectors/httpserver.h")
    list(APPEND server_connector_source "server/connectors/httpserver.cpp")
    list(APPEND server_connector_libs ${CMAKE_THREAD_LIBS_INIT} libmicrohttpd::libmicrohttpd)
    set(SERVER_LIBS "${SERVER_LIBS} -lmicrohttpd")
endif ()

# setup sources for redis connectors
if (REDIS_CLIENT)
    list(APPEND client_connector_header "client/connectors/redisclient.h")
    list(APPEND client_connector_source "client/connectors/redisclient.cpp")
    list(APPEND client_connector_libs hiredis::hiredis)
    include_directories(${HIREDIS_INCLUDE_DIRS})
    set(CLIENT_LIBS "${CLIENT_LIBS} -lhiredis")
endif ()

if (REDIS_SERVER)
    list(APPEND server_connector_header "server/connectors/redisserver.h")
    list(APPEND server_connector_source "server/connectors/redisserver.cpp")
    list(APPEND server_connector_libs ${CMAKE_THREAD_LIBS_INIT} hiredis::hiredis)
    set(SERVER_LIBS "${SERVER_LIBS} -lhiredis")
endif ()

# setup sources for unix domain socket connectors
if (UNIX_DOMAIN_SOCKET_SERVER)
    list(APPEND server_connector_header "server/connectors/unixdomainsocketserver.h")
    list(APPEND server_connector_source "server/connectors/unixdomainsocketserver.cpp")
    list(APPEND server_connector_libs ${CMAKE_THREAD_LIBS_INIT})
endif ()

if (UNIX_DOMAIN_SOCKET_CLIENT)
    list(APPEND client_connector_header "client/connectors/unixdomainsocketclient.h")
    list(APPEND client_connector_source "client/connectors/unixdomainsocketclient.cpp")
endif ()

# setup sources for tcp socket connectors
if (TCP_SOCKET_SERVER)
    list(APPEND server_connector_header "server/connectors/tcpsocketserver.h")
    list(APPEND server_connector_source "server/connectors/tcpsocketserver.cpp")
    if (WIN32)
        list(APPEND server_connector_header "server/connectors/windowstcpsocketserver.h")
        list(APPEND server_connector_source "server/connectors/windowstcpsocketserver.cpp")
        list(APPEND server_connector_libs ws2_32)
    endif ()
    if (UNIX)
        list(APPEND server_connector_header "server/connectors/linuxtcpsocketserver.h")
        list(APPEND server_connector_source "server/connectors/linuxtcpsocketserver.cpp")
    endif ()
    list(APPEND server_connector_libs ${CMAKE_THREAD_LIBS_INIT})
endif ()

if (TCP_SOCKET_CLIENT)
    list(APPEND client_connector_header "client/connectors/tcpsocketclient.h")
    list(APPEND client_connector_source "client/connectors/tcpsocketclient.cpp")
    if (WIN32)
        list(APPEND client_connector_header "client/connectors/windowstcpsocketclient.h")
        list(APPEND client_connector_source "client/connectors/windowstcpsocketclient.cpp")
        list(APPEND client_connector_libs ws2_32)
    endif ()
    if (UNIX)
        list(APPEND client_connector_header "client/connectors/linuxtcpsocketclient.h")
        list(APPEND client_connector_source "client/connectors/linuxtcpsocketclient.cpp")
    endif ()
    list(APPEND client_connector_libs ${CMAKE_THREAD_LIBS_INIT})
endif ()

if (SERIAL_PORT_SERVER)
    if (UNIX)
        list(APPEND server_connector_header "server/connectors/linuxserialportserver.h")
        list(APPEND server_connector_source "server/connectors/linuxserialportserver.cpp")
    endif ()
    list(APPEND server_connector_libs ${CMAKE_THREAD_LIBS_INIT})
endif ()

if (SERIAL_PORT_CLIENT)
    if (UNIX)
        list(APPEND client_connector_header "client/connectors/linuxserialportclient.h")
        list(APPEND client_connector_source "client/connectors/linuxserialportclient.cpp")
    endif ()
    list(APPEND client_connector_libs ${CMAKE_THREAD_LIBS_INIT})
endif ()

if (FILE_DESCRIPTOR_SERVER)
    list(APPEND server_connector_header "server/connectors/filedescriptorserver.h")
    list(APPEND server_connector_source "server/connectors/filedescriptorserver.cpp")
    list(APPEND server_connector_libs ${CMAKE_THREAD_LIBS_INIT})
endif ()

if (FILE_DESCRIPTOR_CLIENT)
    list(APPEND client_connector_header "client/connectors/filedescriptorclient.h")
    list(APPEND client_connector_source "client/connectors/filedescriptorclient.cpp")
    list(APPEND client_connector_libs ${CMAKE_THREAD_LIBS_INIT})
endif ()

# configure a header file to pass some of the CMake settings to the source code
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/version.h.in" "${CMAKE_BINARY_DIR}/include/jsonrpccpp/version.h" @ONLY)

# include required directories
include_directories(..)

# setup shared common library
find_package(jsoncpp REQUIRED CONFIG)


add_library(jsonrpc INTERFACE ${jsonrpc_header})

if (BUILD_SHARED_LIBS)
    add_library(jsonrpccommon SHARED ${jsonrpc_source_common} ${jsonrpc_helper_source_common})
    target_include_directories(jsonrpccommon PUBLIC ${CMAKE_BINARY_DIR}/include)
    target_link_libraries(jsonrpccommon PUBLIC JsonCpp::JsonCpp jsonrpc)
    set_target_properties(jsonrpccommon PROPERTIES OUTPUT_NAME jsonrpccpp-common)
endif ()

# setup static common library
if (BUILD_STATIC_LIBS OR MSVC)
    add_library(common STATIC ${jsonrpc_source_common} ${jsonrpc_helper_source_common})
    target_include_directories(common PUBLIC ${CMAKE_BINARY_DIR}/include)
    target_link_libraries(common PUBLIC JsonCpp::JsonCpp jsonrpc)
    set_target_properties(common PROPERTIES OUTPUT_NAME jsonrpccpp-common)

    if (NOT BUILD_SHARED_LIBS)
        add_library(jsonrpccommon ALIAS common)
    endif ()
endif ()



add_library(jsonrpcclientconnector INTERFACE)
target_sources(jsonrpcclientconnector INTERFACE ${client_connector_source})

# setup shared client library
if (BUILD_SHARED_LIBS)
    add_library(jsonrpcclient SHARED ${jsonrpc_source_client} ${jsonrpc_header_client})
    add_dependencies(jsonrpcclient jsonrpccommon)
    target_link_libraries(jsonrpcclient jsonrpccommon ${client_connector_libs} jsonrpcclientconnector)
    set_target_properties(jsonrpcclient PROPERTIES OUTPUT_NAME jsonrpccpp-client)
endif ()

# setup static client library
if (BUILD_STATIC_LIBS OR MSVC)
    add_library(client STATIC ${jsonrpc_source_client} ${jsonrpc_header_client})
    target_link_libraries(client common ${client_connector_libs} jsonrpcclientconnector)
    set_target_properties(client PROPERTIES OUTPUT_NAME jsonrpccpp-client)

    if (NOT BUILD_SHARED_LIBS)
        add_library(jsonrpcclient ALIAS client)
    endif ()
endif ()


add_library(jsonrpcserverconnector INTERFACE)
target_sources(jsonrpcserverconnector INTERFACE ${server_connector_source})

# setup shared server library
if (BUILD_SHARED_LIBS)
    add_library(jsonrpcserver SHARED ${jsonrpc_source_server} ${jsonrpc_header_server})
    add_dependencies(jsonrpcserver jsonrpccommon)
    target_link_libraries(jsonrpcserver jsonrpccommon ${server_connector_libs} jsonrpcserverconnector)
    # target_include_directories(jsonrpcserver PUBLIC ${CMAKE_BINARY_DIR}/include)
    set_target_properties(jsonrpcserver PROPERTIES OUTPUT_NAME jsonrpccpp-server)
endif ()

# setup static server library
if (BUILD_STATIC_LIBS OR MSVC)
    add_library(server STATIC ${jsonrpc_source_server} ${jsonrpc_header_server})
    target_link_libraries(server common ${server_connector_libs} jsonrpcserverconnector)
    set_target_properties(server PROPERTIES OUTPUT_NAME jsonrpccpp-server)
    # target_include_directories(server PUBLIC ${CMAKE_BINARY_DIR}/include)
    if (NOT BUILD_SHARED_LIBS)
        add_library(jsonrpcserver ALIAS server)
    endif ()
endif ()

# setup version
set(VERSION_STRING ${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION})

set_target_properties(
    jsonrpc
    PROPERTIES 
    VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
    PUBLIC_HEADER "${jsonrpc_header}"
)
install(TARGETS jsonrpc
    PUBLIC_HEADER DESTINATION include/jsonrpccpp
)
set_target_properties(
    jsonrpcclientconnector
    PROPERTIES 
    VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
    PUBLIC_HEADER "${client_connector_header}"
)
install(TARGETS jsonrpcclientconnector
    PUBLIC_HEADER DESTINATION include/jsonrpccpp/client/connectors
)
set_target_properties(
    jsonrpcserverconnector
    PROPERTIES 
    VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
    PUBLIC_HEADER "${server_connector_header}"
)
install(TARGETS jsonrpcserverconnector
    PUBLIC_HEADER DESTINATION include/jsonrpccpp/server/connectors
)

if (BUILD_SHARED_LIBS OR NOT BUILD_STATIC_LIBS)
    set_target_properties(
        jsonrpccommon
        PROPERTIES 
        VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
        PUBLIC_HEADER "${jsonrpc_header_common}"
    )
    install(TARGETS jsonrpccommon
        PUBLIC_HEADER DESTINATION include/jsonrpccpp/common
    )

    set_target_properties(
        jsonrpcclient
        PROPERTIES 
        VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
        PUBLIC_HEADER "${jsonrpc_install_header_client}"
    )
    install(TARGETS jsonrpcclient
        PUBLIC_HEADER DESTINATION include/jsonrpccpp/client
    )

    set_target_properties(
        jsonrpcserver
        PROPERTIES 
        VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
        PUBLIC_HEADER "${jsonrpc_install_header_server}"
    )
    install(TARGETS jsonrpcserver
        PUBLIC_HEADER DESTINATION include/jsonrpccpp/server
    )
endif()

if (BUILD_STATIC_LIBS OR MSVC)
    set_target_properties(
        common
        PROPERTIES 
        VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
        PUBLIC_HEADER "${jsonrpc_header_common}"
    )
    install(TARGETS common
        PUBLIC_HEADER DESTINATION include/jsonrpccpp/common
    )

    set_target_properties(
        client
        PROPERTIES 
        VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
        PUBLIC_HEADER "${jsonrpc_install_header_client}"
    )
    install(TARGETS client
        PUBLIC_HEADER DESTINATION include/jsonrpccpp/client
    )

    set_target_properties(
        server
        PROPERTIES 
        VERSION "${VERSION_STRING}" SOVERSION "${SO_VERSION}"
        PUBLIC_HEADER "${jsonrpc_install_header_server}"
    )
    install(TARGETS server
        PUBLIC_HEADER DESTINATION include/jsonrpccpp/server
    )
endif()

if (WIN32 AND NOT HUNTER_ENABLED)
    # On Windows copy manually installed dependencies unless Hunter is used.
    file(GLOB win32_libs ${CMAKE_SOURCE_DIR}/win32-deps/lib/*.dll)
    file(COPY ${win32_libs} DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
    install(FILES ${win32_libs} DESTINATION bin)
    install(DIRECTORY ${CMAKE_SOURCE_DIR}/win32-deps/include DESTINATION .)
endif ()