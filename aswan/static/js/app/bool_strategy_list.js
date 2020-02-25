$(function () {
    // delete button
    $('.strategy-destroy').click(function () {
        var _this = $(this),
            uri = _this.data('uri'),
            id = _this.data('id');
        swal({
            title: gettext('Are you sure? Do you want to delete it!'),
            type: "warning",
            allowOutsideClick: true,
            showCancelButton: true,
            confirmButtonColor: "#ff6700",
            confirmButtonText: gettext('delete'),
            cancelButtonText: gettext('cancel'),
            closeOnConfirm: false
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
                    } else {
                        swal({
                            title: resp.error,
                            type: "error",
                            confirmButtonColor: "#ff6700"
                        });
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