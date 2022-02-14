import re
import html
from django.conf import settings
from docx2python import docx2python
from tempfile import NamedTemporaryFile
import logging


def extract_text_from_txt_file(file):
    return file.read().decode()


def extract_text_from_doc_file(file):
    pass
    '''
    Peut-être nécessaire de transformer doc en docx !
    '''


def extract_text_from_docx_file(file):
    # temp_file = NamedTemporaryFile(delete=False, dir=settings.FILE_UPLOAD_TEMP_DIR)
    # temp_file.write(file.read())
    # temp_file.close()
    # file.close()
    # return docx2python(temp_file.name, html=True, paragraph_styles=False).text
    return docx2python(file.temporary_file_path(), html=True, paragraph_styles=False).text


def extract_text_from_odt_file(file):
    pass
    '''
    Peut-être nécessaire de transformer odt (xml) en docx !
    '''


def read_text_file(file):
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
        raise IOError("Une erreur s'est produite lors du traitement du document.")
    else:
        raise TypeError(f"Ce type de fichier n'est pas pris en charge: {file.content_type}.")


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
