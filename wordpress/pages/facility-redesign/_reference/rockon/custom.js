/*--------------------- Copyright (c) 2025 -----------------------
[Master Javascript]
Project: Rockon WP Theme Demo
-------------------------------------------------------------------*/
(function ($) {
	"use strict";
	var Rockon = {
		initialised: false,
		version: 1.0,
		mobile: false,
		init: function () {
			if(!this.initialised) {
				this.initialised = true;
			} 
			else {
				return;
			}
		/*-------------- Rockon Functions Calling -------------------------------------------------*/
			
			this.rockPodcastCursorEffect();
			this.rockPodcastSearchBox();											
			this.rockPodcastHeaderFixed();	
			this.rockPodcastToggleMenu();																	
			this.rockPodcastButton();	
			this.rockPodcastCountdownTimer();																
			this.rockPodcastEventCountdownTimer1();																
			this.rockPodcastEventCountdownTimer2();																
			this.rockPodcastRangeSlider();																
			this.rockPodcastfilterGallery();	
			this.rockPodcastMagnificPopup();	
			this.rockPodcastDateTimePicker();														
			this.rockPodcastSelect2();														
			this.rockPodcastTestimonialSlider();														
			this.rockPodcastAnimatedText();														
			this.rockPodcastSmoke();														
		 },
		
		/*-------------- Rockon Functions Calling -------------------------------------------------*/					
		
		 // Cursor Effect
		rockPodcastCursorEffect: function(){
			if ($(".rock-podcast-aimated-cursor").length) {
				var e = {x: 0, y: 0}, t = {x: 0, y: 0}, n = .25, o = !1, a = document.getElementsByClassName("rock-podcast-cursor"),
					i = document.getElementsByClassName("rock-podcast-cursor-loader");
				TweenLite.set(a, {xPercent: -50, yPercent: -50}), document.addEventListener("mousemove", function (t) {
					var n = window.pageYOffset || document.documentElement.scrollTop;
					e.x = t.pageX, e.y = t.pageY - n
				}), TweenLite.ticker.addEventListener("tick", function () {
					o || (t.x += (e.x - t.x) * n, t.y += (e.y - t.y) * n , TweenLite.set(a, {x: t.x, y: t.y}))
				}),
				$(".rock-podcast-right, .swiper-button-prev, .swiper-button-next, .rock-podcast-toggle-btn, .rock-podcast-footer-social, .flatpickr-time, .rock-podcast-input-field, .rock-podcast-glry-filters, .rock-podcast-closeBtn, .rock-podcast-header-search, .rock-podcast-range-wrapper, .rock-podcast-main-logo, .hide-cursor,.btn,.rock-podcast-btn,.rock-podcast-book-table,.rock-podcast-next-page-btn,.rock-podcast-menu-link,.rock-podcast-book-tables,.rock-podcast-input-time,.rock-podcast-input-date,.swiper-pagination-bullet").mouseenter(function (e) {
					TweenMax.to(".rock-podcast-cursor", .2, {borderWidth: "1px", scale: 2, opacity: 0,})
				}),
			
				$(".rock-podcast-right, .swiper-button-prev, .swiper-button-next, .rock-podcast-toggle-btn, .rock-podcast-footer-social, .flatpickr-time, .rock-podcast-input-field, .rock-podcast-glry-filters, .rock-podcast-closeBtn, .rock-podcast-header-search, .rock-podcast-range-wrapper, .rock-podcast-main-logo, .hide-cursor,.btn,.rock-podcast-btn,.rock-podcast-book-table,.rock-podcast-next-page-btn,.rock-podcast-menu-link,.rock-podcast-book-tables,.rock-podcast-input-time,.rock-podcast-input-date,.swiper-pagination-bullet").mouseleave(function (e) {
					TweenMax.to(".rock-podcast-cursor", .3, {borderWidth: "2px", scale: 1, opacity: 1})
				})			
			}			
		},
		// Cursor Effect

		// Search Box
		rockPodcastSearchBox: function (){
			$(".rock-podcast-header-search").on("click", function () {
			  $(".rock-podcast-searchBox").addClass("rock-podcast-show");
			});
			$(".closeBtn").on("click", function () {
			  $(".rock-podcast-searchBox").removeClass("rock-podcast-show");
			});
			$(".rock-podcast-searchBox").on("click", function () {
			  $(".rock-podcast-searchBox").removeClass("rock-podcast-show");
			});
			$(".rock-podcast-search-bar-inner").on("click", function () {
			  event.stopPropagation();
			});
		  },
		// Search Box	

		// Header Fixed
		rockPodcastHeaderFixed: function(){								
			if($(window).width() >= 1200){
				$(window).scroll(function() {
					var window_top = $(window).scrollTop() + 1;
					if (window_top > 500) {
						$('.rock-podcast-header-wrapper').addClass('rock-podcast-header-wrapper-fixed animated fadeInDown');
					} else {
						$('.rock-podcast-header-wrapper').removeClass('rock-podcast-header-wrapper-fixed animated fadeInDown');
					}
				});
				$('.rock-podcast-header-wrapper').addClass('rock-podcast-header-wrapper-fixed animated fadeInDown');
				}else{
					$('.rock-podcast-header-wrapper').removeClass('rock-podcast-header-wrapper-fixed animated fadeInDown');
				}							
			return false;
		},
		// Header Fixed

		// Toggle Menu
		rockPodcastToggleMenu: function(){
			$(".rock-podcast-toggle-btn").on("click", function (e) {
				e.stopPropagation();
				$(".rock-podcast-header-parent").toggleClass("rock-podcast-menu-open");
			});
		
			$(".rock-podcast-header-parent").click(function (e) {
				e.stopPropagation();
			});
		
			$("body,html").click(function (e) {
				$(".rock-podcast-header-parent").removeClass("rock-podcast-menu-open");
			});
		},
		// Toggle Menu

		// Button Effect
		rockPodcastButton: function(){
			if ($('.rock-podcast-btn').length > 0) {		
				document.querySelectorAll('.rock-podcast-btn').forEach(function(button) {
					button.onmousemove = function (e) {
						var rect = e.target.getBoundingClientRect();
						var x = e.clientX - rect.left;
						var y = e.clientY - rect.top;
						e.target.style.setProperty('--x', x + 'px');
						e.target.style.setProperty('--y', y + 'px');
					};
				});
			}
		},
		// Button Effect

		// Countdown Timer
		rockPodcastCountdownTimer: function(){	
			if($('.rock-podcast-ticket-wrapper').length > 0){
				var countDownDate = new Date("June 17, 2025 22:00:00").getTime();
				var x = setInterval(function() {
				var now = new Date().getTime();
				var distance = countDownDate - now;  
				var days = Math.floor(distance / (1000 * 60 * 60 * 24));
				var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
				var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
				var seconds = Math.floor((distance % (1000 * 60)) / 1000);		  
				document.getElementById("days").innerHTML = days < 10 ? '0' + days : days;
				document.getElementById("hours").innerHTML = hours < 10 ? '0' + hours : hours;
				document.getElementById("minutes").innerHTML = minutes < 10 ? '0' + minutes : minutes;
				document.getElementById("seconds").innerHTML = seconds < 10 ? '0' + seconds : seconds;
				}, 1000);
			}
		},
		// Countdown Timer

		// Countdown Timer
		rockPodcastEventCountdownTimer1: function(){	
			if($('.rock-podcast-event-wrapper').length > 0){
				var countDownDate = new Date("June 17, 2025 22:00:00").getTime();
				var x = setInterval(function() {
				var now = new Date().getTime();
				var distance = countDownDate - now;  
				var days = Math.floor(distance / (1000 * 60 * 60 * 24));
				var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
				var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
				var seconds = Math.floor((distance % (1000 * 60)) / 1000);		  
				document.getElementById("days1").innerHTML = days < 10 ? '0' + days : days;
				document.getElementById("hours1").innerHTML = hours < 10 ? '0' + hours : hours;
				document.getElementById("minutes1").innerHTML = minutes < 10 ? '0' + minutes : minutes;
				document.getElementById("seconds1").innerHTML = seconds < 10 ? '0' + seconds : seconds;
				}, 1000);
			}			
		},
		// Countdown Timer

		// Countdown Timer
		rockPodcastEventCountdownTimer2: function(){	
			if($('.rock-podcast-event-wrapper').length > 0){
				var countDownDate = new Date("June 17, 2025 22:00:00").getTime();
				var x = setInterval(function() {
				var now = new Date().getTime();
				var distance = countDownDate - now;  
				var days = Math.floor(distance / (1000 * 60 * 60 * 24));
				var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
				var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
				var seconds = Math.floor((distance % (1000 * 60)) / 1000);		  
				document.getElementById("days2").innerHTML = days < 10 ? '0' + days : days;
				document.getElementById("hours2").innerHTML = hours < 10 ? '0' + hours : hours;
				document.getElementById("minutes2").innerHTML = minutes < 10 ? '0' + minutes : minutes;
				document.getElementById("seconds2").innerHTML = seconds < 10 ? '0' + seconds : seconds;
				}, 1000);
			}			
		},
		// Countdown Timer
		
		// Range Slider
		rockPodcastRangeSlider: function(){
			if($('.rock-podcast-ticekt-box').length > 0){
				class App {
					constructor($fir = document.getElementsByClassName('rock-podcast-range-inner')[0]) {
						this.dom = {
							$fir: $fir,
							$range: $fir.querySelector('.rock-podcast-range-input'),
							$counter: document.createElement('div'),
							$line: document.createElement('div')
						};
						this.dimension = {
							min: Math.floor(this.dom.$range.getAttribute('min')),
							max: Math.floor(this.dom.$range.getAttribute('max')),
						};
						this.rangeWidth = this.dom.$range.offsetWidth;		
						this.init();
					}	
					init() {
						this.initRange();
						this.initCounter();
						this.initLine();
						this.initAnimate();
					}	
					initRange() {
						this.textSuperPosition = this.dom.$range.value;
						this.changeVals();		
						this.dom.$range.addEventListener('input', this.changeVals.bind(this));
					}	
					initCounter() {
						this.changeCounter();		
						this.dom.$counter.setAttribute('class', 'rock-podcast-range-value');
						this.dom.$fir.appendChild(this.dom.$counter);
					}	
					initLine() {
						this.changeCounter();		
						this.dom.$line.setAttribute('class', 'rock-podcast-fir-line');
						this.dom.$fir.appendChild(this.dom.$line);
					}	
					initAnimate() {
						setInterval(() => requestAnimationFrame(this.changeCounter.bind(this)), 1000/50);
					}	
					changeVals() {
						this.amount = Math.floor(this.dom.$range.value);
						this.range = (this.amount - this.dimension.min) / (this.dimension.max - this.dimension.min);
					}	
					changeCounter() {
						this.textSuperPosition = this.lerp(this.textSuperPosition, this.amount, 0.1);		
						let newPosition = this.lerp(this.dom.$counter.style.getPropertyValue('--position'), this.rangeWidth * this.range, 0.1);
						let newSize = this.lerp(this.dom.$line.style.getPropertyValue('--size'), this.range, 0.1);
						let logicCounter = this.amount - this.textSuperPosition;
						let currentValue = Math.floor(logicCounter > 0 && logicCounter < 1 ? this.amount : this.textSuperPosition);
						this.dom.$counter.textContent = currentValue;
						this.dom.$counter.style.setProperty('--position', newPosition);
						this.dom.$line.style.setProperty('--size', newSize);						
						}	
						lerp(start, end, amt) {
						return (1-amt) * start + amt * end;
						}
					}
				document.addEventListener('DOMContentLoaded', () => new App());
			}
		},
		// Range Slider

		// Filter Gallery
		rockPodcastfilterGallery: function(){
			$('.grid').isotope({
				itemSelector: '.grid-item',
			});	
			$('.rock-podcast-filter-button-group').on( 'click', 'li', function() {
				var filterValue = $(this).attr('data-filter');
				$('.grid').isotope({ filter: filterValue });
				$('.rock-podcast-filter-button-group li').removeClass('active');
				$(this).addClass('active');
			});
			
		},
		// Filter Gallery
		
		// Magnific Popup For Gallery
		rockPodcastMagnificPopup: function(){
			if($('.imgenView').length > 0){
				$('.imgenView').magnificPopup({
					type: 'image',			  
					gallery: {				
						enabled: true
					}			  			  
				});
			}
		},
		// Magnific Popup For Gallery

		// Date and Time Picker
		rockPodcastDateTimePicker: function(){
			flatpickr("#datepicker", {
				dateFormat: "d-m-Y",
				minDate: "today",	
				clickOpens: true,			
			});
			flatpickr("#timepicker", {
				enableTime: true,
				noCalendar: true,            
				dateFormat: "h:i K",
				time_24hr: false       
			});
			
			 $("#datepicker-icon").on("click", function () {
				$("#datepicker")[0]._flatpickr.open();
			});
			 $("#timepicker-icon").on("click", function () {
				$("#timepicker")[0]._flatpickr.open();
			});
		},
		// Date and Time Picker
		
		// Select2
		rockPodcastSelect2: function(){
			$(".rock-podcast-select").select2({
				placeholder: "Select Here",				
			});
		},
		// Select2
		
		// Testimonial Slider
		rockPodcastTestimonialSlider: function (){			
			var swiper = new Swiper(".rock-podcast-tstml-slider-parent", {
				slidesPerView: 2,
				spaceBetween: 30,				
				loop:true,				
				autoplay:true,
				speed:1000,
				effect: 'slide',								
				navigation: {
					nextEl: ".swiper-button-next",
					prevEl: ".swiper-button-prev",
				},
				breakpoints: {					
					1199: {
						slidesPerView: 2,
						spaceBetween: 30,
					},
					992: {
						slidesPerView: 2,
						spaceBetween: 30,
					},
					768: {
						slidesPerView: 2,
						spaceBetween: 30,
					},
					0: {
						slidesPerView: 1,
						spaceBetween: 30,						
					},					
				}	
			  });		
			;
		},
		// Testimonial Slider
		
		// Animated Text
		rockPodcastAnimatedText: function(){
			$(".rock-podcast-animate-text").each(function() {
				var s = $(this),
					a = s.text().split(""),
					t = s.data("wait") || 0,
					i = s.data("speed") || 4;
				
				i /= 100;
				s.html("<em>321...</em>").addClass("ready");	
				s.waypoint({
					handler: function() {
						if (!s.hasClass("stop")) {
							s.addClass("stop");
							setTimeout(function() {
								s.text("");
								$.each(a, function(e, a) {
									var t = document.createElement("h1");
									t.textContent = a;
									t.style.animationDelay = e * i + "s";
									s.append(t);
								});
							}, t);
						}
					},
					offset: "90%"
				});
			});	
		},
		// Animated Text

		// Smoke
		rockPodcastSmoke: function(){
			window.ga = window.ga || function() {(ga.q = ga.q || []).push(arguments)};
		},
		// Smoke		
	};
	Rockon.init();
}(jQuery));	