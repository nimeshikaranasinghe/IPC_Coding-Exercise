import threading
import subprocess
import sys
import os
import zipfile
import shutil

import components.log_writer as log_Py
import components.read_config_file as config_ini


log_file = log_Py.log_file


def wait_for_process(proc):

    out_list = []
    err_list = []
    out_t = threading.Thread(target=_read_stream, args=(proc.stdout, out_list))
    out_t.start()
    err_t = threading.Thread(target=_read_stream, args=(proc.stderr, err_list))
    err_t.start()
    proc.wait()
    out_t.join()
    err_t.join()
    proc.stderr = err_list
    proc.stdout = out_list


def _read_stream(stream, output: []):
    """ parallelly read subprocess stdout and stderr """

    if stream:
        for line in stream:
            line = line.strip()
            if line:
                output.append(line)


def call_ini_file_methods():
    """ make common object to call Read_ini_File methods """

    read_configs = config_ini.ReadConfig()
    return read_configs


def create_local_directory(dir_path):
    """ create local temp directory """

    cmd = ['mkdir', '-p', dir_path]
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    wait_for_process(proc)
    execute_cmd = " ".join(cmd)

    if proc.returncode != 0:
        log_Py.error("Unable to create local dir {}".format(dir_path))
        log_Py.error("Command executed => " + execute_cmd)
        log_Py.error(" ".join(proc.stderr))
        sys.exit(-1)
    else:
        log_Py.info("Directory named - " + dir_path + " is created")
        log_Py.info("Command executed => " + execute_cmd)


def execute_remote_command(ssh_string, cmd_list):
    """ execute remote command and return results """

    cmd = ['ssh',
           '-oStrictHostKeychecking=no',
           '-oNumberOfPasswordPrompts=0',
           ssh_string] + cmd_list

    proc = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    wait_for_process(proc)

    execute_cmd = " ".join(cmd_list)

    if proc.returncode != 0:
        log_Py.error("Unable to run the remote command")
        log_Py.error("Command executed => " + execute_cmd)
        log_Py.error(" ".join(proc.stderr))
        sys.exit(-1)
    else:
        cmd_ouptput = proc.stdout  # get output
        log_Py.info("Successfully executed remote command on - " + ssh_string)
        log_Py.info("Command executed => " + execute_cmd)
        log_Py.info("Remote command output => {}".format(cmd_ouptput))
        return cmd_ouptput


def execute_local_command(cmd_list):
    """ execute local command and return results """

    cmd = cmd_list

    proc = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    wait_for_process(proc)

    execute_cmd = " ".join(cmd_list)

    if proc.returncode != 0:
        log_Py.error("Unable to run the local command")
        log_Py.error("Command executed => " + execute_cmd)
        log_Py.error(" ".join(proc.stderr))
        sys.exit(-1)
    else:
        cmd_ouptput = proc.stdout  # get output
        log_Py.info("Successfully executed local command")
        log_Py.info("Command executed => " + execute_cmd)
        log_Py.info("Local command output => {}".format(cmd_ouptput))
        return cmd_ouptput


def scp_file(ssh_string, source_folder_file_name, destination_folder):
    """ Copy file from another server to local machine"""

    # scp -r hasith@172.25.93.35:sourceLocation/file_folder_name destination
    sub_cmd = ssh_string + ":" + source_folder_file_name
    cmd = ['scp', '-r', sub_cmd, destination_folder]

    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    wait_for_process(proc)
    execute_cmd = " ".join(cmd)

    if proc.returncode != 0:
        log_Py.error("Unable to copy file - " + source_folder_file_name + "to the location - " + destination_folder)
        log_Py.error("Command executed => " + execute_cmd)
        log_Py.error(" ".join(proc.stderr))
        sys.exit(-1)
    else:
        log_Py.info(source_folder_file_name + " - File is copied to the location - " + destination_folder + " from " + ssh_string)
        log_Py.info("Command executed => " + execute_cmd)


