from django.template import loader
from django.http import HttpResponse

from wavepool.models import NewsPost
from wavepool.code_exercise_defs import code_exercise_defs, code_review_defs, code_design_defs
from django.conf import settings


def front_page(request):
    """ View for the site's front page
        Returns all available newsposts, formatted like:
            cover_story: the newsposts with is_cover_story = True
            top_stories: the 3 most recent newsposts that are not cover story
            archive: the rest of the newsposts, sorted by most recent
    """
    template = loader.get_template('wavepool/frontpage.html')

    # "The newspost designated as the cover story should appear in the cover story box"
    # ------
    # Current implementation is to get the cover story by getting a random result.
    #
    # Need to change this to look for a post with is_cover_story = True.
    #
    # Also, it's unclear if the intended behavior is for there to only ever (and always)
    # be one story with 'is_cover_story' set to True, or if we are to account
    # for multiple/zero stories that meet this criteria. If I was designing the spec for 
    # this app myself, I would consider allowing for any number of posts to be designated
    # as cover stories; this way we would keep track of all historical cover stories and 
    # not lose that information when a new story was chosen to be the covery story.
    # Additionally, it seems intuitive to me that, were there multiple cover stories,
    # the one to show on the front page would be the most recently published one.
    #
    # This has a drawback, however, which is that designating a new cover story that was
    # published less recently than the current cover story would be impossible.
    #
    # If we wanted to solve that problem instead, there is an example of a way to implement 
    # a unique True constraint in the model in this Stack Overflow answer: 
    # https://stackoverflow.com/a/61326996

    all_cover_stories = NewsPost.objects.all().filter(is_cover_story = True)

    if all_cover_stories.count() == 0 :
        # Handling the case where there is no story designated as the cover story by
        # using the most recent story.
        cover_story = NewsPost.objects.all().order_by('publish_date').first()
    else :
        cover_story = NewsPost.objects.all().filter(is_cover_story = True).order_by('publish_date').first()

    top_stories = NewsPost.objects.all().order_by('?')[:3]
    other_stories = NewsPost.objects.all().order_by('?')

    context = {
        'cover_story': cover_story,
        'top_stories': top_stories,
        'archive': other_stories,
    }

    return HttpResponse(template.render(context, request))


def newspost_detail(request, newspost_id):
    template = loader.get_template('wavepool/newspost.html')
    newspost = NewsPost.objects.get(pk=newspost_id)
    context = {
        'newspost': newspost
    }

    return HttpResponse(template.render(context, request))


def instructions(request):
    template = loader.get_template('wavepool/instructions.html')

    context = {
        'code_exercise_defs': code_exercise_defs,
        'code_design_defs': code_design_defs,
        'code_review_defs': code_review_defs,
        'show_senior_exercises': settings.SENIOR_USER,
    }
    return HttpResponse(template.render(context, request))
