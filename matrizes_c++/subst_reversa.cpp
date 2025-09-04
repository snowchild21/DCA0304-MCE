#include "subst_reversa.hpp"


inline double Aij(const std::vector<double>& A, int n, int i, int j) {
    return A[i * n + j];
}

std::vector<double> substituicaoReversa(const std::vector<double>& A, const std::vector<double>& b, int n) {
    std::vector<double> x(n, 0.0);

    
    for (int i = n - 1; i >= 0; i--) {
        double soma = 0.0;

        for (int j = i + 1; j < n; j++) {
            soma += Aij(A, n, i, j) * x[j];
        }

        if (Aij(A, n, i, i) == 0) {
            std::cerr << "Erro: pivo nulo em A[" << i << "][" << i << "]!\n";
            exit(1);
        }

        x[i] = (b[i] - soma) / Aij(A, n, i, i);
    }

    return x;
}