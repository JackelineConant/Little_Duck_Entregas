program serie_fibonnacci;

var i, cantidad, resultado, anterior, temp : int;

main {
    i = 1;
    cantidad = 10;
    anterior = 0;
    resultado = 1;
    
    do {
        print(resultado);
        temp = resultado;
        resultado = resultado + anterior;
        anterior = temp;
        i = i + 1;
    } while (i <= cantidad);
}
end
# un patoprograma que imprime la serie de fibonnacci segun la cantidad de digitos que se quieren conocer de la serie de fibonnacci
