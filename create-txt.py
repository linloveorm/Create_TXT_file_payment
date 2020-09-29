import datetime
import requests
import json
import os

os.chdir('D:\\KBank')



def get_account():
    URL_account_payable_sort = "https://api.airtable.com/v0/appPPfFjCC9DChJWc/Account%20Payable?api_key=keyuZ9jZifvOzDgPO&sort[0][field]=Payable%20ID"
    account_payable_sort = requests.get(URL_account_payable_sort)
    payable_sort = account_payable_sort.json()
    lists = []
    offset = payable_sort['offset']

    # print(lists)
    lists = payable_sort['records']

    while len(payable_sort['records']) == 100 :
        URL_account_payable_sort_offset = URL_account_payable_sort +"&offset="+offset
        account_payable_sort = requests.get(URL_account_payable_sort_offset)
        payable_sort = account_payable_sort.json()
        if 'offset' in payable_sort:
            offset = payable_sort['offset']
        lists += payable_sort['records']
        # print(len(lists))

    return lists

def search_acc(id):
    all_list = get_account()
    k = 0
    while k < len(all_list):
        if id == all_list[k]['id']:
            #print(all_list)
            return all_list[k]['fields']['Bank Account Number'],all_list[k]['fields']['Bank Account Name'],all_list[k]['fields']['Payable ID'],all_list[k]['fields']['Bank'],all_list[k]['fields']['Payable ID']
        else:
            k += 1


def set_zero(ln,num):
    
    if ln != num:
        z = "0"
        nm = num-ln
        while len(z) <= nm:
            z += "0"
    return z 



date = datetime.datetime.now()
date_mcl = datetime.date.today()



URL_payment_log = "https://api.airtable.com/v0/appPPfFjCC9DChJWc/Payment%20Log?api_key=keyuZ9jZifvOzDgPO"
URL_payment_status = "https://api.airtable.com/v0/appPPfFjCC9DChJWc/Payment%20Log?api_key=keyuZ9jZifvOzDgPO&view=Gen%20Text%20File&sort[0][field]=Payment%20Status"


URL_account_payable = "https://api.airtable.com/v0/appPPfFjCC9DChJWc/Account%20Payable?api_key=keyuZ9jZifvOzDgPO"

URL_account_payable_sort = "https://api.airtable.com/v0/appPPfFjCC9DChJWc/Account%20Payable?api_key=keyuZ9jZifvOzDgPO&sort[0][field]=Payable%20ID"

payment_log = requests.get(URL_payment_log)
payment_status_sort = requests.get(URL_payment_status)
account_payable = requests.get(URL_account_payable)
account_payable_sort = requests.get(URL_account_payable_sort)


data = payment_log.json()
sort = payment_status_sort.json()
payable = account_payable.json()
payable_sort = account_payable_sort.json()


#Account number
acc = "0341349230"

#Batch Ref
batch = "000000"
date_1 = datetime.datetime.today() + datetime.timedelta(days=2)
# month_mcl = date_1.month
# date_mcl = date_1.date
# year_mcl = date_1.year
# NextDay_Date_Formatted = date_1.strftime ('%d%m%Y') # format the date to ddmmyyyy

#set date and payment date       
today = date.strftime("%y")+date.strftime("%m")+date.strftime("%d")
today_MCL = date_1.strftime ('%d-%m-%Y')

#set account name
account_name = "มหาวิทยาลัยซีเอ็มเคแอล"

#set Total Credit Items
total_credit_dct = 0

#set check payment status
check = 0
count = 0
record_l = len(sort['records'])
status = ""

#status of payment
for i in range(record_l):
    payment_status = sort['records'][i]['fields']
    if 'Payment Status' in payment_status:   
        count += 1     
    else:
        status = "False"
        check += 1



c = 0 
paid_to = payable_sort['records']
paid_sort1 = payable_sort['records']

list_paid = ""
paid_i = 0
d = 0
idx = 0
p = "D"

