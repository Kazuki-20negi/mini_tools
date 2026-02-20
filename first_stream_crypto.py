
key="abc"
text="helloworld"

def stream(text,key):
    key=ord(key)
    text=ord(text)
    key=key*(len(text)//len(key))+key[:len(text)%len(key)]
    for i in range(len(text)):
        
