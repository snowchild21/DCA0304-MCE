#include "matriz_utils.hpp"

std::vector<double> alocarMatriz(int &variaveis) {
    std::cout << "Digite a quantidade de variaveis do sistema: ";
    while (!(std::cin >> variaveis) || variaveis <= 0 || variaveis % 1 != 0) {
        std::cout << "Por favor, digite um numero inteiro positivo maior que 0: ";
        std::cin.clear();
        std::cin.ignore(1000, '\n');
    }

    std::vector<double> matriz(variaveis * variaveis, 0.0);

    std::cout << "Agora digite os valores da matriz A (" << variaveis << "x" << variaveis << "):\n";
    for (int i = 0; i < variaveis; i++) {
        for (int j = 0; j < variaveis; j++) {
            std::cout << "A[" << i << "][" << j << "] = ";
            while (!(std::cin >> matriz[i * variaveis + j])) {
                std::cout << "Digite um numero valido: ";
                std::cin.clear();
                std::cin.ignore(1000, '\n');
            }
        }
    }
    return matriz;
}

std::vector<double> alocarVetor(int &variaveis) {
    std::vector<double> vetor(variaveis, 0.0);

    std::cout << "Agora digite os elementos do vetor b (" << variaveis << " elementos):\n";
    for (int i = 0; i < variaveis; i++) {
        std::cout << "b[" << i << "] = ";
        while (!(std::cin >> vetor[i])) {
            std::cout << "Digite um numero valido: ";
            std::cin.clear();
            std::cin.ignore(1000, '\n');
        }
    }
    return vetor;
}
