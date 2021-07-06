code_review_defs = [
    {
        'title': 'Site front page',
        'description': 'There are several bugs on the front page of the Wavepool site. Fix these bugs by editing the front_page.html template file and the front_page view in views.py. Submit a pull request for a branch titled "yourlastname_yourfirstname_front_page_fixes"',  # noqa
        'acceptance_criteria': [
            'The newspost designated as the cover story should appear in the cover story box',
            'The 3 most recent stories, excluding the cover story, should be displayed under "top stories", ordered by most recent first',  # noqa
            'All news posts that do not appear as the cover story or as top stories should be listed in the archive, ordered by most recent first',  # noqa
            'Newspost teasers should be properly rendered as HTML',
        ],
        'is_senior': True,
        'pull_request': 'https://github.com/industrydive/wavepool/pull/2',
    },
]

code_design_defs = [
    {
        'title': 'Customize News Post Ads',
        'description': '''
        The sales team currently sells a single advertisement to a client for the whole site. The HTML for this ad is manually updated via engineering team support tickets periodically.
        The Sales Team wants the ability to create their own ads using the CMS and assign them to specific news posts in order to maximize revenue.
        ''',
        'acceptance_criteria': [
            'A Sales Team member can access a set of standard admin pages in the CMS to create advertisements',
            'For each advertisement they should be able to upload a client logo, a link that the ad should open to and the ad\'s text',
            'Each advertisement should appear on the news post that is sold for',
            'The Sales Team might sell more than one news post slot to a client at a time, so they should be able to set a single ad to multiple posts',
        ]
    },

]

code_exercise_defs = [
    {
        'title': 'Site front page',
        'description': 'There are several bugs on the front page of the Wavepool site. Fix these bugs by editing the front_page.html template file and the front_page view in views.py. Submit a pull request for a branch titled "yourlastname_yourfirstname_front_page_fixes"',  # noqa
        'test_class': 'SiteFrontPage',
        'acceptance_criteria': [
            {
                'description': 'The newspost designated as the cover story should appear in the cover story box',
                'test': 'test_cover_story_placement'
            },
            {
                'description': 'The 3 most recent stories, excluding the cover story, should be displayed under "top stories", ordered by most recent first',  # noqa
                'test': 'test_top_stories'
            },
            {
                'description': 'All news posts that do not appear as the cover story or as top stories should be listed in the archive, ordered by most recent first',  # noqa
                'test': 'test_archive_stories'
            },
            {
                'description': 'Newspost teasers should be properly rendered as HTML',
                'test': 'test_newspost_teaser_render'
            },
        ],
        'is_senior': False,
    },
    {
        'title': 'CMS forms',
        'description': 'There are several bugs in the CMS for editing news posts. Fix these by editing the admin.py file and the models.py file. Submit a pull request for a branch titled "yourlastname_yourfirstname_cms_fixes"',  # noqa
        'test_class': 'CmsPage',
        'acceptance_criteria': [
            {
                'description': 'The CMS list page for news posts displays the title of each news post',  # noqa
                'test': 'test_title_shows_on_list_page'
            },
            {
                'description': 'The CMS list of news posts is sorted by the publish date, with the most recent on top',  # noqa
                'test': 'test_displayed_in_order'
            },
            {
                'description': 'Only one story can be saved as the cover story using the is_cover_story field',  # noqa
                'test': 'test_only_one_cover_story'
            },
        ],
        'is_senior': False,
    },
    {
        'title': 'News post detail page',
        'description': 'There are several bugs on the news post detail page. Fix these by editing the news post view in views.py and the newspost.html template file. Submit a pull request for a branch titled "yourlastname_yourfirstname_newspost_detail_fixes".',  # noqa
        'test_class': 'NewsPostDetail',
        'acceptance_criteria': [
            {
                'description': 'Each news post has a unique URL',  # noqa
                'test': 'test_newspost_unique_urls'
            },
            {
                'description': 'The contents of a news post specified by its URL are displayed using the \'newspost.html\' template',  # noqa
                'test': 'test_newspost_page_content'
            },
            {
                'description': 'The news post content should be rendered as formatted HTML on the page',  # noqa
                'test': 'test_newspost_body_render'
            },
            {
                'description': 'Non-logged in users cannot see the "edit" button on the news post page',  # noqa
                'test': 'test_visitor_not_sees_edit_link'
            },
            {
                'description': 'Logged in CMS users can see an "edit" button which opens the CMS change page for the news post',  # noqa
                'test': 'test_cms_user_sees_edit_link'
            },
            {
                'description': 'The title tag of a news post page should be "[story title] | Wavepool | Industry Dive", where the [story title] is the correct title for the given news post',  # noqa
                'test': 'test_newspost_page_title_attribute'
            },
            {
                'description': 'The source link should contain the name of the specific dive site that source is from. There is a map of dive site short names to their display names in the models.py file',  # noqa
                'test': 'test_divesite_display_name'
            },
        ],
        'is_senior': True,
    },
]
