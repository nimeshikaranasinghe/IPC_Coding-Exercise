import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import components.log_writer as log_py
import components.read_config_file as read_config
import components.utils as utils_py
import components.Send_Mail as mail_py
import components.Connect_Mysql as connect_db_py


read_configs = read_config.ReadConfig()

now_date_time = datetime.datetime.now()

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonth.strftime("%Y%m")
file_date = str(lastMonth.strftime("%Y%m%d"))

current_month = str(int(str(now_date_time.strftime("%Y%m"))) - 1)

employee_list = read_configs.get_one_option("EMPLOYEES", "employee_names").split(",")   # get the employee list and split it
employees_with_csv = []
employees_without_csv = []
csv_file_names = []

employee_csv_location = read_configs.get_one_option("PATHS", 'user_csv_location')
csv_files_path = read_configs.get_one_option("PATHS", "management_csv_location")
temp_dir_path = os.path.join(csv_files_path, current_month)

src_files_location = read_configs.get_one_option("PATHS", "src_files")
script_name = read_configs.get_one_option("FILE_NAMES", "file_checker")
csv_file_checker = os.path.join(src_files_location, script_name)

employee_name = ''
employee_ssh_string = ''
source_csv_file = ''

emp_full_name = ''
emp_email = ''
emp_basic = 0.00
no_of_ot_hours = 0
ot_allowance = 0.00
no_of_oncall_hours = 0
oncall_allowance = 0.00
total_allowance = 0.00
total_salary = 0.00


def scp_csv_files(csv_file_name):
    """ scp employee salary file to management server """

    global temp_dir_path, employees_with_csv, employees_without_csv, employee_name, source_csv_file, script_name, \
        employee_ssh_string, csv_file_names, csv_file_checker, employee_csv_location

    # Check if file exist in the user environment
    log_py.info("Checking for csv file existence in user environment")
    return_code = check_for_csv_file(employee_ssh_string, source_csv_file)

    if return_code == '0':
        # file exist

        log_py.info("{} exist in user: {} environment".format(csv_file_name, employee_name))
        employees_with_csv.append(employee_name)
        csv_file_names.append(csv_file_name)

        # scp csv file to management server
        log_py.info("Scp {} user csv file".format(employee_name))
        utils_py.scp_file(employee_ssh_string, source_csv_file, temp_dir_path)

    elif return_code == '1':
        # file doesn't exist

        log_py.error("Cannot find {} file in: {} user environment".format(csv_file_name, employee_name))
        employees_without_csv.append(employee_name)

        # scp bash script to user env
        # scp test.sh nimeshikar@172.25.72.50:
        log_py.info("csv_file_checker copied to {} user environment".format(employee_name))
        scp_cmd = ['scp', csv_file_checker, employee_ssh_string + ":"]
        utils_py.execute_local_command(scp_cmd)

        # change execution permission of the bash script
        # chmod 777 scriptname
        log_py.info("Changing execution permission of the the csv_file_checker")
        chmod_cmd = ['chmod', '755', script_name]
        utils_py.execute_remote_command(employee_ssh_string, chmod_cmd)

        # add entry in .bash profile
        # echo "source csv_file_checker source_csv_file employee_name" >> .bash_profile
        log_py.info("Added entry in .bash_profile")
        cmd2 = ['echo', '\"source', script_name, employee_csv_location, employee_name + "\"", ">>", ".bash_profile"]
        utils_py.execute_remote_command(employee_ssh_string, cmd2)


def check_for_csv_file(emp_ssh, csv_file_path):
    """ Check if file exist in the user environment """

    #  [ -f ~/data/salary/<name_date>.csv ] && echo "0" || echo "1"
    cmd = ['[', '-f', csv_file_path, ']', '&&', 'echo', '\"0\"', '||', 'echo', '\"1\"']
    output = utils_py.execute_remote_command(emp_ssh, cmd)
    return_code = output[0]

    return return_code


