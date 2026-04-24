#########################################################################################
##
##                                 TIME SCHEDULED EVENTS
##                                  (events/schedule.py)
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from ._event import Event

from .. _constants import TOLERANCE


# EVENT MANAGER CLASS ===================================================================

class Schedule(Event):
    """Subclass of base 'Event' that triggers dependent on the evaluation time. 
    
    Monitors time in every timestep and triggers periodically (period). This event
    does not have an event function as the event condition only depends on time.

    .. code-block::

        time == next_schedule_time -> event

    Example
    -------
    Initialize a scheduled event handler like this:

    .. code-block:: python

        #define the action function (callback)
        def act(t):
            #do something at event resolution
            pass
    
        #initialize the event manager
        E = Schedule(
            t_start=0,    #starting at t=0
            t_end=None,   #never ending
            t_period=3,   #triggering every 3 time units
            func_act=act  #resulting in a callback
            )   
    
    Parameters
    ----------
    t_start : float
        starting time for schedule
    t_end : float
        termination time for schedule
    t_period : float
        time period of schedule, when events are triggered
    func_act : callable
        action function for event resolution 
    tolerance : float
        tolerance to check if detection is close to actual event
    """

    def __init__(
        self, 
        t_start=0, 
        t_end=None, 
        t_period=1, 
        func_act=None,      
        tolerance=TOLERANCE
        ):
        raise NotImplementedError


    def _next(self):
        """
        return the next period break
        """
        pass


    def estimate(self, t):
        """Estimate the time until the next scheduled event.

        Parameters
        ----------
        t : float 
            evaluation time for estimation 
        
        Returns
        -------
        float
            estimated time until next event
        """
        pass


    def buffer(self, t):
        """Buffer the current time to history
        
        Parameters
        ----------
        t : float
            buffer time
        """
        pass


    def detect(self, t):
        """Check if the event condition is satisfied, i.e. if the 
        time period switch is within the current timestep.
        
        Parameters
        ----------
        t : float
            evaluation time for detection 
        
        Returns
        -------
        detected : bool
            was an event detected?
        close : bool
            are we close to the event?
        ratio : float
            interpolated event location ratio in timestep
        """
        pass


class ScheduleList(Schedule):
    """Subclass of base 'Schedule' that triggers dependent on the evaluation time. 
    
    Monitors time in every timestep and triggers at the next event time from the 
    time list. This event does not have an event function as the event condition 
    only depends on time.

    .. code-block::

        time == next_scheduled_time -> event

    Example
    -------
    Initialize a scheduled event handler like this:

    .. code-block:: python

        #define the action function (callback)
        def act(t):
            #do something at event resolution
            pass
    
        #initialize the event manager
        E = ScheduleList(
            times_evt=[1, 5, 12, 300],  #event times where to trigger
            func_act=act                #resulting in a callback
            )   
    
    Parameters
    ----------
    times_evt : list[float]
        list of event times in ascending order
    func_act : callable
        action function for event resolution 
    tolerance : float
        tolerance to check if detection is close to actual event
    """

    def __init__(
        self, 
        times_evt, 
        func_act=None,      
        tolerance=TOLERANCE
        ):
        raise NotImplementedError


    def _next(self):
        """return the next event from the event time list by index"""
        pass


    def detect(self, t):
        """Check if the event condition is satisfied, i.e. if the 
        time period switch is within the current timestep.
        
        Parameters
        ----------
        t : float
            evaluation time for detection 
        
        Returns
        -------
        detected : bool
            was an event detected?
        close : bool
            are we close to the event?
        ratio : float
            interpolated event location ratio in timestep
        """
        pass
