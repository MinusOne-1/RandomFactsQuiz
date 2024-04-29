import requests


def get_random_questions(num_questions):
    url = "https://opentdb.com/api.php"
    params = {
        'amount': num_questions,
        'type': 'boolean'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data['results']  # Return the list of questions
    except requests.RequestException as e:
        print(f"Error requesting questions: {e}")
        return None
