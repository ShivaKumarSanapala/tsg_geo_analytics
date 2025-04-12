#!/bin/bash

# Function to fetch data from a given URL and convert to CSV format
fetch_data() {
    local url=$1
    local rename_csv=$2

    response=$(curl -s "$url")

    if [ $? -eq 0 ]; then
        if echo "$response" | jq empty >/dev/null 2>&1; then
            convert_to_csv "$response" "$rename_csv"
        else
            echo "Error: Invalid JSON received."
        fi
    else
        echo "Error fetching data!"
    fi
}

# Function to convert JSON to CSV and apply header renaming
convert_to_csv() {
    local response=$1
    local rename_csv=$2

    # Turn rename string into original/replacement pairs
    IFS=',' read -ra pairs <<< "$rename_csv"

    # Extract headers
    headers=($(echo "$response" | jq -r '.[0][]'))

    # Replace headers using rename pairs
    for i in "${!headers[@]}"; do
        for pair in "${pairs[@]}"; do
            key="${pair%%=*}"
            val="${pair#*=}"
            if [ "${headers[$i]}" == "$key" ]; then
                headers[$i]="$val"
                break
            fi
        done
    done

    # Print headers
    (IFS=','; echo "${headers[*]}")

    # Print data rows with correct handling of commas within fields
    echo "$response" | jq -r '.[1:][] | @csv'
}

# Construct the full URL
construct_url() {
    echo "$1?$2"
}

# Argument validation
if [ $# -ne 3 ]; then
    echo "Usage: $0 <base_url> <url_params> <rename_csv>"
    echo "Example:"
    echo "$0 https://api.census.gov/data/2022/acs/acs1 \"get=NAME,B01001_003E&for=state:06\" \"B01001_003E=under_5,B01001_004E=male_under_5\""
    exit 1
fi

# Parse args
base_url=$1
url_params=$2
rename_csv=$3

# Construct URL and fetch
final_url=$(construct_url "$base_url" "$url_params")
fetch_data "$final_url" "$rename_csv"
