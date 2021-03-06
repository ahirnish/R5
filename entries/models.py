from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

DATE_CHOICES = [ (x,x) for x in range(1,32) ]
MONTH_CHOICES = [ ( 1, "Jan" ), ( 2, "Feb" ), ( 3, "Mar" ), ( 4, "Apr" ), ( 5, "May" ), ( 6, "Jun" ),
                  ( 7, "Jul" ), ( 8, "Aug" ), ( 9, "Sep" ), ( 10, "Oct" ), ( 11, "Nov" ), ( 12, "Dec" ) ]
YEAR_CHOICES = [ (x,x) for x in range(2000,2051) ]
FAULT_CHOICES = [ (x,x) for x in range(0,5) ]
LOCATION_CHOICES = [ ( 'Thadoli', 'Thadoli' ), ( 'Kekri I', 'Kekri I' ), ( 'Kekri II', 'Kekri II' ), ( 'Goyala', 'Goyala' ),
                     ( 'Nasirabad I', 'Nasirabad I' ), ( 'Nasirabad II', 'Nasirabad II' ), ( 'PS 6', 'PS 6' ) ]

PSConstants = {}
for loc in LOCATION_CHOICES:
    tc=0
    fsl=0
    PSConstants[ loc[0] ] = {}
    if loc[0] == 'Thadoli':
        tc=26
        fsl=4.4
    elif loc[0] == 'Kekri I':
        tc = 12
        fsl=4.4
    elif loc[0] == 'Kekri II':
        tc=15
        fsl=5.2
    elif loc[0] == 'Goyala':
        tc=9
        fsl=4
    elif loc[0] == 'Nasirabad I':
        tc=8
        fsl=3.25
    elif loc[0] == 'Nasirabad II':
        tc = 13
        fsl=3.35
    elif loc[0] == 'PS 6':
        tc=6
        fsl=3.35
    PSConstants[ loc[0] ][ 'tankCapacity' ] = tc
    PSConstants[ loc[0] ][ 'FSL' ] = fsl

# Create your models here.

class Entry( models.Model ):
    text = models.TextField()
    author = models.CharField(max_length=100)
    year = models.IntegerField( default=2000, primary_key=True )
    amount = models.FloatField( default=10.0 )

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + ' ' + str(self.year)

class ElectricityBill( models.Model ):
    city = models.CharField( max_length=100, blank=False, help_text="Enter city name" )
    year = models.IntegerField( validators=[MinValueValidator(2000)], blank=False, choices=YEAR_CHOICES, help_text="Enter billing year", default=2000 )
    month = models.IntegerField( validators=[MaxValueValidator(12), MinValueValidator(1)], blank=False,
                                 choices=MONTH_CHOICES, help_text="Enter billing month", default=1 )
    dueDate = models.IntegerField( validators=[MaxValueValidator(31), MinValueValidator(1)], blank=False,
                                   choices=DATE_CHOICES, help_text="Enter billing due date", default=1 )
    amount = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text="Enter billing amount" )

    def __str__(self):
        return self.city + ' ' + str(self.dueDate) + '/' + str(self.month) + '/' + str(self.year) + ' ' + str(self.amount)

class AvgProductionRequirement( models.Model ):
    month = models.IntegerField( validators=[MaxValueValidator(12), MinValueValidator(1)], blank=False,
                                 choices=MONTH_CHOICES, help_text='Enter month', default=1 )
    year = models.IntegerField( validators=[MinValueValidator(2000)], blank=False, help_text='Enter year', default=YEAR_CHOICES[0][0], choices=YEAR_CHOICES )
    avgProdReq = models.FloatField( validators=[MinValueValidator(0)], blank=False,
                                    help_text='Enter average production required in ML for the given month' )
    def __str__( self ):
        return MONTH_CHOICES[ self.month - 1 ][1] + " " + str( self.year ) + " " + str( self.avgProdReq )

