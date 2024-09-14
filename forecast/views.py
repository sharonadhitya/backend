# forecast/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import  Reservoir
from .serializers import  ReservoirSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CsvImportForm



@api_view(['GET'])
def get_reservoirs_by_year_and_month(request, year, month):
    try:
        if isinstance(month, float):
            month = int(month)
        reservoirs = Reservoir.objects.filter(year=year, month=month)
        serializer = ReservoirSerializer(reservoirs, many=True)
        return Response(serializer.data, status=200)
    except Reservoir.DoesNotExist:
        return Response({"error": "No reservoirs found for the given year and month"}, status=404)

@api_view(['GET'])
def get_reservoirs_by_name(request,name):
    try:
        reservoirs = Reservoir.objects.filter(reservoir_name__iexact=name)
        serializer = ReservoirSerializer(reservoirs,many=True)
        return Response(serializer.data, status=200)
    except Reservoir.DoesNotExist:
        return Response({"error": "No reservoirs found for the given name"}, status=404)
    
@api_view(['GET'])
def get_reservoirs(request):
    try:
        reservoirs = Reservoir.objects.values('reservoir_name').distinct()
        return Response(reservoirs, status=200)
    except Reservoir.DoesNotExist:
        return Response({"error": "No reservoirs found"}, status=404)


@api_view(['GET'])
def get_months(request):
    print("Api Called")
    try:
        months = Reservoir.objects.values('month').distinct()
        return Response(months,status=200)
    except months.none:
        return Response({"error":"Not found"},status=400)

@api_view(['GET'])
def get_years(request):
    print("API ------")
    try:
        years = Reservoir.objects.values('year').distinct()
        return Response(years,status=200)
    except years.none:
        return Response({"error":"Not Available"},status=400)

@api_view(['GET'])
def get_basins(request):
    print("Api Called")
    try:
        basins = Reservoir.objects.values_list('basin', flat=True).distinct()
        basins_list = list(basins)
        if not basins_list:
            return Response({"error": "No basins found"}, status=404)
        return Response({'basins': basins_list}, status=200)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response({"error": "Error retrieving basins"}, status=500)


def import_csv_view(request):
    if request.method == 'POST':
        form = CsvImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            df = pd.read_csv(file)

            # Clean column names
            df.columns = df.columns.str.strip('_').str.strip()

            # Import data into the model
            for index, row in df.iterrows():
                month_value = int(row['month']) if pd.notnull(row['month']) else None
                year_value = int(row['year']) if pd.notnull(row['year']) else None

                Reservoir.objects.create(
                    reservoir_name=row['reservoir_name'],
                    basin=row['basin'],
                    year=year_value,
                    month=month_value,
                    full_reservoir_level=row['full_reservoir_level'] if pd.notnull(row['full_reservoir_level']) else None,
                    live_capacity_frl=row['live_capacity_frl'] if pd.notnull(row['live_capacity_frl']) else None,
                    storage=row['storage'] if pd.notnull(row['storage']) else None,
                    level=row['level'] if pd.notnull(row['level']) else None
                )
            messages.success(request, "Data imported successfully")
            return redirect('import_csv')
    else:
        form = CsvImportForm()

    return render(request, 'import_csv.html', {'form': form})
