from django.db import models
from dsh.models import County, ReportingPeriod


class UHCTarget(models.Model):
    KPI_CHOICES = [
        ("sha_onboarded", "SHA Onboarded"),
        ("individuals_treated", "Individuals Treated"),
        ("amount_disbursed", "Amount Disbursed"),
        ("digitized_facilities", "Health Facilities Digitized"),
    ]
    kpi = models.CharField(max_length=50, choices=KPI_CHOICES)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True, blank=True)
    target_value = models.PositiveIntegerField()
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    class Meta:
        ordering = ["kpi", "county", "start_year"]
        verbose_name = "UHC Target"

    def __str__(self):
        county_name = f" | {self.county}" if self.county else ""
        return f"{self.kpi}{county_name} ({self.start_year}-{self.end_year})"
    
class SHAOnboarded(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    onboarded_count = models.PositiveIntegerField()
    target = models.ForeignKey(UHCTarget, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["period", "county"]
        unique_together = ("county", "period")
        verbose_name = "SHA Onboarded"

    def percentage_covered(self):
        if self.target:
            return (self.onboarded_count / self.target.target_value) * 100
        return 0

    def __str__(self):
        return f"{self.county} | Onboarded: {self.onboarded_count} | {self.period}"


class SHAIndividualsTreated(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    treated_count = models.PositiveIntegerField()
    target = models.ForeignKey(UHCTarget, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["period", "county"]
        unique_together = ("county", "period")
        verbose_name = "SHA Individuals Treated"

    def percentage_covered(self):
        if self.target:
            return (self.treated_count / self.target.target_value) * 100
        return 0

    def __str__(self):
        return f"{self.county} | Treated: {self.treated_count} | {self.period}"


class SHADisbursement(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    amount_disbursed = models.DecimalField(max_digits=15, decimal_places=2)
    target = models.ForeignKey(UHCTarget, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["period", "county"]
        unique_together = ("county", "period")
        verbose_name = "SHA Disbursement"

    def percentage_covered(self):
        if self.target:
            return (self.amount_disbursed / self.target.target_value) * 100
        return 0

    def __str__(self):
        return f"{self.county} | Disbursed: {self.amount_disbursed} | {self.period}"


class HealthFacilityDigitized(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    digitized_count = models.PositiveIntegerField()
    target = models.ForeignKey(UHCTarget, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["period", "county"]
        unique_together = ("county", "period")
        verbose_name = "Digitized Health Facilities"

    def percentage_covered(self):
        if self.target:
            return (self.digitized_count / self.target.target_value) * 100
        return 0

    def __str__(self):
        return f"{self.county} | Digitized: {self.digitized_count} | {self.period}"
