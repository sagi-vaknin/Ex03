import requests

file_path = "query.txt"
base_url = "http://127.0.0.1:8000"  # Replace with your API base URL

# Open the file
with open(file_path, "r") as file:
    with open("response.txt", "w") as response_file:
        # Read and process each line
        for line in file:
            url = f"{base_url}/dishes"
            dish_name = line.strip()  

        #POST request
            payload = {"name": dish_name}
            response1 = requests.post(url, json=payload)

            if response1.status_code == 200:
                #GET request
                dish_id = response1.json()
                response2 = requests.get(f"{base_url}/dishes/{dish_id}")
                response2_data = response2.json()
                response_file.write( \
                    f"{dish_name} contains {response2_data['cal']} calories, \
                        {response2_data['sodium']} mgs of sodium, \
                            and {response2_data['sugar']} grams of sugar\n")
    response_file.close()
file.close()