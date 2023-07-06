import os

directory = "TA"

year = 2013
day = 0
missing = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        while(True):
            day += 1
            if(year % 4 == 0):
                days = 366
            else:
                days = 365
            if(day > days):
                year += 1
                day = 1
            expected = str(year) + str(day).zfill(3)
            actual = f[f.index("doy")+3:f.index("doy")+10]
            if(expected == actual):
                break
            print("miss: " + expected)
            missing.append(expected)
        
