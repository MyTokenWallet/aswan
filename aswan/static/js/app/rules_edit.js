for (i = 0; i < $('textarea').length; i++) {
    var el = $('textarea')[i];
    if (el.scrollHeight > el.offsetHeight) {
        $(el).css('height', el.scrollHeight + 2);
    }
}

$.each($('textarea[data-autoresize]'), function () {
    var offset = this.offsetHeight - this.clientHeight;
    var resizeTextarea = function (el) {
        jQuery(el).css('height', 'auto').css('height', el.scrollHeight + offset);
    };
    jQuery(this).on('keyup input', function () {
        resizeTextarea(this);
    });
});


$(function () {
    $("body").on("submit", '#menu_create_form', function (e) {
        e.preventDefault();
        var _this = $(this);
        var uri = _this.attr('action');
        var uuid = uri.split("?")[1].split('=')[1];
        uri = "{% url 'rule:change' %}";

        var title = $('#id_title').val();
        var describe = $('#id_describe').val();
        var status = $('#id_status').val();
        var end_time = $('#id_end_time').val();

        var names = $(".group-name:visible").map(function () {
            return $(this).val();
        });
        var weights = $(".weight:visible").map(function () {
            return $(this).val();
        });
        var strategys = $("#rule-list .strategy:visible").map(function () {
            return $(this).attr('value');
        });
        var controls = $("#rule-list .form-control:visible").map(function () {
            return $(this).find(":selected").val();
        });
        var customs = $(".custom textarea:visible").map(function () {
            return $(this).val();
        });
        if (names.length !== strategys.length || strategys.length !== controls.length || controls.length !== customs.length) {
            swal({
                title: gettext("Policy can't be blank!"),
                type: "error",
                confirmButtonColor: "#1ab394"
            });
            return;
        }
        if (strategys.length <= 0) {
            swal({
                title: gettext("Rules must be added"),
                type: "error",
                confirmButtonColor: "#1ab394"
            });
            return;
        }
        strategy_arr = [];
        control_arr = [];
        custom_arr = [];
        name_arr = [];
        weight_arr = [];
        for (i = 0; i < strategys.length; i++) {
            if (names[i] === '') {
                swal({
                    title: gettext("PolicyGroup Name can't be empty"),
                    type: "error",
                    confirmButtonColor: "#1ab394"
                });
                return;
            }
            if (weights[i] === '') {
                swal({
                    title: gettext("Weight cannot be empty!"),
                    type: "error",
                    confirmButtonColor: "#1ab394"
                });
                return;
            }
            if (strategys[i] === '') {
                swal({
                    title: gettext("Policy can't be blank!"),
                    type: "error",
                    confirmButtonColor: "#1ab394"
                });
                return;
            }
            if (controls[i] === '') {
                swal({
                    title: gettext("Project Management can't be left empty..."),
                    type: "error",
                    confirmButtonColor: "#1ab394"
                });
                return;
            }
            if (customs[i] === '') {
                customs[i] = " ";
            }
            name_arr.push(names[i]);
            weight_arr.push(weights[i]);
            strategy_arr.push(strategys[i]);
            control_arr.push(controls[i]);
            custom_arr.push(customs[i]);
        }

        params = {
            'id': uuid,
            'title': title,
            'describe': describe,
            'status': status,
            'end_time': end_time,
            'strategys': strategy_arr.join('|'),
            'controls': control_arr.join(","),
            "customs": custom_arr.join(":::"),
            "names": name_arr.join(":::"),
            "weights": weight_arr.join(","),
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        };

        _this.addClass("posting");
        $.ajax({
            url: uri,
            data: params,
            dataType: "json",
            type: "POST",
            success: function (resp) {
                if (resp.state) {
                    window.location.href = resp.redirect_url + "?id=" + uuid;
                } else {
                    _this.removeClass("posting");
                    var error = resp.error;
                    swal({
                        title: error,
                        type: "error",
                        confirmButtonColor: "#1ab394"
                    });
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

function create_rule() {
    var id = $("#rule-list tr:last").attr("id");
    var num = id.split("-")[1];
    var new_id = parseInt(num) + 1;
    var clone = $("#list-0").clone();
    clone.find("a").attr("data-list-id", "list-" + new_id);
    $('#rule-list').append(
        '<tr id="list-' + new_id + '">' + clone.html() + "</tr>"
    );

    $.each($('textarea[data-autoresize]'), function () {
        var offset = this.offsetHeight - this.clientHeight;
        var resizeTextarea = function (el) {
            jQuery(el).css('height', 'auto').css('height', el.scrollHeight + offset);
        };
        jQuery(this).on('keyup input', function () {
            resizeTextarea(this);
        });
    });
}

function save_strategys() {
    var list_id = $("#save-strategy").val();
    var uuids = $('.ms-selection ul.ms-list-selection').children('li').map(function () {
        if ($(this).css("display") != 'none') {
            return $(this).attr("id").split("-selection")[0];
        }
    });
    var strategys = $('.ms-selection ul.ms-list-selection').children('li').map(function () {
        if ($(this).css("display") != 'none') {
            return $(this).html();
        }
    });
    var uuid_arr = [];
    var strategy_arr = [];
    for (i = 0; i < strategys.length; i++) {
        uuid_arr[i] = uuids[i];
        strategy_arr[i] = strategys[i];
    }
    uuids = uuid_arr.join(";");
    strategys = strategy_arr.join(";");
    $("#" + list_id).find("label.strategy").html(strategys);
    $("#" + list_id).find("label.strategy").attr('value', uuids);
    $("#choose-strategy").modal('hide')
}

function delete_rule(which) {
    $(which).parent().parent().remove();
}


var fun_setVal = function () {
    var body = $("#id_search_input").val();
    $("#id_strategy_name").val("equal" + body + "，In the recent" + time + "s_Inside，No more than" + limit + "Times(" + source + ")");
};
$('#id_search_input').on('propertychange input', fun_setVal);


$('.searchable').multiSelect({
    selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='Filters'>",
    afterInit: function (ms) {
        var that = this,
            $selectableSearch = that.$selectableUl.prev(),
            $selectionSearch = that.$selectionUl.prev(),
            selectableSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selectable:not(.ms-selected)',
            selectionSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selection.ms-selected';

        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
            .on('keydown', function (e) {
                if (e.which === 40) {
                    that.$selectableUl.focus();
                    return false;
                }
            });

        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
            .on('keydown', function (e) {
                if (e.which == 40) {
                    that.$selectionUl.focus();
                    return false;
                }
            });
    },
    afterSelect: function () {
        this.qs1.cache();
        this.qs2.cache();
    },
    afterDeselect: function () {
        this.qs1.cache();
        this.qs2.cache();
    }
});


$("#choose-strategy").on("hidden.bs.modal", function () {
    $('#89multiselect').multiSelect('refresh');
    $('.ms-selection ul.ms-list-selection').sortable();
    $('.ms-selection ul.ms-list-selection').disableSelection();
});


$("#choose-strategy").on("show.bs.modal", function (e) {
    var listId = $(e.relatedTarget).data('list-id');
    $("#save-strategy").val(listId);
});


$(function () {
    $('.ms-selection ul.ms-list-selection').sortable();
    $('.ms-selection ul.ms-list-selection').disableSelection();
});


$('#id_end_time').datetimepicker({
    format: 'yyyy-mm-dd hh:ii:ss',
    language: 'fr',
    weekStart: 1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight: 1,
    weekStart: 1,
});
