
$('#staffTable').DataTable({
    pagingType: "full",
    lengthChange: false
});

$('#logTable').DataTable({
    pagingType: "simple",
    lengthChange: false,
    pageLength: 15
});

$(document).ready(function() {
    $('#staffTable').on('click','.editPersonnel', function() {

        $('#staticBackdropLabel').html('Edit Personnel Data');
        $('#save-btn').html('Update');

        $('#staticBackdrop').modal('show');
        $tr = $(this).closest('tr');
        var data = $tr.children("td").map(function() {
            return $(this).text();
        }).get();
        console.log(data);
        
        $('#p_db_id').val(data[0]);
        $('#p_id').val(data[1]);
        $('#p_name').val(data[2]);
    });
});

$('#confirm-del').on('show.bs.modal', function(e) {
    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    $(this).find('.btn-ok').attr('name', $(e.relatedTarget).data('name'));
    $('.debug-url').html('Debug-url: <strong>' + $(this).find('.btn-ok').attr('href') + '</strong>');
    $('.personnel-name').html('<strong>' + $(this).find('.btn-ok').attr('name') + '</strong>');
});