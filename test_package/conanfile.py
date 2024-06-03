import os

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run


class amphimoveTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        '''
        ref
        ---
        [Using the same requirement as a requires and as a tool_requires]
        (https://docs.conan.io/2/examples/graph/tool_requires/using_protobuf.html#examples-graph-tool-requires-protobuf)
        '''
        self.requires(self.tested_reference_str, run=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if can_run(self):
            cmd = os.path.join(self.cpp.build.bindir, "example")
            self.run(cmd, env="conanrun")
            
            idl_path=os.path.join(self.source_folder, "spec.json")
            out_dir=os.path.join(self.build_folder, "include")
            out_path=os.path.join(out_dir, "abstractstubserver.h")
            os.mkdir(out_dir)
            self.run(f"jsonrpcstub {idl_path} --cpp-server=AbstractStubServer \
                     --cpp-server-file={out_path}", env="conanrun")
