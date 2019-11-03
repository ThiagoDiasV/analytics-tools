$(document).ready(function(){
    $('.sidenav').sidenav();
  });

function validatePdfForm() {
  var uploadFiles = document.forms["pdfsForm"]["pdf_files"].files; 
   
  
  if (uploadFiles.length === 0) {
    alert("Você não selecionou nenhum arquivo");
    return false;
  }

  let regex = new RegExp('.pdf');

  for (var i = 0; i < uploadFiles.length; i++) {
    let text = uploadFiles[i]['name'];
    let result = regex.exec(text);
    
    if (result != '.pdf') {
      alert('Você selecionou arquivos que não são PDFs. Tente novamente.');
      return false;
    }
  }
  var filename = document.getElementById('filename_field').value;
  if (filename.length > 21) {
    alert("Digite um nome de arquivo com menos de 30 caracteres");
  }
}

function validateCsvForm() {
  var uploadFiles = document.forms["csvsForm"]["csv_files"].files; 
   
  
  if (uploadFiles.length === 0) {
    alert("Você não selecionou nenhum arquivo");
    return false;
  }

  let regex = new RegExp('.csv');

  for (var i = 0; i < uploadFiles.length; i++) {
    let text = uploadFiles[i]['name'];
    let result = regex.exec(text);
    
    if (result != '.csv') {
      alert('Você selecionou arquivos que não são CSVs. Tente novamente.');
      return false;
    }
  }

  var filename = document.getElementById('filename_field').value;
  if (filename.length > 21) {
    alert("Digite um nome de arquivo com menos de 30 caracteres");
  }
}

$('input[name="savgol-option"]').on('change', function() {
  var option = $(this).val();
  if (option == 1) {
    $("#savgol-menu").show();
  } else {
    $("#savgol-menu").hide();
  }
}).change();
