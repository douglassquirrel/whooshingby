function completed_task() {
    var name = document.querySelector('*[data-task]').value;
    var time = Math.round(new Date().getTime() / 1000);
    var content = {'name': name, 'time': time};
    store_fact('whooshingby', 'completed_task', content);
}

report_deployment('completed_task.js');