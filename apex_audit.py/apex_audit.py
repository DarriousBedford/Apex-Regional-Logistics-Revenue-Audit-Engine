# apex_audit Exam
# Darrious Bedford

import random
import apex_geometry
import os
import matplotlib.pyplot as plt
import pickle
import apex_models
import apex_dashboard
import apex_database


# Phase I - Console audit core.

QUOTA_THRESHOLD = 50000.0 # dollars
TIER_A_RATE = 0.15 # percantage commission rate
TIER_B_RATE = 0.10 # percantage secondary commission rate
BASE_RATE = 0.05 # percantage fallback rate 
OVER_QUOTA_MULTIPLIER = 1.25 # percantage of performance bonus
FROZEN_LEDGER_CODE = -999.0 # entry that flags a frozon department
MAX_STORES = 10 #largest number of stores
MAX_DEPARTMENTS = 4 #max number of departments
PALLET_CAPACITY = 48 # cartons that fit on one staging pallet
FUEL_SURCHARGE = 2.75 # long haul surcharge per trip
COMPANY_NAME = 'Apex Freight & Supply' # name printed on every report
LEDGER_FILE = 'ledger.txt' # Department ledger written in Phase II
ARCHIVE_PATH = r'C:\Apex\archive\ledger.txt' # windows backup location for the ledger
SNAPSHOT_FILE =  'audit_snapshot.dat' # Pickled audit snapshot written in Phase V
DATABASE_FILE = 'apex.db' # SQLite database created in Phase IX
RESERVED_WORDS = [
            'and', 'as', 'assert', 'async', 'await', 'break', 'class',
            'continue', 'def', 'del', 'elif', 'else', 'except', 'False',
            'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 'raise',
            'return', 'True', 'try', 'while', 'with', 'yield'
        ]
REGIONS  = ['North', 'South', 'East', 'West']
TIER_CODES = ('A', 'B', 'C')
HAZARD_CLASSES = ('HAZMAT',)
audit_run_count = 0

# Input: name a proposed report column name
# returns true if name is a reserved word, otherwise return false

def is_reserved_word(name):
    if name in RESERVED_WORDS:
        return True
    else:
        return False

# input
# returns

def get_store_count():
    # 1. priming read: ask for the store count, convert to int, store it
    store_count = 0

    # 2. while the count is out of range (<= 0 OR > MAX_STORES):
    while store_count <= 0 or store_count > MAX_STORES:
        try:
            store_count = int(input("Enter the number of stores: "))
            if store_count <= 0 or store_count > MAX_STORES:
                print("This is out of range")
        except ValueError:
            print("Please enter a whole number")
            store_count = 0
        
         
    return store_count
# tells if the value falls between a low or high limit
def is_valid_count(value, low, high):
    if value >= low and value <= high:
        return True
    else:
        return False
# ask for the department count and re asks till its in the range
def get_department_count():
    entry = input("Enter the number of departments: ") # ask the user for the number of departments the have
    department_count = int(entry)

    while not is_valid_count(department_count, 1, MAX_DEPARTMENTS):
        print("This is out of the Department Range")
        entry = input("Enter the number of departments: ")
        department_count = int(entry)
    return department_count

def get_tier_code():
    tier_code = input("Enter the tier code: ").strip().upper() # ask use for tier input

    while tier_code !='A' and tier_code !='B' and tier_code !='C': # if the tier input is invalid ask again
        print("Please Enter a Valid tier code")
        tier_code = input("Enter the tier code: ").strip().upper()
    return tier_code

def get_regional_target():
# ask the user for regional target
    regional_target = float(input("Enter your Regional Target: "))

    while regional_target < 0.0:
        print("This Target is Invalid.")
        regional_target = float(input("Enter your Regional Target: "))
    if regional_target == 0.0:
        regional_target = QUOTA_THRESHOLD
    return regional_target