class Production( models.Model ):
    date = models.IntegerField( validators=[MaxValueValidator(31), MinValueValidator(1)], blank=False,
                                choices=DATE_CHOICES, help_text='Enter date', default=1 )
    month = models.IntegerField( validators=[MaxValueValidator(12), MinValueValidator(1)], blank=False,
                                 choices=MONTH_CHOICES, help_text='Enter month', default=1 )
    year = models.IntegerField( validators=[MinValueValidator(2000)], blank=False, help_text='Enter year', choices=YEAR_CHOICES, default=YEAR_CHOICES[0][0] )
    damLevel = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter dam level' )
    availableCapacity = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter available capacity' )
    wsJaipurPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Jaipur' )
    wsAjmerPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Ajmer' )
    totalWsPart = models.FloatField( validators=[MinValueValidator(0)], blank=False )
    irrigationOROtherLosses = models.FloatField( validators=[MinValueValidator(0)], default=0.0 )
    shortFallExcess = models.FloatField( blank=False )
    alert = models.CharField( max_length=100, default="None" )
    faultTypeNumberBisalpur = models.IntegerField( validators=[MaxValueValidator(4), MinValueValidator(0)], default=0,
                                                   choices=FAULT_CHOICES, help_text='Select fault type at Bisalpur' )
    faultTypeNumberThadoli = models.IntegerField( validators=[MaxValueValidator(4), MinValueValidator(0)], default=0,
                                                   choices=FAULT_CHOICES, help_text='Select fault type at Thadoli' )
    faultTypeNumberKekri = models.IntegerField( validators=[MaxValueValidator(4), MinValueValidator(0)], default=0,
                                                   choices=FAULT_CHOICES, help_text='Select fault type at Kekri' )
    faultTypeNumberGoyala = models.IntegerField( validators=[MaxValueValidator(4), MinValueValidator(0)], default=0,
                                                   choices=FAULT_CHOICES, help_text='Select fault type at Goyala' )
    faultTypeNumberNasirabad = models.IntegerField( validators=[MaxValueValidator(4), MinValueValidator(0)], default=0,
                                                   choices=FAULT_CHOICES, help_text='Select fault type at Nasirabad' )
    remarksForLessProduction = models.CharField( max_length=100, default="None" )
    avgProductionRequirement = models.ForeignKey( AvgProductionRequirement, blank=True, null=True ) #null should be False as avg prod req cant be zero. Check!

    def save( self, *args, **kwargs ):
        self.totalWsPart = self.wsAjmerPart + self.wsJaipurPart
        self.shortFallExcess = self.wsAjmerPart - self.avgProductionRequirement.avgProdReq
        if( self.shortFallExcess != -1*self.avgProductionRequirement.avgProdReq ):
            if( self.shortFallExcess < -10 and self.faultTypeNumberBisalpur == 0 and self.faultTypeNumberThadoli == 0 and
                self.faultTypeNumberKekri == 0 and self.faultTypeNumberGoyala == 0 and self.faultTypeNumberNasirabad == 0 ):
                self.alert = "Mark FTN"
        if( not (self.faultTypeNumberBisalpur == 0 and self.faultTypeNumberThadoli == 0 and self.faultTypeNumberKekri == 0 and 
              self.faultTypeNumberGoyala == 0 and self.faultTypeNumberNasirabad == 0) ):
            if( self.faultTypeNumberBisalpur == 4 or self.faultTypeNumberThadoli == 4 or self.faultTypeNumberKekri == 4 or
                self.faultTypeNumberGoyala == 4 or self.faultTypeNumberNasirabad == 4 ):
                self.remarksForLessProduction = "Other reason."
            else:
                remark = ""
                if( self.faultTypeNumberBisalpur == 1 ):
                    remark += "Electric line fault at Intake "
                else:
                    if( self.faultTypeNumberThadoli == 1 ):
                        remark += "Electric line fault at Thadoli "
                    else:
                        if( self.faultTypeNumberKekri == 1 ):
                            remark += "Electric line fault at Kekri "
                        else:
                            if( self.faultTypeNumberGoyala == 1 ):
                                remark += "Electric line fault at Goyala "
                            else:
                                if( self.faultTypeNumberNasirabad == 1 ):
                                    remark += "Electric line fault at Nasirabad "
                remark += ", "
                if( self.faultTypeNumberBisalpur == 2 ):
                    remark += "Fault in pH at Intake "
                else:
                    if( self.faultTypeNumberThadoli == 2 ):
                        remark += "Fault in pH at Thadoli "
                    else:
                        if( self.faultTypeNumberKekri == 2 ):
                            remark += "Fault in pH at Kekri "
                        else:
                            if( self.faultTypeNumberGoyala == 2 ):
                                remark += "Fault in pH at Goyala "
                            else:
                                if( self.faultTypeNumberNasirabad == 2 ):
                                    remark += "Fault in pH at Nasirabad "
                remark += ", "
                if( self.faultTypeNumberBisalpur == 3 ):
                    remark += "Breakdown in PL in between Intake and Thadoli."
                else:
                    if( self.faultTypeNumberThadoli == 3 ):
                        remark += "Breakdown in PL in between Thadoli and Kekri."
                    else:
                        if( self.faultTypeNumberKekri == 3 ):
                            remark += "Breakdown in PL in between Kekri and Goyala.."
                        else:
                            if( self.faultTypeNumberGoyala == 3 ):
                                remark += "Breakdown in PL in between Goyala and Nasirabad."
                self.remarksForLessProduction = remark

        if( self.damLevel == 0 ):
            self.irrigationOROtherLosses = 0
        else:
            # HACK
            # irrigationOROtherLosses in RHS contains previous date available capacity. Value set in the form in views.py
            self.irrigationOROtherLosses = self.irrigationOROtherLosses - self.availableCapacity - self.totalWsPart

        super().save(*args, **kwargs)

    def __str__( self ):
        return str(self.date) + '/' + str(self.month) + '/' + str(self.year) + ' ' + self.remarksForLessProduction + ' ' + str( self.avgProductionRequirement.avgProdReq ) + ' ' + str( self.irrigationOROtherLosses ) + ' ' + str( self.shortFallExcess ) + ', wsAjmerPart = ' + str(self.wsAjmerPart)

                                 
