
key="abc"
text="helloworld"

def stream(text,key):
    key=ord(key)
    text=ord(text)
    key=key*(len(text)//len(key))+key[:len(text)%len(key)]
    result=""
    for i in range(len(text)):
        result+=text[i]^key[i]
    return result