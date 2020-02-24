$(function () {
    Date.prototype.format = function (fmt) {
        var o = {
            "M+": this.getMonth() + 1,                 //月份
            "d+": this.getDate(),                    //日
            "h+": this.getHours(),                   //小时
            "m+": this.getMinutes(),                 //分
            "s+": this.getSeconds(),                 //秒
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度
            "S": this.getMilliseconds()             //毫秒
        };
        if (/(y+)/.test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        }
        for (var k in o) {
            if (new RegExp("(" + k + ")").test(fmt)) {
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
            }
        }
        return fmt
    };

    function getLocalTime(datetime_str, area) {
        //Parameter i is a time zone value number, for example, Beijing for the East 8 district is input 8, West 5 input-5
        if (typeof area !== 'number') return;
        datetime_str = datetime_str.replace(/-/g, "/");
        var date = new Date(datetime_str);
        //Time offset difference between local time and GMT time
        var offset = date.getTimezoneOffset() * 60000;
        //get the green wichita time now
        var utcTime = date.getTime() + offset;
        var date_ = new Date(utcTime + 3600000 * area).format("yyyy-MM-dd hh:mm:ss");
        return date_
    }

    if ($("#id_end_time").val() == "") {
        $("#id_end_time").val(getLocalTime('2049-01-01 00:00:00', 8));
    }

});