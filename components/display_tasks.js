function get_newest_n_facts(factspace, type, criteria, n, onresponse) {
    var kropotkin_criteria = 'result-newest,number-' + n;
    criteria['kropotkin_criteria'] = kropotkin_criteria;
    var query_string = to_query_string(criteria);
    var url = '/factspace/' + factspace + '/fact/' + type
        + '?' + to_query_string(criteria);
    http_request(url, 'GET', null, function(responseText) {
        onresponse(JSON.parse(responseText));
    });
}

function timestamp_to_string(timestamp) {
    var date = new Date(timestamp * 1000);
    return date.toString();
}

function fill_row(row, task) {
    row.cells[0].innerHTML = task['task_id'];
    row.cells[1].innerHTML = task['name'];
    row.cells[2].innerHTML = timestamp_to_string(task['time']);
    row.cells[3].innerHTML = '';
    row.cells[4].innerHTML = '';
}

function check_task() {
    get_next_fact('whooshingby', 'completed_task', display_task);
}

function display_task(task) {
    var tasks_table = document.querySelectorAll('*[data-tasks]')[0];

    for (var i=9; i>0; i--) {
        var from = tasks_table.rows[i-1]
        var to = tasks_table.rows[i];
        for (j=0; j<5; j++) {
            to.cells[j].innerHTML = from.cells[j].innerHTML;
        }
    }
    fill_row(tasks_table.rows[0], task);

    setTimeout(check_task, 1000);
}

function initialise(tasks) {
    var tasks_table = document.querySelectorAll('*[data-tasks]')[0];
    var rows = tasks_table.rows;
    for (var i=0; i<tasks.length; i++) {
        fill_row(rows[i], tasks[i]);
    }
    setTimeout(check_task, 1000);
}

subscribe('whooshingby', 'fact', 'completed_task');
get_newest_n_facts('whooshingby', 'completed_task', {}, 10, initialise);
report_deployment('display_tasks.js');
