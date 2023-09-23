import requests
import zipfile

# Step 1: Retrieve the list of selections  2.1
selections_url = "https://old.stat.gov.kz/api/rcut/ru"
selections_response = requests.get(selections_url)

# Check if the response contains valid JSON data
if selections_response.status_code == 200:
    try:
        selections_data = selections_response.json()
    except ValueError as e:
        print("Error parsing JSON response:", e)
        selections_data = []
else:
    print(f"Failed to retrieve selections. Status code: {selections_response.status_code}")
    selections_data = []

# Step 2: Choose the desired selection (modify this based on your requirement)
if selections_data:
    selected_selection = selections_data[0]

    # Step 3: Send a sample request and obtain an application number
    sample_request_data = {
        "conditions": [
            {
                "classVersionId": 2153,  # Modify based on your conditions
                "itemIds": [742679]  # Modify based on your conditions
            }
        ],
        "cutId": selected_selection["id"]
    }
    # 2.2
    request_url = "https://old.stat.gov.kz/api/sbr/request/?api"
    request_response = requests.post(request_url, json=sample_request_data)

    # Check if the response contains valid JSON data
    if request_response.status_code == 200:
        try:
            request_data = request_response.json()
            if "obj" in request_data and isinstance(request_data["obj"], str):
                # Extract the NUMBER from the "obj" field
                NUMBER = request_data["obj"]
                # NUMBER = '94ac5c52-02e0-40aa-a9ee-b0f04c35a7b9'
                print(f"NUMBER received: {NUMBER}")


                if "obj" in request_data and isinstance(request_data["obj"], str):
                # Step 4: Check the status of the application (wait until "Processed")
                    status_url = f"https://stat.gov.kz/api/sbr/requestResult/{NUMBER}/ru"
                    while True:
                        status_response = requests.get(status_url)
                        try:
                            status_data = status_response.json()
                            if "description" in status_data and (status_data["description"] == "Processed" or status_data["description"] == "Обработан" or status_data["description"] == "Өңделді" ):
                                if "obj" in status_data and "fileGuid" in status_data["obj"]:
                                    # Extract the file GUID
                                    file_guid = status_data["obj"]["fileGuid"]
                                    print(f"File GUID received: {file_guid}")
                                    download_url = f"https://stat.gov.kz/api/sbr/download?bucket=SBR_UREQUEST&guid={file_guid}"


                                    # excel_file_path = "selection_data.zip"
                                    excel_response = requests.get(download_url)

                                    if excel_response.status_code == 200:
                                        # Save the zip file 
                                        with open("selection_data.zip", "wb") as excel_file:
                                            excel_file.write(excel_response.content)
                                        print("Excel file downloaded successfully.")

                                    else:
                                        print(f"Failed to download the Excel file. Status code: {excel_response.status_code}")
                                else:
                                    print("No valid 'fileGuid' found in the status data.")
                                break
                        except ValueError as e:
                            print("Error parsing JSON response:", e)
                            status_data = {}

                 
                else:
                    print("No valid 'obj' found in the request data.")


            else:
                print("No valid 'obj' found in the request data.")
        except ValueError as e:
            print("Error parsing JSON response:", e)
    else:
        print(f"Failed to send the request. Status code: {request_response.status_code}")

   
else:
    print("No selections data received.")


