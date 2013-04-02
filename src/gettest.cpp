#include<string>
#include<iostream>
#include<algorithm>

int main (int argc, char** argv)
{
   std::string str;
   do
   {

      std::cout<<"test: "<<str<<std::endl;

   }while(std::getline(std::cin, str));
}
