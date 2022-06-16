"""
    
 """
import math
import pandas as pd

class TempDataset:
    '''Class for temperature datasets'''
    num_objects = 0

    def __init__(self):
        '''Init method for class'''
        self._data_set = None
        self._name = "Unnamed"
        TempDataset.num_objects += 1

    @property
    def data_set(self):
        '''Getter for data set variable'''
        return self._data_set

    @data_set.setter
    def data_set(self, newset):
        '''Setter for data set variable'''
        self._data_set = newset

    @property
    def name(self):
        '''Getter for data set name variable'''
        return self._name

    @name.setter
    def name(self, newname):
        '''Setter for data set name variable'''
        if len(newname) >= 3 and len(newname) <= 20:
            self._name = newname
        else:
            raise ValueError

    def process_file(self, filename):
        '''Function to process file'''
        self._data_set = []
        try:
            file = open(filename, 'r')
        except FileNotFoundError:
            return False
            main()
        for next_line in file:
            data_line = next_line.split(',')
            if data_line[3] == 'TEMP':
                data_line[0] = int(data_line[0])
                data_line[1] = (math.floor(float(data_line[1]) * 24))
                data_line[2] = int(data_line[2])
                data_line[4] = float(data_line[4])
                data_line = tuple(data_line[0:3] + data_line[-1:])
                self._data_set.append(data_line)
        file.close()

    def get_summary_statistics(self, active_sensors):
        '''Function to get summary statistics'''
        global current_unit
        convert = []
        if self._data_set == None:
            return None
        if active_sensors == [] or (active_sensors != [] and all(v[3] is None for v in self._data_set)):
            return None
        else:
            readings = [v[3] for v in self._data_set
                           if v[2] in active_sensors]
            summary = ((sum(readings)/len(readings)), max(readings), min(readings))
            unitkey=(list(UNITS.keys())[list(UNITS.values()).index((current_unit, current_unit[0]))])
            return (f'Average: {float(convert_units(summary[0],unitkey).split(" ")[5]):.2f} {UNITS[unitkey][1]} \n'
                    f'Maximum: {float(convert_units(summary[1],unitkey).split(" ")[5]):.2f} {UNITS[unitkey][1]} \n'
                    f'Minimum: {float(convert_units(summary[2],unitkey).split(" ")[5]):.2f} {UNITS[unitkey][1]}')


    def get_avg_temperature_day_time(self, active_sensors, day, time):
        '''Function to get avg temp by day,time'''
        readings = []
        if self._data_set == None:
            return None
        if active_sensors == [] or (active_sensors != [] and all(v[3] is None for v in self._data_set)):
            return None
        else:
            readings = [v[3] for v in self._data_set
                           if v[0] == day and v[1] == time and v[2] in active_sensors]
            return sum(readings)/ len(readings)

    def get_num_temps(self, active_sensors,lower_bound, upper_bound):
        '''Function get num temps'''
        if self._data_set == None:
            return None
        else:
            return 0

    def get_loaded_temps(self):
        '''Function get loaded temps'''
        if self._data_set == None:
            return None
        else:
            row_count = sum(1 for row in self._data_set)
            return row_count

    @classmethod
    def get_num_objects(cls):
        '''Class method to return number of class objects created'''
        return cls.num_objects

def print_header():
    '''Function that prints header for project'''
    print('''STEM Center Temperature Project
Robert Blanton''')


def convert_units(celsius_value, units):
    '''Function that converts a celsius temperature into celsius, fahrenheit, or Kelvin.'''
    if units == 0:
        return f'The temperature in Celsius is: {celsius_value}'
    elif units == 1:
        return f'The temperature in Fahrenheit is: {celsius_value * (9/5) + 32}'
    elif units == 2:
        return f'The temperature in Kelvin is: {celsius_value + 273.15}'
    else:
        return 'Please enter 0,1, or 2 for conversion unit. Please run program again.'


def print_menu():
    print('''Main Menu
----------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit''')


def new_file(dataset):
    'Function to open new file'
    print('New file function called')
    filename = input('Please enter a temp dataset file: ')
    dataset.process_file(filename)
    print(f'{dataset.get_loaded_temps()} samples loaded')
    if dataset.process_file(filename) == False:
        print('File not found')
        return
    while len(dataset.data_set) > 1 and dataset.name == 'Unnamed':
        try:
            dataname = input("Please enter a 3-20 character name for dataset: ")
            dataset.name = dataname
            print(dataset.name)
        except ValueError:
            print('Name is incorrect length')
            continue


UNITS = {
        0: ("Celsius", "C"),
        1: ("Fahrenheit", "F"),
        2: ("Kelvin", "K"),
    }
current_unit = UNITS[0][0]


def choose_units():
    'Function to choose units'

    global current_unit
    print('Choose units function called')
    print(f'Current units in {current_unit}')
    print('Choose new units: ')
    for x in UNITS:
        print(f'{x} - {UNITS[x][0]}' )
    try:
        unit = int(input(('Enter unit: ')))
        current_unit = UNITS[unit][0]
        return current_unit
    except ValueError:
        print('please select an integer value')
        choose_units()
    except KeyError:
        print('please select available unit')
        choose_units()


