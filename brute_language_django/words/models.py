from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Article(models.Model):

    # title
    word = models.TextField()

    # pageid
    wiki_id = models.IntegerField()

    # Not included : meta/import, meta/reference

    # meta/category
    categories = ArrayField(
        models.TextField(),
    )

    # meta/spellingVariation
    other_spellings = ArrayField(
        models.TextField(),
    )

    # text/pronunciations
    pronunciations = JSONField()

    # Not included : text.etymology


class Pos(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='poses')

    # pronunciations
    # pronunciations on pos don't have the 'area' tag, so just store it as a list
    pronunciations = ArrayField(
        models.TextField(),
    )
    # inflectionInfos
    inflections = JSONField()

    # paradigm
    paradigms = JSONField()

    # translations
    translations = JSONField()

    # subsections
    subsections = JSONField()

    # Attributes on the tag
    # pos[type]
    word_type = models.CharField(
        max_length=30,
    )

    # Not included : pos[homoNb]

    # pos[lemma]
    lemma = models.BooleanField()

    # pos[locution]
    locution = models.BooleanField()

    # pos[gender]
    MASCULIN = 'm'
    FEMENIN = 'f'
    EPICENE = 'e'
    INCONSISTENT = 'inconsistentGender'
    GENDER_CHOICES = (
        (MASCULIN, 'm'),
        (FEMENIN, 'f'),
        (EPICENE, 'e'),
        (INCONSISTENT, 'inconsistentGender')
    )
    gender = models.CharField(
        max_length=1,
        null=True,
        blank=False,
        choices=GENDER_CHOICES,
    )

    # pos[number]
    SINGULAR = 's'
    PLURAL = 'p'
    INVARIABLE = 'sp'
    SINGULAR_TANTUM = 'singulareTantum'
    PLURAL_TANTUM = 'pluraleTantum'
    INCONSISTENT = 'inconsistentNumber'
    NUMBER_CHOICES = (
        (SINGULAR, 'singular'),
        (PLURAL, 'plural'),
        (INVARIABLE, 'invariable'),
        (SINGULAR_TANTUM, 'singulareTantum'),
        (PLURAL_TANTUM, 'pluraleTantum'),
        (INCONSISTENT, 'inconsistentNumber')
    )
    number = models.CharField(
        max_length=15,
        null=True,
        blank=False,
        choices=NUMBER_CHOICES,
    )

    # pos[equivMasc]
    equivMasc = models.TextField(null=True)

    # pos[equivFem]
    equivFem = models.TextField(null=True)

    # pos[demonym]
    demonym = models.NullBooleanField(null=True)


class Definition(models.Model):
    word = models.ForeignKey(
        Pos, on_delete=models.CASCADE, related_name='definitions')

    # gloss/txt
    definition_txt = models.TextField(null=True, blank=False)
    # gloss/xml
    definition_xml = models.TextField(null=True, blank=False)
    # glos/parsed
    definition_CoNLL = models.TextField(null=True, blank=False)

    # gloss/label
    labels = JSONField(null=True)


class Example(models.Model):
    definition = models.ForeignKey(
        Definition, on_delete=models.CASCADE, related_name='examples')

    # txt
    example_txt = models.TextField(null=True, blank=False)
    # xml
    example_xml = models.TextField(null=True, blank=False)
    # parsed
    example_CoNLL = models.TextField(null=True, blank=False)

    # label
    # I'm not sure that this ever happens
    labels = JSONField(null=True)
