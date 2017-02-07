# colored_spheres_list.py
# Author: Joseph Aicher
# Purpose: For CISMM / Professor Russell Taylor, as part of taking
#  output from Brownian motion simulator to a format readable
#  by the Microscope Simulator (Fluorosim)

# defines a class that manages multiple spheres together, categorizing
#  them by `color' (an integer value)

# this depends on micro_sphere:
import micro_sphere

class colored_spheres_list :
    
    def __init__ ( self, set_radius = 20.0, preallocate = 500 ) :
        # _default_radius defines the default radius of each sphere
        self._default_radius = float( set_radius )
        # _mycolors is a list of the color of each sphere
        self._mycolors = [ None ]*preallocate
        # _myspheres is a list of the spheres
        self._myspheres = [ None ]*preallocate
        # _color_radius is a dictionary of non_default radii for specified colors
        self._color_radius = { }

        # keep track of how many spheres are in the list since we moved
        # to allow preallocation of space.
        self._count = 0
        return
    
    def __len__ ( self ) :
        # return the number of spheres that colored_spheres_list has:
        return len( self._mycolors )
    
    def get_colors_length ( self, colors ) :
        # return the number of spheres that are of a color in the list colors
        ret_count = 0
        # loop through the colors of our spheres
        for i in range( self._count ) :
            if self._mycolors[i] in colors:
                ret_count += 1
        # we finished looping through the colors of our spheres
        # now we return the count
        return ret_count

    def update_coordinate ( self, index, x, y, z ) :
        # updates the sphere of chosen index in the list to have positional
        # coordinates (x,y,z)
        assert index < self._count, \
            'update_coordinate(): index chosen outside of list'
        self._myspheres[index].set_x( x )
        self._myspheres[index].set_y( y )
        self._myspheres[index].set_z( z )
        return
    
    def add_sphere ( self, x, y, z, color, density, color_str = 'all' ) :
        # adds a sphere at the specified location with given color
        
        
        # determine name of this object :
        name = 'color{0}index{1}'.format( color, self._mycolors.count( color ) )
        
        # add sphere to _myspheres :
        # first get radius:
        radius = self._default_radius
        # check if we have a non-default value
        if color in self._color_radius :
            radius = self._color_radius[color]
        # we now have everything we need, make the sphere.
        sphere = micro_sphere.micro_sphere( name, x, y, z, radius, density, color_str )

        
        if self._count == len( self._mycolors ) :
            # add the sphere to the list of spheres
            self._myspheres.append( sphere )
            # add color to _mycolors :
            self._mycolors.append( color )
        else :
            # we are still on preallocated space.
            self._myspheres[self._count] = sphere
            self._mycolors[self._count] = color
        
        # increase the count
        self._count += 1
        
        # we're done with this function now!
        return
    
    def set_default_radius ( self, new_radius ) :
        # changes the default radius of each sphere
        self._default_radius = float( new_radius )
        return
    
    def resize_color ( self, color, new_radius ) :
        # specifies a new radius to set spheres of given color to new_radius
        
        # ensure that new_radius is a float
        float_radius = float( new_radius )
        
        # add/modify current entry in _color_radius for given color to new_radius:
        self._color_radius[color] = float_radius
        
        # now go through all those of this color and set radius to the new value:
        for i in range( self._count ) :
            if self._mycolors[i] == color :
                self._myspheres[i].set_radius( float_radius )
        # end loop over the spheres
        return
    
    def reset_colors ( self ) :
        # undoes the changes made by resize_color ( int, float )
        #  that is, it makes _color_radius empty
        
        self._color_radius = { }
        # loop through all the spheres, set radius of each object to _default_radius
        for i in range( self._count ) :
            self._myspheres[i].set_radius( self._default_radius )
        # end loop through all the spheres
        return
    
    def make_ModelObjectList ( self, colors ) :
        # returns an XML formatted string of a ModelObjectList for the
        #  Microscope simulator including all the spheres with a color
        #  inside the list colors
        
        # ret_str is a string that will be modified and eventually returned
        ret_str = '<ModelObjectList>'
        # changed is a boolean value that will check if anything was of the given color (some objects)
        changed = False
        
        # loop through all the spheres
        for i in range( self._count ) :
            # check if the color of the current sphere is in colors
            if self._mycolors[i] in colors :
                changed = True
                ret_str += str( self._myspheres[i] )
        # end loop to add the XML formats of spheres that had given colors
        
        # if nothing was changed, we may have a problem.
        if not changed :
            print( 'WARNING: ModelObjectList was empty' )
        
        # add end tag of the ModelObjectList
        ret_str += '</ModelObjectList>'
        
        # return this string
        return ret_str
