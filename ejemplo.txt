program ejemplo;
var A, B, C,D,E,F,G : int;

void suma(z : float) [
    {
        z = 4;
        if (z != 0){
            z = z + 1;
            A = 4;
        };
    }
];

void compara(z : float, a : int, y : int ) [
    var  b : float;
    {
        b = 3.5;
        a = 2.5;
        resultado = a * b;
        print("bien");
    }
];

void nose() [
    var x, y, resultado : int;
    {
        x = 3;
        y = 7;
        resultado = x + y;
        print("Resultado de suma: ", resultado);
    }
];

main {
    A = 10;
    B = 20;
    C = A + B;
    print("Valor de C: ", C);
    if (C != B){
        suma(z);
        A = 4;
    } else {
        A = 2;
        print("Hola mundo");
        A = 3;
        A = 4;
    };
    nose();
    compara(B, A, C);
    print("hola");
    A = 0;
    D = 3;
    E = 4;
    F = 3;
    G = 4;
    do {
        print(D + E + 9);
        F = F + 1;
    } while (F < G );
}
end