$(function () {
        // delete
        $('.event-destroy').click(function () {
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
        // Add
        $('#eventSave').click(function () {
            var _this = $(this);
            var uri = _this.data('uri'),
                event_name = $("#id_event_name").val();
            $.ajax({
                url: uri,
                data: {
                    'event_name': event_name,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                dataType: "json",
                type: "POST",
                success: function (resp) {
                    if (resp.state) {
                        window.location.reload();
                    } else {
                        var error = resp.error;
                        for (var name in error) {
                            $("#id-" + name + "-error").html(error[name][0]);
                        }
                    }
                },
                error: function (err) {
                    if (err.statusText !== 'abort') {
                        swal({
                            title: gettext('Oops, something went wrong'),
                            type: "error",
                            confirmButtonColor: "#1ab394"
                        });
                    }
                }
            })
        });
        // Error prompt reset
        $("#id_event_name").focus(function () {
            $("#id-event_name-error").html("");
        });
    });