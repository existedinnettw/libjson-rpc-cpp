#include <jsonrpccpp/client.h>
#include <jsonrpccpp/common/errors.h>
#include <jsonrpccpp/server.h>
#include <jsonrpccpp/server/connectors/httpserver.h>
#include <string>

int main() {
  [[maybe_unused]] auto e = jsonrpc::Errors::ERROR_RPC_JSON_PARSE_ERROR;
  jsonrpc::HttpServer httpserver(8383);
}