# collect the sales from each store
def collect_store_sales(num_stores, num_departments):
    total_sales = 0.0
    stores_processed = 0
    store_sales = [0.0] * num_stores

    for store in range(1, num_stores + 1):
        store_total = 0.0
        for dept in range(1, num_departments + 1):
            sales = float(input(f'Store {store}, Dept {dept} Sales: '))
            if sales < 0.0:
                if sales == FROZEN_LEDGER_CODE:
                    print(f' Frozen Ledger at Store: {store}, Dept: {dept}')
                    sales = 0.0
                else:
                    sales = 0.0
            append_ledger_entry(store, dept, sales)
            total_sales += sales
            store_total += sales
        store_sales[store - 1] = store_total
        stores_processed += 1
    return total_sales, stores_processed, store_sales
# get the store performance and multiply it by the quota multiplier
def evaluate_store_performance(store_sales, regional_target, tier_code):
    if tier_code == 'A':
        if store_sales >= regional_target:
            effective_rate = TIER_A_RATE * OVER_QUOTA_MULTIPLIER
        else:
            effective_rate = TIER_A_RATE
    elif tier_code == 'B':
        if store_sales >= regional_target:
            effective_rate = TIER_B_RATE * OVER_QUOTA_MULTIPLIER
        else:
            effective_rate = TIER_B_RATE
    else:
        effective_rate = BASE_RATE
    commission_earned = store_sales * effective_rate

    return commission_earned, effective_rate
# display the tier and compare
def display_tier_comparison(total_sales, regional_target):
    for tier in ['A', 'B', 'C']:
        commission, rate = evaluate_store_performance(tier_code = tier, regional_target = regional_target, store_sales = total_sales)
        print(f' Tier {tier} | Commission: ${commission:,.2f}| Rate: {rate:.1%}')
# work out full pallets leftovers and the cartons per store
def compute_logistics_metrics(total_units, store_count):
    full_pallets = total_units//PALLET_CAPACITY
    loose_cartons = total_units%PALLET_CAPACITY
    units_per_store = total_units/store_count
    projected = total_units * (1 + 0.04)**3
    return full_pallets, loose_cartons, units_per_store, projected
# runs a sample ledger to show everyaugmented assignment operator
def apply_ledger_adjustments(amount, store_count, years):
    amount -= 250.0
    amount *= 1.02
    amount /= store_count
    cents = 12345
    cents %= 100
    cartons = 500
    cartons //= PALLET_CAPACITY
    factor = 1.04
    factor **= years

    return amount, cents, cartons, factor
# randomy picks a store and departmentto spot-audit
def select_spot_audit(store_count, department_count):
    random.seed(2024)
    audited_store = random.randint(1, store_count)
    audited_dept = random.randrange(1, department_count + 1)
    recount = random.random() < 0.25
    variance = random.uniform(0.95, 1.05)

    return audited_store, audited_dept, recount, variance
# figures the grid size
def get_rack_size(store_count, department_count):
    rows = store_count + 2
    columns = department_count + 2

    return rows, columns
# prints the rack as a grid the edges then alternatates and bins inside
def build_inventory_matrix(rows, columns):
    for r in range(1, rows + 1):
        for c in range(1, columns + 1):
            if r == 1 or r == rows or c == 1 or c == columns:
                print('[E]', end='')
            else:
                if (r + c)%2 == 0:
                    print('[X]', end='')
                else:
                    print('[O]', end='')
        print()
# prints the banner notice, division and the motto
def display_banner():
    banner = '''
========================================
     Apex's Regional Audit 
========================================
'''
    print(banner)
    notice = """ Confidential: Apex's "internal use only" audit report. """
    print(notice)
    print('Apex Freight & Supply')
    print("Apex's Regional Audit")
    division = 'Commercial ' + 'Operations'
    motto = 'Moving Freight '  'since 1998'
    print(division)
    print(motto)
