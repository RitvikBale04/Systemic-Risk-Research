#Imports
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def Average_Coeff_Function(
    Coefficient_Table: np.ndarray
):
    #Creating an Array which wil containg the average of the coefficient of all the points (the mean coordinates)
    Average_Coeff = []

    #Appending the Average Beta of each Risk Factor to the Average_Coeff Array
    Average_Coeff.append(np.mean(np.array(Coefficient_Table['bond'])))
    Average_Coeff.append(np.mean(np.array(Coefficient_Table['sp500'])))
    Average_Coeff.append(np.mean(np.array(Coefficient_Table['credit'])))
    Average_Coeff.append(np.mean(np.array(Coefficient_Table['cmdty'])))
    Average_Coeff.append(np.mean(np.array(Coefficient_Table['dvix'])))
    Average_Coeff.append(np.mean(np.array(Coefficient_Table['dhouse'])))

    return Average_Coeff


def PCA(
    Coefficient_Table: np.ndarray
):
    #Initializing Standardization Function
    sc = StandardScaler()
    #Initializing a Standardized Matrix of the Coefficient Table
    Coeff_PCA_std = sc.fit_transform(Coefficient_Table)
    #Constructing a Covariance Matrix from the Standardized Matrix
    Cov_Mat = np.cov(Coeff_PCA_std.T)

    #Determining the Eigenvectors and the Eigenvalues from the Covariance Matrix
    Eigen_Vals, Eigen_Vecs = np.linalg.eig(Cov_Mat)
    #Determining the Percentage Explained Variances
    Total = sum(Eigen_Vals)
    Var_Exp = [(i / Total) for i in sorted(Eigen_Vals, reverse=True)]
    #Array Containing Cumulative Proportion of Variances
    Cum_Var = []
    #Initializing a Variable that will be incremented by the Proportion of Variance for each EigenValue
    total = 0
    for i in Var_Exp:
        total += i
        Cum_Var.append(total)

    return Total, Var_Exp, Cum_Var


def Distance_Function(
    Coefficient_Table: np.ndarray
):
    #Calculating the Average Coefficient
    Average_Coeff = Average_Coeff_Function(Coefficient_Table)
    Average_Coeff = np.square(Average_Coeff)
    #Initializing the Normal(Perpendicular/Orthogonal) Vector to our Surface/Manifold of Complete Systemic Risk
    Normal = [1, 1, 1, 1, 1, 1]
    #Initializing the Vector between a Randomly Selected Point on the Manifold (1, 0, 0, 0, 0, 0) and the Average_Coeff Point
    Random_Point = [1, 0, 0, 0, 0, 0]
    #Determining the Vector Between the Mean Coefficient Point and the Random_point as the Vector in the Plane of the Manifold
    Vector = np.subtract(Average_Coeff, Random_Point)
    #Taking the Dot Product of the Normal Vector and the Arbitrary Vector to determine the distance of the point from the Manifold of Complete Systemic Risk
    Distance = np.dot(Normal, Vector)

    return Distance


def Distance_SD_Function(
    Coefficient_Table: np.ndarray
):
    #Initializing the Distances of all Firms from the Line of Complete Systemic Risk
    Distances = []

    #Initializing the Normal(Perpendicular/Orthogonal) Vector to our Surface/Manifold of Complete Systemic Risk
    Normal = [1, 1, 1, 1, 1, 1]
    #Initializing the Vector between a Randomly Selected Point on the Manifold (1, 0, 0, 0, 0, 0) and the Average_Coeff Point
    Random_Point = [1, 0, 0, 0, 0, 0]

    for i in range(len(Coefficient_Table.bond)):
        #Setting the Firm's Point equivalent to its Coefficient Values
        Firm_Point = Coefficient_Table.loc[i]
        Firm_Point = Firm_Point[1:]
        #Determining the Vector Between the Firm Point and the Random_point as the Vector in the Plane of the Manifold
        Vector = np.subtract(Firm_Point, Random_Point)
        #Taking the Dot Product of the Normal Vector and the Arbitrary Vector to determine the distance of the point from the Manifold of Complete Systemic Risk
        distance = np.dot(Normal, Vector)
        #Appending the Distance of the Firm to the Distances Array
        Distances.append(distance)

    #Calculating the Standard Deviation of the Distances of the Firms
    Distance_SD = np.std(Distances)

    return Distance_SD


def Squared_Beta_Function(
    Coefficient_Table: np.ndarray
):
    #Calculating the Average Coefficient
    Average_Coeff = Average_Coeff_Function(Coefficient_Table)
    #Calculating the Squared Beta
    #Initializing the Square Beta Variable
    Squared_Beta = 0
    #Looping through the Coefficients and Incrementing the Variable by each Squared Coefficient
    for i in Average_Coeff:
        #Incrementing by the Squared Coefficient
        Squared_Beta += (i**2)
    
    return Squared_Beta


def Clustering_SD_Function(
    Coefficient_Table: np.ndarray
):
    #Initializing the Array which will hold the Distances of all the Points from the Mean Point
    distances = []

    #Calculating the Average Coefficient
    Average_Coeff = Average_Coeff_Function(Coefficient_Table)

    #Iterating through all Firms and their Coefficients in the Coefficients Table
    for i in range(len(Coefficient_Table.bond)):
        #Initialzing the Squared Differences for each Coefficient
        Bond_Distance = (Coefficient_Table.bond[i] - Average_Coeff[0])**2
        SP500_Distance = (Coefficient_Table.sp500[i] - Average_Coeff[1])**2
        Credit_Distance = (Coefficient_Table.credit[i] - Average_Coeff[2])**2
        CMDTY_Distance = (Coefficient_Table.cmdty[i] - Average_Coeff[3])**2
        DVIX_Distance = (Coefficient_Table.dvix[i] - Average_Coeff[4])**2
        DHouse_Distance = (Coefficient_Table.dhouse[i] - Average_Coeff[5])**2
        
        #Determining the Distance via all Coefficient Differences and the Pythagorean Theorem
        distance = np.sqrt((Bond_Distance + SP500_Distance + Credit_Distance + CMDTY_Distance + DVIX_Distance + DHouse_Distance))
        #Appending the distance to the distances array
        distances.append(distance)

    #Calculating the SD of the Distances array (the smaller the SD the greater the Clustering and Systemic Risk)
    Clustering_SD = np.std(distances)

    return Clustering_SD


def KMeans_Clustering(
    Coefficient_Table: np.ndarray
):
    #Initializing the SSE Array Which Will Contain the Sum of Squared Errors for each Number of Clusters
    SSE = []

    #Running K-Means Clustering from 1 - 11 Clusters, and appending the SSE for each Number of Clusters
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(Coefficient_Table)
        SSE.append(kmeans.inertia_)

    for i in range(0,9):
        lowest = 0
        difference = SSE[i]/SSE[i+1]
        if difference > 1.10:
            lowest = i+1
    
    return SSE[lowest]