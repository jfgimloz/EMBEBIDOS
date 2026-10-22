cmake_minimum_required(VERSION 3.16)
project(odometro_cursor C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
add_compile_options(-Wall -Wextra -Wpedantic)

find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
  pkg_check_modules(XDO QUIET IMPORTED_TARGET xdo)
  pkg_check_modules(GTK3 QUIET IMPORTED_TARGET gtk+-3.0)
endif()
if(NOT XDO_FOUND)
  find_path(XDO_INCLUDE_DIR NAMES xdo.h)
  find_library(XDO_LIBRARY NAMES xdo)
endif()

add_library(odometro_core STATIC
  src/odometro.c
  src/odometro_estado.c)
target_include_directories(odometro_core PUBLIC include)
# libm se usa solo en el cálculo interno del núcleo.
target_link_libraries(odometro_core PRIVATE m)

option(FUENTE_COMPARTIDA "Construir la adquisición como biblioteca compartida" ON)
if(FUENTE_COMPARTIDA)
  set(TIPO_FUENTE SHARED)
else()
  set(TIPO_FUENTE STATIC)
endif()
add_library(fuente_posicion ${TIPO_FUENTE}
  src/fuente_posicion.c
  src/fuente_csv.c
  src/fuente_xdo.c)
target_include_directories(fuente_posicion PUBLIC include)
if(XDO_FOUND OR (XDO_INCLUDE_DIR AND XDO_LIBRARY))
  target_compile_definitions(fuente_posicion PRIVATE HAVE_XDO)
  if(XDO_FOUND)
    target_link_libraries(fuente_posicion PRIVATE PkgConfig::XDO)
  else()
    target_include_directories(fuente_posicion PRIVATE "${XDO_INCLUDE_DIR}")
    target_link_libraries(fuente_posicion PRIVATE "${XDO_LIBRARY}")
  endif()
endif()

add_executable(odometro_cli src/odometro_cli.c)
target_link_libraries(odometro_cli PRIVATE odometro_core fuente_posicion)

if(GTK3_FOUND AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/odometro_gtk.c")
  add_executable(odometro_gtk src/odometro_gtk.c)
  target_link_libraries(odometro_gtk PRIVATE odometro_core fuente_posicion PkgConfig::GTK3)
endif()

include(CTest)
if(BUILD_TESTING)
  add_executable(test_odometro ../pruebas/test_odometro.c)
  target_link_libraries(test_odometro PRIVATE odometro_core)
  add_test(NAME nucleo_odometro COMMAND test_odometro)
  add_test(NAME trayectoria_reproducible
    COMMAND odometro_cli --csv ${CMAKE_CURRENT_SOURCE_DIR}/../datos/trayectoria_10.csv
                         --intervalo-ms 0 --silencioso)
  set_tests_properties(trayectoria_reproducible PROPERTIES
    PASS_REGULAR_EXPRESSION "muestras=3 distancia=10.000")
endif()

if(BUILD_TESTING)
  find_package(Python3 COMPONENTS Interpreter)
  if(Python3_FOUND AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../pruebas/test_archivos.py")
    add_test(NAME archivos
      COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/../pruebas/test_archivos.py
              $<TARGET_FILE:odometro_cli>)
  endif()
  option(PROBAR_GTK "Probar callbacks después de completar S6-A2" OFF)
  if(PROBAR_GTK AND GTK3_FOUND AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../pruebas/test_gtk.c")
    add_executable(test_gtk ../pruebas/test_gtk.c)
    target_link_libraries(test_gtk PRIVATE odometro_core fuente_posicion PkgConfig::GTK3)
    add_test(NAME callbacks_gtk
      COMMAND test_gtk ${CMAKE_CURRENT_SOURCE_DIR}/../datos/trayectoria_10.csv)
    set_tests_properties(callbacks_gtk PROPERTIES SKIP_RETURN_CODE 77
      ENVIRONMENT "G_DEBUG=fatal-warnings")
  endif()
endif()
