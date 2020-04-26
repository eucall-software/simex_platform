""" :module GAPDPhotonDiffractorParameters: Module that holds the GAPDPhotonDiffractorParameters class.  """
##########################################################################
#
# Modified by Juncheng E in 2020                                         #
# Copyright (C) 2016-2017 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

import os
import warnings

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance


class GAPDPhotonDiffractorParameters(AbstractCalculatorParameters):
    """
    :class GAPDPhotonDiffractorParameters: Class representing parameters for the GAPDPhotonDiffractor calculator.
    """
    def __init__(self,
                 sample=None,
                 sample_rotation=None,
                 rotation_quaternion=None,
                 uniform_rotation=None,
                 calculate_Compton=None,
                 slice_interval=None,
                 number_of_slices=None,
                 pmi_start_ID=None,
                 pmi_stop_ID=None,
                 number_of_diffraction_patterns=None,
                 beam_parameters=None,
                 detector_geometry=None,
                 number_of_MPI_processes=None,
                 parameters_dictionary=None,
                 **kwargs):
        """
        :param sample: Name of file containing atomic sample geometry (default None).
        :type sample: str

        :param sample_rotation: Whether to rotate the sample. 
        :type sample_rotation: bool, default False

        :param rotation_quaternion: The rotation quaternion for sample rotation. If \
                                    `sample_rotation` is True, it will perform the rotation.
                                     It will conflict with `uniform_rotation`.
        :type rotation_quaternion: list, default None

        :param uniform_rotation: Uniform or random sampling of rotation space. It will take \
                                 effect only if `sample_rotation` is True.
                                 uniform_rotation = True: uniform sampling of rotation space
                                 uniform_rotation = Flase: random sampling of rotation space
                                 uniform_rotation = None: No automatic rotation
                                 It will conflict with `rotation_quaternion`.
        :type uniform_rotation: bool, default None

        :param calculate_Compton: Whether to calculate incoherent (Compton) scattering.
        :type calculate_Compton: bool, default False

        :param slice_interval: Length of time slice interval to extract from each trajectory.
        :type slice_interval: int, default 100

        :param number_of_slices: Number of time slices to read from each trajectory.
        :type number_of_slices: int, default 1

        :param pmi_start_ID: Identifier for the first pmi trajectory to read in.
        :type pmi_start_ID: int, default 1

        :param pmi_stop_ID: Identifier for the last pmi trajectory to read in.
        :type pmi_stop_ID: int, default 1

        :param number_of_diffraction_patterns: Number of diffraction patterns to calculate from each trajectory.
        :type number_of_diffraction_patterns: int, default 1

        :param beam_parameters: Path of the beam parameter file or DetectorGeometry object.
        :type beam_parameters: str or DetectorGeometry object

        :param detector_geometry: Path of the beam geometry file or PhotonBeamParameters object.
        :type detector_geometry: str or PhotonBeamParameters object

        :param number_of_MPI_processes: Number of MPI processes
        :type number_of_MPI_processes: int, default 1

        """
        # Legacy support for dictionaries.
        if parameters_dictionary is not None:
            self.sample = None
            self.uniform_rotation = parameters_dictionary['uniform_rotation']
            self.calculate_Compton = parameters_dictionary['calculate_Compton']
            self.slice_interval = parameters_dictionary['slice_interval']
            self.number_of_slices = parameters_dictionary['number_of_slices']
            self.pmi_start_ID = parameters_dictionary['pmi_start_ID']
            self.pmi_stop_ID = parameters_dictionary['pmi_stop_ID']
            self.beam_parameters = parameters_dictionary['beam_parameters']
            self.detector_geometry = parameters_dictionary['detector_geometry']
            self.number_of_diffraction_patterns = parameters_dictionary[
                'number_of_diffraction_patterns']

        else:
            # Check all parameters.
            self.sample = sample
            self.uniform_rotation = uniform_rotation
            self.calculate_Compton = calculate_Compton
            self.slice_interval = slice_interval
            self.number_of_slices = number_of_slices
            self.pmi_start_ID = pmi_start_ID
            self.pmi_stop_ID = pmi_stop_ID
            self.beam_parameters = beam_parameters
            self.detector_geometry = detector_geometry
            self.number_of_diffraction_patterns = number_of_diffraction_patterns

        # super to access the methods of the base class.
        super(GAPDPhotonDiffractorParameters, self).__init__(**kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    ### Setters and queries.
    @property
    def sample(self):
        """ Query for the 'sample' parameter. """
        return self.__sample

    @sample.setter
    def sample(self, value):
        """ Set the 'sample' parameter to a given value.
        :param value: The value to set 'sample' to.
        """
        # Allow None.
        if value is not None:
            value = checkAndSetInstance(str, value, None)
        self.__sample = value

    @property
    def sample_rotation(self):
        """ Query for the 'sample_rotation' parameter. """
        return self.__uniform_rotation

    @sample_rotation.setter
    def sample_rotation(self, value):
        """ Set the 'sample_rotation' parameter to a given value.
        :param value: The value to set 'sample_rotation' to.
        """
        # Allow None.
        if value is not None:
            self.__uniform_rotation = checkAndSetInstance(bool, value, False)
        else:
            self.__uniform_rotation = None

    @property
    def rotation_quaternion(self):
        """ Query for the 'rotation_quaternion' parameter. """
        return self.rotation_quaternion

    @rotation_quaternion.setter
    def rotation_quaternion(self, value):
        """ Set the 'rotation_quaternion' parameter to a given value.
        :param value: The value to set 'rotation_quaternion' to.
        """
        # Allow None.
        if value is not None:
            if self.__sample_rotation != True:
                raise ValueError(
                    "'rotation_quaternion' is not set since 'sample_rotation' is not True."
                )
            if self.__uniform_rotation != None:
                warnings.warn(
                    "'uniform_rotation' will be overrided by 'rotation_quaternion'"
                )
                self.__uniform_rotation = None
            self.__rotation_quaternion = checkAndSetInstance((list, tuple),
                                                             value, None)
        else:
            self.__rotation_quaternion = None

    @property
    def uniform_rotation(self):
        """ Query for the 'uniform_rotation' parameter. """
        return self.__uniform_rotation

    @uniform_rotation.setter
    def uniform_rotation(self, value):
        """ Set the 'uniform_rotation' parameter to a given value.
        :param value: The value to set 'uniform_rotation' to.
        """
        # Allow None.
        if value is not None:
            if self.__sample_rotation != True:
                raise ValueError(
                    "'uniform_rotation' is not set since 'sample_rotation' is not True."
                )
            if self.__rotation_quaternion != None:
                warnings.warn(
                    "'rotation_quaternion' will be overrided by 'uniform_rotation'"
                )
                self.__rotation_quaternion = None
            self.__uniform_rotation = checkAndSetInstance(bool, value, None)
        else:
            self.__uniform_rotation = None

    @property
    def calculate_Compton(self):
        """ Query for the 'calculate_Compton' parameter. """
        return self.__calculate_Compton

    @calculate_Compton.setter
    def calculate_Compton(self, value):
        """ Set the 'calculate_Compton' parameter to a given value.
        :param value: The value to set 'calculate_Compton' to.
        """
        self.__calculate_Compton = checkAndSetInstance(bool, value, False)

    @property
    def number_of_slices(self):
        """ Query for the 'number_of_slices' parameter. """
        return self.__number_of_slices

    @number_of_slices.setter
    def number_of_slices(self, value):
        """ Set the 'number_of_slices' parameter to a given value.
        :param value: The value to set 'number_of_slices' to.
        """
        number_of_slices = checkAndSetInstance(int, value, 1)

        if number_of_slices > 0:
            self.__number_of_slices = number_of_slices
        else:
            raise ValueError(
                "The parameter 'slice_interval' must be a positive integer.")

    @property
    def slice_interval(self):
        """ Query for the 'slice_interval' parameter. """
        return self.__slice_interval

    @slice_interval.setter
    def slice_interval(self, value):
        """ Set the 'slice_interval' parameter to a given value.
        :param value: The value to set 'slice_interval' to.
        """
        slice_interval = checkAndSetInstance(int, value, 100)

        if slice_interval > 0:
            self.__slice_interval = slice_interval
        else:
            raise ValueError(
                "The parameter 'slice_interval' must be a positive integer.")

    @property
    def pmi_start_ID(self):
        """ Query for the 'pmi_start_ID' parameter. """
        return self.__pmi_start_ID

    @pmi_start_ID.setter
    def pmi_start_ID(self, value):
        """ Set the 'pmi_start_ID' parameter to a given value.
        :param value: The value to set 'pmi_start_ID' to.
        """
        pmi_start_ID = checkAndSetInstance(int, value, 1)
        if pmi_start_ID >= 0:
            self.__pmi_start_ID = pmi_start_ID
        else:
            raise ValueError(
                "The parameters 'pmi_start_ID' must be a positive integer.")

    @property
    def pmi_stop_ID(self):
        """ Query for the 'pmi_stop_ID' parameter. """
        return self.__pmi_stop_ID

    @pmi_stop_ID.setter
    def pmi_stop_ID(self, value):
        """ Set the 'pmi_stop_ID' parameter to a given value.
        :param value: The value to set 'pmi_stop_ID' to.
        """
        pmi_stop_ID = checkAndSetInstance(int, value, 1)
        if pmi_stop_ID >= 0:
            self.__pmi_stop_ID = pmi_stop_ID
        else:
            raise ValueError(
                "The parameters 'pmi_stop_ID' must be a positive integer.")

    @property
    def beam_parameters(self):
        """ Query for the 'beam_parameters' parameter. """
        return self.__beam_parameters

    @beam_parameters.setter
    def beam_parameters(self, value):
        """ Set the 'beam_parameters' parameter to a given value.
        :param value: The value to set 'beam_parameters' to.
        """
        value = checkAndSetInstance((str, PhotonBeamParameters), value, None)

        if isinstance(value, str):
            if not os.path.isfile(value):
                raise IOError(
                    "The beam_parameters %s is not a valid file or filename." %
                    (value))
            raise TypeError(
                "Passing beam parameters as a file is currently unsupported. Please use the PhotonBeamParameters class."
            )

        self.__beam_parameters = value

    @property
    def detector_geometry(self):
        """ Query for the 'detector_geometry' parameter. """
        return self.__detector_geometry

    @detector_geometry.setter
    def detector_geometry(self, value):
        """ Set the 'detector_geometry' parameter to a given value.
        :param value: The value to set 'detector_geometry' to.
        """
        if value is None:
            print(
                "WARNING: Geometry not set, calculation will most probably fail."
            )

        else:
            # Check if it is a DetectorGeometry object / string
            value = checkAndSetInstance((str, DetectorGeometry), value, None)

            if isinstance(value, str):
                if not os.path.isfile(value):
                    raise IOError(
                        'The parameter "detector_geometry" %s is not a valid file or filename.'
                        % (value))

                value = DetectorGeometry(filename=value)

        # Store on object and return.
        self.__detector_geometry = value

    @property
    def number_of_diffraction_patterns(self):
        """ Query for the 'number_of_diffraction_patterns_file' parameter. """
        return self.__number_of_diffraction_patterns

    @number_of_diffraction_patterns.setter
    def number_of_diffraction_patterns(self, value):
        """ Set the 'number_of_diffraction_patterns' parameter to a given value.
        :param value: The value to set 'number_of_diffraction_patterns' to.
        """
        number_of_diffraction_patterns = checkAndSetInstance(int, value, 1)

        if number_of_diffraction_patterns > 0:
            self.__number_of_diffraction_patterns = number_of_diffraction_patterns
        else:
            raise ValueError(
                "The parameters 'number_of_diffraction_patterns' must be a positive integer."
            )