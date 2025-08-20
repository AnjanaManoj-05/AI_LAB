count_n=int(input("Enter the room number: "))
a=[1,1,1,1]
c=0
while c!=4:
    if(a[(count_n-1)%4]==1):
        a[(count_n-1)%4]=0
        if(count_n<=4):
            print("Room {} cleaned.".format(count_n))
        else:
            print("Room {} cleaned.".format(count_n%4))
        
    count_n+=1
    c+=1;
