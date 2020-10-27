# Compute checksum for Coronalert test code mod 97
# following the calculation in the appendix of
#    Coronalert: A Distributed Privacy-Friendly Contact Tracing App for Belgium
#    Version 1.3, 16 August 2020
#    https://www.esat.kuleuven.be/cosic/sites/corona-app/wp-content/uploads/sites/8/2020/09/02_Belgium_app_description_full_aug16_v1_3.pdf
# Author: Christiane Peters,
# Contact me via http://cbcrypto.org/
# this code is hosted at https://github.com/christianepeters
# Date: 27-Oct-2020
import sys

def digits(num):
   count = 0
   while  num > 0:
      count += 1
      num //= 10
   return count

# single-precision with all terms less than 10^9 (which is less than 32 bits)
def check_digits_sp(_t0,_R1):
   if(digits(_t0)!=6 or digits(_R1)!=15):
        return("error")
   else:
        c1=_t0//10      # leading 5 digits of _t0
        c1%=97
        #print(c1)
        c2=_R1//(10**7)
        c2+=(_t0%10)*(10**8)
        c2%=97
        #print(c2)
        c3=_R1%(10**7)*100
        c3%=97
        #print(c3)
        c=(89*c1+34*c2+c3)%97
        #print(c)
        return c

def checksum(_x):
   if(digits(_x)!=23):
        return("error")
   else:
     print("compute checksum mod 97  of",x)
     c1=_x//(10**18)
     #print(c1)
     c2=(_x-(c1*10**18))//(10**9)
     #print(c2)
     c3=_x-(c1*10**18)-(c2*10**9)
     #print(c3)
     c1%=97
     #print(c1)
     c1=(c1*89)%97
     c2%=97
     #print(c2)
     c2=(c2*34)%97
     c3%=97
     #print(c3)
     c=(c1+c2+c3)%97
     return c

t0 = 200813                 # 6 digits
R1 = 123456789012345        # 15 digits
print("### example test code ###")
print(t0)
print(R1)
x=(t0*(10**digits(R1))+R1)*100+(97-check_digits_sp(t0,R1))
print(checksum(x))

# another test with test code from the app
print("### test code generated in the app ###")
t0=201012 # date of infectiousness
code=44559257531208704 # Code: 4455-9257-5312-0870-4
x=t0*(10**17)+code
print(checksum(x))