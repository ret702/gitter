from github import *
import json
import sys
import base64
from polls.forms import UploadFileForm
from django.core.files.uploadedfile import UploadedFile
import tempfile

commands=[]
g=Github()

files=[]

def processCommand(data,f):
    global files
    files=f
    global commands
    commands=data.split()
    command=commands[0]

    try:
        return getattr(sys.modules[__name__],command)()
    except NameError as e:
        raise NameError(e)




def login():
    try:
        if(len(commands) == 3):
            global g
            g = Github(commands[1], commands[2])
            return {"result":"Successfully logged in!"}
        else:
            return {"result":"Error: Not enough arguments"}
    except Exception as e:
        raise ValueError(str(e))
        return {"result":"Login Failed!"}


def push():
    repo=commands[1]
    message=commands[2]
    branch=commands[3]
    if(files is not None):
        if(len(commands)==4):
            try:
                repo=g.get_user().get_repo(repo)
                commit_message = message
                master_ref = repo.get_git_ref('heads/'+branch)
                master_sha = master_ref.object.sha
                base_tree = repo.get_git_tree(master_sha)
                element_list = list()
                data=""
                for entry in files:
                    element = InputGitTreeElement(entry, '100644', 'blob', handle_uploaded_file(entry))
                    element_list.append(element)
                tree = repo.create_git_tree(element_list, base_tree)
                parent = repo.get_git_commit(master_sha)
                commit = repo.create_git_commit(commit_message, tree, [parent])
                master_ref.edit(commit.sha)

                return {"result":"File pushed please check your repository to make sure it went through!"}
            except Exception as e:
                raise e
                return {"result":"Error: Hint:Are you logged in?"}
        else:
             return {"result":"Not enough arguments"}
    else:
        return {"result":"No files staged"}


def staged():
    return showstaged()

def showstaged():
    if(len(commands)==2):
        if(commands[1]=="clear"):
            global files
            files=[]
            return {"result":"Staged files cleared"}
    else:
        fileList=""
        for filename in files:
            fileList+=filename +  " "
        if(fileList != ""):
            print(files)
            print(fileList)
            return {"result":fileList}
        else:
            return {"result":"No files staged"}
            
