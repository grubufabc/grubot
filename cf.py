import requests
import json

def user_submissions(handle):
    response = requests.get("https://codeforces.com/api/user.status?handle=" + handle + "&from=1&count=3")
    return json.loads(response.text)

def get_problem(submission):
    return submission["problem"]

def get_veredict(submission):  
    return submission["verdict"]

def get_creation_time(submission):
    return submission["creationTimeSeconds"]

def main():
    user = "pedrotunin"
    submissions = user_submissions(user)

    for submission in submissions["result"]:
        problem = get_problem(submission)
        verdict = get_veredict(submission)
        creation_time = get_creation_time(submission)
        print("Titulo problema: " + problem["name"])
        print("Veredito: " + verdict)
        print("Criado em: " + str(creation_time) + "\n")

if __name__ == "__main__":
    main()