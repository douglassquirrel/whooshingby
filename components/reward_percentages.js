window.percentagesChanged = false;

function create_controls(percentages_fact) {
    var percentages = [];
    if (null != percentages_fact) {
        percentages = JSON.parse(percentages_fact['percentages']);
    }
    var html = '';
    for (var i=0; i<percentages.length; i++) {
        var name  = percentages[i][0];
        var value = percentages[i][1];
        html += '<label>' +  name + ' '
              + '<input data-percentage-input '
              + '       onchange="window.percentagesChanged=true;" '
              + '       type="range" min="0" max="100" '
              + '       name="' + name + '" '
              + '       value="' + value + '"/>'
              + '</label>';
    }
    var percentages_div = document.querySelectorAll('*[data-percentages]')[0];
    percentages_div.innerHTML = html;
}

function save_percentages() {
    if (window.percentagesChanged == false) { return; }
    window.percentagesChanged = false;
    var inputs = document.querySelectorAll('*[data-percentage-input]');
    var percentages = [];
    for (var i=0; i<inputs.length; i++) {
        percentages.push([inputs[i].name, parseInt(inputs[i].value)]);
    }
    store_fact('whooshingby', 'reward_percentages',
               {'percentages': JSON.stringify(percentages)});
}

get_newest_fact('whooshingby', 'reward_percentages', {}, create_controls);
setInterval(save_percentages, 1000);
report_deployment('display_rewards.js');
