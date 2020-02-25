$(function () {
    // Add
    $('#valueSave').click(function () {
        var _this = $(this);
        var uri = _this.data('uri'),
            value = $("#id_value").val(),
            menu_type = $("#id_menu_type").val(),
            event_code = $("#id_event_code").val(),
            end_time = $("#id_end_time").val(),
            menu_desc = $("#id_menu_desc").val();
        $.ajax({
            url: uri,
            data: {
                'value': value,
                'menu_type': menu_type,
                'event_code': event_code,
                'end_time': end_time,
                'menu_desc': menu_desc,
                'dimension': "ip",
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
    // {% comment %}Translators: Error prompt reset{% endcomment %}

    $("#id_value").focus(function () {
        $("#id-value-error").html("");
    });
    $("#id_menu_type").focus(function () {
        $("#id-menu_type-error").html("");
    });
    $("#id_event_code").focus(function () {
        $("#id-event-error").html("");
    });
    $("#id_start_time").focus(function () {
        $("#id-start_time-error").html("");
    });
    $("#id_end_time").focus(function () {
        $("#id-end_time-error").html("");
    });
    $("#id_menu_desc").focus(function () {
        $("#id-menu_desc-error").html("");
    });
});