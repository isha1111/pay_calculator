from datetime import date, datetime
from dateutil.easter import easter, EASTER_ORTHODOX
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import six

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
WEEKEND = (SAT, SUN)

JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC = range(1, 13)

OBSERVED = True

class Holidays(object):
    def populate(state, year):
        # ACT:  Holidays Act 1958
        # NSW:  Public Holidays Act 2010
        # NT:   Public Holidays Act 2013
        # QLD:  Holidays Act 1983
        # SA:   Holidays Act 1910
        # TAS:  Statutory Holidays Act 2000
        # VIC:  Public Holidays Act 1993
        # WA:   Public and Bank Holidays Act 1972

        # TODO do more research on history of Aus holidays
        calculated_holidays = {}

        # New Year's Day
        name = "New Year's Day"
        jan1 = date(year, JAN, 1)
        
        if OBSERVED and jan1.weekday() not in WEEKEND:
            calculated_holidays[jan1] = name
        else:
            calculated_holidays[jan1 + rd(weekday=MO)] = name + " (Observed)"

        # Australia Day
        jan26 = date(year, JAN, 26)
        if year >= 1935:
            if state == 'NSW' and year < 1946:
                name = "Anniversary Day"
            else:
                name = "Australia Day"
            
            if OBSERVED and jan26.weekday() not in WEEKEND:
                calculated_holidays[jan26] = name 
            else:
                calculated_holidays[jan26 + rd(weekday=MO)] = name + " (Observed)"
        elif year >= 1888 and state != 'SA':
            name = "Anniversary Day"
            calculated_holidays[jan26] = name

        # Adelaide Cup
        if state == 'SA':
            name = "Adelaide Cup"
            if year >= 2006:
                # subject to proclamation ?!?!
                calculated_holidays[date(year, MAR, 1) + rd(weekday=MO(+2))] = name
            else:
                calculated_holidays[date(year, MAR, 1) + rd(weekday=MO(+3))] = name

        # Canberra Day
        if state == 'ACT':
            name = "Canberra Day"
            calculated_holidays[date(year, MAR, 1) + rd(weekday=MO(+1))] = name

        # Easter
        calculated_holidays[easter(year) + rd(weekday=FR(-1))] = "Good Friday"
        if state in ('ACT', 'NSW', 'NT', 'QLD', 'SA', 'VIC'):
            calculated_holidays[easter(year) + rd(weekday=SA(-1))] = "Easter Saturday"
        if state == 'NSW':
            calculated_holidays[easter(year)] = "Easter Sunday"
        calculated_holidays[easter(year) + rd(weekday=MO)] = "Easter Monday"

        # Anzac Day
        if year > 1920:
            name = "Anzac Day"
            apr25 = date(year, APR, 25)
            
            if OBSERVED and apr25.weekday() not in WEEKEND:
                calculated_holidays[apr25] = name
            else:
                calculated_holidays[apr25 + rd(weekday=MO)] = name + " (Observed)"


        # Western Australia Day
        if state == 'WA' and year > 1832:
            if year >= 2015:
                name = "Western Australia Day"
            else:
                name = "Foundation Day"
            calculated_holidays[date(year, JUN, 1) + rd(weekday=MO(+1))] = name

        # Sovereign's Birthday
        if year >= 1952:
            name = "Queen's Birthday"
        elif year > 1901:
            name = "King's Birthday"
        if year >= 1936:
            name = "Queen's Birthday"
            if state == 'QLD':
                if year == 2012:
                    calculated_holidays[date(year, JUN, 11)] = "Queen's Diamond Jubilee"
                if year < 2016 and year != 2012:
                    dt = date(year, JUN, 1) + rd(weekday=MO(+2))
                    calculated_holidays[dt] = name
                else:
                    dt = date(year, OCT, 1) + rd(weekday=MO)
                    calculated_holidays[dt] = name
            elif state == 'WA':
                # by proclamation ?!?!
                calculated_holidays[date(year, OCT, 1) + rd(weekday=MO(-1))] = name
            else:
                dt = date(year, JUN, 1) + rd(weekday=MO(+2))
                calculated_holidays[dt] = name
        elif year > 1911:
            calculated_holidays[date(year, JUN, 3)] = name  # George V
        elif year > 1901:
            calculated_holidays[date(year, NOV, 9)] = name  # Edward VII

        # Picnic Day
        if state == 'NT':
            name = "Picnic Day"
            calculated_holidays[date(year, AUG, 1) + rd(weekday=MO)] = name

        # Labour Day
        name = "Labour Day"
        if state in ('NSW', 'ACT', 'SA'):
            calculated_holidays[date(year, OCT, 1) + rd(weekday=MO)] = name
        elif state == 'WA':
            calculated_holidays[date(year, MAR, 1) + rd(weekday=MO)] = name
        elif state == 'VIC':
            calculated_holidays[date(year, MAR, 1) + rd(weekday=MO(+2))] = name
        elif state == 'QLD':
            if 2013 <= year <= 2015:
                calculated_holidays[date(year, OCT, 1) + rd(weekday=MO)] = name
            else:
                calculated_holidays[date(year, MAY, 1) + rd(weekday=MO)] = name
        elif state == 'NT':
            name = "May Day"
            calculated_holidays[date(year, MAY, 1) + rd(weekday=MO)] = name
        elif state == 'TAS':
            name = "Eight Hours Day"
            calculated_holidays[date(year, MAR, 1) + rd(weekday=MO(+2))] = name

        # Family & Community Day
        if state == 'ACT':
            name = "Family & Community Day"
            if 2007 <= year <= 2009:
                calculated_holidays[date(year, NOV, 1) + rd(weekday=TU)] = name
            elif year == 2010:
                # first Monday of the September/October school holidays
                # moved to the second Monday if this falls on Labour day
                # TODO need a formula for the ACT school holidays then
                # http://www.cmd.act.gov.au/communication/holidays
                calculated_holidays[date(year, SEP, 26)] = name
            elif year == 2011:
                calculated_holidays[date(year, OCT, 10)] = name
            elif year == 2012:
                calculated_holidays[date(year, OCT, 8)] = name
            elif year == 2013:
                calculated_holidays[date(year, SEP, 30)] = name
            elif year == 2014:
                calculated_holidays[date(year, SEP, 29)] = name
            elif year == 2015:
                calculated_holidays[date(year, SEP, 28)] = name
            elif year == 2016:
                calculated_holidays[date(year, SEP, 26)] = name
            elif 2017 <= year <= 2020:
                labour_day = date(year, OCT, 1) + rd(weekday=MO)
                if year == 2017:
                    dt = date(year, SEP, 23) + rd(weekday=MO)
                elif year == 2018:
                    dt = date(year, SEP, 29) + rd(weekday=MO)
                elif year == 2019:
                    dt = date(year, SEP, 28) + rd(weekday=MO)
                elif year == 2020:
                    dt = date(year, SEP, 26) + rd(weekday=MO)
                if dt == labour_day:
                    dt += rd(weekday=MO(+1))
                calculated_holidays[date(year, SEP, 26)] = name

        if state == 'VIC':
            # Grand Final Day
            if year >= 2015:
                calculated_holidays[date(year, SEP, 24) + rd(weekday=FR)] = "Grand Final Day"
            # Melbourne Cup
            calculated_holidays[date(year, NOV, 1) + rd(weekday=TU)] = "Melbourne Cup"

        # The Royal Queensland Show (Ekka)
        # The Show starts on the first Friday of August - providing this is
        # not prior to the 5th - in which case it will begin on the second
        # Friday. The Wednesday during the show is a public holiday.
        if state == 'QLD':
            name = "The Royal Queensland Show"
            calculated_holidays[date(year, AUG, 5) + rd(weekday=FR) + rd(weekday=WE)] = \
                name

        # Christmas Day
        name = "Christmas Day"
        dec25 = date(year, DEC, 25)
        
        if OBSERVED and dec25.weekday() not in WEEKEND:
            calculated_holidays[dec25] = name
        else:
            calculated_holidays[date(year, DEC, 27)] = name + " (Observed)"
        # Boxing Day
        if state == 'SA':
            name = "Proclamation Day"
        else:
            name = "Boxing Day"
        dec26 = date(year, DEC, 26)
        
        if OBSERVED and dec26.weekday() not in WEEKEND:
            calculated_holidays[dec26] = name
        else:
            calculated_holidays[date(year, DEC, 28)] = name + " (Observed)"            

        return calculated_holidays



