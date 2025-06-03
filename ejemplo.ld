program ejemplo;
var A, B, C : int;

void suma(z : float, y : int) [
    var resultado : int;
    {
        resultado = z + y;
        print("resultado: ", resultado);
    }
];

main {
    A = 10;
    B = 20;
    C = 10;
    if (C != B){
        suma(A, B);
        A = 4;
    } else {
        print("Hola mundo");
        B = A / C;
    };
    do {
        print(D + E + 9);
        F = F + 1;
        print(F);
    } while (F < G );
}
end