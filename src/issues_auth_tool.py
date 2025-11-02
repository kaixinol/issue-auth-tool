import re
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

def strip_markdown(md: str) -> str:
    text = md
    # 删除代码块 ```...``` 和 ~~~...~~~
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'~~~[\s\S]*?~~~', '', text)
    # 删除行内代码 `...`
    text = re.sub(r'`[^`]*`', '', text)
    # 删除图片 ![alt](url)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 删除链接 [text](url) -> 保留 text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 删除加粗/斜体 **text**, __text__, *text*, _text_
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
    # 删除标题 #
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # 删除引用 >
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)
    # 删除水平线 ---
    text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
    # 删除多余的空白行
    text = re.sub(r'\n\s*\n', '\n', text)
    # 去除首尾空白
    return text.strip()


def fetch_issues_and_discussions() -> Iterator[dict]:
    # issues
    if 'issues' in setting['type']:
        for issue in repo.get_issues(state='open'):
            # 过滤 PR（在 PyGithub 中 pull_request 属性可能存在）
            if getattr(issue, 'pull_request', None):
                continue
            yield {
                'title': issue.title,
                'num': issue.number,
                'text': strip_markdown(issue.body or '(无内容)'),
            }

    # discussions
    if 'discussions' in setting['type']:
        for disc in repo.get_discussions(
            discussion_graphql_schema='id number title body', answered=False
        ):
            yield {
                'title': disc.title,
                'num': disc.number,
                'text': strip_markdown(disc.body or '(无内容)'),
            }


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

CONTENT = """
标题：{title}
编号：{num}
内容：{text}
"""

def run():
    for post in fetch_issues_and_discussions():
        print(CONTENT.format(**post))


if __name__ == '__main__':
    run()
