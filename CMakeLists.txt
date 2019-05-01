# =====================================================================
# \file CMakeLists.txt
# \brief File for cmake to build petibm-rollingpitching
# \author Olivier Mesnard (mesnardo@gwu.edu)
# =====================================================================

cmake_minimum_required(VERSION 3.5)

project(PetIBMRollingPitching)
set(PetIBMRollingPitching_VERSION_MAJOR 0)
set(PetIBMRollingPitching_VERSION_MINOR 1)

enable_language(CXX)

if(NOT DEFINED ENV{CXX})
    set(ENV{CXX} mpicxx)
endif()

if(NOT DEFINED ENV{CC})
    set(ENV{CC} mpicc)
endif()

configure_file(
    "${PROJECT_SOURCE_DIR}/src/config.h.in"
    "${PROJECT_BINARY_DIR}/config.h"
)

# Provide a default install directory
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/installdir"
        CACHE PATH "Installation directory" FORCE)
endif()


# =====================================================================
# Cache variables
# =====================================================================

set(CMAKE_CXX_FLAGS_DEBUG "-g" CACHE STRING "")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG" CACHE STRING "")
set(CMAKE_BUILD_TYPE RELEASE CACHE STRING "Choose the type of build.")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH ON CACHE STRING "")

set(PETSC_DIR "$ENV{PETSC_DIR}" CACHE PATH "Path of PETSc")
set(PETSC_ARCH "$ENV{PETSC_ARCH}" CACHE STRING "PETSc build folder")
set(PETIBM_DIR "$ENV{PETIBM_DIR}" CACHE PATH "Path of PetIBM")
set(YAMLCPP_DIR "$ENV{YAMLCPP_DIR}" CACHE PATH "Path of yaml-cpp")

# =====================================================================
# Project settings
# =====================================================================

message("")
message("====================================")
message("Begin configuration")
message("====================================")

include(GNUInstallDirs)

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR})

include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++14" COMPILER_SUPPORTS_CXX14)
if(COMPILER_SUPPORTS_CXX14)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
else()
    message(FATAL_ERROR
        "Compiler ${CMAKE_CXX_COMPILER} does not support flag -std=c++14 \
        Please specify C++14 flag manually through CMAKE_CXX_FLAGS.")
endif()

set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_COLOR_MAKEFILE ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake-modules")

# =====================================================================
# PETSc
# =====================================================================

message("")
message("-- Finding PETSc")

find_package(PETSc REQUIRED)

if(${PETSC_FOUND})
    message("-- Finding PETSc - Sucess")
endif()

# =====================================================================
# yaml-cpp
# =====================================================================

message("")
message("-- Finding yaml-cpp")

message("-- Finding yaml-cpp/yaml.h")
find_path(YAMLCPP_INCLUDE_DIRS
          NAME yaml-cpp/yaml.h
          PATHS ${YAMLCPP_DIR} $ENV{YAMLCPP_DIR}
          PATH_SUFFIXES "include")

if(${YAMLCPP_INCLUDE_DIRS} STREQUAL "YAMLCPP_INCLUDE_DIRS-NOTFOUND")
    message(FATAL_ERROR "Could not find yaml-cpp/yaml.h!")
else()
    message("-- Finding yaml-cpp/yaml.h - found in "
            ${YAMLCPP_INCLUDE_DIRS})
endif()

message("-- Finding yaml-cpp library")
find_library(YAMLCPP_LIBRARIES
             NAMES yaml-cpp
             PATHS ${YAMLCPP_DIR} $ENV{YAMLCPP_DIR}
             PATH_SUFFIXES "lib" "lib64")

if(${YAMLCPP_LIBRARIES} STREQUAL "YAMLCPP_LIBRARIES-NOTFOUND")
    message(FATAL_ERROR "Could not find yaml-cpp library!")
else()
    message("-- Finding yaml-cpp library - found in "
            ${YAMLCPP_LIBRARIES})
endif()

message("-- Finding yaml-cpp - Sucess")


# =====================================================================
# PetIBM
# =====================================================================

message("")
message("-- Finding PetIBM")