#Paid Amount
paid_data_DCT = 0
paid_data_MCL = 0
paid_dct = 0
paid_MCL = 0
print(status)
for paid_itr in range(check):
    acc_approve_check = sort['records'][paid_itr]['fields']
    # if 'Approved By' in acc_approve_check :
        # paid = sort['records'][paid_itr]['fields']['Paid Amount']
    types = sort['records'][paid_itr]['fields']['Payment Type']
    if types == "Direct Credit (DCT)":
        # types = "HDCT"
        # print(types)
        if status == "False":
            paid_dct = sort['records'][paid_itr]['fields']['Paid Amount']
            paid_data_DCT += paid_dct
            print("DCT : "+str(paid_data_DCT))
    elif types == "Smart Credit Next Day (MCL)":
        # print(types)
        if status == "False":
            paid_MCL = sort['records'][paid_itr]['fields']['Paid Amount']
            paid_data_MCL += paid_MCL
            print("MCL : "+str(paid_data_MCL))
    # else:
    #    pass

# print(paid_data_DCT)
# print(paid_data_MCL)
# print(paid_data)
# str_paid_MCL = str()

#length of Paid Amount
# paid_l = len(str(paid_data_DCT))+1

#print paid amount
# zr = set_zero(paid_l,13)        
# paid_amount = zr+str(round(paid_data_DCT*100))

#Defind variable DCT
strs = ""
total_MCL = 0
str_Detail_MCL = ""
types_mcl = ""
types = ""
types_dct = ""

#Defind variable MCL

amount_mcl = ""
acc_id_mcl = 0
str_cut = ""
bank_name = ""
bank_id = ""

check_approve = []


