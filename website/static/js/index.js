var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

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

function currentTime() {
    var date = new Date(); /* creating object of Date class */
    var hour = date.getHours();
    var min = date.getMinutes();
    var sec = date.getSeconds();

    var newformat = hour >= 12 ? 'PM' : 'AM'; 
    hour = hour % 12; 
    hour = hour ? hour : 12; 
    min = min < 10 ? '0' + min : min;

    hour = updateTime(hour);
    min = updateTime(min);
    sec = updateTime(sec);
    document.getElementById("clock").innerText = hour + ":" + min + ":" + sec + " " + newformat; /* adding time to the div */
    var t = setTimeout(function(){ currentTime() }, 1000); /* setting timer */
  }

  function updateTime(k) {
    if (k < 10) {
      return k;
    }
    else {
      return k;
    }
  }

  currentTime(); /* calling currentTime() function to initiate the process */
