import csv
import sys
import os
import traceback
from datetime import datetime,timedelta

def main(csvfilename):
    ''' load the csv data to auxiliary space. In this case into a list '''
    data = []
    with open(csvfilename, "r",) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                data.append(row)
    #remove the headers
    data.pop(0)
    return data
  
    

def validate_trading_price(data):
    abc = 0
    stock = 0
    l2 = []
    list_time = []
    net_stock = 0
    len_data = len(data)
    date_time_1min = ''
    date_time_after_1min_after = ''
    date_time_after_10min = ''
    row_count = 0
    list_for_average_1min = []
    list_for_average_10min = []
    date_time_after_1min = ''
    date_time_after_10min = ''
    try:
        for i in range(1,len_data-1):
            if row_count == 0:
                l2.append(data[i-1])
            else:
                if data[i][5] == data[i-1][5]:
                    pass
                else:
                    l2.append(data[i])
            row_count +=1
        print('length of row are', len(l2))
        for i in l2:
            
            if (date_time_1min and date_time_after_1min_after and date_time_after_10min) == '':
                date_time_1min = i[4].split(" ")
                date_time_1min[-1] = date_time_1min[-1][:12]
                date_time_1min = " ".join(date_time_1min)
                date_time_1min = datetime.strptime(date_time_1min,"%Y-%m-%d %H:%M:%S.%f")
                date_time_after_1min_after = date_time_1min + timedelta(seconds = 59)
                date_time_after_10min = date_time_1min + timedelta(minutes = 10)

            if i[4] >= str(date_time_1min) and i[4] < str(date_time_after_1min_after):
                list_time.append(i[4])
            else:
                for each_rows in l2:  
                    try:
                        if each_rows[4] <= str(date_time_after_1min_after) and each_rows[4] >= str(date_time_1min):
                            list_for_average_1min.append(each_rows)
                        if each_rows[4] <= str(date_time_after_10min) and each_rows[4] >= str(date_time_1min):
                            list_for_average_10min.append(each_rows)
                        elif each_rows[4] > str(date_time_after_10min):
                            sum_price_1min = 0
                            for prices in list_for_average_1min:
                                sum_price_1min += int(prices[5])
                            running_average_1min = sum_price_1min//len(list_for_average_1min)

                            sum_price_10min = 0
                            for prices_10min in list_for_average_10min:
                                sum_price_10min += int(prices_10min[5])
                            running_average_10min = sum_price_10min//len(list_for_average_10min)

                            if running_average_1min > running_average_10min:
                                stock += 10*9
                            elif running_average_1min < running_average_10min:
                                stock -= 10*9  
                            date_time_1min, date_time_after_1min_after, date_time_after_10min = '', '', ''                          
                            break

                    except Exception as ex:
                        print(ex)
                        break
        print('Value of stock after final trade ', stock)      
        
    except Exception as ex:
        trace = traceback.format_exc()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(trace, exc_type, exc_obj, exc_tb )

#add file Location
if __name__ == "__main__":
    data = main('REL_future_Raw.csv')
    validate_trading_price(data)
