const toggle = document.querySelector('.navbar_toggle');
const menu = document.querySelector('.navbar_menu');
const log = document.querySelector('.navbar_log');

// 햄버거 눌러서
toggle.addEventListener('click', () => {
  menu.classList.toggle('active');
  log.classList.toggle('active');
});