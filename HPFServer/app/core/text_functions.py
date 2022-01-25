import re
import html


def parse_text(text):
    tag_replace = {
        "[b]": "<b>", "[/b]": "</b>",
        "[i]": "<i>", "[/i]": "</i>",
        "[u]": "<u>", "[/u]": "</u>",
    }
    tag_pattern = r"\[/?\w\]"
    parsed_text = re.sub(tag_pattern, lambda match: tag_replace.get(match.group(0), ""), text)

    return parsed_text


def count_words(text):
    tag_pattern = re.compile(r"<[^>]*>")
    word_pattern = re.compile(r"([\w'’-]+)")  # qu'il c’est a-t-il = 1 mot chacun
    words = re.findall(word_pattern, re.sub(tag_pattern, "", html.unescape(text)))
    return len(words)
