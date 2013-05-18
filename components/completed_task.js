function completed_task() {
    var name = document.querySelector('*[data-task]').value;
    var time = Math.round(new Date().getTime() / 1000);
    var content = {'name': name, 'time': time, 'kropotkin_id': -1};
    store_fact('whooshingby', 'completed-task', content);
}