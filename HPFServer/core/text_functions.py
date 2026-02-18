import re
import html
from docx2python import docx2python
from django.core.files import File

import logging


def extract_text_from_txt_file(file: File) -> str:
    return file.read().decode()


def extract_text_from_doc_file(file: File) -> str:
    pass
    '''
    Peut-être nécessaire de transformer doc en docx !
    '''


def extract_text_from_docx_file(file: File) -> str:
    # temp_file = NamedTemporaryFile(delete=False, dir=settings.FILE_UPLOAD_TEMP_DIR)
    # temp_file.write(file.read())
    # temp_file.close()
    # file.close()
    # return docx2python(temp_file.name, html=True, paragraph_styles=False).text
    return docx2python(file.temporary_file_path(), html=True, paragraph_styles=False).text


def extract_text_from_odt_file(file: File) -> str:
    pass
    '''
    Peut-être nécessaire de transformer odt (xml) en docx !
    '''


def read_text_file(file: File) -> str:
    try:
        if file.content_type == "text/plain":
            return extract_text_from_txt_file(file)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx_file(file)
        # elif file.content_type == "application/msword":
        #     return extract_text_from_doc_file()
    #     elif file.content_type == "application/vnd.oasis.opendocument.text":
    #         return extract_text_from_odt_file(file)
    except Exception as e:
        logging.error(e)
        msg = "Une erreur s'est produite lors du traitement du document."
        raise IOError(msg)
    else:
        msg = f"Ce type de fichier n'est pas pris en charge: {file.content_type}."
        raise TypeError(msg)


def parse_text(text: str) -> str:
    tag_replace = {
        "[b]": "<b>", "[/b]": "</b>",
        "[i]": "<i>", "[/i]": "</i>",
        "[u]": "<u>", "[/u]": "</u>",
    }
    tag_pattern = r"\[/?\w\]"
    parsed_text = re.sub(tag_pattern, lambda match: tag_replace.get(match.group(0), ""), text)

    return parsed_text


def count_words(text: str) -> int:
    tag_pattern = re.compile(r"<[^>]*>")
    word_pattern = re.compile(r"([\w'’-]+)")  # qu'il c’est a-t-il = 1 mot chacun
    words = re.findall(word_pattern, re.sub(tag_pattern, "", html.unescape(text)))
    return len(words)
