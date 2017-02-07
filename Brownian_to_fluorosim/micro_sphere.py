# micro_sphere.py
# Author: Joseph Aicher
# Purpose: For CISMM / Professor Russell Taylor, as part of taking
#  output from Brownian motion simulator to a format readable
#  by the Microscope Simulator (Fluorosim)

# Defines a class (micro_sphere) that contains most of the information 
#  for defining a sphere in the Microscope Simulator

# class micro_sphere
#   private variables:
#     string _name
#     boolean _visible, _scannable
#     float _x, _y, _z, radius
#   public methods:
#     __init__ (name, pos_x, pos_y, pos_z, radius(, visible)(, scannable))
#     __str__ ( )
#     get_name ( )
#     is_visible ( )
#     is_scannable ( )
#     get_x ( ), get_y ( ), get_z ( )
#     get_radius ( )
#     set_visible ( visibility )
#     set_scannable ( scannability )
#     set_x ( new_x ), set_y ( new_y ), set_z ( new_z )
#     set_radius ( new_radius )




# information that I'm not going to mess with now:
FLUOROPHORE_MODEL_STR = '<SurfaceFluorophoreModel enabled="false" channel="{color}" intensityScale="1.000000" optimize="false" density="100.000000" numberOfFluorophores="12" samplingMode="fixedDensity" samplePattern="singlePoint" numberOfRingFluorophores="2" ringRadius="10.000000" randomizePatternOrientations="false"/><VolumeFluorophoreModel enabled="true" channel="{color}" intensityScale="1.000000" optimize="false" density="{density:f}" numberOfFluorophores="41" samplingMode="fixedDensity" samplePattern="singlePoint" numberOfRingFluorophores="2" ringRadius="10.000000" randomizePatternOrientations="false"/><GridFluorophoreModel enabled="false" channel="{color}" intensityScale="1.000000" optimize="false" sampleSpacing="50.000000"/>'

class micro_sphere :
    
    def __init__ ( self, name, pos_x, pos_y, pos_z, \
                   radius, density, color = 'all', visible = True, scannable = True ) :
        # constructor, just put into private variables
        self._name = str(name)
        self._x = float(pos_x)
        self._y = float(pos_y)
        self._z = float(pos_z)
        self._radius = float(radius)
        self._visible = bool(visible)
        self._scannable = bool(scannable)
        
        self._density = float(density)
        
        # added option for color.
        assert ( (color == 'all') or (color == 'red') or (color == 'green') or (color == 'blue') ), \
          'micro_sphere.__init__() : invalid choice of color.'
        self._color = color
        
        return

    def __str__ ( self ) :
        # return the correct XML string for this object
        ret_str = '<SphereModel>'
        # add the name
        ret_str += '<Name value="{0}"/>'.format(self._name)
        # add visibility value
        ret_str += '<Visible value="{0}"/>'.format( \
                   str(self.is_visible()).lower())
        # add scannable value
        ret_str += '<Scannable value="{0}"/>'.format( \
                   str(self.is_scannable()).lower())
        # add x,y,z values
        ret_str += '<PositionX value="{0:f}" optimize="false"/>'.format( \
                   self.get_x())
        ret_str += '<PositionY value="{0:f}" optimize="false"/>'.format( \
                   self.get_y())
        ret_str += '<PositionZ value="{0:f}" optimize="false"/>'.format( \
                   self.get_z())
        # add radius value
        ret_str += '<Radius value="{0:f}" optimize="false"/>'.format( \
                   self.get_radius())
        # add fluorophore model string
        ret_str += FLUOROPHORE_MODEL_STR.format( \
                   color = self._color, density = self._density )
        # add end of tag
        ret_str += '</SphereModel>'
        # we're done, so return ret_str
        return ret_str
    
    # get name (read-only variable)
    def get_name ( self ) :
        return self._name

    # get/set visible
    def is_visible ( self ) :
        return self._visible

    def set_visible ( self, visibility ) :
        self._visible = visibility
        return

    # get/set scannable
    def is_scannable ( self ) :
        return self._scannable

    def set_scannable ( self, scannability ) :
        self._scannable = scannabililty
        return
        
    # get/set color
    def get_color ( self ) :
        return self._color
        
    def set_color ( self, color ) :
        assert ( (color == 'all') or (color == 'red') or (color == 'green') or (color == 'blue') ), \
          'micro_sphere.set_color() : invalid choice of color.'
        self._color = color
        return
        
    # get/set density
    def get_density ( self ) :
        return self._density
    
    def set_density ( self, new_density ) :
        self._density = new_density
        return

    # get/set x-coordinate
    def get_x ( self ) :
        return self._x

    def set_x ( self, new_x ) :
        self._x = new_x
        return

    # get/set y-coordinate
    def get_y ( self ) :
        return self._y

    def set_y ( self, new_y ) :
        self._y = new_y
        return

    # get/set z-coordinate
    def get_z ( self ) :
        return self._z

    def set_z ( self, new_z ) :
        self._z = new_z
        return

    # get/set radius
    def get_radius ( self ) :
        return self._radius

    def set_radius ( self, new_radius ) :
        self._radius = new_radius
        return
