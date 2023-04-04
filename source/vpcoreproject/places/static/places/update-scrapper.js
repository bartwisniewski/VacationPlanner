let endpoint = '';
let waiting_state = false;

function get_data() {
	setTimeout(async function() {
		const response = await fetch(endpoint);
		const data = await response.json();
		if(!data.done){
		    render_waiting();
		    get_data();
		}
		else{
		    if(data.ok)
                render_result(data.result)
            else
                render_error()
		}
	}, 1000);
}

function render_waiting(){
    const waiting_text = document.getElementById('waiting-text');
    waiting_text.textContent = "waiting for results";
    waiting_text.className = waiting_state ? "has-text-white" : "hast-text-light";
    waiting_state = !waiting_state;
}

function render_result(result){
    console.log('result: ' + result);
    const results_div = document.getElementById('results');
    results_div.textContent = "";
    const h2 = document.createElement('h2');
    h2.textContent = "Scrap results:"
    results_div.appendChild(h2);
    const ul = document.createElement('ul');
    ul.setAttribute('id','results_list');
    results_div.appendChild(ul);
    result.forEach(render_result_item);
    function render_result_item(element, index, arr){
        const li = document.createElement('li');
        li.setAttribute('id', 'results_item_'+index);
        ul.appendChild(li);
        const a = document.createElement('a');
        a.setAttribute('href', element.url);
        li.appendChild(a);
        const span = document.createElement('span');
        span.textContent=element.name;
        a.appendChild(span)
    }
}

function render_error(){
    const waiting_text = document.getElementById('waiting-text');
    const results_div = document.getElementById('results');
    results_div.removeChild(waiting_text);
    const err = document.createElement('p');
    err.innerHTML = 'Scrap ended with failure';
    err.className = "has-text-danger";
    results_div.appendChild(err);
}

get_data();
