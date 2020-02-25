$(function () {
        // Add
        $('#valueSave').click(function () {
            var _this = $(this);
            var uri = _this.data('uri'),
                name_key = $("#id_name_key").val(),
                name_show = $("#id_name_show").val(),
                content = $("#id_content").val();
            $.ajax({
                url: uri,
                data: {
                    'name_key': name_key,
                    'name_show': name_show,
                    'content': content,
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
                    if (err.statusText !== gettext('abort')) {
                        swal({
                            title: gettext('Oops, something went wrong'),
                            type: "error",
                            confirmButtonColor: "#1ab394"
                        });
                    }
                }
            })
        });
        //delete
        $('.source-destroy').click(function () {
            var _this = $(this),
                uri = _this.data('uri'),
                key = _this.data('name_key');
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
                        'name_key': key,
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
                        if (err.statusText !== gettext('abort')) {
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
        // Error prompt reset
        $("#id_name_key").focus(function () {
            $("#id-name_key-error").html("");
        });
        $("#id_name_value").focus(function () {
            $("#id-name_value-error").html("");
        });
        $("#id_content").focus(function () {
            $("#id-content-error").html("");
        });
    });