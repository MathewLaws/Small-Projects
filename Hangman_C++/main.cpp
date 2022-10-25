#include <iostream>
#include <stdlib.h>
#include <ctime>
#include <fstream>
#include <string>
#include <vector>

int main() {
    std::string word_list[99];
    int tries = 7;
    char guess;
    std::vector <char> usedLetters;
    srand (time(NULL));
    std::ifstream words;
    words.open("Words.txt");

    for (int i = 0; i < 99; i++) {
        words >> word_list[i];
    }

    words.close();

    std::string word = word_list[rand()%(sizeof(word_list)/sizeof(*word_list))];

    std::string mask (word.length(), '*');

    while (tries >= 0) {
        if (mask == word) {
            std::cout << "\nYou win!" << std::endl;
            std::cout << "The word was " << word << std::endl;
            return 0;
        }
        bool correct = false;
        std::cout << "\nWord: " << mask << std::endl;
        std::cout << "Tries: " << tries << std::endl;
        std::cout << "Used letters: ";

        for (int i=0; i < usedLetters.size(); i++) {
            std::cout << usedLetters[i] << " ";
        }

        std::cout << "\nGuess: ";
        std::cin >> guess;


        for (int i=0; i < mask.length(); i++) {
            if (word[i] == guess) {
                mask[i] = guess;
                correct = true;
            }
        }
        if (correct != true) {
            tries -= 1;
        }
        usedLetters.push_back(guess);
    }

    std::cout << "\nYou lose!" << std::endl;
    std::cout << "The word was " << word << std::endl;

    return 0;
}
