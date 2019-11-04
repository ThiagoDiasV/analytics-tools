// Validates the PDF form at hplcpc template
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
