import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pprint
from google.cloud import translate

'''
def detect_language(text):
	"""Detects the text's language."""
	translate_client = translate.Client()

	# Text can also be a sequence of strings, in which case this method
	# will return a sequence of results for each text.
	result = translate_client.detect_language(text)

	print('Text: {}'.format(text))
	print('Confidence: {}'.format(result['confidence']))
	print('Language: {}'.format(result['language']))

	return result['language']
'''


def get_worksheet_client():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), scope)
    client = gspread.authorize(creds)
    return client


def get_col_data(sheet, index):
    col = sheet.col_values(index)
    return col


'''
def get_col_data(client):
	sheet = client.open('multi-trans').sheet1
	#sh1_records = sheet.get_all_records()

	result = sheet.col_values(1)
	print(result)

	pp = pprint.PrettyPrinter()
	pp.pprint(result)

	#print(sh1_records)
	return result
'''


def get_sheet(client):
    sheet = client.open('multi-trans').sheet1
    return sheet


'''
def write_detected_lang(sheet):
	language_test = sheet.cell(10,1).value
	d_lang = detect_language(language_test)
	print(d_lang)
	#sheet.update_cell(1,1, d_lang)
	return d_lang
'''


def insert_lang_code(sheet):
    def make_row_languages():
        """Lists all available languages."""
        translate_client = translate.Client()
        results = translate_client.get_languages()
        # print(results)
        row_langs = [result['language'] for result in results]
        return row_langs

    lang_code_row = make_row_languages()
    row = ['en'] + lang_code_row
    # print(row)
    sheet.insert_row(row, 1)


def insert_lang_name(sheet):
    def make_row_lang_names():
        """Lists all available languages."""
        translate_client = translate.Client()

        results = translate_client.get_languages()
        # print(results)

        row_lang_names = [result['name'] for result in results]
        return row_lang_names

    lang_name_row = make_row_lang_names()
    row = ['english'] + lang_name_row

    # print(row)
    sheet.insert_row(row, 2)


def trans_sentences(tr_client, sentences, target_lang, format, src_lang):
    translations = tr_client.translate(sentences, target_lang, format, src_lang)
    print(translations)
    result_sentences = [translation['translatedText'] for translation in translations]
    return result_sentences


def trans_col(tr_client, sentences, sheet, index):
    print(index)
    target_col = get_col_data(sheet, index)
    target_lang = target_col[0]
    if target_lang is '':
        return
    print(target_lang)
    outformat = 'text'
    source_lang = 'en'
    translatedTexts = trans_sentences(tr_client, sentences, target_lang, outformat, source_lang)
    # print(translatedTexts)

    sentences_size = len(sentences)
    # print(sentences_size)
    cells = sheet.range(3, index, sentences_size - 1, index)

    for idx, cell in enumerate(cells):
        if cell.value is '':
            cell.value = translatedTexts[idx]

    sheet.update_cells(cells)


if __name__ == "__main__":
    ws_client = get_worksheet_client()
    sheet = get_sheet(ws_client)
    # write_detected_lang(sheet)
    # cell = sheet.cell(5,1).value
    # print("cell(1,5) = " + cell)

    check_cell = sheet.cell(1, 1).value
    if check_cell == '':
        insert_lang_code(sheet)
        insert_lang_name(sheet)

    src_sentences = get_col_data(sheet, 1)

    # print(src_sentences)
    sentences = src_sentences[2:]
    # print(sentences)

    translate_client = translate.Client()
    lang_size = len(sheet.row_values(1))
    for idx in range(2, lang_size + 1):
        trans_col(translate_client, sentences, sheet, idx)

    print('end~')
