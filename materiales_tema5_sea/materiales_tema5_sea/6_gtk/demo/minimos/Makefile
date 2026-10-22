CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic
BUILD_DIR ?= /tmp/sea-demo-gtk
GTK_CFLAGS := $(shell pkg-config --cflags gtk+-3.0)
GTK_LIBS := $(shell pkg-config --libs gtk+-3.0)
PROGRAMAS := 01_ventana 02_boton 03_senal 04_contexto

.PHONY: all
all: $(addprefix $(BUILD_DIR)/,$(PROGRAMAS))

$(BUILD_DIR)/%: %.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(GTK_CFLAGS) $< -o $@ $(GTK_LIBS)
