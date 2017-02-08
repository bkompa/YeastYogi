#!/usr/bin/env python
# BrownianXMLtoTIFF.py
# Author: Joseph K. Aicher
# Summary: A script that runs through a folder containing Microscope Simulator
#  formatted XML files from ParseBrownian and exports each file to a TIFF file 
#  containing the z-stack. Has an option to rename them according to the ordering
#  that makes for easy import as an image sequence in ImageJ.

from __future__ import print_function # imports print statement syntax from Python 3

import sys
import os
import glob
import subprocess
import time

USAGE_STR = '''USAGE:
{program_name} [args] input_folder
        input_folder: the folder containing the XML files we are generating TIFF files from
        [args]: 
          [-red]: enables saving red color channel
          [-green]: enables saving green color channel
          [-blue]: enables saving blue color channel
          [-simulator path]: specifies the path of Microscope Simulator
          [-out folder]: specifies the folder to output TIFF files to
          [-norename]: prevents automatic rename of files that look like output to have ordering on end
          [-h],[-help]: prints out usage information and exits
'''

class commandParams :
    # initialize commandParams with arguments
    def __init__ ( self, arguments ) :
        # get name of the script
        self.name = arguments[0]
        # we must have at least one argument in addition to the name of the script
        if not ( len( arguments ) > 1 ) :
            print( 'Too few arguments.' )
            print( USAGE_STR.format( program_name = self.name ) )
            sys.exit( -1 )

        # path of Microscope Simulator
        self.microscope_path = "C:\\Program Files (x86)\\CISMM\\Microscope Simulator 2.3.0\\bin\\MicroscopeSimulator.exe"
        # do we include red, green blue channels in output?
        self.red = False
        self.green = False
        self.blue = False
        # folder to output TIFF stacks to?
        self.output_folder = "output_tiff"
        # rename enabled?
        self.rename = True
        # folder to obtain TIFF files from
        self.input_folder = os.path.realpath( sys.argv[-1] )

        # loop through arguments
        for i in range( 1, len( arguments ) - 1 ) :
            if arguments[i] == '-red' or arguments[i] == '-r' :
                self.red = True
            elif arguments[i] == '-green' or arguments[i] == '-g' :
                self.green = True
            elif arguments[i] == '-blue' or arguments[i] == '-b' :
                self.blue = True
            elif arguments[i] == '-simulator' :
                self.microscope_path = os.path.realpath( sys.argv[i+1] )
            elif arguments[i] == '-out' :
                self.output_folder = arguments[i+1]
            elif arguments[i] == '-norename' :
                self.rename = False
        # end loop through arguments

        # make sure that microscope_path is a file
        if not os.path.isfile( self.microscope_path ) :
            print( "'{}' is not a file".format( self.microscope_path ) )
            print( USAGE_STR.format( program_name = self.name ) )
            sys.exit( -2 )
        
        # make sure that input_folder is a folder
        if not os.path.isdir( self.input_folder ) :
            print( "'{}' is not a directory".format( self.input_folder ) )
            print( USAGE_STR.format( program_name = self.name ) )
            sys.exit( -3 )
        
        # deal with output_folder
        self.output_folder = os.path.realpath( self.output_folder )
        if os.path.isfile( self.output_folder ) :
            print( "'{}' is an already existing file".format( self.output_folder ) )
            print( USAGE_STR.format( program_name = self.name ) )
            sys.exit( -4 )
        if not os.path.isdir( self.output_folder ) :
            os.mkdir( self.output_folder )

        # if after reading all flags, red, green and blue unchanged, then all True
        if not (self.red or self.green or self.blue) :
            self.red = True
            self.green = True
            self.blue = True

        # make list with the red green blue flags
        self.rgb_flags = []
        if self.red : self.rgb_flags.append( '--red' )
        if self.green : self.rgb_flags.append( '--green' )
        if self.blue : self.rgb_flags.append( '--blue' )

        # get list of XML files in input_folder
        self.file_list = glob.glob( os.path.join( self.input_folder, '*.xml' ) )
        # we are going to sort by the integer after the last _ in each file name
        getval = lambda x : int( x.split('_')[-1].split('.')[0] )
        # sort by the number
        self.file_list.sort( key = getval )

        self.values = [ getval( x ) for x in self.file_list ]

        # generate list that will be what we want our outfiles to be named
        self.out_list = [ os.path.join( self.output_folder, 
            os.path.splitext( os.path.basename( x ) )[0] + '_' ) for x in self.file_list ]    

def main( ) :
    # did they want help?
    if '-h' in sys.argv or '-help' in sys.argv :
        print( USAGE_STR.format( program_name = sys.argv[0] ) )
        sys.exit(1)
    # parse our command line parameters
    params = commandParams( sys.argv )

    # get our start time
    start_time = time.time( )

    # open up devnull for sending output of subprocesses we will cal to nothingness
    devnull = open( os.devnull )
    print(params.input_folder,params.output_folder)
    for i in range( len( params.file_list ) ) :
        # how much we have processed?
        print( 'Processed {} out of {} files... {:.4f} seconds elapsed.'.format( i, 
            len( params.file_list ), time.time( ) - start_time ) )
        # make a list with the arguments we are going to process
        call_list = [ params.microscope_path, '--batch-mode', '--open-simulation',
            params.file_list[i], '--save-fluorescence-stack' ] + params.rgb_flags + [ params.out_list[i] ]
        # call it.
        subprocess.call( call_list, stdout = devnull, stderr = devnull )
    # end loop through all the files

    print( 'Processed {0} out of {0} files...'.format( len( params.file_list ) ) )

    print( 'Processing complete!' )
    # do we need to rename the output?
    if params.rename :
        # loop through all the outfile templates
        for i in range( len( params.out_list ) ) :
            # what value should we use?

            # get files that match this pattern
            matches = glob.glob( params.out_list[i] + '*' )

            # rename each match
            for path in matches :
                # split apart the extension from the file path
                spfext = os.path.splitext( path )
                # make the new path
                newpath = '{base}_{value}{ext}'.format( base = spfext[0], 
                    value = params.values[i], ext = spfext[1] )
                # rename
                os.rename( path, newpath )
        # end loop through all the files, done renaming
        print( 'Renaming complete! You can import the different channels as image sequences in Fiji.' )
    # we're done

# if this is the script being run, call main
if __name__ == '__main__' :
    main( )