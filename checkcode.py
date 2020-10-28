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
import random

# get number of digits
def digits(num):
   count = 0
   while  num > 0:
      count += 1
      num //= 10
   return count

# return 10^digits(_x) mod 97
def mod97(_x):
   d=digits(_x)-1
   mod=10
   while d>0:
       mod=(mod*10)%97
       d-=1
   return mod

#print(mod97(1))
# returns 10^1 mod 97 =10
#print(mod97(25))
# returns 10^2 mod 97=3
#print(mod97((10**9)-1))
# returns 10^9 mod 97 = 34

# compute 2 check digits
def check_digits(_t0,_R1):
   dt=digits(_t0)
   if(dt!=6):
      return 0;
   c1=_t0//10      # leading 5 digits of _t0
   #print("c1=",c1)
   c1%=97
   c2=_R1//(10**7)
   c2+=(_t0%10)*(10**8)
   #print("c2=",c2)
   m=mod97(c2)   # compute 10^digits(c2) mod 97, split over the resp 9-digit chunks
   c2%=97
   c3=_R1%(10**7)*100
   c3%=97
   # 10^18 %97=89
   # m=10^x % 97 where x=digits(c2)
   c=(89*c1+m*c2+c3)%97
   return c

# check if _x equals 0 mod 97
def checksum(_x):
     print("Compute",x,"mod 97")
     c1=_x//(10**18)
     #print(c1)
     c2=(_x-(c1*10**18))//(10**9)
     m=mod97(c2)   # compute 10^digits(c2) mod 97, split over the resp 9-digit chunks
     #print(c2)
     c3=_x-(c1*10**18)-(c2*10**9)
     #print(c3)
     c1%=97
     #print(c1)
     c1=(c1*89)%97
     c2%=97
     #print(c2)
     c2=(c2*m)%97
     c3%=97
     #print(c3)
     c=(c1+c2+c3)%97
     return c


###################################################

print("### Tech specs example ###")
t0 = 200813                 # 6 digits
R1 = 123456789012345        # 15 digits
c=check_digits(t0,R1)
print("t0",t0)
print("R1",R1)
print("c",97-c)
x=(t0*(10**15)+R1)*100+(97-c)
print(checksum(x), "\n")

###################################################

print("### 13-digit R0 and t0 ending on 0 ###")
t0 = 200920                 # 6 digits with 0 at the end
R1 = 3456789012345          # 13 digits = 15 digits with two trailing zeros
c=check_digits(t0,R1)
print("t0",t0)
print("R1",R1)
print("c",97-c)
x=(t0*(10**15)+R1)*100+(97-c)
print(checksum(x), "\n")

###################################################

print("### Example test code with bogus date and 1-digit R1 ###")
t0 = 200000                 # bogus number, not a date
R1 = 5                      # 1 digit only
c=check_digits(t0,R1)
print("t0",t0)
print("R1",R1)
print("c",97-c)
x=(t0*(10**15)+R1)*100+(97-c)
print(checksum(x), "\n")

###################################################

# another test with test code from the app
print("### Test code generated in the app ###")
t0=201012 # date of infectiousness
code=44559257531208704 # Code: 4455-9257-5312-0870-4
x=t0*(10**17)+code
print(checksum(x))

###################################################

# generate bogus code
t0=random.randint(20,21)*10**4
t0+=random.randint(1,12)*10**2
t0+=random.randint(1,28)
R1=random.randint(10**14, 10**15)
print("somewhat random t0:",t0)
print("random R1:", R1)
x=(t0*(10**digits(R1))+R1)*100+(97-check_digits(t0,R1))
print(checksum(x))

