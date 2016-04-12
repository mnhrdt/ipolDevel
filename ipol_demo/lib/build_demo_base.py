"""
Base class for BuildDemo

Karl Krissian

"""

import os, shutil
from lib.misc import ctime
import shutil
import stat
import urlparse
from os import path
from lib import build
import tempfile
import time 

#-------------------------------------------------------------------------------
class BuildDemoBase:
  
  #-----------------------------------------------------------------------------
  def __init__(self,base_dir):
    self.base_dir    = base_dir
    self.src_dir     = os.path.join(self.base_dir,'src/')
    self.bin_dir     = os.path.join(self.base_dir,'bin/')
    self.scripts_dir = os.path.join(self.base_dir,'scripts/')
    self.dl_dir      = os.path.join(self.base_dir,'dl/')
    self.log_file    = os.path.join(self.base_dir, "build.log"   )
      
  #-----------------------------------------------------------------------------
  # set the build parameters as a dictionnary (usually read from JSON file)
  def set_params(self,params):
    self.params=params
      
  #-----------------------------------------------------------------------------
  def make(self, clean_previous=True):
    # can be overridden, need self.params to be defined
    """
    program build/update
    """
    print "make begin"
    total_start = time.time()
    make_info = ""
    programs = self.params['binaries']
    
    #print "make(clean_previous={0})".format(clean_previous)
    zip_filename  = urlparse.urlsplit(self.params['url']).path.split('/')[-1]
    src_dir_name  = self.params['srcdir']
    src_path      = path.join(self.src_dir, src_dir_name)

    # store common file path in variables
    tgz_file  = path.join( self.dl_dir,   zip_filename  )
    
    print "make download archive"
    # get the latest source archive
    build.download(self.params['url'], tgz_file)

    rebuild_needed = False

    # test if the dest file is missing, or too old, for each program to build
    for program in programs:
        print "build ", program
        # use first binary name to check time
        prog_filename = program[1]
        prog_file = path.join( self.bin_dir,  os.path.basename(prog_filename) )
        if os.path.basename(prog_filename)=='' and len(program)==3:
            prog_file = path.join( self.bin_dir,program[2])
        if not(path.isfile(prog_file)) or (ctime(tgz_file) > ctime(prog_file)):
            rebuild_needed = True
            
    # test timestamp for scripts too
    if 'scripts' in self.params.keys():
        for script in self.params['scripts']:
            script_file = path.join(  self.scripts_dir, script[1])
            if os.path.basename(script[1])=='' and len(script)==3:
                script_file = path.join( self.scripts_dir,script[1],script[2])
            if not(path.isfile(script_file)) or (ctime(tgz_file) > ctime(script_file)):
                rebuild_needed = True

    #--- build
    if not(rebuild_needed):
        make_info += "no rebuild needed "
        print "no rebuild needed ",
    else:
      print "extracting archive"
      # extract the archive
      start = time.time()
      build.extract(tgz_file, self.src_dir)
      make_info += "extracting archive: {0} sec.; ".format(time.time()-start)

      print "creating bin_dir"
      # delete and create bin dir
      if path.isdir(self.bin_dir): 
        if clean_previous: 
          shutil.rmtree(self.bin_dir)
          os.mkdir(self.bin_dir)
      else:
        os.mkdir(self.bin_dir)

      print "creating scripts dir"
      # create scripts dir if needed
      if not(path.isdir(self.scripts_dir)): 
        os.mkdir(self.scripts_dir)
      #else:
        # don't clean previous contents
        #if clean_previous: 
          #shutil.rmtree(self.scripts_dir)
          #os.mkdir(self.scripts_dir)
            
      #----- CMAKE build
      start = time.time()
      print "creating bin_dir"
      if  ('build_type' in self.params.keys()) and \
          (self.params['build_type'].upper()=='cmake'.upper()):
        print "using CMAKE"
        # Run cmake first:
        # create temporary build dir IPOL_xxx_build
        build_dir = path.join(src_path,"__IPOL_build__")
        os.mkdir(build_dir)
        # prepare_cmake can fix some options before configuration
        if ('prepare_cmake' in self.params.keys()):
          print 'prepare_cmake :', self.params['prepare_cmake']
          build.run(self.params['prepare_cmake'],
                    stdout=self.log_file, cwd=src_path)
        print "..."
        # set release mode by default, other options could be added
        if ('cmake_flags' in self.params.keys()):
          cmake_flags = self.params['cmake_flags']
        else:
          cmake_flags = ''
        build.run("cmake -D CMAKE_BUILD_TYPE:string=Release "+cmake_flags+ " " +src_path,
                  stdout=self.log_file, cwd=build_dir)
        # build
        build.run("make %s " % ( self.params['flags']), 
                  stdout=self.log_file,cwd=build_dir)
        # copy binaries
        for program in programs:
          prog_path=path.join(build_dir, program[0])
          bin_path =path.join(prog_path, program[1])
          if os.path.isdir(bin_path):
            print "copying all files in bin dir"
            # copy all files to bin dir
            src_files = os.listdir(bin_path)
            for file_name in src_files:
              full_file_name = os.path.join(bin_path, file_name)
              if (os.path.isfile(full_file_name)):
                print "{0}; ".format(file_name),
                shutil.copy(full_file_name, self.bin_dir)
            print ''
          else:
            # copy binary to bin dir
            print "{0}-->{1}".format(bin_path,self.bin_dir)
            shutil.copy(bin_path,self.bin_dir)
      else:
      #----- MAKE build
        print "using MAKE"

        # prepare_cmake can fix some options before configuration
        if ('prepare_make' in self.params.keys()):
          print 'prepare_make :', self.params['prepare_make']
          build.run(self.params['prepare_make'],
                    stdout=self.log_file, cwd=src_path)
        print "..."

        # build the programs for make
        for program in programs:
          prog_path=path.join(src_path,  program[0])
          bin_path =path.join(prog_path, program[1])
          # build
          if os.path.isdir(bin_path):
            cmd = "make %s -C %s" % (self.params['flags'], prog_path)
          else:
            cmd = "make %s -C %s %s" % (self.params['flags'], prog_path, program[1])
          print cmd
          build.run(cmd, stdout=self.log_file)
          if os.path.isdir(bin_path):
            print "copying all files in bin dir ", bin_path
            # copy all files to bin dir
            src_files = os.listdir(bin_path)
            for file_name in src_files:
              full_file_name = os.path.join(bin_path, file_name)
              if (os.path.isfile(full_file_name)):
                print "{0}; ".format(file_name),
                shutil.copy(full_file_name, self.bin_dir)
            print ''
          else:
            # copy binary to bin dir
            print "{0}-->{1}".format(bin_path,self.bin_dir)
            shutil.copy(bin_path,self.bin_dir)

      if 'scripts' in self.params.keys():
        print self.params['scripts']
        # Move scripts to the scripts dir
        for script in self.params['scripts']:
          print "moving ",path.join(src_path, script[0], script[1]), " to ", self.scripts_dir
          new_file = path.join( self.scripts_dir, script[1])
          if os.path.exists(new_file):
              if path.isfile(new_file): 
                os.remove(new_file)
              else:
                os.chmod( new_file, stat.S_IRWXU )
                shutil.rmtree(new_file)
          shutil.move(path.join(src_path, script[0], script[1]),self.scripts_dir)
          # Give exec permission to the script
          os.chmod( new_file, stat.S_IREAD | stat.S_IEXEC )
      # prepare_cmake can fix some options before configuration
      if ('post_build' in self.params.keys()):
        print 'post_build command:', self.params['post_build']
        build.run(self.params['post_build'],
                stdout=self.log_file, cwd=src_path)
          
      # cleanup the source dir
      shutil.rmtree(self.src_dir)
      make_info += "build: {0} sec.; ".format(time.time()-start)

    make_info += "total elapsed time: {0} sec.".format(time.time()-total_start)
    print "make end"
      
    return make_info

  
  #-----------------------------------------------------------------------------
  def clean(self):
    "Cleaning"
    if path.exists(self.src_dir):      shutil.rmtree(self.src_dir)
    if path.exists(self.bin_dir):      shutil.rmtree(self.bin_dir)
    if path.exists(self.scripts_dir):  shutil.rmtree(self.scripts_dir)
    if path.exists(self.dl_dir) :      shutil.rmtree(self.dl_dir)
    # clean log?
