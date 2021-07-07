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
    # a unique True constraint in the NewsPost model in this Stack Overflow answer: 
    # https://stackoverflow.com/a/61326996
    #
    # In that case, I could also simplify the below code a bit in the 'else' case to something like:
    # cover_story = NewsPost.objects.get(is_cover_story=True) 
    # if I could be assured that there was a maxiumum of one cover story.       

    all_cover_stories = NewsPost.objects.all().filter(is_cover_story = True)

    if all_cover_stories.count() == 0 :
        # Handling the case where there is no story designated as the cover story by
        # using the most recent story.
        cover_story = NewsPost.objects.all().order_by('-publish_date').first()
    else :
        cover_story = NewsPost.objects.all().filter(is_cover_story = True).order_by('-publish_date').first() 

    # "The 3 most recent stories, excluding the cover story, should be displayed 
    # under "top stories", ordered by most recent first"
    # ------
    # Current implementation is to get 3 random stories.
    #
    # Need to change this to retrieving the 3 most recent stories that are not the cover story
    #
    # A note on how I implemented this - I'm specifically using the id from the cover_story instance variable
    # because I'm considering the possibility that we're showing a de facto cover story that isn't actually marked as
    # is_cover_story = true in the database; if we took the approach of insisting on is_cover_story = true being a unique
    # constraint in the db, we could do filter(is_cover_story = False) for a similar result.

    top_stories = NewsPost.objects.all().exclude(id = cover_story.id).order_by('-publish_date')[:3]

    # "All news posts that do not appear as the cover story or as top stories should be listed in the archive, 
    # ordered by most recent first"
    # ------
    # Current implementation is to list all stories randomly.
    # 
    # Need to order stories chronologically and exclude top stories + the cover story.
    #
    # This one is pretty straightforward; just build a list of ids to exclude from our existing variables (top_stories and cover_story)
    # and make sure to order the posts correctly.

    exclude_from_other_stories = [top_story.id for top_story in top_stories]
    exclude_from_other_stories.append(cover_story.id)
    
    other_stories = NewsPost.objects.all().exclude(id__in = exclude_from_other_stories).order_by('-publish_date')

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
