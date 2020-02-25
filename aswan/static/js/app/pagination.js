$("body").on("change", "#change-count", function () {
    var value = $(this).val();
    var urlVars = getUrlVars(window.location.href);
    urlVars['page_size'] = value;
    urlVars['page'] = 1;
    var itemArray = [];
    $.each(urlVars, function (key, value) {
        if (value) {
            itemArray.push(key + '=' + value);
        }
    });
    var path = itemArray.join("&");

    window.location.href = window.location.origin + window.location.pathname + "?" + path;
});

function getUrlVars() {
    var vars = {};
    if (window.location.href.indexOf('?') > 0) {
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for (var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            vars[hash[0]] = hash[1];
        }
    }
    return vars;
}