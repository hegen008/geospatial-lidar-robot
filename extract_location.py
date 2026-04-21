import pandas

def return_position(time, integrated_imu_file): 
   
    integrated_imu_data = pandas.read_csv('data/imu_integration.csv')

    # index of integrated data at the time we're looking for
    exact_index = imu_dataframe.index[imu_dataframe['timestamp_us']==time].tolist()

    if len(exact_index) > 0:      # we found an exact match for the time

        px = imu_dataframe.iloc[exact_index[0]]['px']
        py = imu_dataframe.iloc[exact_index[0]]['py']

        return px, py
    
    # look for the closest times and interpolate approximate position
    else:
        #iterate through rows of dataframe
        for i, rows in imu_dataframe.iterrows():
            # pass if before the time we want
            if row['timestamp_us'] < time:
                pass
            # once we get to time after the one we're searching for
            else:
                # get data directly before and after the time we want
                before_row = imu_dataframe.iloc[i-1]
                after_row = imu_dataframe.iloc[i]
                # math to figure out position in between
                between_ratio = (time-before_row['timestamp_us'])/(after_row['timestamp_us'] - before_row['timestamp_us'])
                px = between_ratio * (after_row['px'] - before_row['px']) + before_row['px']
                py = between_ratio * (after_row['py'] - before_row['py']) + before_row['py']

                return px, py



'''
with open('data/imu_integration.csv', 'r') as fp:
    reader = csv.reader(fp)
    integrated_imu_data  = []   # each element is a row from the csv file;
    for row in reader:
        integrated_imu_data.append(row)

print(lines)
'''


