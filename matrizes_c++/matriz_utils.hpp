#ifndef MATRIZ_UTILS_HPP
#define MATRIZ_UTILS_HPP

#include <iostream>
#include <vector>

// Funções de alocação
std::vector<double> alocarMatriz(int &variaveis);
std::vector<double> alocarVetor(int &variaveis);

// Função auxiliar para acessar matriz A como se fosse 2D
inline double& A(std::vector<double>& matriz, int n, int i, int j) {
    return matriz[i * n + j]; // matriz[i][j]
}

#endif
