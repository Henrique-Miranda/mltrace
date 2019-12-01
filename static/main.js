function calcular() {
  let aquisicao = parseFloat(document.getElementById('aquisicao').value);
  let quantidade = parseInt(document.getElementById('quantidade').value);
  let reputacao = document.getElementById('reputacao').selectedIndex;
  let peso = document.getElementById('peso').selectedIndex;
  let lucro = parseFloat(document.getElementById('lucro').value);
  let fretegratis = document.getElementById('fretegratis').checked;
  let extra = 0;
  let frete = 0;
  let desconto = 0;
  if (fretegratis){
    if (peso == 0){
      frete = 30.9;
    } else if (peso == 1){
      frete = 33.90;
    } else if (peso == 2){
      frete = 34.9;
    } else if (peso == 3){
      frete = 43.9;
    } else if (peso == 4){
      frete = 63.9;
    } else if (peso == 5){
      frete = 99.9;
    } else if (peso == 6){
      frete = 110.9;
    } else if (peso == 7){
      frete = 129.9;
    } else if (peso == 8){
      frete = 149.9;
    } else if (peso == 9){
      frete = 169.9;
    }
  }
  if (reputacao == 0){
    desconto = 0.5;
  } else if (reputacao == 1){
    desconto = 0.6;
  } else if (reputacao == 2){
    desconto = 1;
  }
  frete = frete * desconto;
  valor = aquisicao * quantidade + lucro + frete;
  if (valor < 120){
      valor = valor + 5;
  }
  classico = valor / 0.89;
  premium = valor / 0.84;
  console.log('frete: ' + frete + ' ' + 'Classico: ' + classico + ' Premium: ' + premium);
  document.getElementById('result1').innerHTML = 'R$' + classico.toFixed(2).toString();
  document.getElementById('result2').innerHTML = 'R$' + premium.toFixed(2).toString();
}

function copiar(id){
  console.log(id);
  let copyText = document.getElementById(id).innerHTML;
  navigator.clipboard.writeText(copyText);
}
