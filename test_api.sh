#!/bin/bash

BASE_URL="http://127.0.0.1:8000/api"

# Check if API is reachable
if ! curl -s "$BASE_URL" >/dev/null; then
    echo "Error: API server is not running or unreachable at $BASE_URL"
    exit 1
fi

echo "✅ Uploading file..."
curl -s -X POST "$BASE_URL/upload/" -F "file=@housing.csv" | jq .

echo -e "\n🔍 Dataset Overview:"
curl -s -X GET "$BASE_URL/overview/" | jq .

echo -e "\n📊 Basic Statistics:"
curl -s -X GET "$BASE_URL/basic-stats/" | jq .

echo -e "\n🔢 Numerical Analysis:"
curl -s -X GET "$BASE_URL/numerical-analysis/" | jq .

echo -e "\n🔠 Categorical Analysis:"
curl -s -X GET "$BASE_URL/categorical-analysis/" | jq .

echo -e "\n🔗 Correlation Analysis:"
curl -s -X GET "$BASE_URL/correlation-analysis/" | jq .

echo -e "\n✅ Data Integrity Checks:"
curl -s -X GET "$BASE_URL/data-integrity/" | jq .
