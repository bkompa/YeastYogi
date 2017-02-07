ParseBrownian and BrownianXMLtoTIFF
===================================


General Information
-------------------

ParseBrownian and BrownianXMLtoTIFF are two scripts 
written in [Python] [] that allow the user to convert the 
output from the brownianMotion simulator to Microscope 
Simulator formatted XML files (ParseBrownian) to TIFF files 
of each Z-stack (BrownianXMLtoTIFF). ParseBrownian allows 
the user to specify which points from the brownianMotion 
simulator are fluorescing based on a colors file generated 
by the brownianMotion application, allowing scientists to 
generate fluorescence microscope videos of simulations 
supposing that specific structures in the simulation are 
fluorescently labeled.

Author: Joseph K. Aicher

Plugin originally written as part of a summer project 
with Professor Russell M. Taylor II for the [UNC CAP REU] [] 
and [CISMM] [] during the summer of 2013.

Note: this file is written in [Markdown] [] for easy 
formatting into HTML.

   [UNC CAP REU]: http://physics.unc.edu/cap/
       (UNC Chapel Hill Computational Astronomy and Physics Summer REU Program)
   [CISMM]: http://cismm.cs.unc.edu/
       (Computer Integrated Systems for Microscopy and Manipulation)
   [Python]: http://www.python.org/ (Link to Python website)
   [Markdown]: http://daringfireball.net/projects/markdown/ 
       (Link to Markdown website)


Requirements
------------

These scripts require you to have Python installed. 
ParseBrownian and BrownianXMLtoTIFF were written using Python 
3.3.2; however, they should work with any version of Python
above 2.6.

BrownianXMLtoTIFF requires you to have [Microscope Simulator] [] 
installed from the CISMM website.

   [Microscope Simulator]: http://cismm.cs.unc.edu/downloads/?dl_cat=5
       (Microscope Simulator download page)


Installing ParseBrownian and BrownianXMLtoTIFF
----------------------------------------------

As Python scripts, ParseBrownian and BrownianXMLtoTIFF do 
not need to be installed. However, ParseBrownian must be 
kept in the same folder as `colored_spheres_list.py` and `micro_sphere.py`.


Using ParseBrownian and BrownianXMLtoTIFF
-----------------------------------------

We will assume that the locations of ParseBrownian
and BrownianXMLtoTIFF are `$ParseBrownian` and `$BrownianXMLtoTIFF`.


#### ParseBrownian ####

ParseBrownian allows you to convert the output of the 
brownianMotion simulator to XML files readable by Microscope 
Simulator. Recall that from the brownianMotion simulator you 
get two files: one with the coordinates at each time and one 
with the "color" of each coordinate, where the "color" is some 
integer value. Using these files, along with optional arguments 
that you can specify, ParseBrownian will generate an XML file 
for Microscope Simulator at each point in time for coordinates 
matching specific colors, setting their color channel to green.

We will assume that the locations of the coordinates file and 
the colors file are `$coordinates` and `$point_colors`.

Running ParseBrownian, at its simplest, boils down to the 
following command:

    > python $ParseBrownian $point_colors $coordinates

Running that command will automatically create a Microscope 
Simulator file using color 4 for each time step to a directory 
titled "output," along with other settings that were specific 
to the script's original use case. These parameters can be changed 
by adding commandline arguments before `$point_colors`, so that 
the command being run would be:

	> python $ParseBrownian [args] $point_colors $coordinates

where `[args]` specify parameters of interest. A useful example 
of this would be:

	> python $ParseBrownian -random 1 1 1 -zxy -use_colors colors.txt -PSF PSF_gain.txt -out myoutput -width 300 -height 300 -noise 3.5 -every 10 $point_colors $coordinates

This will translate the coordinates found in `$coordinates` by a 
random vector +/- 1 micron in the three coordinate directions, 
rotate the coordinate system so that the simulation z-axis is parallel
to the focal planes, set the colors and PSF/gain values being used 
to those found in `colors.txt` and `PSF_gain.txt` in the current 
directory, set the output directory to "myoutput," set the width and height
of the output microscope images would to 300 pixels, add simulated 
Gaussian noise with a standard deviation of 3.5, and only use every 
10th time step.

The -PSF flag deserves extra mention. You must specify a point 
spread function that you have put into Microscope Simulator. The 
details of adding a point spread function to Microscope Simulator 
are beyond the scope of this README. Assuming that you have a point
spread function named "GFP" in Microscope Simulator and would 
like to simulate it with a gain of 15, you could make a file named 
`GFPgain15.txt` with "GFP" as the first line and "15" as the second 
line. You will probably need to adjust the gain before moving on to 
BrownianXMLtoTIFF to ensure that you get an image.

More information about the commandline flags can be found by 
running the command:

	> python $ParseBrownian -help


#### BrownianXMLtoTIFF ####

BrownianXMLtoTIFF allows you to convert the output of ParseBrownian 
to TIFF files of the microscope stack at each time step. Recall that 
the output of ParseBrownian is put into some folder. We will assume 
that the path to that folder is `$input_folder`.

Running BrownianXMLtoTIFF, at its simplest, boils down to the 
following command:

    > python $BrownianXMLtoTIFF $input_folder

Running that command will automatically create TIFF files for 
each XML file in `$input_folder` for the red, green, and blue color 
channels and put them into a folder named `output_tiff` in the 
current directory, so long as Microscope Simulator is installed to the path
`C:\Program Files (x86)\CISMM\Microscope Simulator 2.3.0\bin\MicroscopeSimulator.exe`.
Note that this program takes a while to complete because Microscope 
Simulator is a graphics-intensive program, so while it runs you may 
want to grab a cup of coffee or go to lunch. Unfortunately, due
to how Microscope Simulator is written, it will take up your first 
(and possibly only) computer screen while it runs.

You will typically only care about the green channel. Meanwhile, 
you may want to have the TIFF files go to a folder named something 
else, say "different". Microscope Simulator may be installed 
somewhere else, which we will suppose is `$microscope_path`. We 
can make the script only output the green channel to the folder 
`different` using Microscope Simulator installed to 
`$microscope_path` by using the following command:

	> python $BrownianXMLtoTIFF -green -out different -simulator $microscope_path $input_folder

More information about the commandline flags can be found by 
running the command:

	> python $BrownianXMLtoTIFF -help
