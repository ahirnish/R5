from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from .models import Entry, ElectricityBill, AvgProductionRequirement, Production, CWR, Distribution
from .models import MONTH_CHOICES, LOCATION_CHOICES
from .forms import EntryForm, ElectricityBillForm, ProductionForm, AvgProductionRequirementForm, CWRForm, DistributionForm
from matplotlib import pyplot as PLT
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.ticker as ticker
import urllib
import json
import datetime

errorList = {}
errorList['NO_AVG_PROD_REQ'] = "*Average Production Requirement for month %s, %s does not exist. Please add it first!"
errorList['NO_PREV_DAY_ENTRY'] = "*Previous day's record does not exist. Please enter it first!"

def index(request):
    entries = Entry.objects.all()
    electricityBills = ElectricityBill.objects.all()
    avgProdReqs = AvgProductionRequirement.objects.all()
    productions = Production.objects.all()
    cwrValues = CWR.objects.all()
    distributions = Distribution.objects.all()
    return render( request, 'entries/index.html', {'entries':entries,
                                                   'electricityBills':electricityBills,
                                                   'avgProdReqs':avgProdReqs,
                                                   'productions':productions,
                                                   'cwrValues':cwrValues,
                                                   'distributions':distributions } )

def add_data( request ):
    if request.method == 'POST':

        # Checks if given year's data is already there
        # if yes, then delete it and take the provided one
        # as updated one.
        yearGiven = request.POST.get( 'year' )
        entryExists = Entry.objects.filter( year=yearGiven ).exists()
        if( entryExists ):
            Entry.objects.get( year=yearGiven ).delete()

        form = EntryForm( request.POST )
        
        if form.is_valid():
            # form.is_valid() checks for DB constraints of uniqueness and primary-key. 
            # If same year given and
            # year being primary-key, it will crib and wont let you update. It
            # will force you to change the year. Hence taking care of updation
            # happens before checking the validity of form.

            # Save the data
            form.save(commit=True)

            # Show the main page
            return index( request )
        else:
            print(form.errors)
    else:
        form = EntryForm()
    
    return render( request, 'entries/add_data.html', {'form': form} )

def display_image( request ):
    entries = Entry.objects.all()
    yearSet = []
    amountSet = []
    for entry in entries:
        yearSet.append( entry.year )
        amountSet.append( entry.amount )
    year = [ i[0] for i in sorted( zip(yearSet,amountSet) ) ]
    amount = [ i[1] for i in sorted( zip(yearSet,amountSet) ) ]

    fig = Figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(year, amount, '-')
    ax1.set_xlabel( 'Year' )
    ax1.set_ylabel( 'Amount' )
    tick_spacing = 1
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def electricityBillView( request ):
    if request.method == 'POST':

        # Checks if given year's data is already there
        # if yes, then delete it and take the provided one
        # as updated one.
        cityGiven = request.POST.get( 'city' )
        yearGiven = request.POST.get( 'year' )
        monthGiven = request.POST.get( 'month' )
        dueDateGiven = request.POST.get( 'dueDate' )
        billExists = ElectricityBill.objects.filter( city=cityGiven, year=yearGiven,
                                                     month=monthGiven, dueDate=dueDateGiven ).exists()
        if( billExists ):
            form = ElectricityBillForm( request.POST, instance = ElectricityBill.objects.get( city=cityGiven, year=yearGiven,month=monthGiven, dueDate=dueDateGiven ) )
        else:
            form = ElectricityBillForm( request.POST )
        
        if form.is_valid():
            # form.is_valid() checks for DB constraints of uniqueness and primary-key. 
            # If same year given and
            # year being primary-key, it will crib and wont let you update. It
            # will force you to change the year. Hence taking care of updation
            # happens before checking the validity of form.

            # Save the data
            form.save(commit=True)

            # Redirecting to same page with empty form
            return render( request, 'entries/add_electricity_bill.html', {'form': ElectricityBillForm()} )

            # Show the main page
            # return index( request )
        else:
            print(form.errors)
    else:
        form = ElectricityBillForm()
    
    return render( request, 'entries/add_electricity_bill.html', {'form': form} )

