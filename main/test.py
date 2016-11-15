import time

n=0
l=[0,0,0,0,0,1,2]
def gitpush():
    global n
    try:
        print(l[n])
        n+=1
        time.sleep(1)
        b=1/l[n]
    except:
        gitpush()
    finally:
        print('b')
        
gitpush()