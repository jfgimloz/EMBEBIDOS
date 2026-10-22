CC := gcc
AR := ar
ROOT := ../..
SRC := $(ROOT)/comun/src
INC := $(ROOT)/comun/include
DATOS := $(ROOT)/datos/trayectoria_10.csv
BUILD := build
CFLAGS := -std=c11 -Wall -Wextra -Wpedantic -O0 -g3
CPPFLAGS := -I$(INC)
CORE_O := $(BUILD)/odometro.o $(BUILD)/odometro_estado.o
FUENTE_O := $(BUILD)/fuente_posicion.o $(BUILD)/fuente_csv.o $(BUILD)/fuente_xdo.o

.PHONY: all test dinamico clean
all: $(BUILD)/odometro_cli

$(BUILD):
	mkdir -p $@

$(BUILD)/odometro.o: $(SRC)/odometro.c $(INC)/odometro.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD)/odometro_estado.o: $(SRC)/odometro_estado.c | $(BUILD) # TODO S5-A3-01: completa la regla del objeto de estado
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD)/fuente_%.o: $(SRC)/fuente_%.c $(INC)/fuente_posicion.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD)/odometro_cli.o: $(SRC)/odometro_cli.c $(INC)/odometro.h $(INC)/fuente_posicion.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD)/libodometro_core.a: $(CORE_O)
	$(AR) rcs $@ $^

$(BUILD)/libfuente_posicion.a: $(FUENTE_O)
	$(AR) rcs $@ $^

$(BUILD)/libfuente_posicion.so: $(FUENTE_O)
	$(CC) -shared $^ -o $@

$(BUILD)/odometro_cli: $(BUILD)/odometro_cli.o $(BUILD)/libodometro_core.a $(BUILD)/libfuente_posicion.a
	# TODO S5-A3-02: completa la receta de enlace de la CLI

$(BUILD)/odometro_cli_dinamico: $(BUILD)/odometro_cli.o $(BUILD)/libodometro_core.a $(BUILD)/libfuente_posicion.so
	# TODO S5-A3-03: completa la receta de enlace de la variante compartida

dinamico: $(BUILD)/odometro_cli_dinamico

test: $(BUILD)/odometro_cli
	$(BUILD)/odometro_cli --csv $(DATOS) --intervalo-ms 0 --silencioso

clean:
	rm -rf $(BUILD)
