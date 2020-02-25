$(function () {
    // Create a vulnerability form submission
    $("body").on("submit", '#menu_create_form', function (e) {
        $("#id-req_body-error").html("");
        $("#id-strategy-error").html("");
        $("#resultArea").html("");

        e.preventDefault();
        var form = $(this);
        var _this = $(this);
        var uri = _this.attr('action');
        var params = form.serializeArray();

        _this.addClass("posting");
        $.ajax({
            url: uri,
            data: params,
            dataType: "json",
            type: "POST",
            success: function (resp) {
                if (resp.state) {
                    var data = JSON.stringify(resp.data, null, 4);
                    $("#resultArea").html(data);
                } else {
                    _this.removeClass("posting");
                    var error = resp.error;
                    for (var name in error) {
                        $("#id-" + name + "-error").html(error[name][0]);
                    }
                }
            },
            error: function (err) {
                if (err.statusText !== 'abort') {
                    _this.removeClass("posting");
                    swal({
                        title: gettext('Oops, something went wrong'),
                        type: "error",
                        confirmButtonColor: "#1ab394"
                    });
                }
            }
        })
    });
});

function get_data_example() {
    uuid = $(".searchable-select-item.selected").data('value');
    $.ajax({
        url: "{% url 'strategy:bool_strategy_data' %}",
        data: {
            "uuid": uuid,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        dataType: "json",
        type: "POST",
        success: function (resp) {
            if (resp.state) {
                var req_body = JSON.stringify(resp.req_body, null, 4);
                $("#id_req_body").val(req_body);
            }
        },
    })
}


$(function () {
    $('select.form-control').searchableSelect();
});
