#include <jsonrpccpp/client.h>
#include <jsonrpccpp/server.h>
#include <jsonrpccpp/server/connectors/httpserver.h>
#include <string>

int main() { jsonrpc::HttpServer httpserver(8383); }