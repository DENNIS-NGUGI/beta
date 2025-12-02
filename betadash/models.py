from django.db import models

class County(models.Model):
    name = models.CharField(max_length=100)
    sha_registrations = models.IntegerField()
    population = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Counties"
        
class HealthRecord(models.Model):
    COUNTY_CHOICES = [
        ('Mombasa', 'Mombasa'),
        ('Bomet', 'Bomet'),
        ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
        ('Kirinyaga', 'Kirinyaga'),
        ('Nyeri', 'Nyeri'),
        ('Kisumu', 'Kisumu'),
        ('Embu', 'Embu'),
        ('Tharaka Nithi', 'Tharaka Nithi'),
        ('Taita Taveta', 'Taita Taveta'),
        ('Kericho', 'Kericho'),
        ('Lamu', 'Lamu'),
        ('Nandi', 'Nandi'),
        ('Nairobi', 'Nairobi'),
        ('Homa Bay', 'Homa Bay'),
        ('Nyamira', 'Nyamira'),
        ('Laikipia', 'Laikipia'),
        ('Kajiado', 'Kajiado'),
        ('Uasin Gishu', 'Uasin Gishu'),
        ('Kakamega', 'Kakamega'),
        ('Kiambu', 'Kiambu'),
        ('Nyandarua', 'Nyandarua'),
        ('Machakos', 'Machakos'),
        ('Nakuru', 'Nakuru'),
        ('Migori', 'Migori'),
        ('Vihiga', 'Vihiga'),
        ('Kisii', 'Kisii'),
        ('Baringo', 'Baringo'),
        ('Siaya', 'Siaya'),
        ('Bungoma', 'Bungoma'),
        ('Makueni', 'Makueni'),
        ('Busia', 'Busia'),
        ('Samburu', 'Samburu'),
        ('Kilifi', 'Kilifi'),
        ('Kitui', 'Kitui'),
        ('Kwale', 'Kwale'),
        ('Meru', 'Meru'),
        ('Muranga', 'Muranga'),
        ('Trans Nzoia', 'Trans Nzoia'),
        ('Narok', 'Narok'),
        ('Mandera', 'Mandera'),
        ('West Pokot', 'West Pokot'),
        ('Tana River', 'Tana River'),
        ('Wajir', 'Wajir'),
        ('Garissa', 'Garissa'),
        ('Marsabit', 'Marsabit'),
        ('Isiolo', 'Isiolo'),
        ('Turkana', 'Turkana'),
    ]
    county = models.CharField(max_length=100, choices=COUNTY_CHOICES)
    month_and_year = models.CharField(max_length=100, null=True)
    diabetes_cases = models.PositiveIntegerField(default=0)
    hypertension_cases = models.PositiveIntegerField(default=0)
    no = models.IntegerField(default=0)

    class Meta:
        ordering = ['county']

    def __str__(self):
        return f"{self.county} - {self.month_and_year}"

        