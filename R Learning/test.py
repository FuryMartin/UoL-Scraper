import emoji
import re

test_str = """服务周到，性价比高，量还多，强烈推荐😍😍😍"""
result = emoji.replace_emoji(test_str, replace='')
print(result)
print(emoji.emojize(result))
