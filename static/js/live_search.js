// This is a very quick and dirty 2010's style jQuery implementation of a dynamic search results app. I'd prefer to use a more modern front-end
// framework in an actual production app, but this is quick enough for me to write without having to bring in too much external code (besides jQ).

$(document).ready(function(){
	var $topics = $('#topics');
	var $searchinput = $('#id_text_search');
	var $search_results = $('#search_results');
	var $search_results_feed = $('#search_results_feed');
	var $archived_posts = $('#news_archive');
	var $search_term = $('#search_term');
	var $clear = $('#clear');

	var search_text = "";

	// from: http://davidwalsh.name/javascript-debounce-function
	// This is necessary to keep the text search from initiating 
	// a new AJAX request on every keypress when typing quickly
	function debounce(func, wait, immediate) {
	    var timeout;
	    return function() {
	        var context = this, args = arguments;
	        var later = function() {
	            timeout = null;
	            if (!immediate) func.apply(context, args);
	        };
	        var callNow = immediate && !timeout;
	        clearTimeout(timeout);
	        timeout = setTimeout(later, wait);
	        if (callNow) func.apply(context, args);
	    };
	};

	// Compose the backend query, fire it off, and then render the new data into the page when it arrives
	function get_results() {
		var $topic_list = $('#topic_list');
		var query_string = "";

		// Clear the topic list of any existing topics
		$topic_list.html("");

		// Use the selected topics to formulate the query string
		$topics.find("option:selected").each(function() {
			var value = $(this).val();
			query_string += "topics_" + value + "=" + value + "&";
			$topic_list.append(render_topic_tag($(this).html())); // render this topic tag in the list of topics!
		});

		if (search_text) {
			// good to make sure our inputs will work as GET params in the query string!
			query_string +=	"text_search=" + encodeURIComponent(search_text); 
			$search_term.html(search_text);
		}

		$.ajax({
			url: "/api/v1/news/",
			data: query_string
		}).done(function(data){
			$search_results_feed.html(""); // Clear the search results of any existing posts

			$.each(data, function(index, value) {
				$search_results_feed.append(render_post(value, index)); // render each post snippet
			})
		})
	}

	// Do we want to show Django's news archive output or the js-powered search results? If the latter, kick off an update of search results.
	// Toggles whether the dynamic results or the django-rendered results <span>'s are showing/hidden
	function update_page() {
		if ($topics.find("option:selected").length || search_text != "") {
			get_results();
			$search_results.show();
			$archived_posts.hide();
		} else {
			$search_results.hide();
			$archived_posts.show();
		}
	}

	// Given a topic name, output a jQuery object encapsulating a topic tag.
	function render_topic_tag(topic) {
		var $tag = $("<div>");

		$tag.attr('class', 'label label--tag');
		$tag.html(topic);

		return $tag;
	}

	// Given a post and post index, output a jQuery object encapsulating a news post
	function render_post(post, i) {
		var $post = $("<li>");

		$post.attr('data-newspost-id', post.id);
		$post.attr('data-feed-placement', i);

		var $labelSpan = $('<span class="label label--soft">');
		$labelSpan.html(post.publish_date);

		$post.append($labelSpan);

		$.each(post.topic_names, function(index, value) {
			$post.append(render_topic_tag(value));
		});

		var $feedLink = $("<div class='feed-link'>");
		$feedLink.append($("<a>").attr('href', post.source).html(post.title));

		$post.append($feedLink);

		var $feedTeaser = $("<div class='feed-teaser'>");
		$feedTeaser.attr('data-story_id', post.id);
		$feedTeaser.html(post.teaser + " ...");

		$post.append($feedTeaser);

		return $post;
	}

	// Trigger an update when topics are changed
	$topics.change(function() {
		update_page();
	}).change();

	// Trigger an update when search text changes; debounced for better UX
	$searchinput.keyup(debounce(function() {
		search_text = $(this).val();
		update_page();
	}, 500)).change();

	// Resets all filtering/search
	$clear.click(function(){
		$searchinput.val("");
		search_text = "";
		$topics.val([]);
		update_page();
	});

	update_page();

});
