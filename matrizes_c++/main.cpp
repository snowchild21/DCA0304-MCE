#include <iostream>
#include "matriz_utils.hpp"

int main() {
    int variaveis;

    auto A_matriz = alocarMatriz(variaveis);
    auto b_vetor = alocarVetor(variaveis);

    std::cout << "\nSistema Ax = b:\n\n";
    for (int i = 0; i < variaveis; i++) {
        std::cout << "| ";
        for (int j = 0; j < variaveis; j++) {
            std::cout << A_matriz[i * variaveis + j] << "\t";
        }
        std::cout << "|   ";

        std::cout << "| x" << (i+1) << " |   =   ";

        std::cout << "| " << b_vetor[i] << " |\n";
    }

    return 0;
}
