$("#setThreshold").on("show.bs.modal", function (e) {
    var strategyList = $(e.relatedTarget).data('strategy_list');  // Modifying Policy Group's data
    var strategyIndex = $(e.relatedTarget).data('strategy_index');  // Modifying the policy Group's bid
    $("#thresholdModalBody").html("");
    $("#thresholdSave").attr('data-strategy_index', strategyIndex - 1);
    for (var i in strategyList) {
        // Construct threshold input box
        var inputList = "";
        for (var t in strategyList[i][1]) {
            if (t !== 0) {
                inputList += '&nbsp;&nbsp;'
            }
            var inputItem = "<input style='width: 50px;' name='threshold_" + t + "' value='" + strategyList[i][1][t] + "'><span class='err-msg'></span>";
            inputList += inputItem
        }
        // constructr's html
        var htmlBody = "<tr><td><div class='strategy-item' data-uuid='" + strategyList[i][0] + "'>" + strategyList[i][2] + "</div></td><td>" + inputList + "</td></tr>";
        $("#thresholdModalBody").append(htmlBody);
    }
});

$('#thresholdSave').click(function () {
    var _this = $(this);
    var hasError = false;
    var regexPattern = /^\d{1,10}(\.\d{1,2})?$/;
    var uri = _this.data('uri'),
        strategy_index = Number(_this.data('strategy_index')),
        rule_uuid = _this.data('id');
    var data = {'rule_uuid': rule_uuid, 'strategy_index': strategy_index, 'strategy_list': []};
    $(".strategy-item").each(function (index, obj) {
        var strategyUuid = $(this).data('uuid');
        var strategyDesc = $(this).html();
        var thresholdList = [];
        $(this).parents('tr').find("input").each(function () {
            var inputValue = $(this).val();
            // Verify input parameters
            if (strategyDesc.match("^Cell phone number")) {
                var phoneRe = /^\d{1,4}(,\d{1,4})*$/;
                if (phoneRe.test(inputValue)) {
                    $(this).next('span').html("");
                } else {
                    $(this).next('span').html(gettext('The argument is not legal'),);
                    hasError = true
                }
            } else if (strategyDesc.match("Currency Type $")) {
                if (inputValue.indexOf("，") !== -1) {
                    $(this).next('span').html(gettext('The argument is not legal'),);
                    hasError = true;
                } else {
                    $(this).next('span').html("");
                }
            } else if (regexPattern.test(inputValue)) {
                $(this).next('span').html("");
            } else {
                $(this).next('span').html(gettext('The argument is not legal'),);
                hasError = true
            }
            thresholdList.push(inputValue);
        });
        data["strategy_list"].push({'strategy_uuid': strategyUuid, 'threshold_list': thresholdList})
    });
    if (hasError) {
        return false
    }
    $.ajax({
        url: uri,
        data: {
            "data": JSON.stringify(data),
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        dataType: "json",
        type: "POST",
        success: function (resp) {
            if (resp.state) {
                window.location.reload();
            } else {
                swal({
                    title: gettext("Operation failed"),
                    text: resp.msg,
                    type: "warning",
                    confirmButtonColor: "#1ab394"
                });
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


var cur_url = window.location.href;
var url = "{% url 'rule:edit'%}?" + cur_url.split("?")[1];
$("#id_edit_rule").attr("href", url);
