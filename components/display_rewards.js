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

function check_rewards() {
    stamp = 'display_rewards_'
        + kropotkin_components['display_tasks.js']['kropotkin_id']
        + '_' + display_rewards_start_id;
    get_newest_n_facts_stamp('whooshingby', 'reward', {}, 10, stamp,
                             display_rewards);
}

function display_rewards(rewards) {
    if (rewards.length != 0) {
        var tasks_table = document.querySelectorAll('*[data-tasks]')[0];
        for (var i=0; i<rewards.length; i++) {
            reward = rewards[i];
            for (var j=0; j<10; j++) {
                row = tasks_table.rows[j];
                current_id = row.cells[0].innerHTML;
                if (current_id == reward['task_id']) {
                    time = timestamp_to_string(reward['kropotkin_timestamp']);
                    row.cells[3].innerHTML = reward['name'];
                    row.cells[4].innerHTML = time;
                }
            }
        }
    }
    setTimeout(check_rewards, 1000);
}

function initialise(fact) {
    var latest_reward_id = 0;
    if (fact != null) { latest_reward_id = fact['kropotkin_id']; }
    window.display_rewards_start_id = latest_reward_id;
    setTimeout(check_rewards, 1000);
}

get_newest_fact('whooshingby', 'reward', {}, initialise);
report_deployment('display_rewards.js');
