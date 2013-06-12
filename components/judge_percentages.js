window.judgePercentagesChanged = false;

function create_judge_percent_controls(percentages_fact) {
    var percentages = [];
    if (null != percentages_fact) {
        percentages = JSON.parse(percentages_fact['percentages']);
    }
    var html = '';
    for (var i=0; i<percentages.length; i++) {
        var name  = percentages[i][0];
        var value = percentages[i][1];
        html += '<label>' +  name + ' '
              + '<input data-judge-percentage-input '
              + '       onchange="window.judgePercentagesChanged=true;" '
              + '       type="range" min="0" max="100" '
              + '       name="' + name + '" '
              + '       value="' + value + '"/>'
              + '</label>';
    }
    var div = document.querySelectorAll('*[data-judge-percentages]')[0];
    div.innerHTML = html;
}

function save_judge_percentages() {
    if (window.judgePercentagesChanged == false) { return; }
    window.judgePercentagesChanged = false;
    var inputs = document.querySelectorAll('*[data-judge-percentage-input]');
    var percentages = [];
    for (var i=0; i<inputs.length; i++) {
        percentages.push([inputs[i].name, parseInt(inputs[i].value)]);
    }
    store_fact('whooshingby', 'judge_percentages',
               {'percentages': JSON.stringify(percentages)});
}

get_newest_fact('whooshingby', 'judge_percentages',
                {}, create_judge_percent_controls);
setInterval(save_judge_percentages, 1000);
report_deployment('judge_percentages.js');
