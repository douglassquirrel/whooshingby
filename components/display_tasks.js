function get_newest_n_facts_stamp(factspace, type, criteria, n, stamp, onresp) {
    kropotkin_criteria = 'result-newest,number-' + n + ',stamp-' + stamp;
    criteria['kropotkin_criteria'] = kropotkin_criteria;
    var query_string = to_query_string(criteria);
    url = '/factspace/' + factspace + '/fact/' + type
        + '?' + to_query_string(criteria);
    http_request(url, 'GET', null, function(responseText) {
        onresp(JSON.parse(responseText));
    });
}

function timestamp_to_string(timestamp) {
    date = new Date(timestamp * 1000);
    return date.toString();
}

function check_tasks() {
    stamp = 'display_tasks_'
        + kropotkin_components['display_tasks.js']['kropotkin_id'];
    get_newest_n_facts_stamp('whooshingby', 'completed_task', {}, 10, stamp,
                             display_tasks);
}

function display_tasks(tasks) {
    if (tasks.length != 0) {
        var tasks_table = document.querySelectorAll('*[data-tasks]')[0];
        for (var i=9; i>=tasks.length; i--) {
            from = tasks_table.rows[i-tasks.length]
            to = tasks_table.rows[i];
            for (j=0; j<5; j++) {
                to.cells[j].innerHTML = from.cells[j].innerHTML;
            }
        }
        for (var i=0; i<tasks.length; i++) {
            row = tasks_table.rows[i];
            row.cells[0].innerHTML = tasks[i]['kropotkin_id'];
            row.cells[1].innerHTML = tasks[i]['name'];
            row.cells[2].innerHTML = timestamp_to_string(tasks[i]['time']);
            row.cells[3].innerHTML = '';
            row.cells[4].innerHTML = '';
        }
    }
    setTimeout(check_tasks, 1000);
}

setTimeout(check_tasks, 1000);
report_deployment('display_tasks.js');