def avgProductionRequirementView( request ):
    if request.method == 'POST':

        # Checks if given year's data is already there
        # if yes, then delete it and take the provided one
        # as updated one.
        yearGiven = request.POST.get( 'year' )
        monthGiven = request.POST.get( 'month' )
        avgProdReqExists = AvgProductionRequirement.objects.filter( month=monthGiven, year=yearGiven ).exists()

        if( avgProdReqExists ):
            form = AvgProductionRequirementForm( request.POST, instance=AvgProductionRequirement.objects.get( month=monthGiven, year=yearGiven ) )
        else:
            form = AvgProductionRequirementForm( request.POST )
        
        if form.is_valid():
            # form.is_valid() checks for DB constraints of uniqueness and primary-key. 
            # If same year given and
            # year being primary-key, it will crib and wont let you update. It
            # will force you to change the year. Hence taking care of updation
            # happens before checking the validity of form.

            # Save the data
            form.save(commit=True)

#            !! implemented post_save signal receive method in models.py to get the notification. Below lines now not required !!
#            for prod in Production.objects.filter( month=monthGiven, year=yearGiven ):
#                prod.save()

            # Redirecting to same page with empty form
            return render( request, 'entries/add_avg_production_requirement.html', {'form': AvgProductionRequirementForm()} )

            # Show the main page
            # return index( request )
        else:
            print(form.errors)
    else:
        form = AvgProductionRequirementForm()
    
    return render( request, 'entries/add_avg_production_requirement.html', {'form': form} )

def productionView( request ):
    if request.method == 'POST':

        # Checks if given year's data is already there
        # if yes, then delete it and take the provided one
        # as updated one.
        dateGiven = request.POST.get( 'date' )
        monthGiven = request.POST.get( 'month' )
        yearGiven = request.POST.get( 'year' )
        productionExists = Production.objects.filter( date=dateGiven, month=monthGiven, year=yearGiven ).exists()
        if( productionExists ):
            form = ProductionForm( request.POST, instance=Production.objects.get( date=dateGiven, month=monthGiven, year=yearGiven ) )
        else:
            form = ProductionForm( request.POST )

        avgProdReqExists = AvgProductionRequirement.objects.filter( month=monthGiven, year=yearGiven ).exists()
        if( avgProdReqExists==False ):
            form.add_error( None,
                            errorList['NO_AVG_PROD_REQ'] %(MONTH_CHOICES[ int(monthGiven) - 1 ][1], yearGiven) )

        prev_date = datetime.datetime(day=int(dateGiven), month=int(monthGiven), year=int(yearGiven)) + datetime.timedelta( days=-1 )

        if( avgProdReqExists and Production.objects.count() != 0 and 
            not Production.objects.filter( date=prev_date.day, month=prev_date.month, year=prev_date.year ).exists() and not productionExists ):
            form.add_error( None, errorList['NO_PREV_DAY_ENTRY'] )

        if form.is_valid():

            form.instance.avgProductionRequirement = AvgProductionRequirement.objects.get( month=monthGiven, year=yearGiven )

            form.instance.irrigationOROtherLosses = Production.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year ).availableCapacity

            # Save the data
            form.save(commit=True)

            # Redirecting to same page with empty form
            return render( request, 'entries/add_production.html', {'form': ProductionForm()} )

            # Show the main page
            # return index( request )
        else:
            print(form.errors)
    else:
        form = ProductionForm()

    return render( request, 'entries/add_production.html', {'form': form} )

