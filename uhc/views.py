from django.shortcuts import render
# from django.http import JsonResponse
# from django.db.models import Sum, Count
# from django.views.decorators.http import require_GET
# from django.contrib.auth.decorators import login_required

# from .models import (
#     County,
#     ReportingPeriod,
#     UHCTarget,
#     SHAOnboarded,
#     SHAIndividualsTreated,
#     SHADisbursement,
#     HealthFacilityDigitized,
# )

def uhc_dashboard(request):
    # counties = County.objects.all().order_by("name")
    # years = ReportingPeriod.objects.values_list("year", flat=True).distinct().order_by("year")
    
    # targets_qs = UHCTarget.objects.all()
    # targets = {}
    # for t in targets_qs:
    #     if t.kpi in targets:
    #         targets[t.kpi] += t.target_value
    #     else:
    #         targets[t.kpi] = t.target_value

    return render(
        request,
        "pages/uhc/uhc_dashboard.html",
        #{"counties": counties, "years": years, "targets": targets}
    )

# @require_GET
# def uhc_overview(request):
#     year = request.GET.get("year")
#     county_id = request.GET.get("county")

#     onboarded_qs = SHAOnboarded.objects.all()
#     treated_qs = SHAIndividualsTreated.objects.all()
#     disbursed_qs = SHADisbursement.objects.all()
#     digitized_qs = HealthFacilityDigitized.objects.all()

#     # Apply year filter
#     if year:
#         onboarded_qs = onboarded_qs.filter(period__year=year)
#         treated_qs = treated_qs.filter(period__year=year)
#         disbursed_qs = disbursed_qs.filter(period__year=year)
#         digitized_qs = digitized_qs.filter(period__year=year)

#     # Apply county filter
#     if county_id:
#         onboarded_qs = onboarded_qs.filter(county_id=county_id)
#         treated_qs = treated_qs.filter(county_id=county_id)
#         disbursed_qs = disbursed_qs.filter(county_id=county_id)
#         digitized_qs = digitized_qs.filter(county_id=county_id)

#     return JsonResponse({
#         "sha_onboarded": onboarded_qs.aggregate(total=Sum("onboarded_count"))["total"] or 0,
#         "individuals_treated": treated_qs.aggregate(total=Sum("treated_count"))["total"] or 0,
#         "amount_disbursed": float(disbursed_qs.aggregate(total=Sum("amount_disbursed"))["total"] or 0),
#         "digitized_facilities": digitized_qs.aggregate(total=Sum("digitized_count"))["total"] or 0,
#     })


# # ------------------------------
# # SHA Onboarded Analytics
# # ------------------------------
# @require_GET
# def onboarded_data(request):
#     year = request.GET.get("year")
#     county_id = request.GET.get("county")

#     qs = SHAOnboarded.objects.select_related("county")
#     if year:
#         qs = qs.filter(period__year=year)
#     if county_id:
#         qs = qs.filter(county_id=county_id)

#     # County table for dashboard
#     table_data = qs.values("county__name").annotate(total_onboarded=Sum("onboarded_count")).order_by("county__name")

#     return JsonResponse({"by_county": list(table_data)})


# # ------------------------------
# # SHA Individuals Treated Analytics
# # ------------------------------
# @require_GET
# def treated_data(request):
#     year = request.GET.get("year")
#     county_id = request.GET.get("county")

#     qs = SHAIndividualsTreated.objects.select_related("county")
#     if year:
#         qs = qs.filter(period__year=year)
#     if county_id:
#         qs = qs.filter(county_id=county_id)

#     table_data = qs.values("county__name").annotate(total_treated=Sum("treated_count")).order_by("county__name")

#     return JsonResponse({"by_county": list(table_data)})


# # ------------------------------
# # SHA Disbursement Analytics
# # ------------------------------
# @require_GET
# def disbursement_data(request):
#     year = request.GET.get("year")
#     county_id = request.GET.get("county")

#     qs = SHADisbursement.objects.select_related("county")
#     if year:
#         qs = qs.filter(period__year=year)
#     if county_id:
#         qs = qs.filter(county_id=county_id)

#     table_data = qs.values("county__name").annotate(total_disbursed=Sum("amount_disbursed")).order_by("county__name")

#     return JsonResponse({"by_county": list(table_data)})


# # ------------------------------
# # Digitized Health Facilities Analytics
# # ------------------------------
# @require_GET
# def digitized_facilities_data(request):
#     year = request.GET.get("year")
#     county_id = request.GET.get("county")

#     qs = HealthFacilityDigitized.objects.select_related("county")
#     if year:
#         qs = qs.filter(period__year=year)
#     if county_id:
#         qs = qs.filter(county_id=county_id)

#     table_data = qs.values("county__name").annotate(total_digitized=Sum("digitized_count")).order_by("county__name")

#     return JsonResponse({"by_county": list(table_data)})
