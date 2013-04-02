#include <algorithm>
#include <string>
#include <iostream>

int main(int argc, char** argv)
{
    std::string s(argv[1]);
    std::sort(s.begin(), s.end()); // it's actually important to sort first
    do {
        std::cout << s << '\n';
    } while(std::next_permutation(s.begin(), s.end()));
}
// void swap(std::string &s, int i, int j)
// {
//   char temp = s[i];
//   s[i] = s[j];
//   s[j] = temp;
// }
// // This is an algorithm as described by the answer to http://stackoverflow.com/questions/1995328/are-there-any-better-methods-to-do-permutation-of-string
// // useful in unusual circumstances
// void permutation(int k, std::string &s)
// {
//     for(unsigned int j = 1; j < s.size(); ++j)
//     {
//         swap(s, k % (j + 1), j);
//         k = k / (j + 1);
//     }
// }

