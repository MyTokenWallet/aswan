$(function () {
    $('.rules-destroy').click(function () {
        var _this = $(this),
            uri = _this.data('uri'),
            id = _this.data('id');
        swal({
            title: gettext('Are you sure you want to delete it'),
            type: "warning",
            allowOutsideClick: true,
            showCancelButton: true,
            confirmButtonColor: "#ff6700",
            confirmButtonText: gettext('delete'),
            cancelButtonText: gettext('cancel'),
            closeOnConfirm: true
        }, function () {
            $.ajax({
                url: uri,
                data: {
                    'id': id,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                dataType: "json",
                type: "POST",
                success: function (resp) {
                    if (resp.state) {
                        window.location.reload();
                    }
                },
                error: function (err) {
                    if (err.statusText !== 'abort') {
                        swal({
                            title: gettext('failed to delete'),
                            type: "error",
                            confirmButtonColor: "#ff6700"
                        });
                    }
                }
            })
        });
    });
});
$(function () {
    $('.rules-on').click(function () {
        var _this = $(this),
            uri = _this.data('uri'),
            title = _this.data('title'),
            status = _this.data('status'),
            id = _this.data('id');
        if (status === 'on') {
            swal({
                title: gettext("Rules") + title + gettext("already enabled"),
                type: "error",
                confirmButtonColor: "#ff6700"
            });
            return;
        }
        swal({
            title: gettext("You determine the Enable rule") + title + gettext("Do you?"),
            type: "warning",
            allowOutsideClick: true,
            showCancelButton: true,
            confirmButtonColor: "#ff6700",
            confirmButtonText: gettext("enable"),
            cancelButtonText: gettext('cancel'),
            closeOnConfirm: true
        }, function () {
            $.ajax({
                url: uri,
                data: {'id': id, 'status': status},
                dataType: "json",
                type: "POST",
                success: function (resp) {
                    if (resp.state) {
                        window.location.reload();
                    }
                },
                error: function (err) {
                    if (err.statusText !== 'abort') {
                        swal({
                            title: gettext("Enable failed"),
                            type: "error",
                            confirmButtonColor: "#ff6700"
                        });
                    }
                }
            })
        });
    });
});

$(function () {
    $('.rules-off').click(function () {
        var _this = $(this),
            uri = _this.data('uri'),
            title = _this.data('title'),
            status = _this.data('status'),
            id = _this.data('id');
        if (status === 'off') {
            swal({
                title: gettext("Rules") + title + gettext("already disabled"),
                type: "error",
                confirmButtonColor: "#ff6700"
            });
            return;
        }
        swal({
            title: gettext("You determine the Disable rule") + title + gettext("Do you?"),
            type: "warning",
            allowOutsideClick: true,
            showCancelButton: true,
            confirmButtonColor: "#ff6700",
            confirmButtonText: gettext("disable"),
            cancelButtonText: gettext('cancel'),
            closeOnConfirm: true
        }, function () {
            $.ajax({
                url: uri,
                data: {'id': id, 'status': status},
                dataType: "json",
                type: "POST",
                success: function (resp) {
                    if (resp.state) {
                        window.location.reload();
                    }
                },
                error: function (err) {
                    if (err.statusText !== 'abort') {
                        swal({
                            title: gettext("Disable failed"),
                            type: "error",
                            confirmButtonColor: "#ff6700"
                        });
                    }
                }
            })
        });
    });
});

$(function () {
    $('.rules-detail').click(function () {
        var _this = $(this),
            uri = _this.data('uri'),
            id = _this.data('id'),
            url = uri + "?id=" + id;
        window.location.href = url;
    });
});

$(function () {
    $('.rules-edit').click(function () {
        var _this = $(this),
            uri = _this.data('uri'),
            id = _this.data('id'),
            url = uri + "?id=" + id;
        window.location.href = url;
    });
});

$(function () {
    $('td .rules-on').map(function () {
        if ($(this).attr("data-status") == "on") {
            $(this).parent().attr("hidden", "");
        }
    });
    $('td .rules-off').map(function () {
        if ($(this).attr("data-status") == "off") {
            $(this).parent().attr("hidden", "");
        }
    });
});

$(function () {
    $('th.id').click(function () {
        var _this = $(this),
            new_uri = '';
        var uri = _this.find('a').attr('href');
        var target = window.location.href.substr(window.location.href.indexOf("?"));
        if (target.indexOf('sort=id') < 0) {
            new_uri = uri.replace("sort=-id", "sort=id");
            _this.find('a').attr('href', new_uri);
        } else {
            new_uri = uri.replace("sort=id", "sort=-id");
            _this.find('a').attr('href', new_uri);
        }
    });
});