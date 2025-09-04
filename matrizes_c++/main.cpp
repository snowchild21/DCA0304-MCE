#include <iostream>
#include <algorithm>
#include <cctype>
#include <string>
#include "matriz_utils.hpp"
#include "subst_reversa.hpp"
#include "subst_direta.hpp"


int main() {
    int variaveis;
    std::string metodo;
    bool triangularSuperior = true;
    bool triangularInferior = true;

    auto A_matriz = alocarMatriz(variaveis);
    auto b_vetor = alocarVetor(variaveis);

    
    std::cout << "\nSistema Ax = b:\n\n";
    for (int i = 0; i < variaveis; i++) {
        std::cout << "| ";
        for (int j = 0; j < variaveis; j++) {
            std::cout << A_matriz[i * variaveis + j] << "\t";
        }
        std::cout << "|   | x" << (i+1) << " |   =   | " << b_vetor[i] << " |\n";
    }

    std::cout << "\n==Selecione o metodo de resolucao (reversa/direta)==: " << std::endl;

    std::vector<double> solucao;

    while (true) {
        std::cin >> metodo;

        
        std::transform(metodo.begin(), metodo.end(), metodo.begin(),
                       [](unsigned char c){ return std::tolower(c); });

        if (metodo == "reversa") {
            for (int i = 1; i < variaveis; i++){
                for (int j = 0; j < i; j++){
                    if (A(A_matriz, variaveis, i, j) != 0){
                        std::cout<<"A matriz A nao e triangular superior";
                        triangularSuperior = false;
                        break;
                    }
                }
            }
            if (!triangularSuperior){
                break;
                exit(1);
            }
            solucao = substituicaoReversa(A_matriz, b_vetor, variaveis);
            break;
            
        } else if (metodo == "direta"){
            for (int i = 0; i < variaveis; i++){
                for (int j = i + 1; j < variaveis; j++){
                    if (A(A_matriz, variaveis, i, j) != 0){
                        std::cout<<"A matriz A nao e triangular inferior";
                        triangularInferior = false;
                        break;
                    }
                }
            }
            if(!triangularInferior){
                exit(1);
            }
            solucao = substituicaoDireta(A_matriz, b_vetor, variaveis);
            break;
        }else{
            std::cout << "==Digite exatamente um dos metodos listados acima==\n";
        }
    }

    
    std::cout << "\nSolucao:\n";
    for (int i = 0; i < variaveis; i++) {
        std::cout << "x" << (i+1) << " = " << solucao[i] << "\n";
    }

    return 0;
}
