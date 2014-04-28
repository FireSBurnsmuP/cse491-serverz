function GetImage(imgId, containerId, thumbs)
{
    // default value for thumbs
    if(typeof thumbs === 'undefined')
    {
        thumbs = false;
    }
    // figure out what query I should use
    var query = "";
    if(imgId === "latest")
    {
        // newest...
        query = "special=latest";
    }
    else if(imgId === "first")
    {
        // first...
        query = "special=first";
    }
    else
    {
        // a normal img by ID
        query = "img_id=" + imgId;
    }

    // if we're getting thumbnails, make sure the server knows
    if(thumbs)
    {
        query += "&thumbs=true";
    }

    // and load the stuff into the thing.
    // TODO progress circle + callback stuffs
    $('#'+containerId).html('<span class="loader"></span>Loading...')
    .load("/imageshare/image_markup?"+query, function( response, status, xhr ) {
        if ( status == "error" )
        {
            var msg = "The following error occurred while attempting to load this image: ";
            $('#'+containerId).html(
                '<p class="alert alert-error">' +
                msg + xhr.status + " " + xhr.statusText +
                '</p>');
        }
    });
}
