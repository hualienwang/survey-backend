import requests
import uuid

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def test_survey_api():
    print("Testing Survey API...")
    
    # Create a survey
    survey_data = {
        "title": "Employee Satisfaction Survey",
        "description": "A survey to gauge employee satisfaction"
    }
    
    response = requests.post(f"{BASE_URL}/surveys/", json=survey_data)
    print(f"Create Survey - Status: {response.status_code}")
    if response.status_code == 200:
        survey = response.json()
        print(f"Created Survey: {survey}")
        survey_id = survey['id']
        
        # Get the survey
        response = requests.get(f"{BASE_URL}/surveys/{survey_id}")
        print(f"Get Survey - Status: {response.status_code}")
        print(f"Survey Details: {response.json()}")
        
        # List all surveys
        response = requests.get(f"{BASE_URL}/surveys/")
        print(f"List Surveys - Status: {response.status_code}")
        print(f"Surveys: {response.json()}")
        
        return survey_id
    else:
        print(f"Failed to create survey: {response.text}")
        return None

def test_response_api(survey_id):
    if not survey_id:
        print("No survey ID provided, skipping response tests")
        return
        
    print("\nTesting Response API...")
    
    # Create a response using form data with survey_id as part of URL
    response_data = {
        "employee_name": "John Doe",
        "text_response": "Great workplace!"
    }
    
    response = requests.post(f"{BASE_URL}/responses/?survey_id={survey_id}", data=response_data)
    print(f"Create Response - Status: {response.status_code}")
    if response.status_code == 200:
        response_data = response.json()
        print(f"Created Response: {response_data}")
        response_id = response_data['id']
        
        # Get the response
        response = requests.get(f"{BASE_URL}/responses/{response_id}")
        print(f"Get Response - Status: {response.status_code}")
        print(f"Response Details: {response.json()}")
        
        # Get responses for survey
        response = requests.get(f"{BASE_URL}/responses/survey/{survey_id}")
        print(f"Get Responses for Survey - Status: {response.status_code}")
        print(f"Responses for Survey: {response.json()}")
    else:
        print(f"Failed to create response: {response.text}")

if __name__ == "__main__":
    print("Starting API tests...")
    survey_id = test_survey_api()
    test_response_api(survey_id)
    print("API tests completed.")