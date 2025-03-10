#!/bin/bash

BASE_URL="http://127.0.0.1:8000/api"

echo "Uploading file..."
curl -X POST "$BASE_URL/upload/" -F "file=@housing.csv"

echo -e "\nDataset Overview:"
curl -X GET "$BASE_URL/overview/"

echo -e "\nBasic Statistics:"
curl -X GET "$BASE_URL/basic-stats/"

echo -e "\nNumerical Analysis:"
curl -X GET "$BASE_URL/numerical-analysis/"

echo -e "\nCategorical Analysis:"
curl -X GET "$BASE_URL/categorical-analysis/"

echo -e "\nCorrelation Analysis:"
curl -X GET "$BASE_URL/correlation-analysis/"

echo -e "\nData Integrity Checks:"
curl -X GET "$BASE_URL/data-integrity/"
