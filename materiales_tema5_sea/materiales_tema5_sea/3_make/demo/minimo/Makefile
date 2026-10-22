CC := gcc
CFLAGS := -std=c11 -Wall -Wextra -Wpedantic

sumar: main.o sumar.o
	$(CC) $^ -o $@

main.o: main.c sumar.h
	$(CC) $(CFLAGS) -c $< -o $@

sumar.o: sumar.c sumar.h
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f main.o sumar.o sumar
