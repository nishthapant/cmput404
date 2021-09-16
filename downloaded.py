import requests as rq

response = rq.get("https://raw.githubusercontent.com/nishthapant/cmput404/master/lab1.py")

# download the script from raw Github url and save it
filePath = "downloaded.py"
f = open(filePath, "wb")
f.write(response.content)
f.close()

# print source code from downloaded file
f = open(filePath, "r")
print(f.read())
f.close()

