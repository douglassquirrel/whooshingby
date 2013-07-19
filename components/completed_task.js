function completed_task() {
    var name = document.querySelector('*[data-task]').value;
    var time = Math.round(new Date().getTime() / 1000);
    var computer_name = window.kropotkin_computer_name;
    var id = window.kropotkin_components['completed_task.js']['local_id'];
    var task_id = [computer_name, id, time].join('.');
    var content = {'name': name, 'time': time, 'task_id': task_id};
    store_fact('whooshingby', 'completed_task', content);
}

report_deployment('completed_task.js');