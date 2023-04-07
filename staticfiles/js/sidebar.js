// @ts-check
console.log('In main.js!');

// sidebar toggle
const btnToggle = document.querySelector('.toggle-btn');

btnToggle.addEventListener('click', function () {
  console.log('clik')
  document.getElementById('sidebar').classList.toggle('active');
  console.log(document.getElementById('sidebar'))
});

$(document).ready(function() {
  $('#menu-toggle').click(function() {
     $('.sidebar-nav').fadeToggle(300); 
  });
});