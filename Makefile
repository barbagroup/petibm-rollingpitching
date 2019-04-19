PETSC_DIR = $(HOME)/opt/petsc/3.10.2
PETSC_ARCH = linux-gnu-openmpi-opt

YAMLCPP_DIR = $(HOME)/software/yaml-cpp/0.6.2/linux-gnu-opt

LDFLAGS = -L$(PETSC_DIR)/$(PETSC_ARCH)/lib \
          -Wl,-rpath,$(PETSC_DIR)/$(PETSC_ARCH)/lib

LIBS = -lpetibmapps \
       -lpetibm \
       -lpetsc \
       -lyaml-cpp

INCLUDES = -I$(PETSC_DIR)/include \
           -I$(PETSC_DIR)/$(PETSC_ARCH)/include

CXX = mpicxx
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
