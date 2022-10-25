# IPC Application User Manual

Version 1.0

Author: Nimeshika Ranasinghe

Date: 2022/10/25


## Description:

This program is used for inter-processes communication between applications inside the same machine that does the following task.
-	Application A (MonitorChanges) monitors the changes to a file that contains surrounding Wireless APs in JSON format and informs application B
-	Application B (DisplayChanges) is responsible for displaying the changes that are one to the JSON file.


## Prerequisites:

1.	Python3 should be configured in the server.
`sudo apt-get install python3.6`


## Run:

1.	Download the application from git

`git clone https://github.com/nimeshikaranasinghe/IPC_Coding-Exercise.git `

2.	Go inside the app folder

`cd Connect-Applications-Nimeshika`

3.	Configure ‘File_Configs.ini’ file with the correct details

4.	Run ‘DisplayChanges.py’ script in the background

`python3 DisplayChanges.py &`

5.	Run ‘MonitorChanges.py’ to get the terminal output of the changes

`python3 MonitorChanges.py`



## Configuration file 
#### Connect-Applications-Nimeshika/src/ File_Configs.ini’

x.	‘CHECK_FILE_DETAILS’ section
  -	‘file_name’ – Wireless APs in JSON file’s name. If the file is a separate location specify the absolute file path 
  -	‘read_wait_time’ – How much time do you need to wait until the next JSON check

y.	‘CONNECTION_DETIALS’ section
  -	‘hostname’ – Hostname of the server
  -	‘port’ -  Port number that is used to do the communication

z.	‘PATHS’ section
  -	‘log_path’ = Define the logs folder

 
