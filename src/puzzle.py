import heapq
import time

# variabel global untuk menghitung total node yang telah terbentuk
totalNode=1

# fungsi untuk copy matrix
def copyMat(mat):
    ret=[[0 for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            ret[i][j]=mat[i][j]
    return ret

# fungsi untuk menghitung total KURANG(i) dengan i adalah seluruh ubin pada matriks
def kurang(mat):
    ans=0
    for i in range(4):
        for j in range(4):
            for k in range(i*4+j+1,16):
                if(mat[k//4][k%4]<mat[i][j]):
                    ans+=1
    return ans

# Fungsi untuk mengecek apakah ubin yang kosong berada pada bagian yang diblok
def X(mat):
    for i in range(4):
        for j in range(4):
            if(mat[i][j]==16):
                return (i&1)^(j&1)

# Menampilkan nilai kurang[i]
def displayKurang(mat):
    kurangI=[0 for i in range(16)]
    for i in range(4):
        for j in range(4):
            for k in range(i*4+j+1,16):
                if(mat[k//4][k%4]<mat[i][j]):
                    kurangI[mat[i][j]-1]+=1
    for i in range(16):
        print("Kurang[{}] = {}".format(i+1,kurangI[i]))


# Menghitung setiap ubin pada puzzle yang belum pada tempatnya
def cost(mat):
    ans=0
    for i in range(4):
        for j in range(4):
            if(mat[i][j]!=i*4+j+1):
                ans+=1
    return ans

# Menampilkan matriks
def displayMat(mat):
    for i in range(4):
        for j in range(4):
            if(mat[i][j]==16):
                print("-",end=" ")
            else:
                print(mat[i][j],end=" ")
        print()

# Mengecek apakah setiap ubin pada puzzle telah berada pada posisinya
def isSolution(mat):
    for i in range(4):
        for j in range(4):
            if(i*4+j+1!=mat[i][j]):
                return False
    return True

# Mengembalikan indeks ubin yang kosong pada matriks
def findSpace(mat):
    for i in range(4):
        for j in range(4):
            if(mat[i][j]==16):
                return i,j

# Memasukkan node ke priority queue berdasarkan costnya untuk setiap command yang valid
def pushToQueue(last,lastStep,mat,listMat,prioQueueMat,depth):
    global totalNode
    i,j=findSpace(mat)

    # Command = U
    if(lastStep!="D" and i!=0):
        totalNode+=1
        retMat4=copyMat(mat)
        retMat4[i][j],retMat4[i-1][j]=retMat4[i-1][j],retMat4[i][j]
        heapq.heappush(prioQueueMat,(cost(retMat4)+depth+1,depth+1,last,len(listMat),"U",copyMat(retMat4)))
        listMat.append((last,"U",retMat4))

    # Command = R
    if(lastStep!="L" and j!=3):
        totalNode+=1
        retMat1=copyMat(mat)
        retMat1[i][j],retMat1[i][j+1]=retMat1[i][j+1],retMat1[i][j]
        heapq.heappush(prioQueueMat,(cost(retMat1)+depth+1,depth+1,last,len(listMat),"R",copyMat(retMat1)))
        listMat.append((last,"R",retMat1))
    
    # Command = D
    if(lastStep!="U" and i!=3):
        totalNode+=1
        retMat3=copyMat(mat)
        retMat3[i][j],retMat3[i+1][j]=retMat3[i+1][j],retMat3[i][j]
        heapq.heappush(prioQueueMat,(cost(retMat3)+depth+1,depth+1,last,len(listMat),"D",copyMat(retMat3)))
        listMat.append((last,"D",retMat3))
    
    # Command = L
    if(lastStep!="R" and j!=0):
        totalNode+=1
        retMat2=copyMat(mat)
        retMat2[i][j],retMat2[i][j-1]=retMat2[i][j-1],retMat2[i][j]
        heapq.heappush(prioQueueMat,(cost(retMat2)+depth+1,depth+1,last,len(listMat),"L",copyMat(retMat2)))
        listMat.append((last,"L",retMat2))

# Menampilkan urutan command pada matriks hingga mencapai matriks solusi
def printPath(listMat,idAns):
    ret=[]
    while(idAns!=-1):
        ret.append(listMat[idAns])
        idAns=listMat[idAns][0]
    for i in range(len(ret)-2,-1,-1):
        print("LANGKAH {} =".format(len(ret)-1-i),end=" ")
        if(ret[i][1]=="U"):
            print("UP")
        elif(ret[i][1]=="D"):
            print("DOWN")
        elif(ret[i][1]=="R"):
            print("RIGHT")
        elif(ret[i][1]=="L"):
            print("LEFT")
        displayMat(ret[i][2])
        print()


def puzzleSolver(mat):
    print("\nMasukan matriks :")
    displayMat(mat)
    print()
    displayKurang(mat)
    print()
    print("Total kurang[i]+X =",kurang(mat)+X(mat),end="\n\n")

    startTime=time.time()

    if((kurang(mat)+X(mat))%2==1):
        print("Puzzle tidak bisa dipecahkan")
    else:
        # inisialisasi variabel
        listMat=[] # Berperan sebagai linked list sebagai sisi dari node yang terbentuk
        prioQueueMat=[] # List node yang perlu diproses dan terurut berdasarkan prioritasnya

        # cek apakah matriks merupakan solusi
        if(isSolution(mat)):
            print("Solusi telah dicapai")
        else:
            # masukkan kondisi awal matriks ke listMat
            listMat.append((-1,"",mat))
            heapq.heapify(prioQueueMat)
            pushToQueue(0,"",copyMat(mat),listMat,prioQueueMat,0)

            # lakukan iterasi hingga ditemukan solusi
            while(True):
                cur=heapq.heappop(prioQueueMat)
                if(isSolution(cur[5])):
                    print("Urutan penyelesaian puzzle :\n")
                    printPath(listMat,cur[3])
                    print("Total node terbentuk =",totalNode)
                    break
                pushToQueue(cur[3],cur[4],copyMat(cur[5]),listMat,prioQueueMat,cur[1])
    print("Waktu eksekusi :",round(time.time()-startTime,10),"s")

