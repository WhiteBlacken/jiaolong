(function ($) {
    //更多精品模板：http://www.bootstrapmb.com
    "use strict";
    $(document).on('click', '.add_to_wishlist', function(ev) {
        ev.preventDefault();
        var $this = $(this);
        $this.siblings('.ajax-loading').css({
            'visibility': 'visible',
            'margin-top': '6px'
        });
        window.setTimeout(function() {
            $this.siblings('.ajax-loading').css('visibility', 'hidden');
            var msg = $('#yith-wcwl-popup-message');
            if (msg[0] === undefined) {
                $('body').append('<div id="yith-wcwl-popup-message" style="display:none"></div>');
                msg = $('#yith-wcwl-popup-message')
            }
            msg.html('<div id="yith-wcwl-message">Product added!</div>');
            msg.css('margin-left', '-' + $(msg).width() + 'px').fadeIn();
            window.setTimeout(function() {
                msg.fadeOut();
            }, 2000);
        }, 1000);
		return false;
    });
	
    $(document).on('click', '.add_to_cart_button, .single_add_to_cart_button', function(ev) {
        ev.preventDefault();
        var $this = $(this);
        $this.removeClass('added').addClass('loading');
        window.setTimeout(function() {
            $this.removeClass('loading').addClass('added')
        }, 1000);
		return false;
    });
	
    $('.vertical-megamenu .dropdown').on('hover', function(e) {
        $(this).find('> ul.dropdown-menu').toggle(300)
    });
	
    $('.ver-megamenu-header').on('hover', function(e) {
        var verticalMenu = $(this).find('> ul.vertical-megamenu');
        if (!verticalMenu.is(':visible')) {
            verticalMenu.slideToggle(300);
            verticalMenu.addClass('showed')
        } else {
            if (verticalMenu.hasClass('showed')) {
                verticalMenu.slideToggle(300);
                verticalMenu.removeClass('showed')
            }
        }
    });
	
	$("#ya-totop").hide();
	var wh = $(window).height();
	var whtml = $(document).height();
	$(window).scroll(function() {
		if ($(this).scrollTop() > whtml / 10) {
			$('#ya-totop').fadeIn()
		} else {
			$('#ya-totop').fadeOut()
		}
	});
	$('#ya-totop').on ('click', function() {
		$('body,html').animate({
			scrollTop: 0
		}, 800);
		return !1
	});
	
	try {
		$('.compare').colorbox({
			href: "ajax/compare.html",
			iframe: !0,
			width: '90%',
			height: '90%'
		})
	} catch (e) {}
	
	try {
		jQuery('.phone-icon-search').on( 'click', function(){
			jQuery('.sm-serachbox-pro').toggle("slide");
		});
	} catch (e) {}
	
	$('.product-images').each(function() {
		var $id = this.id;
		var $rtl = $(this).data('rtl');
		var $vertical = $(this).data('vertical');
		var $img_slider = $('#' + $id + ' .product-responsive');
		var $thumb_slider = $('#' + $id + ' .product-responsive-thumbnail');
		var $number_large = ($vertical === !1) ? 4 : 3;
		$img_slider.slick({
			slidesToShow: 1,
			slidesToScroll: 1,
			fade: !0,
			arrows: !1,
			rtl: $rtl,
			asNavFor: $thumb_slider
		});
		$thumb_slider.slick({
			slidesToShow: $number_large,
			slidesToScroll: 1,
			asNavFor: $img_slider,
			arrows: !0,
			focusOnSelect: !0,
			rtl: $rtl,
			vertical: $vertical,
			verticalSwiping: $vertical,
			responsive: [{
				breakpoint: 1199,
				settings: {
					slidesToShow: 3
				}
			}, {
				breakpoint: 991,
				settings: {
					slidesToShow: 4
				}
			}, {
				breakpoint: 767,
				settings: {
					slidesToShow: 3
				}
			}, {
				breakpoint: 480,
				settings: {
					slidesToShow: 1
				}
			}]
		});
		$(".product-images").fadeIn(300, function() {
			$(this).removeClass("loading");
		})
	});
	
	$('.fancybox').fancybox({
		'width': 800,
		'height': 600,
		'autoSize': !1,
		helpers: {
			title: null
		},
		afterShow: function() {
			if ($(window).width() >= 768) {
				try {
					$('#quickview-container .compare').colorbox({
						href: "ajax/compare.html",
						iframe: !0,
						width: '90%',
						height: '90%'
					});
				} catch (e) {}
			} else {
				window.open('ajax/compare.html');
			}
			
			$('#quickview-container .add_to_wishlist').on ('click', function(ev) {
				ev.preventDefault();
				var $this = $(this);
				$this.siblings('.ajax-loading').css({
					'visibility': 'visible',
					'margin-top': '6px'
				});
				window.setTimeout(function() {
					$this.siblings('.ajax-loading').css('visibility', 'hidden');
					var msg = $('#yith-wcwl-popup-message');
					if (msg[0] === undefined) {
						$('body').append('<div id="yith-wcwl-popup-message" style="display:none"></div>');
						msg = $('#yith-wcwl-popup-message')
					}
					msg.html('<div id="yith-wcwl-message">Product added!</div>');
					msg.css('margin-left', '-' + $(msg).width() + 'px').fadeIn();
					window.setTimeout(function() {
						msg.fadeOut();
					}, 2000);
				}, 1000);
				return false;
			});
			
			$('#quickview-container .single_add_to_cart_button').on('click', function(ev) {
				ev.preventDefault();
				var $this = $(this);
				$this.removeClass('added').addClass('loading');
				window.setTimeout(function() {
					$this.removeClass('loading').addClass('added');
				}, 1000);
				return false;
			});
			
			$('.quickview-container .product-images').each(function() {
				var $id = this.id;
				var $rtl = $('body').hasClass('rtl');
				console.log($rtl);
				var $img_slider = $('#' + $id + ' .product-responsive');
				var $thumb_slider = $('#' + $id + ' .product-responsive-thumbnail')
				$img_slider.slick({
					slidesToShow: 1,
					slidesToScroll: 1,
					fade: !0,
					arrows: !1,
					rtl: $rtl,
					asNavFor: $thumb_slider
				});
				$thumb_slider.slick({
					slidesToShow: 3,
					slidesToScroll: 1,
					asNavFor: $img_slider,
					arrows: !0,
					focusOnSelect: !0,
					rtl: $rtl,
					responsive: [{
						breakpoint: 1199,
						settings: {
							slidesToShow: 3
						}
					}, {
						breakpoint: 991,
						settings: {
							slidesToShow: 3
						}
					}, {
						breakpoint: 767,
						settings: {
							slidesToShow: 3
						}
					}, {
						breakpoint: 480,
						settings: {
							slidesToShow: 1
						}
					}]
				});
				$(".product-images").fadeIn(1000, function() {
					$(this).removeClass("loading");
				})
			})
		}
	});
	
	if (Cookies.get && Cookies.get("theme")) {
		try {
			var theme = "css/theme/app-" + Cookies.get("theme") + ".min.css";
			$("#theme").attr("href", theme);
			$('#colorPanel').find('.ya-radio-img-selected').removeClass('ya-radio-img-selected');
			$('img[data-theme=' + Cookies.get("theme") + ']').parents('label').addClass('ya-radio-img-selected')
		} catch (e) {
			console.log(e);
		}
	}
	
	$('#cpanel-reset').on('click', function(e) {
		var defaultTheme = $('#colorPanel').find('[data-theme-default="true"]');
		if (defaultTheme != undefined) {
			var defaultColor = $(defaultTheme).data('theme');
			var theme = "css/theme/app-" + defaultColor + ".min.css";
			$("#theme").attr("href", theme);
			Cookies.remove('theme');
			$('#colorPanel').find('.ya-radio-img-selected').removeClass('ya-radio-img-selected');
			$('img[data-theme=' + defaultColor + ']').parents('label').addClass('ya-radio-img-selected')
		}
		return false;
	});
	
	$('img[data-theme]').on('click', function() {
		var color = $(this).data('theme');
		var theme = "css/theme/app-" + color + ".min.css";
		$("#theme").attr("href", theme);
		Cookies.set('theme', color);
		$('#colorPanel').find('.ya-radio-img-selected').removeClass('ya-radio-img-selected');
		$(this).parents('label').addClass('ya-radio-img-selected')
	});
	
	$('a[href="#cpanel-form"]').on('click', function(e) {
		e.preventDefault();
		var parent = $('#cpanel-form'),
			right = parent.css('right'),
			width = parent.width();
		if (parseFloat(right) < -10) {
			parent.animate({
				right: '0px',
			}, "slow")
		} else {
			parent.animate({
				right: '-' + width,
			}, "slow")
		}
		if ($(this).hasClass('active')) {
			$(this).removeClass('active')
		} else {
			$(this).addClass('active')
		}
		return false;
	});
		
    $('.slideshow').owlCarousel2({
        navText: ['', ''],
        navClass: ['owl-custom-prev', 'owl-custom-next'],
        loop: !0,
        margin: 0,
        responsiveClass: !0,
        nav: !0,
        dots: !1,
        autoplay: !0,
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 1,
            },
            1000: {
                items: 1,
            }
        }
    });
	
    $(".wpb_accordion").each(function(element) {
        var $this = $(this);
        var $this_second = $(this);
        var interval = ($this_second.attr("data-interval"), !isNaN($(this).data("active-tab")) && 0 < parseInt($this_second.data("active-tab"), 10) && parseInt($this_second.data("active-tab")) - 1, 10);
        var collapsible = !1 === interval || "yes" === $this_second.data("collapsible");
        $this = $this_second.find(".wpb_accordion_wrapper").accordion({
            header: "> div > h3",
            autoHeight: !1,
            heightStyle: "content",
            active: interval,
            collapsible: collapsible,
            navigation: !0,
            change: function(element, $this) {
                "undefined" != typeof $.fn.isotope && $this.newContent.find(".isotope").isotope("layout"), carouselBehaviour($this.newPanel)
            }
        }), !0 === $this_second.data("vcDisableKeydown") && ($this.data("uiAccordion")._keydown = function() {})
    })
}(jQuery))