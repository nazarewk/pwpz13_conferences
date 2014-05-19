function UpdateReviewerFields()
{
    userId=$("#id_user_account").val();
    var fields=['id_first_name','id_last_name','id_email'];
    if(userId)
    {
        fields.forEach(function(entry) {
            $("#"+entry).attr('disabled','disabled');
        });
    }
    else
    {
        fields.forEach(function(entry) {
            $("#"+entry).removeAttr('disabled');
        });
    }


}