from django.db import models
from dsh.models import County, ReportingPeriod


class HousingTarget(models.Model):
    KPI_CHOICES = [
        ("kenyans_onboarded", "Kenyans Onboarded"),
        ("units_completed", "Units Completed"),
        ("units_pending", "Units Pending"),
        ("units_bought", "Units Bought"),
    ]
    kpi = models.CharField(max_length=50, choices=KPI_CHOICES)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True, blank=True)
    target_value = models.PositiveIntegerField()
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    class Meta:
        ordering = ["kpi", "county", "start_year"]
        verbose_name = "Housing Target"

    def __str__(self):
        county_name = f" | {self.county}" if self.county else ""
        return f"{self.kpi}{county_name} ({self.start_year}-{self.end_year})"


class KenyansOnboarded(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    onboarded_count = models.PositiveIntegerField()
    target = models.ForeignKey(HousingTarget, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("county", "period")
        ordering = ["period", "county"]
        verbose_name = "Kenyans Onboarded"

    def percentage_covered(self):
        if self.target:
            return (self.onboarded_count / self.target.target_value) * 100
        return 0

    def __str__(self):
        return f"{self.county} | Onboarded: {self.onboarded_count} | {self.period}"


class HousingUnit(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("pending", "Pending"),
    ]
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    unit_count = models.PositiveIntegerField()
    target = models.ForeignKey(HousingTarget, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("county", "period", "status")
        ordering = ["period", "county", "status"]
        verbose_name = "Housing Unit"

    def percentage_covered(self):
        if self.target:
            return (self.unit_count / self.target.target_value) * 100
        return 0

    def __str__(self):
        return f"{self.county} | {self.status.capitalize()} Units: {self.unit_count} | {self.period}"


class HousingUnitBought(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    units_bought = models.PositiveIntegerField()
    target = models.ForeignKey(HousingTarget, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("county", "period")
        ordering = ["period", "county"]
        verbose_name = "Units Bought"

    def percentage_covered(self):
        if self.target:
            return (self.units_bought / self.target.target_value) * 100
        return 0

    def __str__(self):
        return f"{self.county} | Units Bought: {self.units_bought} | {self.period}"