def distributionView( request ):
    if request.method == 'POST':

        dateGiven = request.POST.get( 'date' )
        monthGiven = request.POST.get( 'month' )
        yearGiven = request.POST.get( 'year' )
        distributionExists = Distribution.objects.filter( date=dateGiven, month=monthGiven, year=yearGiven ).exists()
        if( distributionExists ):
            form = DistributionForm( request.POST, instance=Distribution.objects.get( date=dateGiven, month=monthGiven, year=yearGiven ) )
        else:
            form = DistributionForm( request.POST )
        
        productionExists = Production.objects.filter( date=dateGiven, month=monthGiven, year=yearGiven ).exists()
        if( not productionExists ):
            form.add_error( None, "*Production data does not exist for the entered date." )
        

        cwrValuesList = CWR.objects.filter( date=dateGiven, month=monthGiven, year=yearGiven )
        if( len( cwrValuesList ) == 0 ):
            form.add_error( None, "*CWR Values do no exist for given date." )
        elif( len( cwrValuesList ) != len(LOCATION_CHOICES ) ):
            existingLocation = []
            for cwrVal in cwrValuesList:
                existingLocation.append( ( cwrVal.location, cwrVal.location ) )
            missingLocation = list( set( LOCATION_CHOICES ) - set( existingLocation ) )
            header = ''
            for i in range( len(missingLocation) ):
                header = header + missingLocation[i][0]
                if i == len(missingLocation)-2:
                    #second last
                    header = header + ' and '
                elif i == len(missingLocation)-1:
                    # last
                    passx
                else:
                    header = header + ', '
            form.add_error( None, '*CWR Values are missing for %s for given date.' % (header) )

        prev_date = datetime.datetime(day=int(dateGiven), month=int(monthGiven), year=int(yearGiven)) + datetime.timedelta( days=-1 )

        if( len( cwrValuesList ) == len(LOCATION_CHOICES ) and Distribution.objects.count() != 0 and 
            len( CWR.objects.filter( date=prev_date.day, month=prev_date.month, year=prev_date.year ) ) != len(LOCATION_CHOICES ) and distributionExists ):
            form.add_error( None, '*CWR Values of locations are missing (partially or fully) for the previous date.' )

        if form.is_valid():

            form.instance.production = Production.objects.get( date=dateGiven, month=monthGiven, year=yearGiven )

            # Save the data
            form.save(commit=True)

            # Redirecting to same page with empty form
            return render( request, 'entries/add_distribution.html', {'form': DistributionForm()} )

            # Show the main page
            # return index( request )
        else:
            print(form.errors)
    else:
        form = DistributionForm()

    return render( request, 'entries/add_distribution.html', {'form': form} )

def cwrView( request ):
    if request.method == 'POST':

        dateGiven = request.POST.get( 'date' )
        monthGiven = request.POST.get( 'month' )
        yearGiven = request.POST.get( 'year' )
        locationGiven = request.POST.get( 'location' )
        cwrValueExists = CWR.objects.filter( date=dateGiven, month=monthGiven, year=yearGiven, location=locationGiven ).exists()
        if( cwrValueExists ):
            # updates the entry rather than deleting and recreating it.
            form = CWRForm( request.POST, instance=CWR.objects.get( date=dateGiven, month=monthGiven, year=yearGiven, location=locationGiven ) )
        else:
            form = CWRForm( request.POST )
        
        if form.is_valid():
            # form.is_valid() checks for DB constraints of uniqueness and primary-key. 
            # If same year given and
            # year being primary-key, it will crib and wont let you update. It
            # will force you to change the year. Hence taking care of updation
            # happens before checking the validity of form.

            # Save the data
            form.save(commit=True)
            messages.success(request, 'Value entered successfully for %s!' % (locationGiven))
            
            return render( request, 'entries/add_cwr_value.html', {'form': CWRForm()} )
        else:
            print(form.errors)
    else:
        form = CWRForm()
    
    return render( request, 'entries/add_cwr_value.html', {'form': form} )

def cryptoPriceView( request ):
    url = "https://koinex.in/api/ticker"
    response = urllib.request.urlopen( url )
    data = json.loads( response.read() )
    totalAmountEth = str(float( data[ "prices" ][ "ETH" ]) * 4.47) + " INR Ethereum"
    totalAmountLtc = str(float( data[ "prices" ][ "LTC" ]) * 2.05) + " INR Litecoin"
    priceEth = str( float( data[ "prices" ]["ETH"]) ) + " INR/ETH"
    priceLitecoin = str( float( data["prices"]["LTC"]) ) + " INR/LTC"

    return render( request, 'entries/cryptoprice.html', {'priceEth':priceEth, 'priceLitecoin':priceLitecoin, 'totalAmountEth':totalAmountEth, 'totalAmountLtc':totalAmountLtc} )
