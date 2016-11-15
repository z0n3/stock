import time
import shlex
import subprocess

comment = input('pls input commit: ')
#git部分
cwd = "D:\\Users\\zhouyu835\\Downloads\\git\\stock"
cmd = "git add -A"
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git commit -m '{}'".format(comment)
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git push origin master"

def gitpush():
    try:
        time.sleep(5)
        subprocess.check_output(shlex.split(cmd), cwd=cwd)
    except:
        gitpush()

gitpush()
print('done')