import numpy as np
import statistics
import random
from client_moodle import *


def random_selection(cost_array,initial_array,shape):

    '''This function selects two parents based on their fitness and some probabilistic function'''
    cost_array_new2=np.random.randn(shape,1)
    cost_array_new1=[]

    sum_array=np.sum(cost_array) 
    mean=np.mean(cost_array)
    std_dev=np.std(cost_array)
    epsilon=10**-14
    
    #Method number one
    for i in range(shape):
        cost_array_new2[i]=(cost_array[i]-mean)/(std_dev + epsilon) + np.random.randn()/10

    [ind1,ind2]=sorted(range(len(cost_array_new2)), key=lambda i: cost_array_new2[i],reverse=True)[-2:]

   
    #Method number two  
    for i in range(shape):
        cost_array_new1.append(cost_array[i][0]/sum_array) 

    output=np.random.choice(range(shape),size=2,replace=True,p=cost_array_new1)
    # return(initial_array[output[0]],initial_array[output[1]])  
    
    return([initial_array[ind1],initial_array[ind2]])

    

def mutate(child,prob):

    '''This function mutates the child array according to the probability specified'''
    mutated_indices=[]
    for i in range(11):
        if(np.random.rand()<prob):
            mutated_indices.append(i+1)
            child[i]=child[i]*(1+np.random.randn()/100000)
        if(abs(child[i])>=10):
            child[i]=child[i]*(1- abs(np.random.randn()/100000))

    print("Weight Indices that mutated:", mutated_indices)

    return child    


def child_maker(arr1,arr2):

    '''This function joins two arrays arr1 and arr2 at the crossover point to form a child array'''
    arr3=np.random.randn(11,1)
    c=np.random.randint(0,11) # choosing the crossover point
    print("Crossover point:",c)
    d=np.random.randint(0,2) # choosing which one will be the first parent and which one the second
    
    if(d==0):
        temp=arr1
        arr1=arr2
        arr2=temp

    assert(arr1.shape == (11,1))
    assert(arr2.shape == (11,1))

    for i in range(11):
        if ( i<=c):
            arr3[i]=arr1[i]
        else:
            arr3[i]=arr2[i]

    if(d==0):
        print("Swap Parents order: yes")
    else:
        print("Swap Parents order: no")
    
    
    return(arr3)

def fitness_func(input_array):

    '''This function computes the fitness of the array input as a sum of squares from 1.0 for each element in the array'''
    cost=0
    center=1.0
    for i in range(11):
        cost =cost +((input_array[i]-center)**2)
    # print(cost)
    return cost

def genalgo(key,iter=10,shape=10,prob=0.2):

    '''This function loops over various iterations and executes the genetic algorithm'''
   
    initarray=np.random.randn(shape,11)*(10**-13)
    givenarray=[0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
    initial_array= initarray + givenarray #perturbation introduced
    
    print("Given Vector:",list(givenarray))
    
    ind=0
    
    for x in range(iter):
        print("\n*******************************************************************************")
        print("*******************************************************************************")
        print("*******************************************************************************\n")
    
        print("Iteration:",(x+1),"\n\n")
        print("Parent population:\n", initial_array,"\n\n")
        new_array=np.random.randn(shape,11)
        new_cost_array=np.random.rand(shape,1)
        cost_array=np.random.randn(shape,1) 
        actual_cost1=np.random.randn(shape,1)
        actual_cost2=np.random.randn(shape,1) 

        assert(initial_array.shape == (shape,11))

        for i in range(shape):           
            cost=get_errors(key,list(initial_array[i]))
            cost_array[i]=0.75*cost[0]+cost[1]   

        print("Costs for the parent population:\n",cost_array,"\n")         
        
        assert(cost_array.shape == (shape,1))

        for i in range(shape):
            print("\nFor child number:",(i+1),"\n")
            [arr1,arr2]=random_selection(cost_array,initial_array,shape)
            print("Parent 1:",list(arr1))
            print("Parent 2:",list(arr2))

            arr1=arr1.reshape((11,1))
            arr2=arr2.reshape((11,1))
            

            assert(arr1.shape == (11,1))
            assert(arr2.shape == (11,1))

            child=child_maker(arr1,arr2)
            print("Child generated:",list(child))

            child=mutate(child,prob)
            print("Mutated Child:",list(child))
            
            assert(child.shape == (11,1))
            
            for j in range(11):
                new_array[i][j]= child[j]

        print("\n\nChild Population generated:\n",new_array)

        assert(new_array.shape == (shape,11)) 

        
        #validating the iteration        
        for i in range(shape):
            
            cost=get_errors(key,list(new_array[i]))
                        
            new_cost_array[i]=0.75*cost[0]+cost[1]
            actual_cost1[i]=cost[0]
            actual_cost2[i]=cost[1]

        print("\n\n Cost for Child Population:\n",new_cost_array)

        [ind1,ind2,ind3,ind4,ind5]=sorted(range(len(cost_array)), key=lambda i: cost_array[i],reverse=True)[-5:]
        [ind6,ind7,ind8,ind9,ind10]=sorted(range(len(new_cost_array)), key=lambda i: new_cost_array[i],reverse=True)[-5:]

        final_array=np.random.randn(shape,11)
        final_array[0]=initial_array[ind1]
        final_array[1]=initial_array[ind2]
        final_array[2]=initial_array[ind3]
        final_array[3]=initial_array[ind4]
        final_array[4]=initial_array[ind5]
        final_array[5]=new_array[ind6]
        final_array[6]=new_array[ind7]
        final_array[7]=new_array[ind8]
        final_array[8]=new_array[ind9]
        final_array[9]=new_array[ind10]

        initial_array=np.copy(final_array)

        print("\n\n New Generation after taking best 5 from both the generations:\n",initial_array)

        final_costarray=np.random.randn(shape,1)
        final_costarray[0]=cost_array[ind1]
        final_costarray[1]=cost_array[ind2]
        final_costarray[2]=cost_array[ind3]
        final_costarray[3]=cost_array[ind4]
        final_costarray[4]=cost_array[ind5]
        final_costarray[5]=new_cost_array[ind6]
        final_costarray[6]=new_cost_array[ind7]
        final_costarray[7]=new_cost_array[ind8]
        final_costarray[8]=new_cost_array[ind9]
        final_costarray[9]=new_cost_array[ind10]
        
        initial_array=np.copy(final_array)

        ind=np.argmin(final_costarray)
       
        print("\n\nBest vector from the iteration:",list(initial_array[ind]))
        print("\nCost of Best vector:",get_errors(key,list(initial_array[ind])))
        

genalgo(key='AvM1afc4e1EY25wdJSunCD0CrR3AwZbKopel8dMwEUyvpmI5QR')