def change_filter(sensors, sensor_list, filter_list):
    'Function to change filter'
    try:
        print_filter(sensor_list, filter_list)
        filter_to_change = (input('Type the filter to toggle or x to exit: '))
        if sensors[filter_to_change][1] in filter_list:
            filter_list.remove(sensors[filter_to_change][1])
        elif sensors[filter_to_change][1] not in filter_list:
            filter_list.append(sensors[filter_to_change][1])
        change_filter(sensors, sensor_list, filter_list)
    except KeyError:
        if filter_to_change == 'x':
            main()
            quit()
        else:
            print("Error. Please enter a filter value(4201, 4204, 4205, 4213, 4218, Out).")
            change_filter(sensors, sensor_list, filter_list)
    return filter_list


def print_summary_statistics(dataset, active_sensors):
    'Function to print summary statistics'
    print(f'Print summary statistics function called for {dataset.name}')
    if dataset.get_summary_statistics(filter_list) == None:
        print('Please ensure dataset is loaded or there is at least one active sensor with data')
    else:
        print(dataset.get_summary_statistics(filter_list))


def print_temp_by_day_time(dataset, active_sensors):
    'Function to print temperature by day and time'
    DAYS = {
        0: "SUN",
        1: "MON",
        2: "TUE",
        3: "WED",
        4: "THU",
        5: "FRI",
        6: "SAT"
    }

    HOURS = {
        0: "Mid-1AM  ",
        1: "1AM-2AM  ",
        2: "2AM-3AM  ",
        3: "3AM-4AM  ",
        4: "4AM-5AM  ",
        5: "5AM-6AM  ",
        6: "6AM-7AM  ",
        7: "7AM-8AM  ",
        8: "8AM-9AM  ",
        9: "9AM-10AM ",
        10: "10AM-11AM",
        11: "11AM-NOON",
        12: "NOON-1PM ",
        13: "1PM-2PM  ",
        14: "2PM-3PM  ",
        15: "3PM-4PM  ",
        16: "4PM-5PM  ",
        17: "5PM-6PM  ",
        18: "6PM-7PM  ",
        19: "7PM-8PM  ",
        20: "8PM-9PM  ",
        21: "9PM-10PM ",
        22: "10PM-11PM",
        23: "11PM-MID ",
    }
    unitkey = (list(UNITS.keys())[list(UNITS.values()).index((current_unit, current_unit[0]))])

    dict1 = {}
    print('Print temperature by day and time function called')
    if dataset.get_loaded_temps() == None:
        print('please load dataset')
        main()
    else:
        for day in DAYS:
            dict1[day] = [x for x in range(24)]
            for hour in HOURS:
                try:
                    dict1[day][hour] = float(
                    convert_units(dataset.get_avg_temperature_day_time(filter_list, day, hour), unitkey).split(' ')[5])
                except ValueError:
                    dict1[day][hour] = "---"
        df = pd.DataFrame.from_dict(dict1, orient='index').transpose()
        df = df.round(2)
        df.columns = df.columns.map(DAYS)
        df.index = df.index.map(HOURS)
        print(df)

def print_histogram(dataset, active_sensors):
    'Function to print histogram'
    print('Print histogram function called')


def recursive_sort(list_to_sort, key=0):
    """Function that will recursively bubble sort a list"""
    flips = 0
    if flips == 0:
        for i in range(len(list_to_sort) - 1):
            if list_to_sort[i][key] > list_to_sort[i + 1][key]:
                list_to_sort[i], list_to_sort[i + 1] = list_to_sort[i + 1], list_to_sort[i]
                flips = + 1
            if flips > 0:
                list_to_sort[:-1] =recursive_sort(list_to_sort[:-1], key=key)
    return (list_to_sort)


def print_filter(sensor_list,filter_list):
    '''Function returns sorted list indicating if filter is active'''
    sensor_list = recursive_sort(sensor_list, key =0)
    for k in range(len(sensor_list)):
        if sensor_list[k][2] in filter_list:
            print(sensor_list[k][0] + ': ' + sensor_list[k][1] + '[ACTIVE]')
        else:
            print(sensor_list[k][0] + ': ' + sensor_list[k][1])

current_set = TempDataset()

sensors1 = {'4213': ('STEM Center', 0), '4201': ('Foundations Lab', 1), '4204': ('CS Lab', 2),
               '4218': ('Workshop Room', 3), '4205': ('Tiled Room', 4), 'Out': ('Outside', 5)}
sensor_list = [(k, v[0], v[1]) for k, v in sensors1.items()]
filter_list = [(v[1]) for k, v in sensors1.items()]

def main():
    '''Main function where the Mainline Code is placed.'''
    print(current_set.get_avg_temperature_day_time(filter_list, 5, 7))  # for testing
    '''Dictionary comprehension'''
    sensors = {sub[0]: sub[1:] for sub in sensor_list}
    try:
        print_menu()
        choice = int(input("Please select an option: "))
        if choice == 1:
            new_file(current_set)
        elif choice == 2:
            choose_units()
        elif choice == 3:
            change_filter(sensors, sensor_list, filter_list)
        elif choice == 4:
            print_summary_statistics(current_set, filter_list)
        elif choice == 5:
            print_temp_by_day_time(current_set, filter_list)
        elif choice == 6:
            print_histogram(current_set, None)
        elif choice == 7:
            return (print('Thank you for using the STEM Center Temperature Project'))
        elif choice > 7 or choice < 1:
            print('Error. Please select 1-7.')
        main()
    except ValueError:
        choice = 0
        print("Error. Please enter an integer value.")
        main()


if __name__ == '__main__':
    main()


r'''

'''
