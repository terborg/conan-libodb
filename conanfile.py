 
from conans import ConanFile, tools, AutoToolsBuildEnvironment
import shutil
import os

class LibodbConan( ConanFile ):
    name = "libodb"
    version = "2.4.0"
    license = "GPL"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def source(self):
        tools.get( "https://www.codesynthesis.com/download/odb/2.4/libodb-2.4.0.tar.bz2", sha1="42bd2a8023e338e004711e755eb30bd122b844a6" )

    def source_path( self ):
        return os.path.join( self.source_folder, self.name + '-' + self.version )

    def build( self ):
        #
        # Here, we remove the stdlib c++, because it can not be found by the configure script
        # for Android
        #
        if tools.cross_building( self.settings ):
            del self.settings.compiler.libcxx
        
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = self.options.fPIC

        configure_args = []
        if not self.options.shared:
            configure_args.extend( [ '--enable-static', '--disable-shared', '--enable-static-boost' ] )
        
        env_build.configure( configure_dir = self.source_path(), args=configure_args )
        env_build.make()

    def package(self):
        
        self.copy( "*.hxx", dst="include/odb", src= os.path.join( self.source_path(), "odb" )  )
        self.copy( "*.a", dst="lib", keep_path=False )

    def package_info(self):
        self.cpp_info.libs = ["odb"]

