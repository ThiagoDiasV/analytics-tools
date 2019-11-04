// Validates the CSV form at spectrowsm template
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
  
    if ($('#savgol-menu').is(':visible')){
      var windowLengthOptions = document.getElementById('windowlength').options;
      for (var i = 0; i < windowLengthOptions.length; i++) {
        if (windowLengthOptions[i].selected) {
          var windowLengthValue = parseInt(windowLengthOptions[i].value);
        }
      }
      var polyorderOptions = document.getElementById('polyorder').options;
      for (var i = 0; i < polyorderOptions.length; i++) {
        if (polyorderOptions[i].selected) {
          var polyorderValue = parseInt(polyorderOptions[i].value);
        }
      }   
      
      if (polyorderValue >= windowLengthValue) {
        alert('O valor de ordem polinomial não pode ser maior que o valor de intervalo de janela (window length)');
        return false;
      }
    }
  }
  
// Show and hide the savgol menu at spectrowsm
$('input[name="savgol-option"]').on('change', function() {
var option = $(this).val();
if (option == 1) {
    $("#savgol-menu").show();
} else {
    $("#savgol-menu").hide();
}
}).change();