#!/usr/bin/env python
# ParseBrownian.py
# Author: Joseph K. Aicher
# Summary: A script that uses output from the brownianMotion simulator to automatically
#  generate Microscope Simulator formatted XML files. Takes commandline flags that can
#  specify different settings in Microscope Simulator.

from __future__ import print_function # imports print statement syntax from Python 3

import colored_spheres_list
import sys
import os
import datetime
import random


USAGE_STR = \
'''Usage: 
{program_name} [args] point_colors coordinates
        point_colors: the output from brownianMotion of the points' colors
        coordinates: the ouput from brownianMotion of the points' coordinates over time
        [args]:
          [-translate x y z]: constant vector to translate coordinates by
          [-random x y z]: translate coordinates by vector randomly selected between ([-x,x], [-y,y], [-z,z])
          [-xyz, -xzy, -yxz, -yzx, -zxy, -zyx]: read coordinates (x,y,z) in order specified by flag (-zyx read as (z,y,x)) after applying -translate and -random
          [-use_colors file]: open file with colors to put into our XML files, different colors separated by spaces, commas, and new lines
          [-PSF file]: open file, read in name of PSF in Microscope Simulator on first line, gain to use on second line
          [-out folder]: use folder to store output
          [-width dimension]: set width of simulated slide to dimension pixels
          [-height dimension]: set height of simulated slide to dimension pixels
          [-focal_planes dimension]: set number of slices in simulated stack to dimension
          [-sphere_radius radius]: set radius of spheres to radius (in brownianMotion units)
          [-fake_poles distance]: display fake spindle pole bodies, distance brownianMotion units away from origin
          [-nm_per conversion]: one brownianMotion unit is conversion nanometers
          [-pixel_size size]: the width and length of pixels in nanometers
          [-voxel_depth size]: the height of voxels in nanometers
          [-density low high]: sets the fluorophore densities for fake poles (low) and everything else (high)
          [-contrast min max]: sets the minimum and maximum levels for contrast
          [-intensity max]: sets the maximum voxel intensity
          [-noise deviation]: sets Gaussian noise to be simulated in Microscope Simulator with some positive standard deviation
          [-every skip]: only outputs an XML file for every skip-th time steps
          [-h],[-help]: prints out usage information and exits
'''

