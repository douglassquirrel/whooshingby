function check_reward() {
    get_oldest_fact_and_stamp('whooshingby', 'reward', [],
                              'display_reward', display_reward);
}

function display_reward(fact)
{
    name = fact['name'];
    reward_elts = document.querySelectorAll('*[data-reward]');
    hidden_elts = [];
    for (i=0; i<reward_elts.length; i++) {
        if (reward_elts[i].style.display != 'none') {
            reward_elts[i].style.display = 'none';
        } else {
            hidden_elts.push(reward_elts[i]);
        }
    }
    r = Math.random();
    chosen_element = hidden_elts[Math.floor(r * hidden_elts.length)];
    chosen_element.style.display = 'block';
    name_elts = chosen_element.querySelectorAll('*[data-reward-name]');
    for (i=0; i<name_elts.length; i++) {
        name_elts[i].innerHTML = name;
    }
}

setInterval(check_reward, 1000);
report_deployment('display_reward.js');