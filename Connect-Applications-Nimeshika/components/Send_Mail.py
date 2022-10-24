import os
import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import components.log_writer as log_py
import components.read_config_file as read_config
import components.utils as utils_py


now_date_time = datetime.datetime.now()
year = str(now_date_time.strftime("%Y"))
current_month = str(int(str(now_date_time.strftime("%m"))) - 1)
year_month = str(int(str(now_date_time.strftime("%Y%m"))) - 1)


def get_css_styles():

    head = """\
    <html>
        <head>
            <style>
            table, th, td {
                width: 20%;
                border: 1px solid black;
                border-collapse: collapse;
            }
            th#ot, td#ot {
                width: 20%;
                background-color: #FE2D00;
            }
            th#allowance, td#allowance {
                width: 20%;
                background-color: #ffbf00;
            }
            th#total, td#total {
                width: 20%;
                background-color: #32CD32;
            }
            tr#tr01 {
                border: 2px solid black;
                background-color: #f1f1c1;
            }

            </style>
        </head>
    """

    return head


def emp_send_mail(emp, emp_full_name, emp_email, no_of_ot, ot_allowance, no_of_oncall, oncall_allowance, basic, total):

    html_head = get_css_styles()

    html_body = """\
        <body>
            <p>Hi {}!<br>
            Here is your salary slip for the month of {} in {}
            </p>
            <br> <br>
    """.format(emp_full_name, current_month, year)

    table_head = "<table><tr><th></th><th>No of Hours</th><th>Allowance</th></tr>"

    ot_row = "<tr> " \
             "<td>OT</td> " \
             "<td>" + str(no_of_ot) + "</td>" \
             "<td>" + str(ot_allowance) + "</td>" \
             "</tr>"

    oncall_row = "<tr> " \
                 "<td>Oncall</td> " \
                 "<td>" + str(no_of_oncall) + "</td>" \
                 "<td>" + str(oncall_allowance) + "</td>" \
                 "</tr>"

    basic_row = "<tr> " \
                "<td colspan=\"2\"> Basic Salary</td>" \
                "<td>" + str(basic) + "</td>" \
                "</tr>"

    total_row = "<tr id = \"tr01\"> " \
                "<td colspan=\"2\"> Total Salary</td>" \
                "<td>" + str(total) + "</td>" \
                "</tr>"

    end_html = "</table></body></html>"

    salary_table = table_head + ot_row + oncall_row + basic_row + total_row
    html_page = html_head + html_body + salary_table + end_html

    html_file_name = emp+".html"
    log_py.info("Salary slip saved to {}".format(html_file_name))
    hs = open(html_file_name, 'w')
    hs.write(html_page)

    emp_subject = "Salary Slip for the month of {}/{}".format(year, current_month)
    send_mail(emp_email, emp_subject, html_page)


def manager_mail(records, manager_name, manager_email):

    html_head = get_css_styles()

    html_body = """\
            <body>
                <p>Hi {}!<br>
                Here is Salary Report for the month of {} in {}
                </p>
                <br> <br>
        """.format(manager_name, current_month, year)

    table_head = "<table>" \
                 "<tr><th> Employee Name </th>" \
                 "<th id = \"ot\">No of OT Hours</th>" \
                 "<th>No of On Call Hours</th>" \
                 "<th id = \"allowance\">Total Allowance</th>" \
                 "<th id = \"total\">Total Salary</th></tr>"

    report_table = table_head

    for emp in records:

        emp_full_name = emp[0]
        ot_hours = emp[1]
        oncall_houres = emp[2]
        allowance = emp[3]
        total = emp[4]

        one_row = "<tr> <td>{}</td> " \
                  "<td id = \"ot\"> {} </td> " \
                  "<td> {} </td> " \
                  "<td id = \"allowance\"> {} </td> " \
                  "<td id = \"total\"> {} </td> </tr>".format(emp_full_name, ot_hours, oncall_houres, allowance, total)

        report_table = report_table + one_row

    end_html = "</table></body></html>"
    html_page = html_head + html_body + report_table + end_html

    html_file_name = "SalaryReport_{}.html".format(year_month)
    # log_py.info("Salary slip saved to {}".format(html_file_name))
    hs = open(html_file_name, 'w')
    hs.write(html_page)

    report_subject = "Salary Report for the month of {}/{}".format(year, current_month)
    send_mail(manager_email, report_subject, html_page)


def send_mail(to, subject, body):

    sender_email = read_config.ReadConfig().get_one_option('MANAGER_DETAILS', 'email_sender')
    log_py.info("Sending email to the employee")
    mail_l(sender_email, to, subject, body)
    # mail_w(sender_email, to, body)


def mail_w(from_mail, to_mail, body):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = from_mail
    receiver_email = to_mail
    password = "abc_123_abc"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')

    # Record the MIME types of both parts - text/plain and text/html.
    part = MIMEText(body, 'html')
    msg.attach(part)
    body = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, body)


def mail_l(from_mail, to_mail, subject, body):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = to_mail

    # Record the MIME types of both parts - text/plain and text/html.
    part = MIMEText(body, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part)

    body = msg.as_string()

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(from_mail, to_mail, body)
    s.quit()
