cmake_minimum_required(VERSION 3.16)
project(demo_odometro C)

# La descripción real de las bibliotecas y los ejecutables está en comun/.
include(CTest)
add_subdirectory(../../../comun ${CMAKE_BINARY_DIR}/componentes)
