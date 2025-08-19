int main() {
    float x, y;
    int z;
    x = 3.14;
    y = 2.5;
    z = 10;
    if (y > 2.0) {
        while (x < 5.0) {
            x = x + 0.5;
        }
    }
    if (x < y) {
        printf("%f", x);
    }
    while (z < 20) {
        z = z + 1;
    }
}
