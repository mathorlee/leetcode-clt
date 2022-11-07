import argparse
import json
import os
import re
import time
import warnings

from bs4 import BeautifulSoup

import common

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
COOKIE = os.environ.get("LC_COOKIE", "")
assert COOKIE, "please set env LC_COOKIE, you can get it from browser by capturing http graphql header"
csrftoken = re.search(r"csrftoken=(?P<result>\w+);", COOKIE).group("result")
assert csrftoken, "failed to fetch csrftoken from LC_COOKIE"
language = os.environ.get("language", "python3")
print(f"language: {language}")


def _pp(s: str):
    """pretty print"""
    print("=" * 50 + s + "=" * 50)


def get_problem_list(status: str):
    if status == "todo":
        status = "NOT_STARTED"
    elif status == "attempted":
        status = "TRIED"
    elif status == "solved":
        status = "AC"
    else:
        raise Exception("unsupported status")
    input = {
        "query": "query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n    }\n  }\n}",
        "variables": {
            "categorySlug": "algorithms",
            "skip": 0,
            "limit": 1000,
            "filters": {
                "difficulty": "HARD",
                "status": status,
            }
        }
    }
    _, output = common.request_post("https://leetcode.com/graphql", headers={"cookie": COOKIE}, payload=input)
    assert _ == 200, f"problemsetQuestionList失败 {_} {output}"
    total = output["data"]["problemsetQuestionList"]["total"]
    print(f"一共{total}个problem")
    i = 0
    for _ in output["data"]["problemsetQuestionList"]["questions"]:
        if _["paidOnly"] is False:
            print("%3d" % i, _["status"], _["difficulty"], _["titleSlug"])
            i += 1


def questionData(title: str) -> tuple[str, str, str]:
    input = {
        "operationName": "questionData",
        "variables": {
            "titleSlug": title,
        },
        "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    canSeeQuestion\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    exampleTestcases\n    categoryTitle\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      hasVideoSolution\n      paidOnlyVideo\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    challengeQuestion {\n      id\n      date\n      incompleteChallengeCount\n      streakCount\n      type\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    _, output = common.request_post("https://leetcode.com/graphql", headers={"cookie": COOKIE}, payload=input)
    assert _ == 200, f"problemsetQuestionList失败 {_} {output}"
    _ = output["data"]["question"]
    question_id = _["questionId"]
    content = _["content"]
    content = BeautifulSoup(content, "html.parser").get_text()
    code = list(filter(lambda _: _["langSlug"] == language, _["codeSnippets"]))[0]["code"]
    return question_id, code, content


def do_submit(title: str):
    """submit result by title. code is read from 11.py in work dir"""
    _pp(title)

    question_id, code, _ = questionData(title)
    with open("func.py", mode="r") as f:
        s = f.read()
        s1 = re.search(r"# begin(?P<result>[\s\S]*)# end", s, flags=re.MULTILINE).group("result")

    # WARNING: code generate only suited for python3!!!
    code = f"{code}\n{s1}"
    _pp(f"code")
    print(code)

    input = {
        "question_id": question_id,
        "lang": language,
        "typed_code": code,
    }
    headers={"cookie": COOKIE, "referer": f"https://leetcode.com/problems/{title}/submissions/", "x-csrftoken": csrftoken}
    _, output = common.request_post(f"https://leetcode.com/problems/{title}/submit/", headers=headers, payload=input)
    assert _ == 200, f"submit失败 {_} {output}"
    _pp(f"submit")
    print(output)
    submission_id = output["submission_id"]

    for i in range(10):
        _, output = common.request_get(f"https://leetcode.com/submissions/detail/{submission_id}/check/", headers={"cookie": COOKIE})
        assert _ == 200, f"check失败 {_} {output}"
        if output["state"] in ("PENDING", "STARTED"):
            print(output, "sleep 5 seconds")
            time.sleep(5)
        else:
            _pp(f"{submission_id} result")
            print(json.dumps(output, sort_keys=True, indent=4))
            print(output["state"], output["status_code"], output["status_msg"])
            if output["status_msg"] == "Accepted":
                _pp("add file")
                print(f"cp func.py acs/{title}.py")
                _pp("commit message")
                print(f"{title} ac, runtime_percentile: {output['runtime_percentile']}, memory_percentile: {output['memory_percentile']}")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser("l clt")
    parser.add_argument("-l", "--list-problems", action="store_true", help="list problems")
    parser.add_argument("--status", type=str, required=False, help='problem status, todo|attempted|solved', default="todo")

    parser.add_argument("-t", "--title", type=str, required=False, help='title of problem')
    parser.add_argument("-s", "--submit", action="store_true", help="submit problems")

    args = parser.parse_args()
    list_problems = args.list_problems
    status = args.status
    title = args.title
    submit = args.submit

    if list_problems:
        get_problem_list(status)
    elif title:
        if submit:
            do_submit(title)
        else:
            question_id, code, content = questionData(title)
            _pp("question_id")
            print(question_id)
            _pp("code")
            print(code)
            _pp("content")
            print(content)