def calculate_salary(emp_sal_file):
    """ Calculate salary """

    global emp_full_name, emp_email, emp_basic, no_of_ot_hours, ot_allowance, no_of_oncall_hours, oncall_allowance, \
        total_allowance, total_salary

    # reset the value for new employee.
    emp_full_name = ''
    emp_email = ''
    emp_basic = 0.00
    no_of_ot_hours = 0
    ot_allowance = 0.00
    no_of_oncall_hours = 0
    oncall_allowance = 0.00
    total_allowance = 0.00
    total_salary = 0.00

    # consider each line in the file
    for b in range(len(emp_sal_file)):

        one_record = emp_sal_file[b].split(',')

        if b == 0:
            # define employee full name
            emp_full_name = one_record[1]

        elif b == 1:
            # define employee email
            emp_email = one_record[1]

        elif b == 2:
            # define employee basic salary
            emp_basic = one_record[1]

        elif b > 3:
            # calculate total allowance for ot and oncall
            no_of_ot_hours = no_of_ot_hours + int(one_record[1])
            ot_allowance = ot_allowance + float(one_record[2])
            no_of_oncall_hours = no_of_oncall_hours + int(one_record[3])
            oncall_allowance = oncall_allowance + float(one_record[4])

    # calculate total allowance
    total_allowance = total_allowance + ot_allowance + oncall_allowance
    print("Total Allowance: {}".format(str(total_allowance)))
    total_salary = float(emp_basic) + total_allowance
    print("Total Salary: {}".format(str(total_salary)))


# ===================

print("Main started")

# create temp directory to store employee csv files
log_py.info("Creating temp directory to store employee csv files")
utils_py.create_local_directory(temp_dir_path)

# scp salary files to management server
log_py.info("Copying .csv salary files to management server")
for i in range(len(employee_list)):

    employee_name = employee_list[i].strip()  # remove white spaces in name
    log_py.info("Considering user: {}".format(employee_name))

    employee_ssh_string = read_configs.get_one_option("EMPLOYEES_SSH_STRINGS", employee_name)
    file_name = employee_name + "_" + file_date + ".csv"
    source_csv_file = os.path.join(employee_csv_location, file_name)

    scp_csv_files(file_name)

# calculate salary and send email for each employee
log_py.info("Reading csv file and Calculating salary for each employee")
for a in range(len(employees_with_csv)):

    # define csv file path in management server
    csv_file = os.path.join(temp_dir_path, csv_file_names[a])
    file_content = []

    # read csv file and obtain each line to a list
    log_py.info("Reading csv file of employee: {}".format(employees_with_csv[a]))
    with open(csv_file, 'r') as f:
        for line in f:
            file_content.append(line)

    log_py.info("Calculating salary for the employee: {}".format(employees_with_csv[a]))
    calculate_salary(file_content)

    log_py.info("Sending email to the employee")
    mail_py.emp_send_mail(employees_with_csv[a], emp_full_name, emp_email, no_of_ot_hours, ot_allowance,
                          no_of_oncall_hours, oncall_allowance, emp_basic, total_salary)

    log_py.info("Adding salary details to database")
    insert_salary = "INSERT INTO EMPLOYEE_SALARY(USER_NAME, EMAIL, FULL_NAME, OT_HOURS, ONCALL_HOURS, ALLOWANCE, " \
                    "TOTAL, MONTH) VALUES(\"{}\", \"{}\", \"{}\", {}, {}, {}, {}, {})".format(employees_with_csv[a],
                                                                                              emp_email,
                                                                                              emp_full_name,
                                                                                              no_of_ot_hours,
                                                                                              no_of_oncall_hours,
                                                                                              total_allowance,
                                                                                              total_salary,
                                                                                              current_month)
    connection = connect_db_py.connect_db()
    connect_db_py.insert_query(insert_salary, connection)
    connect_db_py.close_connection(connection)


# select data from database and send email to manager
log_py.info("Selecting Salary details for the month of {}".format(current_month))
connection = connect_db_py.connect_db()
select_query = "SELECT FULL_NAME, OT_HOURS, ONCALL_HOURS, ALLOWANCE, TOTAL FROM EMPLOYEE_SALARY WHERE MONTH={};".format(current_month)
records = connect_db_py.select_query(select_query, connection)
connect_db_py.close_connection(connection)

# send email to the manager
log_py.info("Sending email to the manager")
manager_name = read_configs.get_one_option("MANAGER_DETAILS", "name")
manager_email = read_configs.get_one_option("MANAGER_DETAILS", "email")
mail_py.manager_mail(records, manager_name, manager_email)