# prints the formatted report using f strings
def display_audit_report(total_sales, commission_earned, effective_rate, store_count, department_count, total_units, yearly_cartons):
    title = 'Regional Audit Report'
    print('=' * 60)
    print(f'{title:^60}')
    header_rate = f'Commission rate : {effective_rate:.0%}'
    print(f'{header_rate:^60}')
    print('=' * 60)

    label = 'Total Sales:'
    print(f'{label:<22}{total_sales:>14,.2f}')
    label = 'Commission earned:'
    print(f'{label:<22}${commission_earned:>14,.2f}')
    label = 'Effective rate:'
    print(f'{label:<22}{effective_rate:.1%}')

    average = total_sales / store_count
    print(f'Average per store: {average:.2f}')

    print(f'Store count: {store_count:d}')
    print(f'Store column:[{store_count:10}]')

    print(f'Departments audited: {store_count * department_count}')
    print(f'Total cartons: {total_units:,}')
    print(f'Yearly cartons: {yearly_cartons:,d}')

    print(f'Quota: {QUOTA_THRESHOLD:e} | {QUOTA_THRESHOLD:E} | {QUOTA_THRESHOLD:.2e}')

    print(f'Grand total:{total_sales:^18,.2f}')

    print('\nColumn check:\tSales\tRate\n')

    print('Store', 'Dept', 'Sales', sep='\t')
    print('Stores audited:', store_count)

    print(f'Audit trail rate: {effective_rate:%}')

    footer = f'{COMPANY_NAME}' + f' | Stores: {store_count}'
    print(footer)

    signature = f'Prepared for {COMPANY_NAME} ' f'on {store_count} stores'
    print(signature)

    print('Auditor\'s signature: __________')
    print("Status: \"FINAL\"")
    print('Saved to C:\\Apex\\reports')

    net_after_commission = total_sales - \
            commission_earned
    print(f'Net after commission: {net_after_commission:,.2f}',
          f'({effective_rate:.1%} paid out)')
    print('=' *60)
# adds 1 to the global audit run counter
def record_audit_run():
    global audit_run_count
    audit_run_count += 1
    return audit_run_count
# finds the first store and flags as frozen
def find_frozen_store(frozen_flags):
    for index in range(len(frozen_flags)):
        if frozen_flags[index]:
            return index + 1
    return None
# prints whether a frozen store is found           
def report_frozen_store(store):
    if store is None:
        print('No frozen ledgers')
    if store is not None:
        print(f'Frozen ledger found at store {store}')
# placeholder for a future esport
def export_to_erp(total_sales):
    pass

def get_unit_counts():
    total_units = int(input("What is the total carton count?: "))
    yearly_cartons = total_units * 12
    return total_units, yearly_cartons

def get_route_length(dx, dy):
    return apex_geometry.route_distance(dx, dy)


# Phase II The ledger files and the exceptions
# creates a new ledger file
def start_new_ledger():
    ledger = open(LEDGER_FILE,'w')
    ledger.write('Store,Dept,Sales\n')
    ledger.close()
# adds one store, dept, sales line to the end of the ledger closing the file also
def append_ledger_entry(store, dept, sales):
    ledger = open(LEDGER_FILE, 'a')
    try:
        ledger.write(str(store) + ',' + str(dept) + ',' + str(sales) + '\n')
    except IOError as err:
        print(err)
    finally:
        ledger.close()
# reads the ledger back skipping the header and adds up the sales confirms if its a ledger
def read_ledger_total():
    ledger_total = 0.0
    ledger = open(LEDGER_FILE, 'r')
    ledger.readline()
    try:
        for line in ledger:
            line = line.rstrip('\n')
            fields = line.split(',')
            sales = float(fields[2])
            ledger_total += sales
    except ValueError:
        print('Corrupt line found in ledger')
    else:
        print('Ledger is Verified')
    ledger.close()
    return ledger_total
# prints the whole file
def display_ledger_text():
    try:
        ledger = open(LEDGER_FILE, 'r')
        contents = ledger.read()
        print(contents)
        ledger.close()
    except Exception as err:
        print(err)
# averages sales per the department
def average_department_sales(total_sales, department):
    try:
        average = total_sales / department
        return average
    except ZeroDivisionError:
        return 0.0
# delets the old archive and renames the ledger to an archive
def archive_ledger():
    try:
        os.remove('ledger_archive.txt')
    except FileNotFoundError:
        pass
    try:
        os.rename(LEDGER_FILE, 'ledger_archive.txt')
        source = open('ledger_archive.txt', 'r')
        backup = open(ARCHIVE_PATH, 'w')
        backup.write(source.read())
        source.close()
        backup.close()
        print('Ledger Archived')
    except:
        print('Archive step skipped ledger left in place')

