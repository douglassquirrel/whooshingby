function timestamp_to_string(timestamp) {
    var date = new Date(timestamp * 1000);
    return date.toString();
}

function check_reward() {
    get_next_fact('whooshingby', 'reward', display_reward);
}

function display_reward(reward) {
    var tasks_table = document.querySelectorAll('*[data-tasks]')[0];
    for (var j=0; j<10; j++) {
        var row = tasks_table.rows[j];
        var current_id = row.cells[0].innerHTML;
        if (current_id == reward['task_id']) {
            row.cells[3].innerHTML = reward['name'];
            row.cells[4].innerHTML = timestamp_to_string(reward['time']);
        }
    }
    setTimeout(check_reward, 1000);
}

subscribe('whooshingby', 'fact', 'reward');
setTimeout(check_reward, 1000);
report_deployment('display_rewards.js');