# class that holds user provided parameters and initializes based off defaults modified by sys.argv
class userParams :
    def _getColors ( self, path ) :
        # opens up path to get a list of colors that will be used for microscope simulation
        # initialize the colors list
        colors = [ ]
        # loop through the file, add as we go along
        for line in open( path ) :
            for value in line.replace( ',', ' ' ).split( ) :
                colors.append( int( value ) )
        # end loop through file
        assert len( colors ) > 0, "The file '{0}' did not include any colors".format( path )
        # we are done, return colors
        return colors

    def _getPSF ( self, path ) :
        # opens up path to get:
        #  first line - name of PSF
        #  second line - value of gain
        # returns ( name, gain )
        pfile = open( path )
        name = pfile.readline( ).replace('\n', '' )
        gain = float( pfile.readline( ) )
        pfile.close( )
        return ( name, gain )

    # applies the basic translation vectors to coordinates vec
    def applyTranslation ( self, vec ) :
        return tuple( x + y + z for x,y,z in zip( vec, self.translate_vector, self.random_vector ) )

    # takes coordinates in brownianMotion and converts to Microscope Simulator where origin moved to center of slide and slices
    def coordTransform ( self, vec ) :
        translated = self.applyTranslation( vec )
        rotated = self.axes_transform( translated )
        scaled = ( ( rotated[0] * self.input_conversion ) + ( self.microscope_width * self.pixel_size ) / 2.0,
                   ( rotated[1] * self.input_conversion ) + ( self.microscope_height * self.pixel_size ) / 2.0,
                   ( rotated[2] * self.input_conversion ) + ( ( self.microscope_slices - 1 ) * self.voxel_depth ) / 2.0 )
        return scaled

    XML_STRING = '<?xml version="1.0" encoding="ISO-8859-1"?>\n<SimulatedExperiments file="{path}" modified="{time}" created="{time}"><Version major="2" minor="2" revision="1"/><AFMSimulation pixelSize="10.000000" imageWidth="300" imageHeight="300" clipGroundPlane="false" displayAsWireframe="false" surfaceOpacity="1.000000"/><FluorescenceSimulation focalPlaneIndex="0" focalPlaneSpacing="{voxel_depth:f}" numberOfFocalPlanes="{focal_planes_ct}" useCustomFocalPlanePositions="false" gain="{gain:f}" offset="0.000000" maximumVoxelIntensity="{max_voxel_intensity:f}" pixelSize="{pixel_size:f}" psfName="{point_spread}" imageWidth="{image_width}" imageHeight="{image_height}" shearInX="0.000000" shearInY="0.000000" addGaussianNoise="{use_noise}" noiseStdDev="{noise_stdev:f}" showImageVolumeOutline="false" showRefGrid="true" refGridSpacing="1000.000000" superimposeSimulatedImage="false" superimposeComparisonImage="false" minimumIntensityLevel="{min_intensity:f}" maximumIntensityLevel="{max_intensity:f}"><FocalPlanes><Plane index="0" position="0.000000"/><Plane index="1" position="0.000000"/><Plane index="2" position="0.000000"/><Plane index="3" position="0.000000"/><Plane index="4" position="0.000000"/><Plane index="5" position="0.000000"/><Plane index="6" position="0.000000"/><Plane index="7" position="0.000000"/><Plane index="8" position="0.000000"/><Plane index="9" position="0.000000"/><Plane index="10" position="0.000000"/><Plane index="11" position="0.000000"/><Plane index="12" position="0.000000"/><Plane index="13" position="0.000000"/><Plane index="14" position="0.000000"/><Plane index="15" position="0.000000"/><Plane index="16" position="0.000000"/><Plane index="17" position="0.000000"/><Plane index="18" position="0.000000"/><Plane index="19" position="0.000000"/><Plane index="20" position="0.000000"/><Plane index="21" position="0.000000"/><Plane index="22" position="0.000000"/><Plane index="23" position="0.000000"/><Plane index="24" position="0.000000"/><Plane index="25" position="0.000000"/><Plane index="26" position="0.000000"/><Plane index="27" position="0.000000"/><Plane index="28" position="0.000000"/><Plane index="29" position="0.000000"/></FocalPlanes><GradientDescentFluorescenceOptimizer><Iterations value="100"/><DerivativeEstimateStepSize value="1e-008"/><StepScaleFactor value="1"/><ObjectiveFunction name="Gaussian Noise Maximum Likelihood"/></GradientDescentFluorescenceOptimizer><NelderMeadFluorescenceOptimizer><MaximumIterations value="100"/><ParametersConvergenceTolerance value="1e-008"/><ObjectiveFunction name="Gaussian Noise Maximum Likelihood"/></NelderMeadFluorescenceOptimizer><PointsGradientFluorescenceOptimizer><StepSize value="1"/><Iterations value="100"/><ObjectiveFunction name=""/></PointsGradientFluorescenceOptimizer><FluorescenceComparisonImageModelObject name="None"/></FluorescenceSimulation>{model_object_list}</SimulatedExperiments>'

    def xmlString ( self, out_path, myModelObjectList ) :
    	return self.XML_STRING.format( path = out_path, time = str( datetime.datetime.now() ),
                                   point_spread = self.psf_name, gain = self.psf_gain,
                                   model_object_list = myModelObjectList, pixel_size = self.pixel_size,
                                   image_width = self.microscope_width, image_height = self.microscope_height,
                                   voxel_depth = self.voxel_depth, focal_planes_ct = self.microscope_slices,
                                   min_intensity = self.constrast_levels[0], max_intensity = self.constrast_levels[1],
                                   max_voxel_intensity = self.max_voxel_intensity, use_noise = str( self.use_noise ).lower( ),
                                   noise_stdev = self.noise_stdev )

    def __str__ ( self ) :
        ret_str = "Parameters: \n"
        ret_str += "-----------\n\n"
        ret_str += "Translation vector: ({}, {}, {})\n".format( self.translate_vector[0], self.translate_vector[1], self.translate_vector[2] )
        ret_str += "Random bounds: ({}, {}, {})\n".format( self.random_bounds[0], self.random_bounds[1], self.random_bounds[2] )
        ret_str += "Random vector: ({}, {}, {})\n".format( self.random_vector[0], self.random_vector[1], self.random_vector[2] )
        ret_str += "Coordinates ('x','y','z') read in as {}\n".format( self.axes_transform( ('x','y','z') ) )
        ret_str += "Colors used: {}\n".format( self.use_colors )
        ret_str += "PSF name: {}\n".format( self.psf_name )
        ret_str += "Gain: {}\n".format( self.psf_gain )
        ret_str += "Output folder: {}\n".format( self.out_folder )
        ret_str += "Width: {}\n".format( self.microscope_width )
        ret_str += "Height: {}\n".format( self.microscope_height )
        ret_str += "Slices: {}\n".format( self.microscope_slices )
        ret_str += "Sphere radius: {}\n".format( self.sphere_radius )
        ret_str += "Fake Poles: {}\n".format( self.fake_poles )
        ret_str += "Fake distance: {}\n".format( self.fake_distance )
        ret_str += "Fake radius: {}\n".format( self.fake_radius )
        ret_str += "Input Conversion: {}\n".format( self.input_conversion )
        ret_str += "Pixel Size: {}\n".format( self.pixel_size )
        ret_str += "Voxel Depth: {}\n".format( self.voxel_depth )
        ret_str += "Fluorophore Densities: {}\n".format( self.fluorophore_density )
        ret_str += "Gaussian noise: {}\n".format( self.noise_stdev )
        ret_str += "Using every {}-th time steps\n".format( self.skip )
        return ret_str

    def __init__ ( self, arguments ) :
        # constant vector to translate coordinates by
        self.translate_vector = ( 0.0, 0.0, 0.0 )
        # vector (x,y,z) such that we pick random number in [-x,x], [-y,y], [-z,z] to translate all vectors by
        self.random_bounds = ( 0.0, 0.0, 0.0 )
        # function to change axes by
        self.axes_transform = lambda vec : vec # identity
        # list with color integers to give fluorescence
        self.use_colors = [ 4 ]
        # details of PSF name and gain
        self.psf_name = "Gaussian"
        self.psf_gain = 1.0
        # folder to put output in
        self.out_folder = "output"
        # width of slide, pixels
        self.microscope_width = 1392
        self.microscope_height = 1040
        # number of focal planes
        self.microscope_slices = 5
        # radius of spheres in *brownianMotion units*
        self.sphere_radius = 0.005
        # make fake poles, and if so, distance and radius in *brownianMotion units*? (this is a stupid feature)
        self.fake_poles = False
        self.fake_distance = 0.750
        self.fake_radius = 0.150
        # number of nanometers per brownianMotion unit (typically in microns, so 1000)
        self.input_conversion = 1000.0
        # pixel width in nanometers
        self.pixel_size = 63.0971
        # voxel depth in nanometers
        self.voxel_depth = 200.0
        # fluorophore density for spindle pole bodies, everything else
        self.fluorophore_density = ( 200000, 5000000 )
        # minimum and maximum constrast levels
        self.constrast_levels = ( 0.0, 200.0 )
        # maximum voxel intensity
        self.max_voxel_intensity = 200.0
        # use Gaussian noise?
        self.use_noise = False
        self.noise_stdev = 0.0
        # do every time step
        self.skip = 1
        # loop through the indices that index arguments (sort of inefficient)
        for i in range( len( arguments ) ) :
            if arguments[i] == '-translate' :
                self.translate_vector = tuple( [ float( arguments[j] ) for j in range( i+1, i+4 ) ] )
            elif arguments[i] == '-random' :
                self.random_bounds = tuple( [ float( arguments[j] ) for j in range( i+1, i+4 ) ] )
            elif arguments[i] == '-xyz' :
                self.axes_transform = lambda vec : vec
            elif arguments[i] == '-xzy' :
                self.axes_transform = lambda vec : ( vec[0], vec[2], vec[1] )
            elif arguments[i] == '-yxz' :
                self.axes_transform = lambda vec : ( vec[1], vec[0], vec[2] )
            elif arguments[i] == '-yzx' :
                self.axes_transform = lambda vec : ( vec[1], vec[2], vec[0] )
            elif arguments[i] == '-zxy' :
                self.axes_transform = lambda vec : ( vec[2], vec[0], vec[1] )
            elif arguments[i] == '-zyx' :
                self.axes_transform = lambda vec : ( vec[2], vec[1], vec[0] )
            elif arguments[i] == '-use_colors' :
                self.use_colors = self._getColors( arguments[i+1] )
            elif arguments[i] == '-PSF' :
                ( self.psf_name, self.psf_gain ) = self._getPSF( arguments[i+1] )
            elif arguments[i] == '-out' :
                self.out_folder = arguments[i+1]
            elif arguments[i] == '-width' :
                self.microscope_width = int( arguments[i+1] )
            elif arguments[i] == '-height' :
                self.microscope_height = int( arguments[i+1] )
            elif arguments[i] == '-focal_planes' :
                self.microscope_slices = int( arguments[i+1] )
            elif arguments[i] == '-sphere_radius' :
                self.sphere_radius = float( arguments[i+1] )
            elif arguments[i] == '-fake_poles' :
                self.fake_poles = True
                self.fake_distance = float( arguments[i+1] )
                self.fake_radius = float( arguments[i+2] )
            elif arguments[i] == '-nm_per' :
                self.input_conversion = float( arguments[i+1] )
            elif arguments[i] == '-pixel_size' :
                self.pixel_size = float( arguments[i+1] )
            elif arguments[i] == '-voxel_depth' :
                self.voxel_depth = float( arguments[i+1] )
            elif arguments[i] == '-density' :
                self.fluorophore_density = tuple( [ int( arguments[j] ) for j in range( i+1, i+3 ) ] )
            elif arguments[i] == '-contrast' :
                self.constrast_levels = tuple( [ float( arguments[j] ) for j in range( i+1, i+3 ) ] )
            elif arguments[i] == '-intensity' :
                self.max_voxel_intensity = float( arguments[i+1] )
            elif arguments[i] == '-noise' :
            	self.noise_stdev = float( arguments[i+1] )
            	# if the standard deviation is greater than zero, then we're actually doing it
            	self.use_noise = self.noise_stdev > 0.0
            	# if use_noise is false, we want standard deviation to remain zero
            	self.noise_stdev *= self.use_noise # multiply by either True (1) or False (0)
            elif arguments[i] == '-every' :
                self.skip = int( arguments[i+1] )
                if self.skip < 1 : self.skip = 1
            # that's all the flags (for now, at least)
        # end loop through the arguments
        # correct out folder and make it
        self.out_folder = os.path.realpath( self.out_folder)
        assert not os.path.isfile( self.out_folder ), "'{0}' is the name of an already existing file".format( self.out_folder )
        if not os.path.isdir( self.out_folder ) :
            os.mkdir( self.out_folder )
        # construct random vector from self.random_bounds
        random.seed() # initialize random
        self.random_vector = ( random.uniform( -self.random_bounds[0], self.random_bounds[0] ), 
                               random.uniform( -self.random_bounds[1], self.random_bounds[1] ), 
                               random.uniform( -self.random_bounds[2], self.random_bounds[2] ) )
        # cache converted sphere and fake radii
        self.csphere_radius = self.sphere_radius * self.input_conversion
        self.cfake_radius = self.fake_radius * self.input_conversion


