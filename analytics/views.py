import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.storage import default_storage
import os

# Global variable to store the uploaded dataset temporarily
dataset_store = {}


from django.shortcuts import render

def index(request):
    return render(request, "index.html")  # Ensure "index.html" exists in templates folder



@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_path = os.path.join("uploads", uploaded_file.name)

        # Save the file temporarily
        default_storage.save(file_path, uploaded_file)

        # Load the dataset into memory
        ext = uploaded_file.name.split('.')[-1]
        if ext == "csv":
            df = pd.read_csv(default_storage.open(file_path))
        elif ext in ["xls", "xlsx"]:
            df = pd.read_excel(default_storage.open(file_path))
        else:
            return JsonResponse({"error": "Unsupported file format"}, status=400)

        # Store dataset globally (temporary solution)
        dataset_store['df'] = df

        return JsonResponse({"message": "File uploaded successfully", "rows": len(df)})
    
    return JsonResponse({"error": "No file uploaded"}, status=400)


def get_dataset():
    """Helper function to retrieve the stored dataset."""
    if 'df' not in dataset_store:
        return None
    return dataset_store['df']


def dataset_overview(request):
    df = get_dataset()
    if df is None:
        return JsonResponse({"error": "No dataset uploaded."}, status=400)

    return JsonResponse({
        "head": df.head().to_dict(orient="records"),
        "columns": df.columns.tolist(),
        "shape": df.shape
    })


def basic_statistics(request):
    df = get_dataset()
    if df is None:
        return JsonResponse({"error": "No dataset uploaded."}, status=400)

    basic_stats = {
        "non_null_count": df.count().to_dict(),
        "unique_values": df.nunique().to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict()
    }

    return JsonResponse(basic_stats)


def numerical_analysis(request):
    df = get_dataset()
    if df is None:
        return JsonResponse({"error": "No dataset uploaded."}, status=400)

    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numerical_cols:
        return JsonResponse({"error": "No numerical columns found."}, status=400)

    stats = df[numerical_cols].describe().to_dict()
    stats["variance"] = df[numerical_cols].var().to_dict()

    return JsonResponse(stats)


def categorical_analysis(request):
    df = get_dataset()
    if df is None:
        return JsonResponse({"error": "No dataset uploaded."}, status=400)

    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    if not categorical_cols:
        return JsonResponse({"error": "No categorical columns found."}, status=400)

    cat_stats = {col: {
        "unique_values": df[col].nunique(),
        "most_frequent": df[col].mode().iloc[0] if not df[col].mode().empty else None
    } for col in categorical_cols}

    return JsonResponse(cat_stats)


def correlation_analysis(request):
    df = get_dataset()
    if df is None:
        return JsonResponse({"error": "No dataset uploaded."}, status=400)

    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numerical_cols) < 2:
        return JsonResponse({"error": "Not enough numerical columns for correlation analysis."}, status=400)

    correlations = df[numerical_cols].corr().to_dict()
    return JsonResponse({"correlation_matrix": correlations})


def data_integrity(request):
    df = get_dataset()
    if df is None:
        return JsonResponse({"error": "No dataset uploaded."}, status=400)

    integrity_stats = {
        "duplicate_rows": int(df.duplicated().sum()),
        "inconsistent_values": {col: df[col].apply(type).nunique() for col in df.columns}
    }

    return JsonResponse(integrity_stats)


def visualization(request):
    df = get_dataset()
    if df is None:
        return render(request, 'error.html', {"message": "No dataset uploaded."})

    return render(request, 'index.html', {"columns": df.columns.tolist()})

import pandas as pd
from django.http import JsonResponse

def compute_correlations():
    # Dummy data for testing (Replace this with your actual dataset)
    data = {
        "soil_moisture": [10, 20, 30, 40, 50],
        "N": [5, 15, 25, 35, 45],
        "P": [2, 12, 22, 32, 42],
        "K": [8, 18, 28, 38, 48],
        "soil_pH": [6.5, 7.0, 6.8, 7.2, 7.1]
    }

    df = pd.DataFrame(data)  # Convert to Pandas DataFrame

    correlation_matrix = df.corr()  # Compute correlation matrix
    return correlation_matrix

def correlation_analysis(request):
    try:
        correlation_matrix = compute_correlations()  # Now it's defined!
        return JsonResponse(correlation_matrix.to_dict(), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
