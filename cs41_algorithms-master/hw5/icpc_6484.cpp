#include <iostream> 
#include <fstream>
#include <stdio.h>
#include <string.h>
using namespace std;

int main () {
  string str;
  //string eof = "0";
  char seq[1000]; // sequence
  int sats[1000]; // satellites 
  int k;

    while(cin >> str) {
      // check for eof
      if (str.compare("0") == 0) {
        break;
      }

      k = 0; // reset variables per test case 
      memset(seq, 0, 1000);
      memset(sats, 0, 1000);

      // convert from input string to char array
      for (int i = 0; i < str.size(); i++) {
        seq[i] = str[i];
      }

      // count satellites
      for (int i = 1; i < str.size(); i++) { // ignore ping at time 0
        if (seq[i] == '1') {
          sats[k] = i;
          k++;
          for (int j = i + 1; j < str.size(); j++) {
            if (j % i == 0) {
              if (seq[j] == '1') {
                seq[j] = '0';
              } else {
                seq[j] = '1';
              }
            }
          }
        }
      }

      // output bells
      for (int i = 0; i < k - 1; i++) {
        cout << sats[i] << " ";
      }
      cout << sats[k - 1] << endl;
    }

  return 0;
}
