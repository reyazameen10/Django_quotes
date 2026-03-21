from django.db import models
import csv
from datetime import datetime

# Create your models here.

class Voter(models.Model):
    # Basic Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    dob = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=5)

    
    # Participation (Stored as Booleans)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.precinct_number})"

def load_data():
        """Function to load CSV data into the Voter model."""
        # Clear existing data to avoid duplicates during testing
        Voter.objects.all().delete()
        
        filename = 'cs412/newton_voters.csv'
        
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    v = Voter(
                        last_name=row['Last Name'],
                        first_name=row['First Name'],
                        street_number=row['Residential Address - Street Number'],
                        street_name=row['Residential Address - Street Name'],
                        apartment_number=row['Residential Address - Apartment Number'],
                        zip_code=row['Residential Address - Zip Code'],
                        dob=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                        registration_date=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                        party_affiliation=row['Party Affiliation'].strip(),
                        precinct_number=row['Precinct Number'],
                        v20state=row['v20state'].upper() == 'TRUE',
                        v21town=row['v21town'].upper() == 'TRUE',
                        v21primary=row['v21primary'].upper() == 'TRUE',
                        v22general=row['v22general'].upper() == 'TRUE',
                        v23town=row['v23town'].upper() == 'TRUE',
                        voter_score=int(row['voter_score'])
                    )
                    v.save()
                except Exception as e:
                    print(f"Error skipping row: {e}")

        print(f"Done! Loaded {Voter.objects.count()} records.")
