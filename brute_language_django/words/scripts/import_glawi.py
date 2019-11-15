from words.models import Article
# TODO auto download the glawi DB if it isnt there 

class ImportGLAWI():
    import xml.etree.ElementTree as ElementTree
    import xml.dom.minidom as minidom
    from django.db import models
    from words.models import Pos

    def parse_article(self, article_section):
        from words.models import Article
        word = article_section.find("title").text
        pageId = article_section.find("pageId").text
        print(word, pageId)
        categories = [category.text for category in article_section.find(
            "meta").findall("category")]

        other_spellings = [spell_var.attrib["norm"] for spell_var in article_section.find(
            "meta").findall("spellingVariation")]

        pronunciations = {}
        pronunciations_section = article_section.find(
            "text").find("pronunciations")
        if pronunciations_section is not None:
            for pron in pronunciations_section.findall("pron"):
                area = "default"
                if "area" in pron.attrib:
                    area = pron.attrib["area"]

                try:
                    pronunciations[area].append(pron.text)
                except:
                    pronunciations[area] = [pron.text]

        a = Article(word=word, wiki_id=pageId, categories=categories,
                    other_spellings=other_spellings, pronunciations=pronunciations)
        a.save()

        poses = article_section.find("text").findall("pos")
        for pos_section in poses:
            self.parse_pos(pos_section, a)

    def parse_pos(self, pos_section, parent_article_section):
        from words.models import Pos

        pronunciations = []
        pronunciations_section = pos_section.find("pronunciations")
        if pronunciations_section is not None:
            pronunciations = [
                pron.text for pron in pronunciations_section.findall("pron")]

        inflections = {}
        inflections_section = pos_section.find("inflectionInfos")
        if inflections_section is not None:
            for i in inflections_section.findall("inflectedForm"):
                # Have to handle this as a list since some have multiple values
                try:
                    inflections[i.attrib["gracePOS"]].append(
                        i.attrib["lemma"])
                except:
                    inflections[i.attrib["gracePOS"]] = [i.attrib["lemma"]]

        # TODO: skipped  equivMasc and equivFem
        paradigmInflections = {}
        paradigm_inflections_section = pos_section.find("paradigm")
        if paradigm_inflections_section is not None:
            for i in paradigm_inflections_section.findall("inflection"):
                # Have to handle this as a list since some have multiple values
                try:
                    paradigmInflections[i.attrib["gracePOS"]].append(
                        {"form": i.attrib["form"], "prons": i.attrib["prons"]})
                except:
                    paradigmInflections[i.attrib["gracePOS"]] = [
                        {"form": i.attrib["form"], "prons": i.attrib["prons"]}]

        translations = {}
        translations_section = pos_section.find("translations")
        if translations_section is not None:
            for trans in translations_section.findall("trans"):
                try:
                    translations[trans.attrib["lang"]].append(
                        trans.text)
                except:
                    translations[trans.attrib["lang"]] = [
                        trans.text]

        # subsection
        subsections = {}
        subsection_sections = pos_section.findall("subsection")
        for subsection_section in subsection_sections:
            subsection_type = subsection_section.attrib["type"]
            items = subsection_section.findall("item")

            subsection = {}
            for item in items:
                item_type = "default"
                if "type" in item.attrib:
                    item_type = item.attrib["type"]

                try:
                    subsection[item_type].append(item.text)
                except:
                    subsection[item_type] = [item.text]

            try:
                subsections[subsection_type].append(subsection)
            except:
                subsections[subsection_type] = [subsection]

        # Attributes

        word_type = None
        if "type" in pos_section.attrib:
            word_type = pos_section.attrib["type"]

        homoNb = None
        if "homoNb" in pos_section.attrib:
            homoNb = pos_section.attrib["homoNb"]

        lemma = None
        if "lemma" in pos_section.attrib:
            lemma = pos_section.attrib["lemma"]

        locution = None
        if "locution" in pos_section.attrib:
            locution = pos_section.attrib["locution"]

        gender = None
        if "gender" in pos_section.attrib:
            gender = pos_section.attrib["gender"]

        number = None
        if "number" in pos_section.attrib:
            number = pos_section.attrib["number"]

        equivMasc = None
        if "equivMasc" in pos_section.attrib:
            equivMasc = pos_section.attrib["equivMasc"]

        equivFem = None
        if "equivFem" in pos_section.attrib:
            equivFem = pos_section.attrib["equivFem"]

        demonym = None
        if "demonym" in pos_section.attrib:
            demonym = pos_section.attrib["demonym"]

        # TODO handle these
        if "inconsistentNumber" in pos_section.attrib:
            number = "inconsistentNumber"

        if "inconsistentGender" in pos_section.attrib:
            gender = "inconsistentGender"

        # genderFromRefLexicon = None
        # if "genderFromRefLexicon" in pos_section.attrib:
        #     genderFromRefLexicon = pos_section.attrib["genderFromRefLexicon"]

        # numberFromRefLexicon = None
        # if "numberFromRefLexicon" in pos_section.attrib:
        #     numberFromRefLexicon = pos_section.attrib["numberFromRefLexicon"]

        l = Pos(article=parent_article_section, pronunciations=pronunciations,
                inflections=inflections,
                paradigms=paradigmInflections,
                translations=translations,
                subsections=subsections,
                word_type=word_type,
                lemma=lemma,
                locution=locution,
                gender=gender,
                number=number,
                equivMasc=equivMasc,
                equivFem=equivFem,
                demonym=demonym,
                )
        l.save()

        definitions_section = pos_section.find("definitions")
        if definitions_section is not None:
            definitions_sections = definitions_section.findall(
                "definition")
            for definition_section in definitions_sections:
                self.parse_definition(definition_section, l)

    def parse_definition(self, definition_section, parent_pos_section):
        from words.models import Definition

        definition = None

        gloss_section = definition_section.find("gloss")

        definition_txt = None
        definition_xml = None
        definition_parsed = None
        labels = None

        if gloss_section is not None:

            txt_section = gloss_section.find("txt")
            if txt_section is not None:
                definition_txt = txt_section.text

            xml_section = gloss_section.find("xml")
            if xml_section is not None:
                definition_xml = self.prettify(xml_section)

            parsed_section = gloss_section.find("parsed")
            if parsed_section is not None:
                definition_parsed = parsed_section.text

            labels = {}
            labels_section = gloss_section.find("labels")

            if labels_section is not None:
                for label_section in labels_section.findall("label"):
                    label_type = label_section.attrib["type"]
                    try:
                        labels[label_type].append(
                            label_section.attrib["value"])
                    except:
                        labels[label_type] = [label_section.attrib["value"]]

        d = Definition(word=parent_pos_section, definition_txt=definition_txt,
                       definition_xml=definition_xml, definition_CoNLL=definition_parsed, labels=labels)
        d.save()

        example_sections = definition_section.findall(
            "example")
        for example_section in example_sections:
            self.parse_example(example_section, d)

    def parse_example(self, example_section, parent_definition_section):
        from words.models import Example

        txt_section = example_section.find("txt")
        if txt_section is not None:
            example_txt = txt_section.text

        xml_section = example_section.find("xml")
        if xml_section is not None:
            example_xml = self.prettify(xml_section)

        parsed_section = example_section.find("parsed")
        if parsed_section is not None:
            example_parsed = parsed_section.text

        labels = {}
        labels_section = example_section.find("labels")

        if labels_section is not None:
            for label_section in labels_section.findall("label"):
                label_type = label_section.attrib["type"]
                try:
                    labels[label_type].append(
                        label_section.attrib["value"])
                except:
                    labels[label_type] = [label_section.attrib["value"]]

        e = Example(definition=parent_definition_section, example_txt=example_txt,
                    example_xml=example_xml, example_CoNLL=example_parsed, labels=labels)
        e.save()

    def prettify(self, elem):
        import xml.dom.minidom as minidom
        import xml.etree.ElementTree as ElementTree
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def run(self):
        import lxml.etree as etree
        for event, elem in etree.iterparse("words/scripts/data/GLAWI_FR_workParsed_D2015-12-26_R2016-05-18.xml", events=['start', 'end']):
            # if elem.tag != "glawi":
            # try:
            #     print("---")
            #     print(elem)
            #     print(prettify(elem))
            # except:
            #     pass
            if event == "end" and elem.tag == "article" and len(elem.getchildren()) > 0:
                article_section = elem
                self.parse_article(article_section)
                elem.clear()


print("Destroy old")
Article.objects.all().delete()
print("Import new")
ig = ImportGLAWI()
ig.run()
