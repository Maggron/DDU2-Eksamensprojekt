import time
start_time = time.time()

MyPrint = True
#Function that prints time. it'll also do that in other terminals, therefore the bool "MyPrint" is set to false.
def PrintTime(text):
    if MyPrint == True:
        print(round((time.time()) - start_time,4),text,)
        print()

#Prints the time
PrintTime("Start")

SmallestAcceptableTime = 2 # in seconds 
import pandas as pd
#df = pd.read_csv("/Users/christiandam/Desktop/3.G/DDU/Eksamensprojekt/NiliasErEnTaber.csv",sep=";" ,dtype=str, usecols=["No.", "Time"])
df = pd.read_csv("NiliasNyeTider.csv",sep=";" ,dtype=str, usecols=["No.", "Time"])
PrintTime("Load Data")



#Make empty arrayes

ConvertedTimesIndexes = []
ConvertedTimes = []

PlottableTimeIndexes = []
PlottableTime = []

def ConverCSVtimeToSeconds(time):
    #Remove plusses from the string. they will always be the last element of the string
    if time[-1:] == "+":
        time = time[:-1]

    #Removes times that didnt finnish. They are in parentheses, so the first four elements and the last are removed.
    if time[0:3] == "DNF":
        time = time[4:-1]

    #Checks if the time contains minutes. else it would return an error
    if len(time)>5:
        min=int(time[:-6])
    else: min = 0

    # Converts the relevant elements in the string to a float representing the seconds.
    sec = float(time[-5:])

    sum = (60*min)+sec

    return sum

#Function to make other code more readable. Returns an element from the data.
def DataAccess(index, column):
   return df.iloc[index][column]

#Fills in the Converted times and its index with values.
def ConvertedArray():
    for i in range(len(df)):
        #print(ConverCSVtimeToSeconds(DataAccess(i,"Time")),DataAccess(i,"No."))
        ConvertedTimes.append(ConverCSVtimeToSeconds(DataAccess(i,"Time")))
        ConvertedTimesIndexes.append(int(DataAccess(i,"No.")))

ConvertedArray()

#Prints the time
PrintTime("Convert time from CSV")

#Exludes Junk data. Some datapoints are "DNF" meaning that it should be ignored. Also ex
def ExludeJunk(time,index):
    for element in range(len(time)):
        #If the three first elements if the string are "DNF", Dont add it to the final arrays
        if DataAccess(element,"Time")[0:3] == "DNF":
            continue
        #Likewise, if the 
        elif time[element] > SmallestAcceptableTime:
                PlottableTime.append(time[element])
                PlottableTimeIndexes.append(index[element])
        else: continue

ExludeJunk(ConvertedTimes,ConvertedTimesIndexes)


AllTimes = [PlottableTime, PlottableTimeIndexes]
#Prints the time
PrintTime("Exlude DNF")

# import json

# with open("names.json", "w") as fp:
#         json.dump(AllTimes, fp)
