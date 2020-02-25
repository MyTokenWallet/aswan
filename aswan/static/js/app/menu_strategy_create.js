function makename() {
    var a = $("#id_dimension").find("option:selected").text();
    var b = $("#id_menu_op").find("option:selected").text();
    var c = $("#id_event").find("option:selected").text();
    var d = $("#id_menu_type").find("option:selected").text();
    $("#id_strategy_name").val(a + b + c + gettext("of") + d + gettext("in"));
}

makename();
$('#id_dimension').on('change', makename);
$('#id_event').on('change', makename);
$('#id_menu_op').on('change', makename);
$('#id_menu_type').on('change', makename);


$(function () {
    // Create a vulnerability form submission
    $("body").on("submit", '#menu_create_form', function (e) {
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
                    window.location.href = resp.redirect_url;
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


// Error prompt reset
$("#id_strategy_op").focus(function () {
    $("#id-strategy_op-error").html("");
});
$("#id_strategy_name").focus(function () {
    $("#id-strategy_name-error").html("");
});
