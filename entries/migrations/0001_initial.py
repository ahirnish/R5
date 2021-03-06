# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-02 17:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvgProductionRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], help_text='Enter month', validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050)], default=2000, help_text='Enter year', validators=[django.core.validators.MinValueValidator(2000)])),
                ('avgProdReq', models.FloatField(help_text='Enter average production required in ML for the given month', validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='CWR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], help_text='Enter date', validators=[django.core.validators.MaxValueValidator(31), django.core.validators.MinValueValidator(1)])),
                ('month', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], help_text='Enter month', validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050)], help_text='Enter year', validators=[django.core.validators.MinValueValidator(2000)])),
                ('location', models.CharField(choices=[('Thadoli', 'Thadoli'), ('Kekri I', 'Kekri I'), ('Kekri II', 'Kekri II'), ('Goyala', 'Goyala'), ('Nasirabad I', 'Nasirabad I'), ('Nasirabad II', 'Nasirabad II'), ('PS 6', 'PS 6')], help_text='Enter location', max_length=100)),
                ('cwrValue', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], help_text='Enter date', validators=[django.core.validators.MaxValueValidator(31), django.core.validators.MinValueValidator(1)])),
                ('month', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], help_text='Enter month', validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050)], help_text='Enter year', validators=[django.core.validators.MinValueValidator(2000)])),
                ('todaRaiSinghPart', models.FloatField(help_text='Enter water supply for TodaRaiSingh', validators=[django.core.validators.MinValueValidator(0)])),
                ('bagheraPHPart', models.FloatField(help_text='Enter water supply for Baghera', validators=[django.core.validators.MinValueValidator(0)])),
                ('filterLossesOldWTP', models.FloatField(help_text='Enter filter losses for old WTP', validators=[django.core.validators.MinValueValidator(0)])),
                ('filterLossesNewWTP', models.FloatField(help_text='Enter filter losses for new WTP', validators=[django.core.validators.MinValueValidator(0)])),
                ('kekriPart', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('sarwarPart', models.FloatField(help_text='Enter water supply for Sarwar', validators=[django.core.validators.MinValueValidator(0)])),
                ('ps4Part', models.FloatField(help_text='Enter water supply for PS 4', validators=[django.core.validators.MinValueValidator(0)])),
                ('ps5Part', models.FloatField(help_text='Enter water supply for PS 5', validators=[django.core.validators.MinValueValidator(0)])),
                ('sr7Part', models.FloatField(help_text='Enter water supply for SR7', validators=[django.core.validators.MinValueValidator(0)])),
                ('beawarPart', models.FloatField(help_text='Enter water supply for Beawar', validators=[django.core.validators.MinValueValidator(0)])),
                ('kishangarhPart', models.FloatField(help_text='Enter water supply for Kishangarh', validators=[django.core.validators.MinValueValidator(0)])),
                ('nasirabadCBPart', models.FloatField(help_text='Enter water supply for Nasirabad CB', validators=[django.core.validators.MinValueValidator(0)])),
                ('mesnsdPart', models.FloatField(help_text='Enter water supply for MES NSD', validators=[django.core.validators.MinValueValidator(0)])),
                ('beawarRuralPart', models.FloatField(help_text='Enter water supply for Beawar Rural', validators=[django.core.validators.MinValueValidator(0)])),
                ('nandlaPHPart', models.FloatField(help_text='Enter water supply for Nandla PH', validators=[django.core.validators.MinValueValidator(0)])),
                ('kekri1200mmPart', models.FloatField(help_text='Enter water supply for Kekri 1200mm', validators=[django.core.validators.MinValueValidator(0)])),
                ('kekri1600mmPart', models.FloatField(help_text='Enter water supply for Kekri 1600mm', validators=[django.core.validators.MinValueValidator(0)])),
                ('tdlOldSystem', models.FloatField(help_text='Enter water supply for Thadoli through old system', validators=[django.core.validators.MinValueValidator(0)])),
                ('tdlNewSystem', models.FloatField(help_text='Enter water supply for Thadoli through new system', validators=[django.core.validators.MinValueValidator(0)])),
                ('kekriOldSystem', models.FloatField(help_text='Enter water supply for Kekri through old system', validators=[django.core.validators.MinValueValidator(0)])),
                ('kekriNewSystem', models.FloatField(help_text='Enter water supply for Kekri through new system', validators=[django.core.validators.MinValueValidator(0)])),
                ('throughNewWTP', models.FloatField(help_text='Enter water supply through new WTP', validators=[django.core.validators.MinValueValidator(0)])),
                ('throughOldWTP', models.FloatField(help_text='Enter water supply through old WTP', validators=[django.core.validators.MinValueValidator(0)])),
                ('reservoirThadoli', models.FloatField(default=0, help_text='Enter water distribution for Thadoli reservoir', validators=[django.core.validators.MinValueValidator(0)])),
                ('reservoirKekriI', models.FloatField(default=0, help_text='Enter water distribution for Kekri I reservoir', validators=[django.core.validators.MinValueValidator(0)])),
                ('reservoirKekriII', models.FloatField(default=0, help_text='Enter water distribution for Kekri II reservoir', validators=[django.core.validators.MinValueValidator(0)])),
                ('reservoirGoyala', models.FloatField(default=0, help_text='Enter water distribution for Goyala reservoir', validators=[django.core.validators.MinValueValidator(0)])),
                ('reservoirNsdI', models.FloatField(default=0, help_text='Enter water distribution for Nasirabad I reservoir', validators=[django.core.validators.MinValueValidator(0)])),
                ('reservoirNsdII', models.FloatField(default=0, help_text='Enter water distribution for Nasirabad II reservoir', validators=[django.core.validators.MinValueValidator(0)])),
                ('reservoirPS6', models.FloatField(default=0, help_text='Enter water distribution for PS 6 reservoir', validators=[django.core.validators.MinValueValidator(0)])),
                ('incomingKekri', models.FloatField(help_text='Enter water incoming value at Kekri', validators=[django.core.validators.MinValueValidator(0)])),
                ('incomingNsd', models.FloatField(help_text='Enter water incoming value at Nasirabad', validators=[django.core.validators.MinValueValidator(0)])),
                ('uawThadoli', models.FloatField(help_text='Enter UAW value at Thadoli', validators=[django.core.validators.MinValueValidator(0)])),
                ('uawKekri', models.FloatField(help_text='Enter UAW value at Kekri', validators=[django.core.validators.MinValueValidator(0)])),
                ('uawNsd', models.FloatField(help_text='Enter UAW value at Nasirabad', validators=[django.core.validators.MinValueValidator(0)])),
                ('totalUAW', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('cwr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.CWR')),
            ],
        ),
        migrations.CreateModel(
            name='ElectricityBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(help_text='Enter city name', max_length=100)),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050)], default=2000, help_text='Enter billing year', validators=[django.core.validators.MinValueValidator(2000)])),
                ('month', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], default=1, help_text='Enter billing month', validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('dueDate', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], default=1, help_text='Enter billing due date', validators=[django.core.validators.MaxValueValidator(31), django.core.validators.MinValueValidator(1)])),
                ('amount', models.FloatField(help_text='Enter billing amount', validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('text', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('year', models.IntegerField(default=2000, primary_key=True, serialize=False)),
                ('amount', models.FloatField(default=10.0)),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], help_text='Enter date', validators=[django.core.validators.MaxValueValidator(31), django.core.validators.MinValueValidator(1)])),
                ('month', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], help_text='Enter month', validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050)], help_text='Enter year', validators=[django.core.validators.MinValueValidator(2000)])),
                ('damLevel', models.FloatField(help_text='Enter dam level', validators=[django.core.validators.MinValueValidator(0)])),
                ('availableCapacity', models.FloatField(help_text='Enter available capacity', validators=[django.core.validators.MinValueValidator(0)])),
                ('wsJaipurPart', models.FloatField(help_text='Enter water supply for Jaipur', validators=[django.core.validators.MinValueValidator(0)])),
                ('wsAjmerPart', models.FloatField(help_text='Enter water supply for Ajmer', validators=[django.core.validators.MinValueValidator(0)])),
                ('totalWsPart', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('irrigationOROtherLosses', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('shortFallExcess', models.FloatField()),
                ('alert', models.CharField(default='None', max_length=100)),
                ('faultTypeNumberBisalpur', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, help_text='Select fault type at Bisalpur', validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)])),
                ('faultTypeNumberThadoli', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, help_text='Select fault type at Thadoli', validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)])),
                ('faultTypeNumberKekri', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, help_text='Select fault type at Kekri', validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)])),
                ('faultTypeNumberGoyala', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, help_text='Select fault type at Goyala', validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)])),
                ('faultTypeNumberNasirabad', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, help_text='Select fault type at Nasirabad', validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)])),
                ('remarksForLessProduction', models.CharField(default='None', max_length=100)),
                ('avgProductionRequirement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entries.AvgProductionRequirement')),
            ],
        ),
        migrations.AddField(
            model_name='distribution',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.Production'),
        ),
    ]
