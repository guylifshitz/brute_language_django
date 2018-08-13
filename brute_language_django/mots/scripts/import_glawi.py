import xml.etree.ElementTree as ElementTree
import lxml.etree as etree
import xml.dom.minidom as minidom
from django.db import models
from mots.models import Article
from mots.models import Lemme
from mots.models import Definition


print("Load...")
# e = ElementTree.parse('mots/scripts/data/GLAWI_FR_workParsed_D2015-12-26_R2016-05-18.xml').getroot()
e = ElementTree.parse('mots/scripts/data/GLAWI_FR_workParsed_D2015-12-26_R2016-05-18-small.xml').getroot()
wiki_articles = e.findall("article")

Article.objects.all().delete()

for article_section in wiki_articles:
    article = article_section.find("title").text
    pageId = article_section.find("pageId").text

    print(article)

    a = Article(word=article, wiki_id=pageId)
    a.save()
    poses = article_section.find("text").findall("pos")
    
    for pos_section in poses:

        if "gender" in pos_section.attrib:
            word_gender = pos_section.attrib["gender"]
    
        if "type" in pos_section.attrib:
            word_type = pos_section.attrib["type"]
    
        if "number" in pos_section.attrib:
            word_number = pos_section.attrib["number"]
        
        if "lemma" in pos_section.attrib:
            word_lemma = pos_section.attrib["lemma"]
            word_lemma = (word_lemma == "1")
        
        pronunciation_section = pos_section.find("pronunciations")
        if pronunciation_section:
            pronunciations = [pron.text for pron in pronunciation_section.findall("pron")]


        translations_section = pos_section.find("translations")
        if translations_section:
            translations = [{trans.attrib["lang"]: trans.text} for trans in translations_section.findall("trans")]

        # TODO: handle the list types correctly (pronunciation, labels, translation)
        l = Lemme(article=a, word=article, word_type=word_type, lemma=word_lemma, gender=word_gender, number=word_number, pronunciation = ", ".join(pronunciations))
        print((a, article, word_lemma, word_gender, word_number, ", ".join(pronunciations)))
        l.save()

        definitions_sections = pos_section.find("definitions")
        for definition_section in definitions_sections:

            definition = definition_section.find("gloss").find("txt").text

            labels_section = definition_section.find("gloss").find("labels")
            if labels_section:
                labels = [l.attrib for l in labels_section.findall("labels")]
            d = Definition(word=l, definition=definition)
            d.save()
    