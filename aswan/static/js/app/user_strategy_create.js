var fun_setVal = function () {
    var source = $("#id_strategy_source").find("option:selected").text();
    var body = $("#id_strategy_body").val();
    var day = $("#id_strategy_day").val();
    var limit = $("#id_strategy_limit").val();
    var pattern = /^[1-9]\d*$/; //Match pattern
    var elements = body.split(',');
    body = elements.join(',');
    if (pattern.test(day) && pattern.test(limit)) {
        $("#id-strategy_name-error").html("");
        if (parseInt(day) === 1) {
            $("#id_strategy_name").val(
                gettext("equal") + body +
                gettext("，Day limit") + limit +
                gettext("Individual_User(") + source + ")");
        } else {
            $("#id_strategy_name").val(
                gettext("equal") + body +
                gettext("，at") + day +
                gettext("Natural days，Limit") + limit +
                gettext("Individual_User(") + source + ")");
        }
    } else {
        $("#id-strategy_name-error").html(
            gettext("The 'default number of days' or 'User numbers' needs to be an integer greater than or greater than 1."));
    }

};
fun_setVal();
$('#id_strategy_source').on('change', fun_setVal);
$('#id_strategy_day').on('propertychange input', fun_setVal);
$('#id_strategy_limit').on('propertychange input', fun_setVal);


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


// Rendering Data Source Data
$.ajax({
    url: "/config/source/ajax/",
    data: {},
    dataType: "json", type: "GET",
    success: function (resp) {
        $.each(resp.data, function (i, e) {
            names = e.content.map(function (d) {
                return d['name'];
            });
            if (names.indexOf('user_id') !== -1) {
                $('#id_strategy_source').append($('<option>', {
                    value: e['name_key'],
                    text: e['name_show']
                }));
                var val = e['name_key'];
                $("#label-strategy_body").attr("data-" + val, JSON.stringify(e['content']));
                if (i === 0) {
                    refresh_checkbox(val);
                }
            }
        });
        change_combox_style();
    }
});

function change_combox_style() {
    $('select#id_strategy_source.form-control').searchableSelect();

    function setWidth() {
        var input_element = document.getElementById("id_strategy_desc");
        var objs = document.getElementsByClassName("searchable-select");
        for (var i = 0; i < objs.length; i++) {
            objs[i].style.cssText = "min-width:" + input_element.offsetWidth + "px;";
        }
    }

    window.onresize = setWidth;
    $(document).ready(setWidth)
}

function refresh_checkbox(name) {
    name = name.toLowerCase();
    var source_data = $("#label-strategy_body").data(name);
    $("#cb-strategy_body").html("");
    $.each(source_data, function (k, v) {
        if (v['name'] !== 'user_id') {
            var innerHtml = '<span style="margin-right: 10px"><input type="checkbox" class="sb_check" style="margin-right: 3px" name="strategy_body_check" value=' + v['name'] + '>' + v['desc'] + '</span>';
            $("#cb-strategy_body").append(innerHtml)
        }
    });
}

function get_data_example() {
    // Data source selection linkage
    var source_name = $(".searchable-select-item.selected").data('value');
    refresh_checkbox(source_name);
}

// Define strategy_body
$(document).on("click", 'input:checkbox', function () {
    var arrs = [];
    $('input:checked[name=strategy_body_check]').each(function () {
        arrs.push($(this).val());
    });
    var strategy_body = arrs.join(',');
    $("input[name=strategy_body]").val(strategy_body);
    fun_setVal()
});


// Error prompt reset
$("#id_strategy_limit").focus(function () {
    $("#id-strategy_limit-error").html("");
});
$("#id_strategy_day").focus(function () {
    $("#id-strategy_day-error").html("");
});
