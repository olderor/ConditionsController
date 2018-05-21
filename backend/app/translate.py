import json
import os
from googletrans import Translator as GTranslator


class Translator:
    __translations_folder_path = "translations/"
    __translations = dict()
    __translator = GTranslator()

    @staticmethod
    def init():
        if not os.path.exists(Translator.__translations_folder_path):
            return
        for filename in os.listdir(Translator.__translations_folder_path):
            if '.' not in filename:
                continue
            langs, extension = filename.split('.')
            if extension != 't':
                continue
            source_language, dest_language = langs.split('-')
            Translator.__translations.setdefault(source_language, dict())
            Translator.__translations[source_language].setdefault(dest_language, dict())
            with open(Translator.__translations_folder_path + filename, 'r') as file:
                lines = file.readlines()
                for i in range(0, len(lines) - 1, 2):
                    Translator.__translations[source_language][dest_language].setdefault(lines[i][:-1], lines[i + 1][:-1])

    @staticmethod
    def get_locale():
        return 'en'

    @staticmethod
    def __save_translation(text, translation, source_language, dest_language):
        Translator.__translations.setdefault(source_language, dict())
        Translator.__translations[source_language].setdefault(dest_language, dict())
        Translator.__translations[source_language][dest_language].setdefault(text, translation)
        if not os.path.exists(Translator.__translations_folder_path):
            os.makedirs(Translator.__translations_folder_path)
        translation_file = '{}-{}.t'.format(source_language, dest_language)
        with open(Translator.__translations_folder_path + translation_file, 'a') as file:
            file.write('{}\n{}\n'.format(text, translation))

    @staticmethod
    def translate(text, source_language, dest_language):
        if dest_language == source_language:
            return text

        translation = text

        if source_language in Translator.__translations and \
                dest_language in Translator.__translations[source_language] and \
                text in Translator.__translations[source_language][dest_language]:
            return Translator.__translations[source_language][dest_language][text]

        res = Translator.__translator.translate(text, src=source_language, dest=dest_language)
        if res.text:
            translation = res.text
        Translator.__save_translation(text, translation, source_language, dest_language)

        return translation

    @staticmethod
    def localeselector(f):
        Translator.get_locale = f


def translate(text):
    return Translator.translate(text, 'en', Translator.get_locale())
