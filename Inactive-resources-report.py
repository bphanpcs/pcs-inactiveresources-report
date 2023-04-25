import requests
import json
from tabulate import tabulate
from fpdf import FPDF

# Set Prisma Cloud login details
username = 'YOUR_ACCESS_KEY'
password = 'YOUR_SECRET_KEY'
login_url = 'https://api.prismacloud.io/login'

# Authenticate and generate bearer authorization token
auth_payload = {
    'username': username,
    'password': password
}
auth_response = requests.post(login_url, json=auth_payload)
auth_data = json.loads(auth_response.content)
bearer_token = auth_data['token']

# Set headers with bearer authorization token
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + bearer_token
}

# Set payload
payload = {
    "filters": [
        {
            "name": "state",
            "operator": "eq",
            "value": "inactive"
        }
    ]
}

# Set API endpoint
endpoint = "/cloud/{}".format("assets/search")

# Make API request to Prisma Cloud
response = requests.post(api_base_url + endpoint, headers=headers, data=json.dumps(payload))

# Parse response JSON data
response_data = json.loads(response.content)

# Extract data for each inactive resource and add to list
inactive_resources = []
for resource in response_data["data"]:
    inactive_resource = {}
    inactive_resource["Account Name"] = resource["cloud"]["account"]["name"]
    inactive_resource["Account ID"] = resource["cloud"]["account"]["id"]
    inactive_resource["Cloud Provider"] = resource["cloud"]["type"]
    inactive_resource["Region"] = resource["cloud"]["region"]
    inactive_resource["Resource Name"] = resource["data"]["details"]["displayName"]
    inactive_resource["Resource ID"] = resource["data"]["details"]["resourceId"]
    inactive_resource["Resource Type"] = resource["data"]["details"]["resourceType"]
    inactive_resource["Last Seen"] = resource["data"]["details"]["lastSeen"]
    inactive_resource["State"] = resource["data"]["details"]["state"]
    if "tags" in resource["data"]["details"]:
        if "owner" in resource["data"]["details"]["tags"]:
            inactive_resource["Owner"] = resource["data"]["details"]["tags"]["owner"]
    inactive_resources.append(inactive_resource)

# Create PDF document and add page
pdf = FPDF()
pdf.add_page()

# Set title and subtitle for PDF report
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Inactive Cloud Resources Report", 0, 1, "C")
pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, "This report shows a list of inactive resources across all supported cloud providers.", 0, 1, "C")
pdf.cell(0, 10, "", 0, 1)

# Create table for inactive resources and add to PDF
pdf.set_font("Arial", "B", 12)
pdf.cell(30, 10, "Account Name", 1)
pdf.cell(30, 10, "Account ID", 1)
pdf.cell(30, 10, "Cloud Provider", 1)
pdf.cell(30, 10, "Region", 1)
pdf.cell(50, 10, "Resource Name", 1)
pdf.cell(30, 10, "Resource ID", 1)
pdf.cell(30, 10, "Resource Type", 1)
pdf.cell(30, 10, "Last Seen", 1)
pdf.cell(30, 10, "State", 1)
pdf.cell(30, 10, "Owner", 1)
pdf.cell(0, 10, "", 0, 1)

pdf.set_font("Arial", "", 12)
for inactive_resource in inactive_resources
