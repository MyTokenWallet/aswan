function makename() {
    var a = $("#id_strategy_var").find("option:selected").text();
    var b = $("#id_strategy_op").find("option:selected").text();
    var c = $(".searchable-select-item.selected")[0].innerHTML;
    var func_name = $("#id_strategy_func").find("option:selected").val();
    if (['is_proxy_ip', 'is_adsl_ip', 'is_cloud_ip', 'is_evil_ip', 'is_idc_ip'].indexOf(func_name) !== -1) {
        $('#id-strategy_func-error').html(gettext("Separate ip information does not indicate that User is a malicious User, please use with other Policy"));
    } else {
        $('#id-strategy_func-error').html("");
    }
    if (b === c) {
        c = "";
    }
    var relation_ops = [
        gettext("Greater than..."),
        gettext("Greater than or equal to..."),
        gettext("Less than..."),
        gettext("Less than or equal to..."),
        gettext("Equals..."),
        gettext("Not equal to...")];

    if (relation_ops.indexOf(b) === -1) {
        $("#id_strategy_name").val(a + b + c);
    } else {
        $("#id_strategy_name").val(a + c + b);
    }
}

$('#id_strategy_var').on('change', makename);
$('#id_strategy_op').on('change', makename);

// $('#id_strategy_func').on('change', makename);  //Added search box plug-in, change event invalidated
function replace_param() {
    var name = $("#id_strategy_name").val();
    var param = $("#id_strategy_threshold").val();
    var new_name = name.replace("...", param);
    $("#id_strategy_name").val(new_name);
}

$("#id_strategy_threshold").blur(replace_param);


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
$("#id_strategy_threshold").focus(function () {
    $("#id-strategy_threshold-error").html("");
});
$("#id_strategy_var").focus(function () {
    $("#id-strategy_var-error").html("");
});
$("#id_strategy_func").focus(function () {
    $("#id-strategy_func-error").html("");
});


$(function () {
    $('select#id_strategy_func').searchableSelect();
});


//Built-in function linkage display (requires special handling due to the addition of search box plug-in)
function get_data_example() {
    makename()
}


// The width of typehead is the same as the input width of the page
function setWidth() {
    var input_element = document.getElementById("id_strategy_op");
    var objs = document.getElementsByClassName("searchable-select");
    for (var i = 0; i < objs.length; i++) {
        objs[i].style.cssText = "min-width:" + input_element.offsetWidth + "px;";
    }
}

window.onresize = setWidth;
$(document).ready(setWidth)

