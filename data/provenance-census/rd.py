import sys,re
t=open('sources/'+sys.argv[1]+'.txt').read()
lines=[re.sub(r'\s+',' ',l).strip() for l in t.split('\n')]
start=next((i for i,l in enumerate(lines) if len(l.split())>=14),0)
mark=sys.argv[3] if len(sys.argv)>3 else None
if mark: start=next((i for i,l in enumerate(lines) if mark in l),start)
n=int(sys.argv[2]) if len(sys.argv)>2 else 6000
out='\n'.join(l for l in lines[start:] if l)
print(out[:n])
