from django.core.files import File

with open("/path/to/hello.world", "w") as f:
    myFile = File(f)
    myFile.write("Gwapo ko")

myFile.closed

f.closed