function resize(designWidth, maxWidth) {
	let doc = document,
	win = window,
	docEl = doc.documentElement,
	remStyle = document.createElement("style"),
	tid;

	function refreshRem() {
		let width = docEl.getBoundingClientRect().width;
		maxWidth = maxWidth || 1920;
		width>maxWidth && (width=maxWidth);

		let rem0 = docEl.clientWidth;
		console.log(rem0, docEl.clientHeight, docEl.style.fontSize);
		let rem = width * 15 / designWidth;
		remStyle.innerHTML = 'html{font-size:' + rem + 'px;}';
	}

	if (docEl.firstElementChild) {
		docEl.firstElementChild.appendChild(remStyle);
	} else {
		let wrap = doc.createElement("div");
		wrap.appendChild(remStyle);
		doc.write(wrap.innerHTML);
		wrap = null;
	}
	//要等 viewport 设置好后才能执行 refreshRem，不然 refreshRem 会执行2次；
	refreshRem();

	win.addEventListener("resize", function() {
		clearTimeout(tid); //防止执行两次
		tid = setTimeout(refreshRem, 300);
	}, false);

	win.addEventListener("pageshow", function(e) {
		if (e.persisted) { // 浏览器后退的时候重新计算
			clearTimeout(tid);
			tid = setTimeout(refreshRem, 300);
		}
	}, false);

}

$(document).ready(resize(1920, 1920));


function f1(){
    let form = document.getElementById('drawcards');
    let fd = new FormData(form);
    let xhr = new XMLHttpRequest();
    xhr.open('post', '/drawcards/');
    xhr.send(fd);
    xhr.onreadystatechange = function(){
        if(4 === xhr.readyState){
            if (xhr.status === 200 || xhr.status === 304){
                let ret = JSON.parse(xhr.responseText);
                document.getElementById('draw_result').innerHTML = ret.length;
            }
        }
    }
}
function f2(){
    let iframe = document.getElementById('iframe1');
    iframe.src = "/drawcards/";
    iframe.width = 660;
    iframe.height = 150;
}
function f3(){
    let iframe = document.getElementById('iframe1');
    iframe.src = "";
    iframe.width = 0;
    iframe.height = 0;
}
$(function () {
    let buttons = $('div.header>div.container>div');
    buttons.mouseenter(function () {
        $(this).find('div').slideDown(300);
    })
    buttons.mouseleave(function () {
        console.log('trying:', $(this).find('div'));
        $(this).find('div').slideUp(100);
    })
});
