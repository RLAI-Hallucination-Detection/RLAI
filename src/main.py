import subprocess
import re

lambda_1 = 0.20  #Weight for FEVER
lambda_2 = 0.55  #Weight for TruthfulQA
lambda_3 = 0.25  #Weight for Google Fact Checker

def get_score_from_script(script_name):
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        
        output = result.stdout.strip()
        
        match = re.search(r'Score:\s*([0-9.]+)', output)
        
        if match:
            score = float(match.group(1))
            return score
        else:
            print(f"Error: No score found in the output of {script_name}.")
            return None
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return None

fever_score = get_score_from_script('src/test_fever.py')
google_score = get_score_from_script('src/test_google_api.py')
truthfulqa_score = get_score_from_script('src/test_truthfulqa.py')

if None in [fever_score, google_score, truthfulqa_score]:
    print("Error: One or more scores could not be obtained.")
else:
    F_score = lambda_1 * fever_score + lambda_2 * truthfulqa_score + lambda_3 * google_score

    if F_score > 0.8:
        response = "Accept Response"
    elif 0.5 <= F_score <= 0.8:
        response = "Needs Review"
    else:
        response = "Regenerate Response"

    print(f"Fever Score: {fever_score}")
    print(f"Google Score: {google_score}")
    print(f"TruthfulQA Score: {truthfulqa_score}")
    print(f"F_score: {F_score}")
    print(f"Decision: {response}")
