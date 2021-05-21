print ("Loading Terminal...")
from flask import Flask
#import TERMINAL

#import os
#os.environ["FLASK_APP"]="TERMINAL"
def env_file():
    with open(".env","w", encoding="UTF-8") as f:
        f.write("FLASK_APP='TERMINAL'\n")
        #f.write("(File automatically created by terminal)\n")
        f.close()


from TERMINAL import create_app
if __name__=="__main__":
    app=create_app()
    app.run()
    #Flask.run(Flask, host="0.0.0.0",port=5000)

# os.environ.__setitem__("AHA","ABC")
# find=os.environ.get("AHA")
# print (find)


## wsgi.py
# from TERMINAL import create_app()
# FLASK_ENV="TERMINAL"
# if __name__=="__main__":
#     app=create_app()