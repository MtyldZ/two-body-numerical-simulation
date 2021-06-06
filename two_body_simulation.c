#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define N
typedef struct TwoBodyController {
    int T;
    double dt;
    long double *du;
    long double u[4];
    double mass_ratio;
    double mass1;
    double mass2;
    double mass2_1;
    double eccentricity;
    char method[11];
    long double position[2][2];

    void (*takeUserInput)(struct TwoBodyController *planetry);

    void (*updatePosition)(struct TwoBodyController *planetry);

} TBC;

void take_user_input(TBC *planetry);

long double *take_derivative(TBC *planetry);

void rk4(TBC *planetry);

void euler(TBC *planetry);

void calculate_position(TBC *planetry);

void update_position(TBC *planetry);

int main() {
    FILE *file = fopen("simulation.txt", "w");
    TBC *pla = malloc(4 * sizeof(TBC));
    pla->takeUserInput = take_user_input;
    pla->updatePosition = update_position;

    pla->takeUserInput(pla);

    double left_time = pla->T;

    // first line
    fprintf(file, "T=%d__&__dt=%lf__&__q=%lf__&__eccentricity=%lf__&__method=%s__&__m1=%lf__&__m2=%lf\n",
            pla->T, pla->dt, pla->mass_ratio, pla->eccentricity, pla->method, pla->mass1, pla->mass2);

    while (left_time > 0) {
        pla->updatePosition(pla);

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                fprintf(file, "%.6Lf", pla->position[i][j]);
                if (i != 1 || j != 1) {
                    fprintf(file, "__&__");
                }
            }
        }
        fprintf(file, "\n");

        left_time = left_time - pla->dt;
    }
    printf("Done!");
    free(pla->du);
    fclose(file);
    return 0;
}

void take_user_input(TBC *planetry) {
    printf("T (e.g. 120): ");
    scanf("%d", &planetry->T);
    printf("δt (e.g. 0.01): ");
    scanf("%lf", &planetry->dt);
    printf("mass ratio (e.g. 0.5): ");
    scanf("%lf", &planetry->mass_ratio);
    printf("eccentricity (e.g. 0.7): ");
    scanf("%lf", &planetry->eccentricity);
    printf("method (e.g. runge-kutta/euler): ");
    scanf("%s", planetry->method);

    //    Stable orbit reset
    planetry->u[0] = 1.0;
    planetry->u[1] = 0.0;
    planetry->u[2] = 0.0;
    planetry->u[3] = sqrt((planetry->mass_ratio + 1) * (planetry->eccentricity + 1));

    //    Update masses
    planetry->mass1 = 1.0;
    planetry->mass2 = planetry->mass_ratio;
    planetry->mass2_1 = 1 + planetry->mass_ratio;
}

void update_position(TBC *planetry) {
    if (strcmp(planetry->method, "runge-kutta") == 0) {
        rk4(planetry);
    } else if (strcmp(planetry->method, "euler") == 0) {
        euler(planetry);
    }
    calculate_position(planetry);
}

void rk4(TBC *planetry) {
    long double *du;
    du = (long double *) malloc(4 * sizeof(long double));
    double a[] = {(planetry->dt) / 2, (planetry->dt) / 2, planetry->dt, 0};
    double b[] = {(planetry->dt) / 6, (planetry->dt) / 3, (planetry->dt) / 3, (planetry->dt) / 6};
    long double u0[4];
    long double ut[4] = {0.0, 0.0, 0.0, 0.0};

    for (int i = 0; i < 4; i++) {
        u0[i] = planetry->u[i];
    }
    for (int j = 0; j < 4; j++) {
        du = take_derivative(planetry);

        for (int i = 0; i < 4; i++) {
            planetry->u[i] = u0[i] + a[j] * du[i];
            ut[i] = ut[i] + b[j] * du[i];
        }
    }
    for (int i = 0; i < 4; i++) {
        planetry->u[i] = u0[i] + ut[i];
    }
}

void euler(TBC *planetry) {
    long double *du;
    du = (long double *) malloc(4 * sizeof(long double));
    du = take_derivative(planetry);
    for (int i = 0; i < 4; i++) {
        planetry->u[i] = planetry->u[i] + du[i] * planetry->dt;
    }
}

long double *take_derivative(TBC *planetry) {
    //double *derivative_u;
    long double *du2;
    long double distance;
    long double r[2];
    du2 = (long double *) malloc(4 * sizeof(long double));
    r[0] = planetry->u[0];
    r[1] = planetry->u[1];
    distance = sqrt(pow(r[0], 2) + pow(r[1], 2));
    for (int i = 0; i < 2; i++) {
        du2[i] = planetry->u[i + 2];
        du2[i + 2] = -(1 + planetry->mass_ratio) * r[i] / (pow(distance, 3));
    }
    return du2;
}

void calculate_position(TBC *planetry) {
    double r = 1;
    long double a1 = (planetry->mass2) / (planetry->mass2_1) * r;
    long double a2 = (planetry->mass1) / (planetry->mass2_1) * r;
    planetry->position[0][0] = -a2 * planetry->u[0];
    planetry->position[0][1] = -a2 * planetry->u[1];
    planetry->position[1][0] = -a1 * planetry->u[0];
    planetry->position[1][1] = -a1 * planetry->u[1];
}

