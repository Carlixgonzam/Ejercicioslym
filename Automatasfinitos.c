#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

// esta es la estructura para representar un autómata finito determinista (DFA)
typedef struct {
    int numStates;       // número total de estados
    int numSymbols;      // tamaño del alfabeto
    char *alphabet;      // cadena que contiene los símbolos del alfabeto
    int **transitions;   // tabla de transiciones: transitions[estado][índice del símbolo] = siguiente estado
    int initialState;    // estado inicial
    bool *finalStates;   // arreglo booleano: finalStates[estado] == true si es estado final
} Automata;

// función para crear y definir el autómata leyendo los datos del usuario
Automata* createAutomata() {
    Automata *a = malloc(sizeof(Automata));
    if (!a) {
        fprintf(stderr, "Error: no se pudo asignar memoria para el autómata.\n");
        exit(EXIT_FAILURE);
    }
    
    // número de estados
    printf("Ingrese el número de estados: ");
    scanf("%d", &(a->numStates));
    
    // número de símbolos del alfabeto
    printf("Ingrese el número de símbolos del alfabeto: ");
    scanf("%d", &(a->numSymbols));
    
    // reservar memoria para el alfabeto
    a->alphabet = malloc((a->numSymbols + 1) * sizeof(char)); // +1 para el terminador nulo
    if (!a->alphabet) {
        fprintf(stderr, "Error: no se pudo asignar memoria para el alfabeto.\n");
        exit(EXIT_FAILURE);
    }
    // Se asume que los símbolos se ingresan sin espacios (por ejemplo, "01" o "abc")
    printf("Ingrese los símbolos del alfabeto (sin espacios): ");
    scanf("%s", a->alphabet);
    
    // estado inicial
    printf("Ingrese el estado inicial (0 a %d): ", a->numStates - 1);
    scanf("%d", &(a->initialState));
    
    // estados finales
    a->finalStates = malloc(a->numStates * sizeof(bool));
    if (!a->finalStates) {
        fprintf(stderr, "Error: no se pudo asignar memoria para los estados finales.\n");
        exit(EXIT_FAILURE);
    }
    // inicializar todos los estados a 'no final'
    for (int i = 0; i < a->numStates; i++) {
        a->finalStates[i] = false;
    }
    int numFinal;
    printf("Ingrese el número de estados finales: ");
    scanf("%d", &numFinal);
    printf("Ingrese los estados finales (separados por espacios): ");
    for (int i = 0; i < numFinal; i++) {
        int final;
        scanf("%d", &final);
        if (final < 0 || final >= a->numStates) {
            fprintf(stderr, "Estado final inválido: %d\n", final);
            exit(EXIT_FAILURE);
        }
        a->finalStates[final] = true;
    }
    
    // reservar memoria para la tabla de transiciones
    a->transitions = malloc(a->numStates * sizeof(int *));
    if (!a->transitions) {
        fprintf(stderr, "Error: no se pudo asignar memoria para la tabla de transiciones.\n");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < a->numStates; i++) {
        a->transitions[i] = malloc(a->numSymbols * sizeof(int));
        if (!a->transitions[i]) {
            fprintf(stderr, "Error: no se pudo asignar memoria para la fila %d de la tabla de transiciones.\n", i);
            exit(EXIT_FAILURE);
        }
    }
    
    // lectura de la tabla de transiciones
    printf("Ingrese las transiciones para cada estado y símbolo.\n");
    printf("Para cada estado y símbolo, ingrese el siguiente estado.\n");
    for (int i = 0; i < a->numStates; i++) {
        for (int j = 0; j < a->numSymbols; j++) {
            printf("Estado %d, símbolo '%c': ", i, a->alphabet[j]);
            scanf("%d", &(a->transitions[i][j]));
            if (a->transitions[i][j] < 0 || a->transitions[i][j] >= a->numStates) {
                fprintf(stderr, "Transición inválida para estado %d, símbolo '%c'.\n", i, a->alphabet[j]);
                exit(EXIT_FAILURE);
            }
        }
    }
    
    return a;
}

// función que simula el autómata con una cadena de entrada
// retorna true si la cadena es aceptada, false en caso contrario.
bool simulateAutomata(Automata *a, char *input) {
    int currentState = a->initialState;
    for (int i = 0; i < strlen(input); i++) {
        char symbol = input[i];
        // busca el índice del símbolo en el alfabeto
        int symbolIndex = -1;
        for (int j = 0; j < a->numSymbols; j++) {
            if (a->alphabet[j] == symbol) {
                symbolIndex = j;
                break;
            }
        }
        if (symbolIndex == -1) {
            printf("El símbolo '%c' no pertenece al alfabeto.\n", symbol);
            return false;
        }
        // actualizar el estado según la tabla de transiciones
        currentState = a->transitions[currentState][symbolIndex];
    }
    //  cadena es aceptada si el estado final alcanzado es un estado final
    return a->finalStates[currentState];
}

// libera la memoria asignada al autómata
void freeAutomata(Automata *a) {
    for (int i = 0; i < a->numStates; i++) {
        free(a->transitions[i]);
    }
    free(a->transitions);
    free(a->alphabet);
    free(a->finalStates);
    free(a);
}

int main() {
    printf("Simulador de Autómatas Finitos (DFA)\n");
    printf("-------------------------------------\n");
    
    // Crea el autómata leyendo la definición del usuario
    Automata *a = createAutomata();
    
    char inputString[1000];
    printf("Ingrese una cadena para evaluar (o 'exit' para terminar): ");
    
    // Ciclo interactivo para evaluar cadenas
    while (scanf("%s", inputString) == 1) {
        if (strcmp(inputString, "exit") == 0)
            break;
        if (simulateAutomata(a, inputString))
            printf("La cadena '%s' es ACEPTADA por el autómata.\n", inputString);
        else
            printf("La cadena '%s' es RECHAZADA por el autómata.\n", inputString);
        printf("Ingrese otra cadena (o 'exit' para terminar): ");
    }
    
    // Libera la memoria utilizada
    freeAutomata(a);
    
    return 0;
}