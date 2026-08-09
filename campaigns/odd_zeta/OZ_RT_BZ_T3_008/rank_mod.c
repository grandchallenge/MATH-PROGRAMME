#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define P 1000003u

static uint32_t modpow(uint32_t a, uint32_t e) {
    uint64_t r = 1, b = a;
    while (e) {
        if (e & 1u) r = (r * b) % P;
        b = (b * b) % P;
        e >>= 1u;
    }
    return (uint32_t)r;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: rank_mod MATRIX.bin\n");
        return 2;
    }
    FILE *f = fopen(argv[1], "rb");
    if (!f) {
        perror("fopen");
        return 2;
    }
    uint32_t nr = 0, nc = 0;
    if (fread(&nr, sizeof(uint32_t), 1, f) != 1 ||
        fread(&nc, sizeof(uint32_t), 1, f) != 1) {
        fclose(f);
        return 2;
    }
    size_t total = (size_t)nr * (size_t)nc;
    uint32_t *data = (uint32_t *)malloc(total * sizeof(uint32_t));
    uint32_t **rows = (uint32_t **)malloc((size_t)nr * sizeof(uint32_t *));
    if (!data || !rows) {
        fclose(f);
        free(data);
        free(rows);
        return 2;
    }
    if (fread(data, sizeof(uint32_t), total, f) != total) {
        fclose(f);
        free(data);
        free(rows);
        return 2;
    }
    fclose(f);
    for (uint32_t i = 0; i < nr; ++i) rows[i] = data + (size_t)i * nc;

    uint32_t rank = 0;
    for (uint32_t c = 0; c < nc && rank < nr; ++c) {
        uint32_t pivot = rank;
        while (pivot < nr && rows[pivot][c] == 0u) ++pivot;
        if (pivot == nr) continue;
        uint32_t *tmp = rows[rank]; rows[rank] = rows[pivot]; rows[pivot] = tmp;
        uint32_t inv = modpow(rows[rank][c], P - 2u);
        for (uint32_t j = c; j < nc; ++j)
            rows[rank][j] = (uint32_t)(((uint64_t)rows[rank][j] * inv) % P);
        uint32_t *pr = rows[rank];
        for (uint32_t i = rank + 1u; i < nr; ++i) {
            uint32_t factor = rows[i][c];
            if (!factor) continue;
            uint32_t *rr = rows[i];
            rr[c] = 0u;
            for (uint32_t j = c + 1u; j < nc; ++j) {
                uint32_t sub = (uint32_t)(((uint64_t)factor * pr[j]) % P);
                rr[j] = rr[j] >= sub ? rr[j] - sub : rr[j] + P - sub;
            }
        }
        ++rank;
    }
    printf("%u\n", rank);
    free(rows);
    free(data);
    return 0;
}
