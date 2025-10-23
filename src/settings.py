from tomllib import load

with open('config.toml', 'rb') as f:
    config = load(f)
setting = config['settings']

REGEX_CMD = r'(del|outdate)(\s+\d+)+'
REGEX_AKA = r'alias(\s+[\u4e00-\u9fff]+){2}(\s+\d+)*'
REGEX_MCP = {'view': r'view(\s+\d+)+', 'google': r'google(\s+[\u4e00-\u9fff]+){2}'}
