program mayor_valor;

var cantidad , mayor : int;
var valor1, valor2, valor3, valor4, valor5 : int;

main{
    cantidad = 5;

    valor1 = 8;
    valor2 = 7;
    valor3 = 10;
    valor4 = 3;
    valor5 = 6;

    mayor = valor1;

    if (valor2 > mayor) {
        mayor = valor2;
    };
    if (valor3 > mayor) {
        mayor = valor3;
    };
    if (valor4 > mayor) {
        mayor = valor4;
    };
    if (valor5 > mayor) {
        mayor = valor5;
    };

    print(mayor);
}
end
# un patoprograma que imprime el valor más grande de 5 valores
# quak!