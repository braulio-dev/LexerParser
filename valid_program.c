int main() {
    int x, y;
    x = 5;
    y = 10;
    if (y > x) {
        while (x < 20) {
            x = x + 1;
        }
    }
    if (x < y) {
        printf("%d", x);
    }
    while (x < 20) {
        x = x + 1;
    }
} 