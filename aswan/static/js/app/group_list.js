$(".perms-group-delete").on("click", function () {
    var $this = $(this);
    var entity_id = $this.data("entity_id");
    swal({
        title: gettext('Are you sure you want to delete it'),
        type: "warning",
        showCancelButton: true,
        confirmButtonClass: "btn-danger",
        confirmButtonColor: "#ff6700",
        confirmButtonText: gettext('delete'),
        cancelButtonText: gettext('cancel'),
        closeOnConfirm: false,
        closeOnCancel: true
    }, function (isConfirm) {
        if (isConfirm) {
            $.ajax({
                method: "DELETE",
                url: "{{ request.get_full_path }}",
                data: {entity_id: entity_id},
                dataType: "json",
                success: function (data) {
                    if (data.state) {
                        swal({
                            title: gettext("delete succeeded!"),
                            type: "success",
                            timer: 800,
                            showCancelButton: false,
                            showConfirmButton: false
                        });
                        $this.parent().parent().css("display", "none");
                    } else {
                        swal({
                            title: gettext('failed to delete'),
                            type: "danger",
                        });
                    }
                }
            });
        }
    });
});