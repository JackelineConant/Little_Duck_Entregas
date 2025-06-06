program ejemplo;
var A, B, C : int;
    j , i : float;
    s : string;

void suma() [
    var x : string;
        z : float;
        A : int;
    {
        x = "respuesta: ";
        z = 4.5;
        if (z <= 0){
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
    i = 2.6;
    j = A * B / 2;
    s = "hola mundo";
    if(C != B){
        suma();
    };
    B = 2;
    print(s, j);
    A = 1;
}
end