class CWR( models.Model ):
    date = models.IntegerField( validators=[MaxValueValidator(31), MinValueValidator(1)], blank=False,
                                choices=DATE_CHOICES, help_text='Enter date', default=1 )
    month = models.IntegerField( validators=[MaxValueValidator(12), MinValueValidator(1)], blank=False,
                                 choices=MONTH_CHOICES, help_text='Enter month', default=1 )
    year = models.IntegerField( validators=[MinValueValidator(2000)], blank=False, help_text='Enter year', choices=YEAR_CHOICES, default=YEAR_CHOICES[0][0] )
    location = models.CharField( max_length=100, blank=False, choices=LOCATION_CHOICES, help_text="Enter location")
    cwrValue = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text="Enter CWR Value" )

    def __str__( self ):
        return 'CWR: ' + self.location + ' ' + str(self.date) + '/' + str(self.month) + '/' + str(self.year) + ' ' + str( self.cwrValue )

class Distribution( models.Model ):
    date = models.IntegerField( validators=[MaxValueValidator(31), MinValueValidator(1)], blank=False,
                                choices=DATE_CHOICES, help_text='Enter date', default=1 )
    month = models.IntegerField( validators=[MaxValueValidator(12), MinValueValidator(1)], blank=False,
                                 choices=MONTH_CHOICES, help_text='Enter month', default=1 )
    year = models.IntegerField( validators=[MinValueValidator(2000)], blank=False, help_text='Enter year', choices=YEAR_CHOICES, default=YEAR_CHOICES[0][0] )

    production = models.ForeignKey( Production )

    todaRaiSinghPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for TodaRaiSingh' )
    bagheraPHPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Baghera' )
    filterLossesOldWTP = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter filter losses for old WTP' )
    filterLossesNewWTP = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter filter losses for new WTP' )
    kekriPart = models.FloatField( validators=[MinValueValidator(0)], blank=False )
    sarwarPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Sarwar' )
    ps4Part = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for PS 4' )
    ps5Part = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for PS 5' )
    sr7Part = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for SR7' )
    beawarPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Beawar' )
    kishangarhPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Kishangarh' )
    nasirabadCBPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Nasirabad CB' )
    mesnsdPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for MES NSD' )
    beawarRuralPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Beawar Rural' )
    nandlaPHPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Nandla PH' )
    kekri1200mmPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Kekri 1200mm' )
    kekri1600mmPart = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Kekri 1600mm' )
    tdlOldSystem = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Thadoli through old system' )
    tdlNewSystem = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Thadoli through new system' )
    kekriOldSystem = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Kekri through old system' )
    kekriNewSystem = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply for Kekri through new system' )
    throughNewWTP = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply through new WTP' )
    throughOldWTP = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water supply through old WTP' )
    reservoirThadoli = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water distribution for Thadoli reservoir', default=0 )
    reservoirKekriI = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water distribution for Kekri I reservoir', default=0 )
    reservoirKekriII = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water distribution for Kekri II reservoir', default=0 )
    reservoirGoyala = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water distribution for Goyala reservoir', default=0 )
    reservoirNsdI = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water distribution for Nasirabad I reservoir', default=0 )
    reservoirNsdII = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water distribution for Nasirabad II reservoir', default=0 )
    reservoirPS6 = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water distribution for PS 6 reservoir', default=0 )
    incomingKekri = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water incoming value at Kekri' )
    incomingNsd = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter water incoming value at Nasirabad' )
    uawThadoli = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter UAW value at Thadoli' )
    uawKekri = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter UAW value at Kekri' )
    uawNsd = models.FloatField( validators=[MinValueValidator(0)], blank=False, help_text='Enter UAW value at Nasirabad' )
    totalUAW = models.FloatField( validators=[MinValueValidator(0)], blank=False )
    
    def save( self, *args, **kwargs ):
        
        self.kekriPart = self.kekri1200mmPart + self.kekri1600mmPart
        self.throughOldWTP = self.kekriOldSystem + self.kekriNewSystem - self.throughNewWTP

        #use of cwr in below quantities
        prev_date = datetime.datetime(day=int(self.date), month=int(self.month), year=int(self.year)) + datetime.timedelta( days=-1 )

        self.reservoirThadoli = ( PSConstants[ LOCATION_CHOICES[0][0] ][ 'tankCapacity' ] / PSConstants[ LOCATION_CHOICES[0][0] ][ 'FSL' ] ) * ( CWR.objects.get( date=self.date, month=self.month, year=self.year, location=LOCATION_CHOICES[0][0] ).cwrValue - CWR.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year, location=LOCATION_CHOICES[0][0] ).cwrValue )
        self.reservoirKekriI = ( PSConstants[ LOCATION_CHOICES[1][0] ][ 'tankCapacity' ] / PSConstants[ LOCATION_CHOICES[1][0] ][ 'FSL' ] ) * ( CWR.objects.get( date=self.date,\
 month=self.month, year=self.year, location=LOCATION_CHOICES[1][0] ).cwrValue - CWR.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year, location=LOCATION_CHOICES[1][0] ).cwrValue )
        self.reservoirKekriII = ( PSConstants[ LOCATION_CHOICES[2][0] ][ 'tankCapacity' ] / PSConstants[ LOCATION_CHOICES[2][0] ][ 'FSL' ] ) * ( CWR.objects.get( date=self.date, month=self.month, year=self.year, location=LOCATION_CHOICES[2][0] ).cwrValue - CWR.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year, location=LOCATION_CHOICES[2][0] ).cwrValue )
        self.reservoirGoyala = ( PSConstants[ LOCATION_CHOICES[3][0] ][ 'tankCapacity' ] / PSConstants[ LOCATION_CHOICES[3][0] ][ 'FSL' ] ) * ( CWR.objects.get( date=self.date,\
 month=self.month, year=self.year, location=LOCATION_CHOICES[3][0] ).cwrValue - CWR.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year, location=LOCATION_CHOICES[3][0] ).cwrValue )
        self.reservoirNsdI = ( PSConstants[ LOCATION_CHOICES[4][0] ][ 'tankCapacity' ] / PSConstants[ LOCATION_CHOICES[4][0] ][ 'FSL' ] ) * ( CWR.objects.get( date=self.date,\
 month=self.month, year=self.year, location=LOCATION_CHOICES[4][0] ).cwrValue - CWR.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year, location=LOCATION_CHOICES[4][0] ).cwrValue )
        self.reservoirNsdII = ( PSConstants[ LOCATION_CHOICES[5][0] ][ 'tankCapacity' ] / PSConstants[ LOCATION_CHOICES[5][0] ][ 'FSL' ] ) * ( CWR.objects.get( date=self.date,\
 month=self.month, year=self.year, location=LOCATION_CHOICES[5][0] ).cwrValue - CWR.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year, location=LOCATION_CHOICES[5][0] ).cwrValue )
        self.reservoirPS6 = ( PSConstants[ LOCATION_CHOICES[6][0] ][ 'tankCapacity' ] / PSConstants[ LOCATION_CHOICES[6][0] ][ 'FSL' ] ) * ( CWR.objects.get( date=self.date,\
 month=self.month, year=self.year, location=LOCATION_CHOICES[6][0] ).cwrValue - CWR.objects.get( date=prev_date.day, month=prev_date.month, year=prev_date.year, location=LOCATION_CHOICES[6][0] ).cwrValue )

        self.incomingKekri = self.tdlOldSystem + self.tdlNewSystem
        self.incomingNsd = self.kekriNewSystem - self.kekri1600mmPart - self.sarwarPart + self.kekriOldSystem - self.kekri1200mmPart - self.ps4Part - self.ps5Part + self.reservoirGoyala
        self.uawThadoli = self.production.wsAjmerPart - self.todaRaiSinghPart - self.bagheraPHPart - self.tdlOldSystem - self.tdlNewSystem + self.reservoirThadoli
        self.uawKekri = self.incomingKekri - self.filterLossesOldWTP - self.filterLossesNewWTP - self.kekriOldSystem - self.kekriNewSystem + self.reservoirKekriI + self.reservoirKekriII
        self.uawNsd = self.incomingNsd - self.sr7Part - self.beawarPart - self.kishangarhPart - self.nasirabadCBPart - self.mesnsdPart - self.beawarRuralPart - self.nandlaPHPart + self.reservoirNsdI + self.reservoirNsdII + self.reservoirPS6
        self.totalUAW = self.uawThadoli + self.uawKekri + self.uawNsd
        
        super().save(*args, **kwargs)

    def __str__( self ):
        return "UAW THADOLI " + str(self.date) + "/" + str(self.month) + '/' + str(self.year) + ' ' + str( self.uawThadoli ) + ' ' + str( self.reservoirThadoli )


@receiver( post_save, sender=Production )
def updateDistributionFromProduction( sender, **kwargs ):
    production_instance = kwargs.get('instance')
    dateGiven = production_instance.date
    monthGiven = production_instance.month
    yearGiven = production_instance.year
    
    for dist in Distribution.objects.filter( date=dateGiven, month=monthGiven, year=yearGiven ):
        dist.save()

@receiver( post_save, sender=AvgProductionRequirement )
def updateProductionFromAvgProductionRequirement( sender, **kwargs ):
    avgProd_instance = kwargs.get( 'instance' )
    monthGiven = avgProd_instance.month
    yearGiven = avgProd_instance.year
    
    for prod in Production.objects.filter( month=monthGiven, year=yearGiven ):
        prod.save()

@receiver( post_save, sender=CWR )
def updateDistributionFromCWR( sender, **kwargs ):
    cwr_instance = kwargs.get( 'instance' )
    dateGiven = cwr_instance.date
    monthGiven = cwr_instance.month
    yearGiven = cwr_instance.year

    for dist in Distribution.objects.filter( date=dateGiven, month=monthGiven, year=yearGiven ):
        dist.save()


