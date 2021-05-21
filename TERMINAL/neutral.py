import sys
import os

import tmp
print (sys.modules)
print ("NEUTRALITY")
inp1=input ("What is your side?")
#sys.exit()
mod=os.environ.get("tmp")
print (mod)
os.kill(mod)
if inp1=="blog":
    import controller