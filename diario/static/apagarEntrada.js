function confirmarDelete(idObj) {
  if (confirm("Tem certeza que deseja apagar este item? ")) {
    document.getElementById('form-apagar-' + idObj).submit()
  }
}