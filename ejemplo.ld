program ejemplo;
var A, B, C : int;

void suma() [
    var x : string;
        z : float;
        A : int;
    {
        x = "respuesta: ";
        z = 4.5;
        # print("#");
        if (z != 0){
            print(x , z );
        } else {
            print(x, "no valida");
        };
    }
];

main {
    A = 5;
    B = 2;
    C = 10;
    suma();
    do {
        suma();
        B = B + 1;
    } while (B <= C );
    A = 1;
}
end