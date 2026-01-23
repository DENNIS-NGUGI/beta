from django.db import models


class County(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Counties"

    def __str__(self):
        return self.name


class ReportingPeriod(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("year", "month")
        ordering = ["year", "month"]
        verbose_name = "Reporting Period"

    def __str__(self):
        return f"{self.year}" if not self.month else f"{self.year}-{self.month:02d}"


class FibreLinkDeployment(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    link_name = models.CharField(max_length=255)
    km_added = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["period__year", "period__month"]
        indexes = [
            models.Index(fields=["county", "period"]),
            models.Index(fields=["link_name"]),
        ]
        verbose_name = "Fibre Link Deployment"

    def __str__(self):
        return f"{self.link_name} | {self.county} | {self.period}"


class PublicWiFiHotspot(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("installed", "Installed"),
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    installation_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["county", "location"]
        verbose_name = "Public WiFi Hotspot"

    def __str__(self):
        return f"{self.location} ({self.county})"


class ICTDigitalHub(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("construction", "Under Construction"),
        ("completed", "Completed"),
        ("operational", "Operational"),
    ]

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    completion_date = models.DateField(null=True, blank=True)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)

    class Meta:
        ordering = ["county", "period"]
        verbose_name = "ICT Digital Hub"

    def __str__(self):
        return f"{self.location} | {self.county} ({self.status})"


class DigitalLiteracyProgramme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DigitalLiteracyStats(models.Model):
    programme = models.ForeignKey(DigitalLiteracyProgramme, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    trained = models.PositiveIntegerField()
    employed = models.PositiveIntegerField()

    class Meta:
        ordering = ["period", "county"]
        unique_together = ("programme", "county", "period")
        verbose_name = "Digital Literacy Statistic"

    def employment_rate(self):
        return (self.employed / self.trained * 100) if self.trained else 0

    def __str__(self):
        return f"{self.programme} | {self.county} | {self.period}"


class StudioMashinani(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("operational", "Operational"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=150)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)

    class Meta:
        ordering = ["county", "name"]
        verbose_name = "Studio Mashinani"

    def __str__(self):
        return f"{self.name} | {self.county}"


class StudioProduction(models.Model):
    studio = models.ForeignKey(StudioMashinani, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    recordings_produced = models.PositiveIntegerField()

    class Meta:
        ordering = ["period"]
        unique_together = ("studio", "period")
        verbose_name = "Studio Production"

    def __str__(self):
        return f"{self.studio} | {self.period}"


class MassMediaTraining(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    students_trained = models.PositiveIntegerField()

    class Meta:
        ordering = ["period", "county"]
        unique_together = ("county", "period")
        verbose_name = "Mass Media Training"

    def __str__(self):
        return f"{self.county} | {self.period}"


class ProgrammeTarget(models.Model):
    programme = models.CharField(max_length=100)
    target_value = models.PositiveIntegerField()
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    class Meta:
        ordering = ["programme", "start_year"]
        verbose_name = "Programme Target"

    def __str__(self):
        return f"{self.programme} ({self.start_year}–{self.end_year})"
