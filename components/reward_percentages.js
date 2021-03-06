window.rewardPercentagesChanged = false;

function create_reward_percent_controls(percentages_fact) {
    var percentages = [];
    if (null != percentages_fact) {
        percentages = JSON.parse(percentages_fact['percentages']);
    }
    var html = '';
    for (var i=0; i<percentages.length; i++) {
        var name  = percentages[i][0];
        var value = percentages[i][1];
        html += '<label>' +  name + ' '
              + '<input data-reward-percentage-input '
              + '       onchange="window.rewardPercentagesChanged=true;" '
              + '       type="range" min="0" max="100" '
              + '       name="' + name + '" '
              + '       value="' + value + '"/>'
              + '</label>';
    }
    var div = document.querySelectorAll('*[data-reward-percentages]')[0];
    div.innerHTML = html;
}

function save_reward_percentages() {
    if (window.rewardPercentagesChanged == false) { return; }
    window.rewardPercentagesChanged = false;
    var inputs = document.querySelectorAll('*[data-reward-percentage-input]');
    var percentages = [];
    for (var i=0; i<inputs.length; i++) {
        percentages.push([inputs[i].name, parseInt(inputs[i].value)]);
    }
    store_fact('whooshingby', 'reward_percentages',
               {'percentages': JSON.stringify(percentages)});
}

get_newest_fact('whooshingby', 'reward_percentages',
                {}, create_reward_percent_controls);
setInterval(save_reward_percentages, 1000);
report_deployment('reward_percentages.js');
