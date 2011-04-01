import numpy
import re

# This class is a line reader, which is used to parse lines from ~ASCII LOGS section of the LAS file

class line_reader:
    def __init__(self):
        self.counter = 0
        self.depth_line = True
        self.current_line = 0

    def read_line(self, line, las_info):

        # if file is not wrapped, we know the exact number of values and can use pre-initialized arrays
        if las_info['version']['WRAP'] == 'NO':
            counter = 0
            line = line.lstrip()            # remove whitespaces from the beginning
            values = re.split(r'[ \t\r\n]+', line)  # split line in tokens by spaces and tabs
            for log_value in values:
                if len(log_value) > 0:
                    las_info['logs'][ las_info['curves_order'][counter] ][self.current_line] = float(log_value)
                    counter+=1
        #   print line
        #   print values

        # if it is wrapped, we need to use append function, because result size is a mistery :)
        else:
            line = re.sub(r'\n','',line)        # remove \n
            line = line.lstrip()            # remove whitespaces from the beginning
            values = re.split(r'[ \t]+', line)  # split line in tokens by spaces and tabs

            # in wrapped mode, we need to check out is this a DEPTH line or not - to parse it in a right way
            # DEPTH line has one value in wrapped mode

            if self.depth_line == True:
                # DEPTH line
                las_info['logs'][ las_info['curves_order'][0] ] = numpy.append(las_info['logs'][ las_info['curves_order'][0] ], float(values[0]))
                self.depth_line = False
            else:
                # Line with values
                for log_value in values:
                    self.counter+=1
                    las_info['logs'][ las_info['curves_order'][self.counter]] = numpy.append(las_info['logs'][ las_info['curves_order'][self.counter]], float(log_value))
                    if self.counter >= len(las_info['curves_order'])-1:
                        self.counter = 0
                        self.depth_line = True
        self.current_line += 1