# Phase 3 Store collections, dock grids and sales charts
# builds an empty sales list, store name list , and store ID list
def build_store_lists(num_stores):
    store_sales = [0.0] * num_stores
    store_names = []
    for number in range(1, num_stores + 1):
        store_names.append(f'Store {number}')
    store_ids = list(range(1, num_stores + 1))
    return store_sales, store_names, store_ids
# returns one store total or none
def analyze_store_sales(store_sales):
    store_count = len(store_sales)
    first_store = store_sales[0]
    last_store = store_sales[-1]
    lowest = min(store_sales)
    highest = max(store_sales)
    top_store = store_sales.index(highest) + 1
    ranked = store_sales[:]
    ranked.sort()
    ranked.reverse()
    half = store_count // 2
    top_half = ranked[0:half]
    alternating = store_sales[0:len(store_sales):2]
    final_ranking = tuple(ranked)
    return store_count, top_store, final_ranking, alternating
# returns one stores or none
def get_store_figure(store_sales, position):
    try:
        return store_sales[position]
    except IndexError:
        return None
# adds prioritize or remove stores on a list the max is 5
def manage_watch_list(watch_list, store_name, action):
    if action == 'priority':
        watch_list.insert(0, store_name)
    elif action == 'add':
        if store_name not in watch_list:
            watch_list.append(store_name)
    elif action == 'resolve':
        if store_name in watch_list:
            watch_list.remove(store_name)
    if len(watch_list) > 5:
        del watch_list[-1]

    north_list = ['Store 1', 'Store 2']
    south_list = ['Store 3']
    combined = north_list + south_list
    print('Combined watch list:', combined)

    return watch_list
# build a list of each stores commission and a list of store under the quota
def flag_and_project(store_sales):
    commissions = [sales * TIER_A_RATE for sales in store_sales]
    below_quota = [sales for sales in store_sales if  sales < QUOTA_THRESHOLD]
    return commissions, below_quota
# picks a random region and 2 differnt stores
def pick_random_audits(store_names):
    region = random.choice(REGIONS)
    repeat_picks = random.choices(store_names, k=3)
    unique_picks = random.sample(store_names, k=min(2,  len(store_names)))
    return region, repeat_picks, unique_picks
# fills a dock bay grid with random pallet counts
def load_dock_bays():
    bays = [[0,0], [0,0]]
    for row in range(2):
        for col in range(2):
            pallets = random.randint(0, PALLET_CAPACITY)
            bays[row][col] = pallets
    return bays
# writes every store total to store sales txt one per ea line
def save_store_list(store_sales):
    outfile =open('store_sales.txt', 'w')
    outfile.writelines([str(sales) + '\n' for sales in store_sales])
    outfile.close()
# stores the txt back into alist of numbers
def load_store_list():
    infile = open('store_sales.txt', 'r')
    lines = infile.readlines()
    infile.close()
    loaded = [float(line) for line in lines]
    return loaded
# hows a line chart of the sales by the store
def chart_store_sales(store_sales, store_names):
    num_stores = len(store_sales)
    store_ids = list(range(1, num_stores + 1))

    plt.plot(store_ids, store_sales, marker='o')
    plt.title('Sales by Store')
    plt.xlabel('Store')
    plt.ylabel('Sales ($)')
    plt.xlim(xmin=0, xmax=num_stores + 1)
    plt.ylim(ymin=0, ymax=max(store_sales) * 1.1)
    plt.xticks(store_ids, store_names)
    plt.yticks([0, QUOTA_THRESHOLD], ['$0', 'Quota'])
    plt.grid(True)
    plt.show()
# show a bar chart  of commission then a pie chartof the regional share 
def chart_tier_mix(tier_totals):
    left_edges = [0, 10, 20]
    heights = tier_totals
    plt.bar(left_edges, heights, 5, color=('r', 'g', 'b'))
    plt.title('Commission by tier')
    plt.xlabel('Tier')
    plt.ylabel('Commission ($)')
    plt.xticks(left_edges, TIER_CODES)
    plt.show()

    total = sum(tier_totals)
    region_totals = [total * 0.30, total * 0.25, total * 0.25, total * 0.20]
    plt.pie(region_totals, labels=REGIONS, colors=('b', 'g', 'y', 'm'))
    plt.title('Regional Sales Share')
    plt.show()
