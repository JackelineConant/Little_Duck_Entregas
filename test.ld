program test;

var x, y, i : int;
    z : float;

void prueba (x : int, z : float ) [
    var res : float;
    {
        res = x * z ;
    }
];

main {
    
    do {
        prueba (x, z);
        i = i + 1;
        if (i == 11) {
            print('termino');
        }
        else {
            print('no termino');
        };
    } while (i <= 10);  
}
end