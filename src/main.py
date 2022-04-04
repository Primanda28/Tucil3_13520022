from puzzle import *
import random

def randomizeMat(mat):
    lst=[i+1 for i in range(16)]
    random.shuffle(lst)
    for i in range(16):
        mat[i//4][i%4]=lst[i]

def main():
    mat=[[0 for i in range(4)] for j in range(4)]

    while True:
        print("Pilihan input :")
        print("1. Input File")
        print("2. Input Random\n")
        inp=int(input("Masukan angka pilihan input : "))
        if(inp==1):
            inp=input("Masukkan nama file : ")
            try:
                i=0
                with open("test/"+inp) as f:
                    line=f.readline()
                    while line:
                        mat[i]=[int(j) if j!='-' else 16 for j in line.split()]
                        line=f.readline()
                        i+=1
            except:
                print("File error")
            break
        elif(inp==2):
            randomizeMat(mat)
            break
        else:
            print("Masukan tidak valid")

    puzzleSolver(mat)

main()