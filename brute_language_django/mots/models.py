from django.db import models

class Article(models.Model):
    word = models.CharField(max_length=100)
    wiki_id = models.IntegerField()

class Lemme(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=100)

    word_type = models.CharField(
        max_length=10,
    )


    # MASCULIN = 'm'
    # FEMENIN = 'f'
    # EPICENE = 'e'
    # GENDER_CHOICES = (
    #     (MASCULIN, 'm'),
    #     (FEMENIN, 'f'),
    #     (EPICENE, 'e'),
    # )
    gender = models.CharField(
        max_length=1,
        # choices=GENDER_CHOICES,
    )

    # SINGULAR = 's'
    # PLURAL = 'p'
    # INVARIABLE = 'i'
    # NUMBER_CHOICES = (
    #     (SINGULAR, 's'),
    #     (PLURAL, 'p'),
    #     (INVARIABLE, 'i'),
    # )
    number = models.CharField(
        max_length=2,
        # choices=NUMBER_CHOICES,
    )

    lemma = models.BooleanField()
    lemmaType = models.CharField(max_length=10)

class Definition(models.Model):
    word = models.ForeignKey(Lemme, on_delete=models.CASCADE)
    definition = models.TextField()
    
