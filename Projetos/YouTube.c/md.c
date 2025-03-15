#include<stdio.h>

int main() {
    float p1, p1m, p2, p2m, media;
    char forum;

    printf("Qual foi sua nota da P1? \n");
    scanf("%f", &p1);
    p1m = p1 * 0.3;

    printf("Qual foi sua nota da P2? \n");
    scanf("%f", &p2);
    p2m = p2 * 0.7;

    printf("Fez o forum avaliativo? (S) sim ou (N) não: ");
    scanf(" %c", &forum);

    if (forum == 'S' || forum == 's') {
        media = p1m + p2m + 1;
    } else {
        media = p1m + p2m;
    }

    printf("Sua media total e: %.2f\n", media);

    return 0;
}

