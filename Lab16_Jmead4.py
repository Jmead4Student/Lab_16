"""
Code Refactoring
John Mead
Fetches the top articles from the Hacker News API and refactors them to handle KeyErrors.
8/9/25
"""

from operator import itemgetter
import requests

url = "https://hacker-news.firebaseio.com/v0/topstories.json"
request = requests.get(url)
print(f"Status code: {request.status_code}")

submission_ids = request.json()
submission_dicts = []

for submission_id in submission_ids[:30]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    request = requests.get(url)
    response_dict = request.json()

    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict.get('descendants', 0),
        }
        submission_dicts.append(submission_dict)
    except KeyError:
        print(f"Skipping item {submission_id} due to missing 'title'.")


submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")