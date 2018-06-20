from conans import ConanFile, CMake
from conans.errors import ConanException


class MsgpackCConan(ConanFile):
    name = "msgpack-c"
    version = "3.0.1"
    description = """msgpack is "MessagePack implementation for C and C++".
                     See: https://github.com/msgpack/msgpack-c"""
    url = "https://github.com/paulobrizolara/msgpack-c-conan"
    license = """Boost Software License - Version 1.0.
                 http://www.boost.org/LICENSE_1_0.txt"""
    settings = "os", "compiler", "build_type", "arch", "cppstd"
    options = {"header_only": [True, False]}
    default_options = "header_only=False"
    sources = "https://github.com/msgpack/msgpack-c"
    source_dir = "{name}-{version}".format(name=name, version=version)
    scm = {
        "type": "git",
        "subfolder": source_dir,
        "url": sources,
        "revision": "cpp-{}".format(version)
    }
    generators = "cmake"

    def is_header_only(self):
        try:
            val = self.options.header_only \
                or (self.settings.cppstd is not None
                    and self.settings.cppstd not in ['98', 'gnu98'])
        except ConanException:
            val = False
        return val

    def configure(self):
        if self.is_header_only():
            self.settings.clear()

    def source(self):
        pass

    def build(self):
        if self.is_header_only():
            return

        cmake = CMake(self)
        #cmake.verbose = True
        cmake.definitions["MSGPACK_CXX11"] = self.is_header_only()
        cmake.definitions["MSGPACK_BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["MSGPACK_BUILD_TESTS"] = self.develop
        cmake.configure(source_folder=self.source_dir)
        cmake.build()
        if self.develop:
            cmake.test()
        cmake.install()

    def package(self):
        # already done by 'make install'
        pass

    def package_info(self):
        if not self.is_header_only():
            self.cpp_info.libs = ["msgpackc"]
