connected=[]
for i in range(201):
    lis=[0 for _ in range(201)]
    connected.append(lis)
s=''
s=input()
N, M=s.split(' ')
N,M=int(N),int(M)
for ii in range(M):
    s=input()
    i,j=s.split(' ')
    i,j=int(i),int(j)
    connected[i][j]=1
    connected[j][i]=1
k=int(input())
for ii in range(k):
    s=input()
    s=s.split(' ')
    ss=s
    s=[]
    for jj in ss:
        s.append(int(jj))
    n=s[0]
    a=s[1:]
    if a[0]==a[n - 1]:
        if(n==N+1):
            visited=[0 for _ in range(300)]
            for i in range(1,n):
                if visited[a[i]]:
                    break
                visited[a[i]]=1
            i+=1
            if i==n:
                for i in range(1,n):
                    if(not connected[a[i]][a[i-1]]):
                        break
                i+=1
                if i==n:
                    print('YES')
                    continue
    print('NO')
