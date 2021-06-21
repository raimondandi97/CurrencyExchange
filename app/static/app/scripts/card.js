let inputs = document.getElementsByClassName("currency-input");
let currencies_to_activate = []

const access_key = '7eede239249bf05f6b0bc8ec18351424';

const rates_url = 'http://api.exchangeratesapi.io/v1/latest?access_key=' + access_key;
const convert_url = 'http://api.exchangeratesapi.io/v1/convert?access_key=' + access_key;

for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener('change', function (event) {
        let card = event.target;
        while (!card.classList.contains("exhange-card")) {
            card = card.parentNode;
        }
        var code_ids = []
        let all_cards = document.getElementsByClassName("exhange-card");

        for (let j = 0; j < all_cards.length; j++) {
            all_cards[j].style.background = "#eaeaea";
            code_ids.push(all_cards[j].id)
        }

        card.style.background = "#cbd6ff";

        let base_url = '&base=EUR';
        let symbols_url = '&symbols=' + code_ids;

        let url = rates_url + base_url + symbols_url

        fetch(url).then(function (response) {
            response.json().then(function (response) {
                let data = {
                    'base': card.id,
                    'amount': event.target.value,
                    'currencies': {}
                }
                for (var j = 0; j < code_ids.length; j++) {
                    data['currencies'][code_ids[j]] = response['rates'][code_ids[j]];
                }

                fetch('/saverates', {
                    method: 'POST',
                    body: JSON.stringify({ data: data, }),
                    headers: { "Content-type": "application/json; charset=UTF-8" }
                }).then(function (response) {
                    response.json().then(function (response) {
                        console.log(response)
                        for (var j = 0; j < code_ids.length; j++) {
                            let current_card = document.getElementById(code_ids[j]);
                            let rate_info = current_card.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild;
                            rate_info.removeAttribute('style');
                            let card_base = rate_info.firstElementChild;
                            card_base.innerText = card.id;
                            let exchange_value = rate_info.children[1];
                            exchange_value.innerText = response[code_ids[j]].rate;
                            let input = current_card.lastElementChild.lastElementChild.firstElementChild.firstElementChild.lastElementChild.firstElementChild;
                            input.value = response[code_ids[j]].amount;
                        }
                    })
                })
            })
        })
    })
}

let cancel_buttons = document.getElementsByClassName("close cancel")
for (let j = 0; j < cancel_buttons.length; j++) {
    cancel_buttons[j].addEventListener('click', function (event) {
        event.stopPropagation();
        let card = event.target.parentNode.parentNode;
        fetch('/archivecurrency/' + card.id).then(function (repsponse) {
            card.parentNode.removeChild(card);
        })
        
    })
}

let btn_add_currency = document.getElementById("btn_add_currency");

btn_add_currency.addEventListener('click', function (event) {
    let add_currency_modal = document.getElementById("add_currency_modal");
    add_currency_modal.style.display = 'inline';
    let currency_list = document.getElementById("add_currency_list")
    fetch('/arhivedcurrencies').then(function (response) {
        response.json().then(function (response) {
            let arhived_currencies = response.arhived_currencies
            for (let i = 0; i < arhived_currencies.length; i++) {
                let currency = document.createElement('div');
                currency.classList.add('archived_currency');
                currency.addEventListener('click', function (event) {
                    event.stopPropagation();
                    let div = event.target;
                    if (div.classList.contains('selected')){
                        div.classList.remove('selected');
                        currencies_to_activate = currencies_to_activate.filter((el) => el != div.lastElementChild.id);
                    }
                    else {
                        div.classList.add('selected');
                        currencies_to_activate.push(div.lastElementChild.id)
                    }
                    console.log(currencies_to_activate);
                });
                let flag = document.createElement('img');
                flag.src = arhived_currencies[i].flag_link;
                flag.style.width = '60px';
                flag.style.height = '35px';
                let currency_name = document.createElement('span');
                currency_name.innerText = arhived_currencies[i].abv + ' - ' + arhived_currencies[i].name;
                currency_name.id = arhived_currencies[i].abv;
                currency.appendChild(flag);
                currency.appendChild(currency_name);
                currency_list.appendChild(currency);
            }
        })
    })
})

const btn_activate_currencies = document.getElementById("btn_activate_currencies");

btn_activate_currencies.addEventListener('click', function (event) {
    event.stopPropagation();
    fetch('/activatecurrencies', {
        method: 'POST',
        body: JSON.stringify({ currencies: currencies_to_activate, }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    }).then(function (response) {
        currencies_to_activate = [];
        window.location.reload();
    })
})