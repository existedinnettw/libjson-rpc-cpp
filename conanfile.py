from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.build import check_min_cppstd, can_run


class LibJsonRPCCPPConan(ConanFile):
    name = "libjson-rpc-cpp"
    version = "1.4.1"
    description = "C++ framework for json-rpc (json remote procedure call)"
    homepage = "https://github.com/cinemast/libjson-rpc-cpp"
    url = "http://gitlab.khomp.corp/conan/conan-libjson-rpc-cpp"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_http_client": [True, False],
        "with_http_server": [True, False],
        "with_redis": [True, False],
        "build_examples": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_http_client": True,
        "with_http_server": True,
        "with_redis": False,
        "build_examples": False,
    }
    exports_sources = ["CMakeLists.txt", "cmake.patch"]
    # _source_subfolder = "source_subfolder"
    # _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("argtable2/[~2.13]")  # argtable3 exist
        self.requires("jsoncpp/[~1.9]")
        if self.options.with_http_client:
            self.requires("libcurl/[~8.6]")
        if self.options.with_http_server:
            self.requires("libmicrohttpd/[~0.9]")
        if self.options.with_redis:
            self.requires("hiredis/[~1]")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BUILD_STATIC_LIBS"] = not self.options.shared
        tc.variables["COMPILE_EXAMPLES"] = self.options.build_examples
        if not self.conf.get("tools.build:skip_test", default=False):
            tc.variables["COMPILE_TESTS"] = True
        else:
            tc.variables["COMPILE_TESTS"] = False
        tc.variables["COMPILE_STUBGEN"] = True
        tc.variables["REDIS_SERVER"] = self.options.with_redis
        tc.variables["REDIS_CLIENT"] = self.options.with_redis
        tc.variables["HTTP_SERVER"] = self.options.with_http_server
        tc.variables["HTTP_CLIENT"] = self.options.with_http_client
        tc.variables["TCP_SOCKET_SERVER"] = True
        tc.variables["TCP_SOCKET_CLIENT"] = True
        tc.variables["WITH_COVERAGE"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if (not self.conf.get("tools.build:skip_test", default=False)) and can_run(
            self
        ):
            cmake.test()  # TODO COMPILE_TESTS  option

    def package(self):
        cmake = CMake(self)
        cmake.install()
        # self.copy(pattern="LICENSE.txt", dst="licenses", src=self._source_subfolder)
        # self.copy(
        #     "*.h",
        #     src=os.path.join(self._source_subfolder, "src", "jsonrpccpp"),
        #     dst=os.path.join("include", "jsonrpccpp"),
        # )
        # self.copy(
        #     "*.h",
        #     src=os.path.join(self._build_subfolder, "gen"),
        #     dst=os.path.join("include"),
        # )
        # self.copy(pattern="*.dll", dst="bin", keep_path=False)
        # self.copy(pattern="*.lib", dst="lib", keep_path=False)
        # self.copy(pattern="*.a", dst="lib", keep_path=False)
        # self.copy(pattern="*.so*", dst="lib", keep_path=False)
        # self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["jsoncpp_lib_static"]
