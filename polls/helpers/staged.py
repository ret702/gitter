

def showstaged():
    fileList=""
    for filename in files:
        fileList+=filename +  " "
    if(fileList != None):
        return {"result":fileList}
    else:
        return {"result":"null"}