message("-- Finding petibm/rigidkinematics/rigidkinematics.h")
find_path(PETIBM_INCLUDE_DIRS
          NAME petibm/rigidkinematics/rigidkinematics.h
          PATHS ${PETIBM_DIR} $ENV{PETIBM_DIR}
          PATH_SUFFIXES "include")

if(${PETIBM_INCLUDE_DIRS} STREQUAL "PETIBM_INCLUDE_DIRS-NOTFOUND")
    message(FATAL_ERROR "Could not find petibm/rigidkinematics/rigidkinematics.h!")
else()
    message("-- Finding petibm/rigidkinematics/rigidkinemtics.h - found in "
            ${PETIBM_INCLUDE_DIRS})
endif()

message("-- Finding PetIBM library")
find_library(PETIBM_LIBRARIES
             NAMES petibm
             PATHS ${PETIBM_DIR} $ENV{PETIBM_DIR}
             PATH_SUFFIXES "lib" "lib64")

if(${PETIBM_LIBRARIES} STREQUAL "PETIBM_LIBRARIES-NOTFOUND")
    message(FATAL_ERROR "Could not find PetIBM library!")
else()
    message("-- Finding PetIBM library - found in "
            ${PETIBM_LIBRARIES})
endif()

message("-- Finding PetIBM Apps library")
find_library(PETIBMAPPS_LIBRARIES
             NAMES petibmapps
             PATHS ${PETIBM_DIR} $ENV{PETIBM_DIR}
             PATH_SUFFIXES "lib" "lib64")

if(${PETIBMAPPS_LIBRARIES} STREQUAL "PETIBMAPPS_LIBRARIES-NOTFOUND")
    message(FATAL_ERROR "Could not find PetIBM Apps library!")
else()
    message("-- Finding PetIBM Apps library - found in "
            ${PETIBMAPPS_LIBRARIES})
endif()

message("-- Finding PetIBM - Sucess")

# =====================================================================
# Targets
# =====================================================================

include_directories("${PROJECT_BINARY_DIR}")

set(SRC ${CMAKE_SOURCE_DIR}/src)
file(GLOB SOURCES "${SRC}/*.cpp")

add_executable(petibm-rollingpitching ${SOURCES})

target_include_directories(petibm-rollingpitching
    PRIVATE ${PETIBM_INCLUDE_DIRS}
    PRIVATE ${PETSC_INCLUDES}
    PRIVATE ${YAMLCPP_INCLUDE_DIRS}
    PUBLIC ${SRC})

target_link_libraries(petibm-rollingpitching
    PRIVATE ${PETIBMAPPS_LIBRARIES}
    PRIVATE ${PETIBM_LIBRARIES}
    PRIVATE ${PETSC_LIBRARIES}
    PRIVATE ${YAMLCPP_LIBRARIES})

install(TARGETS petibm-rollingpitching DESTINATION ${CMAKE_INSTALL_BINDIR})

# =====================================================================
# Print information
# =====================================================================

message("")
message("====================================")
message("Config Information:")
message("====================================")
message("")

message("Build type: " ${CMAKE_BUILD_TYPE})
message("Installation path: " ${CMAKE_INSTALL_PREFIX})
message("")

message("Compilers:")
message("\tCXX compiler: " ${CMAKE_CXX_COMPILER})
message("")

message("Flags:")
message("\tCXX: " ${CMAKE_CXX_FLAGS_${CMAKE_BUILD_TYPE}})
message("")

message("PETSc:")
message("\tPETSc dir: " ${PETSC_DIR})
message("\tHeader path: " ${PETSC_INCLUDES})
message("\tLibraries: " ${PETSC_LIBRARIES})
message("")

message("yaml-cpp:")
message("\tyaml-cpp dir: " ${YAMLCPP_DIR})
message("\tHeader path: " ${YAMLCPP_INCLUDE_DIRS})
message("\tLibraries: " ${YAMLCPP_LIBRARIES})
message("")

message("PetIBM:")
message("\tPetIBM dir: " ${PETIBM_DIR})
message("\tHeader path: " ${PETIBM_INCLUDE_DIRS})
message("\tLibraries: " ${PETIBM_LIBRARIES} ${PETIBMAPPS_LIBRARIES})
message("")