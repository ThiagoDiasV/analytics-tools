$(document).ready(function(){
    $('.sidenav').sidenav();
  });

function validateForm() {
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
}
