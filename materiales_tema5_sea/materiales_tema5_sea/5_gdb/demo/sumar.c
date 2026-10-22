#include <stdio.h>
int sumar(int a, int b)
{
    int resultado = a + b;
    return resultado;
}
int main(void)
{
    printf("resultado=%d\n", sumar(2, 3));
    return 0;
}
