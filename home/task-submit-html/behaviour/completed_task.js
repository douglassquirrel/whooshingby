function completed_task() {
    xmlhttp = new XMLHttpRequest();
    var url = FACT_URL + '/completed-task';
    var content = '{"client_address":"' + CLIENT_ADDRESS + '"}'
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-type",
                             "application/x-www-form-urlencoded");
    xmlhttp.send(content);
}