# calculates what total sales would earn at ea tier
def get_tier_totals(total_sales):
    return [total_sales * rate for rate in (TIER_A_RATE, TIER_B_RATE, BASE_RATE)]
# Phase IV the strings
# cleans one messy manifest line
def clean_manifest_line(line):
    if line.isspace():
        return[]
    line = line.rstrip()
    line = line.replace(';', ',')
    fields = line.split(',')
    fields[0] = fields[0].lstrip('0')
    return fields
# creates a sku line
def validate_sku(sku):
    if not sku.startswith('APX'):
        return False
    if sku.find('-') == -1:
        return False

    parts = sku.split('-')
    if len(parts) != 3:
        return False
    prefix = parts[0]
    number = parts[1]
    region = parts[2]

    if region.islower():
        print('Keying error: region code must be uppercase')
        return False
    if not sku.endswith(('-NW', '-NE', '-SW', '-SE')):
        return False
    if not prefix.isalpha():
        return False
    if not number.isdigit():
        return False
    if not (prefix + number).isalnum():
        return False
    if not region.isupper():
        return False
    return True
# compares two department names while ignoring upper and lowercase letters
def match_department_name(entered, official):
    return entered.lower() == official.lower()
# Phase V dicts, pickle, sets
# builds the department dictionary and rate table handles unkown code and removes d3
def build_department_directory():
    directory = {'D1': 'Bulk Wholesale', 'D2': 'Cold Storage', 'D3': 'Dry Goods'}
    rates = dict()
    rates['D1'] = TIER_A_RATE
    rates['D2'] = TIER_B_RATE
    rates['D3'] = BASE_RATE

    directory['D4'] = 'Hazardous Materials'

    try:
        name = directory['D9']
    except KeyError:
        print('Unknown department code: D9')

    name = directory.get('D9', 'Unassigned')
    del directory['D3']
    return directory, rates
# prints the directory's codes, names and pairs
def summarize_directory(directory, rates):
    codes = list(directory.keys())
    names = list(directory.values())
    print('Codes:', codes)
    print('Names:', names)
    for code, name in directory.items():
        print(f'{code}: {name}')

    high_rates = {code: rate for code, rate in rates.items() if rate > BASE_RATE}

    removed = directory.pop('D2', None)
    directory.popitem()
    rates.clear()
    return high_rates, removed
# compares two carriers' zip codes
def compare_carrier_coverage(north_zips, south_zips):
    north_zips = set(north_zips)
    south_zips = set(south_zips)
    downtown = set(['75201', '75202'])


    north_zips.add('75201')
    north_zips.update(['75202', '75203'])
    north_zips.remove('75203')
    north_zips.discard('99999')

    all_zips = north_zips.union(south_zips)
    all_zips_op = north_zips | south_zips

    shared_zips = north_zips.intersection(south_zips)
    shared_zips_op = north_zips & south_zips

    north_only = north_zips.difference(south_zips)
    north_only_op = north_zips - (south_zips)

    one_carrier = north_zips.symmetric_difference(south_zips)
    one_carrier_op = north_zips^south_zips

    covered = downtown.issubset(north_zips)
    covered_op = downtown <= north_zips

    covers_all = north_zips.issuperset(downtown)
    covers_all_op = north_zips >= downtown

    prefixes = {zip_code[0:3] for zip_code in north_zips}
    return all_zips, shared_zips, north_only
# saves a dictionary run's results to a binary file with a pickle
def save_audit_snapshot(snapshot):
    outfile = open(SNAPSHOT_FILE, 'wb')
    pickle.dump(snapshot, outfile)
    outfile.close()
# loads every single pickled snapshot from the file until the end is reached
def load_audit_snapshots():
    snapshots = []
    infile = open(SNAPSHOT_FILE, 'rb')
    end_of_file = False
    while not end_of_file:
        try:
            snapshot = pickle.load(infile)
            snapshots.append(snapshot)
        except EOFError:
            end_of_file = True
    infile.close()
    return snapshots
