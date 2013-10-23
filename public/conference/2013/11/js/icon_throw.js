
function iconThrow () {
	var canvas = document.querySelector("#overlay_canvas");

	if ( document.documentElement.clientWidth < 480 ) {
		canvas.setAttribute('style', "position: absolute; top: 0; left: 50%; width:600px; margin-left: -300px;");
	}

	var ctx = canvas.getContext("2d");
	var frame_ids;
	var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
                            window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
	var cancelAnimationFrame = window.cancelAnimationFrame || window.webkitCancelAnimationFrame || window.mozCancelAnimationFrame || cancelAnimationFrame;
	function init () {
		var iconList = [], loopTime = 0;
		var iImages = new iconImageReady();
		var iCollection = iImages.iconImages;
		for (var i=0; i<iCollection.length; i++) {
			var icon = new Icons();
			icon.init(iCollection[i]);
			iconList.push(icon);
		}
		function draw () {
			loopTime++;
			ctx.clearRect(0, 0, canvas.width, canvas.height)
			for (var i=0, l=iconList.length; i<l; i++) {
				var icon = iconList[i];
				icon.update();
			}

			frame_ids = requestAnimationFrame(draw);

			if(loopTime > 50) {
				cancelAnimationFrame(frame_ids);
				//console.log(jQuery)
				// $(".kurione-chan-anime").delay(1500).fadeOut(1500, function () {
				// 	$(this).remove();
				// })
				$(".kurione-chan-anime").delay(1500).fadeOut(1500);
			}
		}
		draw();
	}
	function Icons () {
		this.x, this.y, this.tx, this.ty, this.img;
		this.init = function (_img) {
			this.x = canvas.width*.5;
			this.y = canvas.height*.5;
			this.tx = Math.floor(Math.random()*canvas.width-50) + 50;
			this.ty = Math.floor(Math.random()*80);
			this.img = _img;
			this.scale = 0;
			this.tscale = Math.random() * .8 + .2;
			this.trotate = Math.floor(Math.random() * 360);
			this.rotate = 0;
		}
		this.update = function () {
			this.x += (this.tx - this.x) * .2;
			this.y += (this.ty - this.y) * .2;

			//ctx.fillStyle = "#d00000";
			//ctx.arc(this.x, this.y, 10, 0, Math.PI*2, false);
			//ctx.fillRect(this.x, this.y, 20, 20)
			this.rotate += (this.trotate - this.rotate) * 0.2;
			this.scale += (this.tscale - this.scale) * 0.2;
			ctx.save();
			ctx.translate(this.x, this.y);
			ctx.rotate(this.rotate);
			ctx.scale(this.scale, this.scale);
			ctx.drawImage(this.img, -30, -30);
			ctx.restore();
			//ctx.fill();
		}
	}
	init();
}

function iconImageReady () {
	this.iconImages = [];
	var thumbs = [
		"ayumu_sato.png",
		"brian_birtles.png",
		"daisuke_yamazaki.png",
		"futomi_hatano.png",
		"go_otani.png",
		"hayato_ito.png",
		"hiroki_tani.png",
		"keisuke_ai.png",
		"kensaku_komatsu.png",
		"kosuke_nagano.png",
		"masataka_yakura.png",
		"satoshi_shoda.png",
		"takuo_kihira.png",
		"tomoya_asai.png",
		"yoshitaka_kasugai.png",
		"yuya_saito.png",
	];

	for (var i=0, l=thumbs.length; i<l; i++) {
		var img = new Image();
		img.src = "img/speakers/icons/" + thumbs[i];
		this.iconImages.push(img);
	}
}
