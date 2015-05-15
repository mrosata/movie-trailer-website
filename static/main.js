// Pause the video when the modal is closed
$(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
    // Remove the src so the player itself gets removed, as this is the only
    // reliable way to ensure the video stops playing in IE
    $("#trailer-video-container").empty();
});
// Start playing the video whenever the trailer modal is opened
$(document).on('click', '.video-tile', function (event) {
    var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
    var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
    $("#trailer-video-container").empty().append($("<iframe></iframe>", {
      'id': 'trailer-video',
      'type': 'text-html',
      'src': sourceUrl,
      'frameborder': 0
    }));
});

// Animate in the movies when the page loads
$(document).ready(function () {
    $('.video-tile').hide().first().show("fast", function showNext() {
        $(this).next("article").show("fast", showNext);
    });

    // The container elm for all .video-tiles
    var videoGrid = $('#videogrid');
    // Variable to hold all the video tiles and their information
    var tiles = [];

    // Walk through each video-tile div which was templated using Python so that we will have data attributes unique to the video within
    $('.video-tile').each(function (i, elm) {
        var tile = $(this);
        var videoTile = {};
        videoTile.elm = elm;
        videoTile.$ = tile; // same as $(elm)
        videoTile.title = tile.attr('data-video-title');
        videoTile.rating = parseFloat(tile.attr('data-video-rating'));
        videoTile.rated = tile.attr('data-video-rated');
        videoTile.time = parseInt(tile.attr('data-video-time'), 10);
        videoTile.type = tile.attr('data-video-type');
        videoTile.category = tile.attr('data-video-category');
        videoTile.date = parseInt(tile.attr('data-video-date'), 10);
        videoTile.classes = tile.attr('class'); // This is so we can remove all classes belonging to plugin and keep our own
        videoTile.onShelf = true; // Whether it's elm is in html or removed
        /**
         * method - removeVideo()
         *  Check if video-tile is in html, and if so remove from page
         */
        videoTile.removeVideo = function () {
            if (this.onShelf) {
                this.$.fadeOut();
                this.$.remove();
                this.$.removeClass();
                this.$.addClass(this.classes);
                this.onShelf = false;
            }
        }
        /**
         * method - appendVideo()
         *  Check if video-tile is in html, if not put it back into page
         */
        videoTile.appendVideo = function () {
            if (!this.onShelf) {
                this.$.appendTo(videoGrid);
                this.$.fadeIn();
                this.onShelf = true;
            }
        }
        // push this video object into our Array of video-tiles
        tiles.push(videoTile);
    });
    // Let's create a global variable for outer scopes that may want access to the videos
    window.videotiles = tiles;


    /**
     * Initialize the pintrest-like jQuery plugin
     */
    pint = videoGrid.pinterest_grid({
        no_columns: 3,  // 3 columns for desktop/tablet
        padding_x: 10,  // base padding, margin ect.
        padding_y: 10,
        margin_bottom: 50,
        single_column_breakpoint: 768 // Bootstrap breakpoint sm
    });

    /**
    * Setup my filtering functions
    */
    // First let's declare all variables common to tasks below, first elms
    var titleSearch = $('input[name="video-title-search"]'),
        typeDropDown = $('#video-type-search'),
        ratingSlider = $('input[name="video-rating-search"]'),
        starDisplay = $('#starDisplay'),
        introDiv = $('#intro'),
        // and now a bool to track if my intro div w/text is still visible so it only gets removed 1 time
        introIsVisible = true,
        // The length of all tiles, so we can loop through them
        tilesLen = tiles.length;

    /**
     *  Common filtering function for all events, we want any decision to track all selected filters
     */
    function filterAllVideos(e) {
        // If my class intro is still visible, remove it
        if (introIsVisible) {
            introDiv.slideUp();
            introIsVisible = false;
        }
        // Get values from free-search and drop-down in navbar
        var searchVal = titleSearch.val().toLowerCase(),
            searchType = typeDropDown.val().toLowerCase(),
            i = tilesLen,
            // the following are "state" of the tile being checked
            hasTitle, isVideoType, isRatedHigher, tile;
        for (i; i>0; i--) {
            // get quick ref to next tile
            tile = tiles[i-1];
            // Check which of 3 requirements does the tile meet
            hasTitle = (tile.title.toLowerCase().indexOf(searchVal) > -1);
            isVideoType = (searchType == 'any' || tile.type == searchType);
            isRatedHigher = (parseFloat(ratingSlider.val()) < tile.rating);
            // Now take action according to whether tile should be on page, or potentially removed
            if (hasTitle && isVideoType && isRatedHigher) {
                // we use method so we never try to append a tile that is already present
                tile.appendVideo();
            } else {
                // we use method so we never try to remove tile when it's not there
                tile.removeVideo();
            }
        }
    }

    // Turn the rating slider into a jQueryUI range slider with minimun, AKA zero options set.
    ratingSlider.slider();

    // Event for title free-search key-up
    titleSearch.on('keyup.mrosata', function (e) {
       filterAllVideos(e);
    });
    // Event for drop-down change
    typeDropDown.on('change.mrosata', function (e) {
        filterAllVideos(e);
    });
    // Event for slider changed
    ratingSlider.on('change.mrosata', function (e) {
        filterAllVideos(e);
        starDisplay.html(ratingSlider.val() + '<span class="glyphicon glyphicon-star-empty"></span><span class="glyphicon glyphicon-arrow-up"></span>');
    });

    // This mouseup is only to remove the initial intro text, then it's dead
    $('body').on('mouseup.mrosata', function (e) {
        // This is basically just to remove the introDiv
        introDiv.slideUp();
        introIsVisible = false;
        $('body').off('mouseup.mrosata');
    });
});