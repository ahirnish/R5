from django import forms
from .models import Entry, ElectricityBill, Production, AvgProductionRequirement, CWR, Distribution
from .models import DATE_CHOICES, MONTH_CHOICES, FAULT_CHOICES, LOCATION_CHOICES

class EntryForm( forms.ModelForm ):
    text = forms.CharField( widget=forms.Textarea, help_text="Please enter the text.")
    author = forms.CharField(max_length=100, help_text="Please enter author's name.")
    year = forms.IntegerField( help_text="Enter year for amount." )
    amount = forms.FloatField( help_text="Enter amount for given year." )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Entry
        fields = "__all__" 

class ElectricityBillForm( forms.ModelForm ):
#    city = forms.CharField( max_length=100, help_text="Enter city name" )
#    year = forms.IntegerField( help_text="Enter billing year" )
#    month = forms.IntegerField( help_text="Enter billing month", widget=forms.Select(choices=MONTH_CHOICES) )
#    dueDate = forms.IntegerField( help_text="Enter billing due date", widget=forms.Select(choices=DATE_CHOICES) )
#    amount = forms.FloatField( help_text="Enter billing amount" )

    class Meta:
        model = ElectricityBill
        fields = "__all__"

class ProductionForm( forms.ModelForm ):
    class Meta:
        model = Production
        fields = [ 'date', 'month', 'year', 'damLevel', 'availableCapacity', 'wsJaipurPart', 'wsAjmerPart',
                   'faultTypeNumberBisalpur', 'faultTypeNumberThadoli', 'faultTypeNumberKekri', 
                   'faultTypeNumberGoyala', 'faultTypeNumberNasirabad' ]

class DistributionForm( forms.ModelForm ):
    class Meta:
        model = Distribution
        fields = [ 'date', 'month', 'year', 'todaRaiSinghPart', 'bagheraPHPart', 'filterLossesOldWTP', 'filterLossesNewWTP', 'sarwarPart', 'ps4Part',
                   'ps5Part', 'sr7Part', 'beawarPart', 'kishangarhPart', 'nasirabadCBPart', 'mesnsdPart', 'beawarRuralPart', 'nandlaPHPart', 'kekri1200mmPart',
                   'kekri1600mmPart', 'tdlOldSystem', 'tdlNewSystem', 'kekriOldSystem', 'kekriNewSystem', 'throughNewWTP' ]

class AvgProductionRequirementForm( forms.ModelForm ):
    class Meta:
        model = AvgProductionRequirement
        fields = "__all__"
    
class CWRForm( forms.ModelForm ):
    class Meta:
        model = CWR
        fields = "__all__"
