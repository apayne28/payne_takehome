import pandas as pd

#Convert CSV files to DataFrame
slcsp = pd.read_csv("./slcsp.csv",)
plans = pd.read_csv("./plans.csv")
zips = pd.read_csv("./zips.csv")

#Add the leading zeros back in the zipcodes
slcsp['zipcode'] = slcsp['zipcode'].astype('str')
slcsp['zipcode'] = slcsp['zipcode'].str.rjust(5, "0")
zips['zipcode'] = zips['zipcode'].astype('str')
zips['zipcode'] = zips['zipcode'].str.rjust(5, "0")

#Filter plans to only contain silver plans
silver_plans = plans[plans['metal_level'].str.contains('Silver')]

#Prints header
print("zipcode, rate")

#Make calculations for each zipcode in slcsp.csv
for code in slcsp['zipcode']:

    #Filters zips to only contain entries with the current zipcode
    filtered_zips = zips[zips['zipcode'] == code]

    
    #Will print the zipcode with no rate if there are multiple rate_areas
    if len(set(filtered_zips['rate_area'])) > 1:
        print("{code},".format(code=code))
        continue

    #Grabs the state based on the zipcode
    code_state = silver_plans['state'] == filtered_zips.state.iloc[0]

    #Grabs the rate area
    code_rate_area = silver_plans['rate_area'] == filtered_zips.rate_area.iloc[0]

    #Filters silver plans based on the state and rate area, then is sorted by rate from largest to smallest
    filtered_rate_list = silver_plans.loc[ code_state & code_rate_area ].sort_values(by='rate', ascending=False)

    #Will print code and exit if only one Silver plan exists
    if len(filtered_rate_list['metal_level'])  == 1:
        print("{code},".format(code=code))
        continue

    #Will save the rate to the final_rate variable as long as there's more than one rate
    final_rate = "%1.2f " % filtered_rate_list.rate.iloc[-2] if len(filtered_rate_list.rate) > 1 else ''

    #Prints the final output
    print("{code}, {final_rate}".format(code = code, final_rate = final_rate))