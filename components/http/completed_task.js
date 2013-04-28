POST_MIME_TYPE = "application/x-www-form-urlencoded"
function completed_task() {
    task_xmlhttp = new XMLHttpRequest();
    var url = FACT_URL + '/factspace/kropotkin/completed-task';
    var content = '{"client_address":"' + '0.0.0.0' + '"}'
    task_xmlhttp.open("POST", url, true);
    task_xmlhttp.setRequestHeader("Content-type", POST_MIME_TYPE);
    task_xmlhttp.send(content);
}