def main( ) :
    # did they want help?
    if '-h' in sys.argv or '-help' in sys.argv :
        print( USAGE_STR.format( program_name = sys.argv[0] ) )
        sys.exit(1)
    # we have to have at least two arguments in addition to the program name.
    assert len( sys.argv ) > 2, USAGE_STR.format( program_name = sys.argv[0] )
    # okay, so let's get our parameters...
    if not os.path.isfile( sys.argv[-2] ) :
        print( "File {0} does not exist".format( sys.argv[-2] ) )
        sys.exit(-1)
    coordinates_colors = [ int(x) for x in open( sys.argv[-2] ).readlines( ) ]
    coordinates_path = sys.argv[-1]
    if not os.path.isfile( coordinates_path ) :
        print( "File {0} does not exist".format( coordinates_path ) )
        sys.exit(-2)
    # get optional parameters from other arguments
    params = userParams( sys.argv[1:-2] )

    # print out the parameters that we are using to stdout
    print( params )
    print( '\n' )

    # get the number of points we should have for each time step
    num_points = len( coordinates_colors )
    print("num_points ",num_points)
    # make a spheres list and preallocate with spheres at (0,0,0) and correct colors (two extra for spindles)
    spheres_list = colored_spheres_list.colored_spheres_list( params.csphere_radius, num_points + 2 )
    for i in range( num_points ) :
        # add the spheres, put them with fluorophore density params.fluorophore_density[1] and color 'green'
        spheres_list.add_sphere( 0.0, 0.0, 0.0, coordinates_colors[i], params.fluorophore_density[1], 'green' )

    # add fake spindle if desired (color 'blue')
    if params.fake_poles :
        # color that hasn't been used
        fake_color = 42 # because Hitchhiker's Guide
        while fake_color in coordinates_colors :
            fake_color += 1
        # add this to params.use_colors
        params.use_colors.append( fake_color )
        # resize  this color
        spheres_list.resize_color( fake_color, spheres_list.cfake_radius )
        # coordinates of spindle pole bodies
        fake_top = params.coordTransform( ( 0.0, 0.0, self.fake_distance ) )
        fake_bottom = params.coordTransform( ( 0.0, 0.0, -self.fake_distance ) )
        spheres_list.add_sphere( fake_top[0], fake_top[1], fake_top[2], fake_color, 'blue' )
        spheres_list.add_sphere( fake_bottom[0], fake_bottom[1], fake_bottom[2], fake_color, 'blue' )
    # end add fake spindle

    # now open coordinates file
    coordinates_file = open( coordinates_path )

    # make prefix for output XML files
    out_prefix = os.path.splitext( os.path.basename( coordinates_path ) )[0]
    print(out_prefix)
    # loop through the file over each time step
    count = 0 # record how many times we have passed
    times = [] # record all the times that we have used
    read_line = coordinates_file.readline( )
    while read_line != '' :
        assert read_line[:4] == 'Time', 'Current line should tell us the time'
        if count % params.skip == 0 : # is this a time that we will record?
            # get the current time
            times.append( float( read_line[4:] ) )
            # out path is out_prefix + '_' + len(times) + '.xml'
            out_path = os.path.join( params.out_folder, "{}_{}.xml".format( out_prefix, len(times) ) )
            print( 'Time {:.4f} output to {}'.format( times[-1], out_path ) )
            # update our coordinates:
            for i in range( num_points ) :
                coordinates = params.coordTransform( tuple( float(x) for x in coordinates_file.readline( ).split(' ') ) )
                # update coordinates in spheres_list
                spheres_list.update_coordinate( i, coordinates[0], coordinates[1], coordinates[2] )
            # make our xml file
            # get our ModelObjectList using params.use_colors
            myModelObjectList = spheres_list.make_ModelObjectList( params.use_colors )
            write_str = params.xmlString( out_path, myModelObjectList )
            write_file = open( out_path, 'w' )
            write_file.write( write_str )
            write_file.flush( )
            write_file.close( )
        else : # so we don't want to record this one
            for i in range( num_points ) :
                coordinates_file.readline( )

        # add to the number of times we have passed
        count += 1
        # read an empty line
        coordinates_file.readline( )
        # start the next time step (or read EOF)
        read_line = coordinates_file.readline( )
    # finished reading last time step

    # we should be done now, close the file
    coordinates_file.close( )

    # print out the average time step
    if len( times ) > 1 :
        time_steps = [ times[i] - times[i-1] for i in range(1, len( times )) ]
        average_time_step = sum( time_steps ) / len( time_steps )
        print( '\n' )
        print( 'Average Time Step: {:.4f}'.format( average_time_step ) )

# run main if this is what's being run
if __name__ == '__main__' :
    main( )