# Phase VII Recursion
# adds up a list by calling itself: 
def recursive_total(values, index):
    if index == len(values):
        return 0
    else:
        return values[index] + recursive_total(values, index + 1)
# finds the largest batch size that divides two load evenly recursively
def batch_size(cartons_a, cartons_b):
    if cartons_a % cartons_b == 0:
        return cartons_b
    else:
        return batch_size(cartons_b, cartons_a % cartons_b)
# counts down from a number to 1 by calling itself
def dispatch_countdown(seconds):
    if seconds > 0:
        print(seconds)
        dispatch_countdown(seconds - 1)
    else:
        print('Trucks released')
# same countdown using a loop instead of a recursion
def dispatch_window_countdown():
    for seconds in range(5, 0, -1):
        print(seconds)
    print('Trucks released')

    for attempt in range(3):
        print(f'Scanner read attempt {attempt + 1}')
# Phase IX
# saves every store and its total sales into the sqlite database.
def save_to_database(store_names, store_sales, tier_code):
    for i in range(len(store_names)):
        apex_database.save_store(i + 1, store_names[i], REGIONS[i % len(REGIONS)], tier_code)
        apex_database.save_department(i + 1, 1, store_sales[i])


    


        
    
# call everything to run the project by only calling the functions
def main():
    display_banner()

    store_count = get_store_count()
    department_count = get_department_count()
    tier_code = get_tier_code()
    regional_target = get_regional_target()
    start_new_ledger()
    empty_sales, store_names, store_ids = build_store_lists(store_count)

    total_sales, stores_processed, store_sales = collect_store_sales(store_count, department_count)

    commission_earned, effective_rate = evaluate_store_performance(
        store_sales=total_sales, regional_target=regional_target, tier_code=tier_code)

    total_units, yearly_cartons = get_unit_counts()

    display_audit_report(total_sales, commission_earned, effective_rate,
                         store_count, department_count, total_units, yearly_cartons)
    ledger_total = read_ledger_total()
    display_ledger_text()
    archive_ledger()
    display_tier_comparison(total_sales, regional_target)
    store_count_check, top_store, final_ranking, alternating = analyze_store_sales(store_sales)
    commissions, below_quota = flag_and_project(store_sales)
    region, repeat_picks, unique_picks = pick_random_audits(store_names)
    save_store_list(store_sales)
    chart_store_sales(store_sales, store_names)
    tier_totals = get_tier_totals(total_sales)
    chart_tier_mix(tier_totals)

    directory, rates = build_department_directory()
    high_rates, removed = summarize_directory(directory, rates)
    all_zips, shared_zips, north_only = compare_carrier_coverage(
        ['75201', '75204', '75205'], ['75204', '75205', '75206'])
    save_audit_snapshot({'total_sales': total_sales,
                         'stores': store_count,
                         'commission': commission_earned})
    fleet = apex_models.build_fleet()
    fleet_pay = apex_models.settle_fleet(fleet)

    recursive_sales = recursive_total(store_sales, 0)
    carton_batch = batch_size(total_units, PALLET_CAPACITY)

    apex_database.reset_database()
    apex_database.create_schema()
    save_to_database(store_names, store_sales, tier_code)
    all_stores = apex_database.query_audit_results()
    apex_database.update_and_purge(1, 'B')
    apex_database.regional_join_report()
                      

    full_pallets, loose_cartons, units_per_store, projected = \
        compute_logistics_metrics(total_units, store_count)
    amount, cents, cartons, factor = apply_ledger_adjustments(total_sales, store_count, 3)
    audit_store, audit_dept, recount, variance = select_spot_audit(store_count, department_count)

    rows, columns = get_rack_size(store_count, department_count)
    build_inventory_matrix(rows, columns)

    record_audit_run()
    export_to_erp(total_sales)

    route_length = get_route_length(30, 40)
    apex_dashboard.DispatchDashboard(store_names)

if __name__ == '__main__':
        main()
        

    
          
    
    
    

                        
            
                       
    
        
        
        
        
    
                            
                        


    
                           
        

 
    


