#include "key.h"
#include "crypter.h"

using namespace std;

int GetDigitValue (char digit)
{
     int asciiOffset, digitValue;
     if (digit >= 48 && digit <= 57)
     {
		// code for '0' through '9'
		asciiOffset = 48;
		digitValue = digit - asciiOffset;
		return digitValue;
     }
     else if (digit >= 65 && digit <= 70)
     {
		// digit is 'A' through 'F'
		asciiOffset = 55;
		digitValue = digit - asciiOffset;
		return digitValue;
     }
     else if (digit >= 97 && digit <= 102)
     {
		// code for 'a' through 'f'
		asciiOffset = 87;
		digitValue = digit - asciiOffset;
		return digitValue;
     }
     else
     {
           // illegal digit
     	return -1;
     }
}
vector<unsigned char> Convert (SecureString hexNumber)
// assumes 2 character string with legal hex digits
{
     vector<unsigned char> chars;
     int size = hexNumber.length();
     for (int i = 0; i < size; i+=2)
     {
	     char highOrderDig = hexNumber[i];
	     char lowOrderDig  = hexNumber[i+1];
	     int lowOrderValue = GetDigitValue(lowOrderDig);//;  convert lowOrderDig to number from 0 to 15
	     int highOrderValue = GetDigitValue(highOrderDig);//; convert highOrderDig to number from 0 to 15
	     chars.push_back(lowOrderValue + 16 * highOrderValue);
 	}
     return chars;
}
inline double Factorial(int x) {
  return (x == 1 ? x : x * Factorial(x - 1));
}
int main(int argc, char* argv[])
{
	CCrypter crypter;
	CKeyingMaterial vMasterKey;

	// Use the crypto from the locked wallet
    const unsigned int nDeriveIterations = 90367;
    const vector<unsigned char> chSalt = Convert("693f87a08e771ef0");
    const vector<unsigned char> vchCryptedKey = Convert("153eabea2afe4fa960c4d0cc05eb8b233f7f00bc4dc55bebf129f40cdcc3bec3451d572c0851fa5327d08d532f48bbd5");
    const vector<unsigned char> vchPubKey = Convert("04ffa71a0b3024136808c2e131a640e30b9c78812699e4cfa3b38a846207dcded9eade2549378c861e38343873ef9a94c6b54660c8aa0bd20146add7a0df7b4543");
    const vector<unsigned char> vchCryptedSecret = Convert("6c88d9b67f5b3b0cb7390da96b1eeb04e520e3add8c8370959d045f5bb185a39fbea6fddd4f67a665c599e7620d4b9ce");



    // Try any password as input
	SecureString attempt;
    std::getline(std::cin, attempt);

    do{
    	const SecureString strWalletPassphrase = attempt;
    	std::cout << strWalletPassphrase <<"\n";
    	if(!crypter.SetKeyFromPassphrase(strWalletPassphrase, chSalt, nDeriveIterations, 0))
    	{
    		// cout << i << " " << strWalletPassphrase <<"\n";
            continue;
        }
        if (!crypter.Decrypt(vchCryptedKey, vMasterKey))
        {
        	// cout << i << " " << strWalletPassphrase <<"\n";
    		continue;
    	}

        CSecret vchSecret;
        if(!DecryptSecret(vMasterKey, vchCryptedSecret, Hash(vchPubKey.begin(), vchPubKey.end()), vchSecret))
        {
        	// cout << "** didn't decrypt **" <<"\n";
            continue;
        }
        if (vchSecret.size() != 32)
        {
        	// cout << "** wrong size secret **" <<"\n";
            continue;
        }
        CKey key;
        key.SetPubKey(vchPubKey);
        key.SetSecret(vchSecret);
        if (key.GetPubKey() == vchPubKey)
        {
            cout<<"Found it: "<<strWalletPassphrase<<"\n";
            return 0;
        }

    }while(std::getline(std::cin, attempt));

    return 0;
}