for d in range(check):
    acc_approve = sort['records'][d]['fields']
    if 'Entered by' in acc_approve :
        types = sort['records'][d]['fields']['Payment Type']
        #Setup Type DCT
        if types == "Direct Credit (DCT)":
            types_dct = "HDCT"
            if status == "False":
                # list_id = 0
                c += 1 #ลำดับที่ของรายการ
                #print amount of list
                f = open(types_dct+today+".txt","w+")
                zero = set_zero(len(str(c)),17)
                amount_list = zero+str(c)+"N"
                
                #Header & Part Identifier
                # print(paid_amount)
                f.write(types_dct+(' '*16)+batch+(' '*14)+acc+" "+str(round(paid_data_DCT*100)).rjust(15,'0')+" "+today+(' '*25)+account_name.ljust(50,' ')+today+amount_list+(' '*5)+"\n")
                
                zer = set_zero(len(str(c)),5)

                sort_am = sort['records'][d]['fields']

                amount = round(sort_am['Paid Amount']*100)
                
                amount_zero = set_zero(len(str(amount)),14)
                
                acc_id = sort_am['Paid To'][0]
                #searching Bank Account Number, Bank Account Name, Payable ID, Bank
                [acc_num,acc_name,acc_ids,acc_bank,acc_ref] = search_acc(acc_id)               
            
                #Setup Detail 
                strs += (p+zer+str(c)+"              "+acc_num+" "+amount_zero+str(amount)+" "+today+"                         "+acc_name.ljust(50,' ')+today+"000"+str(acc_ids).ljust(16,' ')+(' '*151)+('0'*10)+"."+('0'*12)+"."+('0'*2)+(' '*156)+"\n")
                # print(strs)

        #Setup Type SCND
        elif types == "Smart Credit Next Day (MCL)":
            types_mcl = "HMCL"
            if status == "False":
                total_MCL += 1
                f2 = open(types_mcl+today+".txt","w+")
                f2.write(types_mcl+acc+(' '*16)+today_MCL+(' '*5)+str(total_MCL).rjust(18,'0')+(str("{:.2f}".format(paid_data_MCL))).rjust(18,'0')+"N"+"\n")

                sort_am_mcl = sort['records'][d]['fields']
                amount_mcl = sort_am_mcl['Paid Amount']
                # payment_id = payable_sort['records'][d]['fields']['Payable ID']
                print("MCL")

                acc_id_mcl = sort_am_mcl['Paid To'][0]
                [acc_mcl_num,acc_mcl_name,acc_mcl_id,acc_mcl_bank,acc_mcl_ref] = search_acc(acc_id_mcl)
                str_cut = str(acc_mcl_num)[:3]

                if acc_mcl_bank == "Kasikorn Bank":
                    types = "Direct Credit (DCT)"
                elif acc_mcl_bank == "Thanachart":
                    bank_id = "065"
                elif acc_mcl_bank == "Siam Commercial Bank":
                    bank_id = "014"
                elif acc_mcl_bank == "Krungsri Bank":
                    bank_id = "025"
                elif acc_mcl_bank == "Krungthai Bank":
                    bank_id = "006"
                elif acc_mcl_bank == "TMB":
                    bank_id = "011"
                elif acc_mcl_bank == "BBL":
                    bank_id = "002"
                elif acc_mcl_bank == "KIATNAKIN":
                    bank_id = "069"
                elif acc_mcl_bank == "JPMORGAN CHASE":
                    bank_id = "008"
                elif acc_mcl_bank == "SUMITOMO MITSUI BANKING CORPORATION":
                    bank_id = "018"
                elif acc_mcl_bank == "Citi Bank":
                    bank_id = "017"
                elif acc_mcl_bank == "CIMB THAI":
                    bank_id = "022"
                elif acc_mcl_bank == "DEUTSCHE BANK":
                    bank_id = "032"
                elif acc_mcl_bank == "THE ROYAL BANK OF SCOTLAND N.V.":
                    bank_id = "005"
                elif acc_mcl_bank == "TISCO":
                    bank_id = "067"
                elif acc_mcl_bank == "THE THAI CREDIT RETAIL":
                    bank_id = "071"
                elif acc_mcl_bank == "THAILAND":
                    bank_id = "001"
                elif acc_mcl_bank == "AGRICULTURE AND AGRICULTURAL COOPERATIVES":
                    bank_id = "034"
                elif acc_mcl_bank == "MIZUHO CORPORATE":
                    bank_id = "039"
                elif acc_mcl_bank == "MEGA  INTERNATIONAL COMMERCIAL":
                    bank_id = "026"
                elif acc_mcl_bank == "UNITED OVERSEAS(UOB)":
                    bank_id = "024"
                elif acc_mcl_bank == "LAND AND HOUSES RETAIL":
                    bank_id = "073"
                elif acc_mcl_bank == "STANDARD CHARTERED (THAI)":
                    bank_id = "020"
                elif acc_mcl_bank == "ICBC":
                    bank_id = "070"
                elif acc_mcl_bank == "AMERICA NATIONAL ASSOCIATION":
                    bank_id = "027"
                elif acc_mcl_bank == "THE GOVERNMENT SAVINGS":
                    bank_id = "030"
                elif acc_mcl_bank == "THE GOVERNMENT HOUSING":
                    bank_id = "033"
                elif acc_mcl_bank == "ISLAMIC OF THAILAND":
                    bank_id = "066"
                elif acc_mcl_bank == "THE HONGKONG AND SHANGHAI BANKING CORPORATION":
                    bank_id = "031"
                elif acc_mcl_bank == "CHINESE BANK":
                    bank_id = "052"
                elif acc_mcl_bank == "INZ(THAILAND)":
                    bank_id = "079"
                elif acc_mcl_bank == "BNP Paribas":
                    bank_id = "045"
                # print(bank_id)
                

                str_Detail_MCL += ("D"+(str(total_MCL)).rjust(5,'0')+(' '*5)+str("{:.2f}".format(amount_mcl)).rjust(13,'0')+acc_mcl_name.ljust(80,' ')+(' '*30)+(' '*30)+(' '*30)+(' '*30)+str(acc_mcl_num).rjust(20,'0')+str(acc_mcl_ref).ljust(16,' ')+(' '*13)+str_cut.ljust(4,' ')+bank_id+(' '*255)+(' '*10)+(' '*50)+(' '*1)+(' '*50)+(' '*50)+('0'*10)+"."+('0'*12)+"."+('0'*2)+(''*13)+('0'*3)+"\n")
                # print(str_Detail_MCL)
    

# print Detail DCT        
f = open(types_dct+today+".txt","a")
f.write(strs)

# print Detail MCL
f2 = open(types_mcl+today+".txt","a")
f2.write(str_Detail_MCL)


f.close()
f2.close()


