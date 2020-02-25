"use strict";

var _oGo = $('#goto'),
    _inpNum = _oGo.find('input'),
    _btnConfirm = _oGo.find('a');

$(".num").on("keyup", function () {

    var pageNum = $(this).val(),
        maxNum = parseFloat($(".page-show .page").eq(-1).text()),
        reg = /^\d*$/;

    if (!reg.test(pageNum)) {
        $(this).val("");
    } else {
        pageNum = parseFloat(pageNum);

        if (pageNum > maxNum) {
            $(this).val(maxNum);
        }
        if (pageNum <= 0) {
            $(this).val("1");
        }
    }
});

_btnConfirm.on("click", function () {

    var pageNum = $.trim(_inpNum.val());
    var hrefPrefix = _btnConfirm.attr('data-href');
    hrefPrefix = hrefPrefix.replace("&submit=%E6%9F%A5%E8%AF%A2", "");
    hrefPrefix = hrefPrefix.replace("&page=", "");

    if (pageNum === "") {
        return false;
    } else {
        _btnConfirm[0].href = hrefPrefix + "&page=" + pageNum;
    }
});