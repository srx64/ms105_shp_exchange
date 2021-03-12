let value = 1;
let rotation = 1;
var digit = 1;
var amount = 0;
var number = 1;
var texts = ['Пожарная машина', 'Гоночная машина', 'Попугай', 'Аэропорт', 'Вертолет', 'Дом (красный)'];
var buttons = document.querySelectorAll(".btn");
var anims = ['fadeIn', 'hatch', 'pullUp', 'bigEntrance'];

scrollToHeadline(1);
document.body.style.overflow = "hidden";
document.body.style.pointerEvents = "none";
back.style.opacity = 0;
let elem = document.createElement('img')
elem.src = "img/gold-coin.jpg";
elem.id = "prel";
elem.classList.add('preloader');
document.body.appendChild(elem);
prel.style.transition = 1 + 's';

function Rotate() {
  if (value == 3) {
    back.style.transition = 1 + 's';
    back.style.opacity = 1;
    prel.style.opacity = 0;
    document.body.style.pointerEvents = "auto";
    document.body.style.overflow = "visible";
  }
  if (value % 2 != 0)
    prel.style.transform = 'rotate(' + value * 360 + 'deg) scale(0.5, 0.5)';
  else
    prel.style.transform = 'rotate(' + value * 360 + 'deg) scale(1, 1)';
  value++;

  if (value == 4) {
    prel.parentNode.removeChild(prel);
    clearInterval(timerId);
  }
}
let timerId = setInterval(Rotate, 1000);


document.querySelector("#company").addEventListener('click', function() {
  requestAnimationFrame(function() {
            scrollToHeadline(0);
        });
})
document.querySelector("#info").addEventListener('click', function() {
  requestAnimationFrame(function() {
            scrollToHeadline(650);
        });
})
document.querySelector("#moreinfo").addEventListener('click', function() {
  requestAnimationFrame(function() {
            scrollToHeadline(1200);
        });
})

function scrollToHeadline(coords) {
  if (window.scrollY > coords) {
    window.scrollBy(0, -25);
    if (window.scrollY - 25 < coords)
      scrollTo(0, coords);
    else
    requestAnimationFrame(function() {
              scrollToHeadline(coords);
          });
  }
  else if (window.scrollY < coords) {
    window.scrollBy(0, +25);
    if (window.scrollY + 25 > coords)
      scrollTo(0, coords);
    else
    requestAnimationFrame(function() {
              scrollToHeadline(coords);
          });
  }
}

document.addEventListener('scroll', function() {
  if (window.scrollY >= 0 && window.scrollY < 300) {
    document.querySelector('.active').classList.remove('active');
    company.classList.add('active');
  } else if (window.scrollY > 300 && window.scrollY < 900) {
    document.querySelector('.active').classList.remove('active');
    info.classList.add('active');
  } else if (window.scrollY > 900 && window.scrollY < 1350) {
    document.querySelector('.active').classList.remove('active');
    moreinfo.classList.add('active');
  }

  document.querySelector('.scrollBar').style.width = parseInt(window.scrollY / document.body.clientHeight * 1000) + 'px';
})
