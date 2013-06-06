function get_newest_n_statements(factspace, type, criteria, n, onresponse) {
    criteria['kropotkin_criteria'] = 'result-newest,number-' + n;
    var query_string = to_query_string(criteria);
    url = '/factspace/' + factspace + '/statement/' + type
        + '?' + to_query_string(criteria);
    http_request(url, 'GET', null, function(responseText) {
        onresponse(JSON.parse(responseText));
    });
}

function timestamp_to_string(timestamp) {
    date = new Date(timestamp * 1000);
    return date.toString();
}

function check_tasks() {
    get_newest_n_statements('whooshingby', 'completed_task', {}, 10,
                            display_tasks);
}

function display_tasks(tasks) {
    var tasks_table = document.querySelectorAll('*[data-tasks]')[0];
    for (i=0; i<10; i++) {
        var row_data = [];
        if (i < tasks.length) {
            row_data.push(tasks[i]['kropotkin_id']);
            row_data.push(tasks[i]['name']);
            row_data.push(timestamp_to_string(tasks[i]['time']));
            criteria = {'task_id': tasks[i]['kropotkin_id']};
            console.log(criteria);
            get_newest_fact('whooshingby', 'reward', criteria, display_reward);
        } else {
            row_data = ['', '', '']
        }
        row = tasks_table.rows[i];
        for (j=0; j<3; j++) {
            row.cells[j].innerHTML = row_data[j];
        }
    }
}

function display_reward(reward) {
    console.log(reward);
    var tasks_table = document.querySelectorAll('*[data-tasks]')[0];
    for (i=0; i<10; i++) {
        row = tasks_table.rows[i];
        current_id = row.cells[0].innerHTML;
        if (current_id == reward['task_id']) {
            row.cells[3].innerHTML = reward['name'];
        }
    }
}

setInterval(check_tasks, 1000);
report_deployment('display_tasks.js');