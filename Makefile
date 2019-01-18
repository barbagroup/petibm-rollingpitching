PETIBM_DIR = $(HOME)/software/petibm/0.4/linux-gnu-openmpi-opt

PETSC_DIR = $(HOME)/software/petsc/3.10.1
PETSC_ARCH = linux-gnu-openmpi-opt

MPI_DIR = $(HOME)/software/openmpi/1.8.8/linux-gnu-opt
YAMLCPP_DIR = $(HOME)/software/yaml-cpp/0.6.2/linux-gnu-opt

LDFLAGS = -L$(PETIBM_DIR)/lib \
          -Wl,-rpath,$(PETIBM_DIR)/lib \
          -L$(PETSC_DIR)/$(PETSC_ARCH)/lib \
          -Wl,-rpath,$(PETSC_DIR)/$(PETSC_ARCH)/lib \
          -L$(YAMLCPP_DIR)/lib \
          -Wl,-rpath,$(YAMLCPP_DIR)/lib

LIBS = -lpetibmapps \
       -lpetibm \
       -lpetsc \
       -lyaml-cpp

INCLUDES = -I$(PETSC_DIR)/include \
           -I$(PETSC_DIR)/$(PETSC_ARCH)/include \
           -I$(YAMLCPP_DIR)/include \
           -I$(PETIBM_DIR)/include

CXX = $(MPI_DIR)/bin/mpicxx
CXXFLAGS = -w -O3 -Wall -Wno-deprecated --std=c++14

rootdir = $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
srcdir = $(rootdir)/src
builddir = $(rootdir)/build
bindir = $(rootdir)/bin

srcs = $(shell find $(srcdir) -type f -name *.cpp)
objs = $(patsubst $(srcdir)/%, $(builddir)/%, $(srcs:.cpp=.o))
target = $(bindir)/petibm-rollingpitching

all: $(target)

$(target): $(objs)
	@mkdir -p $(bindir)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS) $(LIBS)

$(builddir)/%.o: $(srcdir)/%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	@rm -rf $(builddir)
	@rm -rf $(bindir)

.PHONY: all clean
