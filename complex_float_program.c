int main() {
    float pi, radius, area;
    int diameter;
    pi = 3.14159;
    radius = 5.5;
    diameter = 11;
    area = pi * radius * radius;
    if (area > 50.0) {
        while (radius < 10.0) {
            radius = radius + 0.5;
            area = pi * radius * radius;
        }
    }
    if (diameter > 10) {
        printf("%f", area);
    }
    while (radius > 1.0) {
        radius = radius - 0.1;
    }
}
