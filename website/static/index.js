
$('#staffTable').DataTable({
    pagingType: "simple",
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
