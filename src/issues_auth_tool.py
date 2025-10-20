import shlex
from typing import Iterator

from github import Auth, Github
from openai import OpenAI

from settings import config

g = Github(auth=Auth.Token(config['secret']['GITHUB_TOKEN']))
repo = g.get_repo(f'{config["secret"]["OWNER"]}/{config["secret"]["REPO_NAME"]}')
print(config['secret'])
client = OpenAI(
    api_key=config['secret']['llm']['key'],
    base_url=config['secret']['llm']['server'],
)
setting = config['settings']



def fetch_issues_and_discussions() -> Iterator[dict]:
    # issues
    if 'issues' in setting['type']:
        for issue in repo.get_issues(state='open'):
            # 过滤 PR（在 PyGithub 中 pull_request 属性可能存在）
            if getattr(issue, 'pull_request', None):
                continue
            yield {'title': issue.title, 'num': issue.number, 'text': issue.body or ''}

    # discussions
    if 'discussions' in setting['type']:
        for disc in repo.get_discussions( discussion_graphql_schema="id number title body", answered=False):
            yield {'title': disc.title, 'num': disc.number, 'text': disc.body or ''}

def get_llm_response(instructions: str, input: str) -> str:
    return client.responses.create(
        model=config['secret']['llm']['model'],
        instructions=instructions,
        input=input,
    ).output_text


def handle_instruction(instructions: list[str]) -> str:
    for instr in instructions:
        instr = shlex.split(instr)
        match instr[0]:
            case 'google':
                pass
            case 'view':
                pass

cache = {}
def run():
    for post in fetch_issues_and_discussions():
        print(post)
        if config['cache']:
            ...


if __name__ == '__main__':
    run()
