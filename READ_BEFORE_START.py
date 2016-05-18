"""
This programm uses an automated error report.
The send information will only be used to identify and resolve bugs/errors.
During this process nobody except members of developement will gain access to this data.
The data contains the type of error (e.g. I mispelled a variable or divided by 0) and a Trace.
The trace is a path to the current line in the code python was executing as well as the code in that line.
If you have read this and agree to the usage of that data (without any warranty of our side) replace the
0 with a 1.
If you do not agree but still want to use this programm replace 0 with -1
If you select -1 it will mean that we will not collect any data.
Also no bugs you encounter will be fixed if you do not send us the information manually (which you always can)
"""
allow_data_collection = 0
