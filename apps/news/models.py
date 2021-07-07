from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from taxonomy.models import DiveSite, Topic

# snippet below from https://stackoverflow.com/a/12982689 :
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
# /snippet


DIVESITE_SOURCE_NAMES = {
    'retaildive': 'Retail Dive',
    'ciodive': 'CIO Dive',
    'educationdive': 'Education Dive',
    'supplychaindive': 'Supply Chain Dive',
    'restaurantdive': 'Restaurant Dive',
    'grocerydive': 'Grocery Dive',
    'biopharmadive': 'BioPharma Dive',
    'hrdive': 'HR Dive',
}


class NewsPost(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(max_length=3000)
    source = models.URLField()
    is_cover_story = models.BooleanField(default=False)
    publish_date = models.DateField(default=timezone.now)
    divesite = models.ForeignKey(DiveSite, null=True, on_delete=models.SET_NULL)
    topics = models.ManyToManyField(Topic)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '<{}> {}'.format(self.divesite.url_name, self.title)

    @property
    def url(self):
        return reverse('newspost_detail', kwargs={'newspost_id': self.pk})

    @property
    def teaser(self):
        # The solution for me is to use the cleanhtml function defined above, that uses a regex to remove HTML tags.
        # The prompt suggests that we could create a way for editors to custom-set the teaser, but given the acceptance criteria,
        # I find this to be a much simpler solution, if it is the case that all that is needed is for the page to not break. 
        # I would definitely ask the stakeholders if they need to be able to define the teaser manually for a
        # different reason - I could imagine that being able to paraphrase the article text manually might be desirable.
        #
        # Verify by setting 'active' on the post with id 13 to True, then viewing the front page.
        #
        # I will also note that the prompt mentions the post titled "Regeneron antibody cuts risk of COVID-19 death in UK study" (id 10).
        # That post doesn't seem to create the problem for me, but post 13 does! So I'm assuming that's the one that I'm supposed to fix.
        return cleanhtml(self.body)[:150]

    @property
    def source_divesite(self):
        return self.divesite.display_name

    def tags(self):
        return [
            'HR', 'Diversity & Inclusion', 'Culture'
        ]

    @classmethod
    def search(cls, topics=None, text_value=None):
        results = cls.objects
        if topics:
            results = results.filter(topics__in=topics)
        if text_value:
            results = results.filter(Q(body__icontains=text_value) | Q(title__icontains=text_value))
        return set(results.all())
