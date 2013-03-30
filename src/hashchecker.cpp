//#include <fstream>
// #include <iostream>
// #include <string>
#include "crypter.h"
using namespace std;

int main(int argc, char* argv[])
{
	cout<<"Hello, World!\n";
	CCrypter crypter;
	const unsigned int nDeriveIterations = 90367;
	string str = "0x153eabea2afe4fa960c4d0cc05eb8b233f7f00bc4dc55bebf129f40cdcc3bec3451d572c0851fa5327d08d532f48bbd5";
	const vector<unsigned char> chSalt (str.begin(), str.end());
	 SecureString attempt= "animal";
	for (int i = 0; i < 100; i++)
	{
		const SecureString strWalletPassphrase = attempt;
		if(!crypter.SetKeyFromPassphrase(strWalletPassphrase, chSalt, nDeriveIterations, 0))
	        cout<<"Nope\n";
	    else
	    {
	    	// Congratulations!!
	    	cout<<"Got it: "<<strWalletPassphrase"\n";
	    	return 0;
	    }
	}
	return 0;
}
