$(document).ready(function() {
    function handle_recurrence($object) {
        if($object.val() == '') {
            // diable recurrence
            $('#id_count').parent('div.form-group').hide();
            $('#id_until').parent().parent('div.form-group').hide();
        } else {
            // enable recurrence
            $('#id_count').parent('div.form-group').show();
            $('#id_until').parent().parent('div.form-group').show();
        }
    }

    function handle_wholeday($object) {
        if($object.is(':checked')) {
            $('#id_start_picker').parent('div.form-group').hide();
            $('#id_end_picker').parent('div.form-group').hide();
            $('#id_day_picker').parent('div.form-group').show();
        } else {
            $('#id_start_picker').parent('div.form-group').show();
            $('#id_end_picker').parent('div.form-group').show();
            $('#id_day_picker').parent('div.form-group').hide();
        }
    }


    handle_wholeday($('#id_whole_day'));
    $('#id_whole_day').bind('change', function() {
        handle_wholeday($(this));
    });

    handle_recurrence($('#id_recurrence'));
    $('#id_recurrence').bind('change', function() {
        handle_recurrence($(this));
    });
});
